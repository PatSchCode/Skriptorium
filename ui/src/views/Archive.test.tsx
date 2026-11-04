import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router";
import { afterEach, describe, expect, it, vi } from "vitest";
import {
  CHAPTER,
  ENTRY,
  fail,
  fakeApi,
  modelList,
  noContent,
  ok,
  openStorySettings,
  STORY,
  WORLD,
} from "../../fake-api";
import { renderShell } from "../../render-shell";
import type { StoryDeletion, WorldDeletion } from "../api";
import { counted } from "./Archive";
import { Stories } from "./Stories";
import { StoryList } from "./StoryList";
import { StoryPage } from "./StoryPage";
import { Worlds } from "./Worlds";

afterEach(() => {
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});

const GLAS = {
  ...WORLD,
  id: "glaskueste",
  name: "Glasküste",
  archived: true,
};
const GLAS_DELETION: WorldDeletion = {
  name: "Glasküste",
  entries: 42,
  images: 11,
  maps: 2,
  stories: 1,
  guest_uses: [
    {
      world: "salzmark",
      world_name: "Die Salzmark",
      story: "ueberfahrt",
      story_title: "Die Überfahrt",
      guests: ["Kael", "Mira"],
      facts: 3,
    },
  ],
};
const OLD = {
  ...STORY,
  id: "erster-versuch",
  title: "Erster Versuch",
  archived: true,
};
const OLD_DELETION: StoryDeletion = {
  title: "Erster Versuch",
  chapters: 1,
  facts: 2,
  cover: true,
};
const STORIES = "/api/worlds/salzmark/stories";

describe("counted", () => {
  it("names one and many", () => {
    expect(counted(1, "Karte", "Karten")).toBe("1 Karte");
    expect(counted(0, "Karte", "Karten")).toBe("0 Karten");
  });
});

describe("archive of the worlds (step 9.9, ADR-098)", () => {
  it("lists archived worlds only in the area Archiv", async () => {
    const { calls } = fakeApi({
      "GET /api/worlds": ok([WORLD, GLAS]),
      "POST /api/worlds/salzmark/archive": ok({ ...WORLD, archived: true }),
      "POST /api/worlds/glaskueste/restore": ok({ ...GLAS, archived: false }),
    });
    const user = userEvent.setup();
    const onOpen = vi.fn();
    render(<Worlds onOpen={onOpen} />);

    const main = await screen.findByRole("button", { name: "Die Salzmark" });
    expect(screen.queryByRole("button", { name: "Glasküste" })).toBeNull();
    expect(screen.getByText("Archiv (1)")).toBeDefined();
    const archive = screen.getByText("Archiv (1)").closest("details");
    expect(archive).not.toBeNull();
    expect(within(archive as HTMLElement).getByText("Glasküste")).toBeDefined();

    await user.click(main);
    expect(onOpen).toHaveBeenCalledWith(WORLD);
    await user.click(
      screen.getByLabelText("Weitere Aktionen für Die Salzmark"),
    );
    await user.click(screen.getByRole("button", { name: "Archivieren" }));
    await user.click(screen.getByRole("button", { name: "Zurückholen" }));
    await waitFor(() => {
      expect(calls.map((c) => `${c.method} ${c.path}`)).toEqual(
        expect.arrayContaining([
          "POST /api/worlds/salzmark/archive",
          "POST /api/worlds/glaskueste/restore",
        ]),
      );
    });
    expect(
      calls.filter((c) => c.path === "/api/worlds").length,
    ).toBeGreaterThan(2);
  });

  it("deletes for good only with the exact name and shows the consequences", async () => {
    const { calls } = fakeApi({
      "GET /api/worlds": ok([WORLD, GLAS]),
      "GET /api/worlds/glaskueste/deletion-preview": ok(GLAS_DELETION),
      "DELETE /api/worlds/glaskueste": noContent(),
    });
    const user = userEvent.setup();
    render(<Worlds onOpen={vi.fn()} />);
    await user.click(
      await screen.findByRole("button", { name: "Endgültig löschen …" }),
    );

    const dialog = await screen.findByRole("dialog", {
      name: "Welt „Glasküste“ endgültig löschen?",
    });
    expect(
      within(dialog).getByText(
        "Mit ihr: 42 Kanon-Einträge, 2 Karten, 11 Bilder, 1 Geschichte.",
      ),
    ).toBeDefined();
    expect(within(dialog).getByRole("listitem").textContent).toBe(
      "2 Gast-Verbindungen in „Die Überfahrt“ (Welt „Die Salzmark“: Kael, Mira) – werden dort samt 3 Fakten entfernt.",
    );
    const confirm = within(dialog).getByRole("button", {
      name: "Endgültig löschen",
    });
    expect(confirm).toHaveProperty("disabled", true);
    const field = within(dialog).getByLabelText(
      "Zum Bestätigen den Namen der Welt eintippen:",
    );
    expect(document.activeElement).toBe(field);
    await user.type(field, "glasküste");
    expect(confirm).toHaveProperty("disabled", true);
    await user.clear(field);
    await user.type(field, "Glasküste");
    expect(confirm).toHaveProperty("disabled", false);
    await user.click(confirm);

    await waitFor(() => {
      expect(screen.queryByRole("dialog")).toBeNull();
    });
    const deleted = calls.find((c) => c.method === "DELETE");
    expect(deleted).toEqual({
      method: "DELETE",
      path: "/api/worlds/glaskueste",
      body: { name: "Glasküste" },
    });
  });

  it("cancels with Escape or the button and shows refusals", async () => {
    const { calls } = fakeApi({
      "GET /api/worlds": ok([WORLD, GLAS]),
      "GET /api/worlds/glaskueste/deletion-preview": ok({
        ...GLAS_DELETION,
        entries: 1,
        maps: 1,
        images: 1,
        stories: 0,
        guest_uses: [
          { ...GLAS_DELETION.guest_uses[0], guests: ["Mira"], facts: 0 },
        ],
      }),
      "DELETE /api/worlds/glaskueste": fail(
        422,
        "Der eingetippte Name passt nicht zur Welt",
      ),
    });
    const user = userEvent.setup();
    render(<Worlds onOpen={vi.fn()} />);
    const open = await screen.findByRole("button", {
      name: "Endgültig löschen …",
    });
    await user.click(open);
    const dialog = await screen.findByRole("dialog");
    expect(
      within(dialog).getByText(
        "Mit ihr: 1 Kanon-Eintrag, 1 Karte, 1 Bild, 0 Geschichten.",
      ),
    ).toBeDefined();
    expect(within(dialog).getByRole("listitem").textContent).toBe(
      "1 Gast-Verbindung in „Die Überfahrt“ (Welt „Die Salzmark“: Mira) – werden dort entfernt.",
    );
    await user.keyboard("{Escape}");
    expect(screen.queryByRole("dialog")).toBeNull();

    await user.click(open);
    await user.click(
      within(await screen.findByRole("dialog")).getByRole("button", {
        name: "Abbrechen",
      }),
    );
    expect(screen.queryByRole("dialog")).toBeNull();

    await user.click(open);
    const again = await screen.findByRole("dialog");
    await user.type(within(again).getByRole("textbox"), "Glasküste");
    await user.click(
      within(again).getByRole("button", { name: "Endgültig löschen" }),
    );
    expect(
      await within(again).findByText(
        "Der eingetippte Name passt nicht zur Welt",
      ),
    ).toBeDefined();
    expect(calls.filter((c) => c.method === "DELETE")).toHaveLength(1);
  });

  it("shows errors of archiving, restoring and the preview", async () => {
    fakeApi({
      "GET /api/worlds": ok([WORLD, GLAS]),
      "POST /api/worlds/salzmark/archive": fail(500, "Archivieren ging nicht"),
      "POST /api/worlds/glaskueste/restore": fail(
        500,
        "Zurückholen ging nicht",
      ),
      "GET /api/worlds/glaskueste/deletion-preview": fail(404, "Welt weg"),
    });
    const user = userEvent.setup();
    render(<Worlds onOpen={vi.fn()} />);
    await user.click(
      await screen.findByLabelText("Weitere Aktionen für Die Salzmark"),
    );
    await user.click(screen.getByRole("button", { name: "Archivieren" }));
    expect(await screen.findByText("Archivieren ging nicht")).toBeDefined();
    await user.click(screen.getByRole("button", { name: "Zurückholen" }));
    expect(await screen.findByText("Zurückholen ging nicht")).toBeDefined();
    await user.click(
      screen.getByRole("button", { name: "Endgültig löschen …" }),
    );
    expect(await screen.findByText("Welt weg")).toBeDefined();
    expect(screen.queryByRole("dialog")).toBeNull();
  });
});

describe("archive of the stories (step 9.9, ADR-098)", () => {
  it("archives, restores and deletes a story for good", async () => {
    const { calls } = fakeApi({
      [`GET ${STORIES}`]: ok([STORY, OLD]),
      [`POST ${STORIES}/ueberfahrt/archive`]: ok({ ...STORY, archived: true }),
      [`POST ${STORIES}/erster-versuch/restore`]: ok({
        ...OLD,
        archived: false,
      }),
      [`GET ${STORIES}/erster-versuch/deletion-preview`]: ok(OLD_DELETION),
      [`DELETE ${STORIES}/erster-versuch`]: noContent(),
    });
    const user = userEvent.setup();
    render(<Stories world="salzmark" onOpen={vi.fn()} />);

    expect(
      await screen.findByRole("button", { name: "Die Überfahrt" }),
    ).toBeDefined();
    expect(screen.queryByRole("button", { name: "Erster Versuch" })).toBeNull();
    expect(screen.getByText("Archiv (1)")).toBeDefined();
    await user.click(
      screen.getByLabelText("Weitere Aktionen für Die Überfahrt"),
    );
    await user.click(screen.getByRole("button", { name: "Archivieren" }));
    await user.click(screen.getByRole("button", { name: "Zurückholen" }));
    await user.click(
      screen.getByRole("button", { name: "Endgültig löschen …" }),
    );

    const dialog = await screen.findByRole("dialog", {
      name: "„Erster Versuch“ endgültig löschen?",
    });
    expect(
      within(dialog).getByText(
        "Wird gelöscht: 1 Kapitel mit Kurzfassungen und Anweisungsverlauf, 2 Fakten, Titelbild.",
      ),
    ).toBeDefined();
    expect(
      within(dialog).getByText(
        "Bleibt: die Kosten im Verbrauch (ohne Bezug zur Geschichte).",
      ),
    ).toBeDefined();
    await user.type(
      within(dialog).getByLabelText("Zum Bestätigen den Titel eintippen:"),
      "Erster Versuch",
    );
    await user.click(
      within(dialog).getByRole("button", { name: "Endgültig löschen" }),
    );
    await waitFor(() => {
      expect(screen.queryByRole("dialog")).toBeNull();
    });
    expect(
      calls
        .filter((c) => c.method !== "GET")
        .map((c) => [c.method, c.path, c.body]),
    ).toEqual([
      ["POST", `${STORIES}/ueberfahrt/archive`, undefined],
      ["POST", `${STORIES}/erster-versuch/restore`, undefined],
      ["DELETE", `${STORIES}/erster-versuch`, { title: "Erster Versuch" }],
    ]);
  });

  it("names only what the story has, and shows errors of the preview", async () => {
    fakeApi({
      [`GET ${STORIES}`]: ok([OLD]),
      [`GET ${STORIES}/erster-versuch/deletion-preview`]: ok({
        ...OLD_DELETION,
        chapters: 3,
        facts: 0,
        cover: false,
      }),
    });
    const user = userEvent.setup();
    const { unmount } = render(<Stories world="salzmark" onOpen={vi.fn()} />);
    expect(await screen.findByText("Noch keine Geschichte.")).toBeDefined();
    await user.click(
      screen.getByRole("button", { name: "Endgültig löschen …" }),
    );
    expect(
      await screen.findByText(
        "Wird gelöscht: 3 Kapitel mit Kurzfassungen und Anweisungsverlauf.",
      ),
    ).toBeDefined();
    await user.click(screen.getByRole("button", { name: "Abbrechen" }));
    expect(screen.queryByRole("dialog")).toBeNull();
    unmount();

    fakeApi({
      [`GET ${STORIES}`]: ok([OLD]),
      [`GET ${STORIES}/erster-versuch/deletion-preview`]: fail(500, "kaputt"),
    });
    render(<Stories world="salzmark" onOpen={vi.fn()} />);
    await user.click(
      await screen.findByRole("button", { name: "Endgültig löschen …" }),
    );
    expect(await screen.findByText("kaputt")).toBeDefined();
  });

  it("leaves archived worlds and stories out of the list on the left", async () => {
    fakeApi({
      "GET /api/worlds": ok([WORLD, GLAS]),
      [`GET ${STORIES}`]: ok([STORY, OLD]),
      "GET /api/worlds/glaskueste/stories": ok([]),
    });
    render(
      <MemoryRouter>
        <StoryList world="salzmark" />
      </MemoryRouter>,
    );
    const list = screen.getByRole("navigation", { name: "Geschichten" });
    expect(
      await within(list).findByRole("link", { name: "Die Überfahrt" }),
    ).toBeDefined();
    expect(
      within(list).queryByRole("link", { name: "Erster Versuch" }),
    ).toBeNull();
    expect(within(list).queryByRole("link", { name: "Glasküste" })).toBeNull();
  });
});

describe("guests from an archived world (step 9.9)", () => {
  it("are not offered anew, but a bound one stays", async () => {
    const king = {
      ...ENTRY,
      world: "glaskueste",
      id: "mira",
      name: "Mira",
    };
    fakeApi({
      "GET /api/models": ok(modelList(["x-ai/grok-4.7"])),
      "GET /api/worlds": ok([
        WORLD,
        GLAS,
        { ...WORLD, id: "nebelreich", name: "Nebelreich" },
      ]),
      "GET /api/worlds/salzmark/entries": ok([ENTRY]),
      "GET /api/worlds/glaskueste/entries/mira": ok(king),
      [`GET ${STORIES}/ueberfahrt/chapters`]: ok([CHAPTER]),
    });
    const user = userEvent.setup();
    render(
      <StoryPage
        story={{
          ...STORY,
          guest_links: [{ world: "glaskueste", entry: "mira" }],
        }}
      />,
    );
    await openStorySettings(user);
    await user.click(await screen.findByText("Gäste aus anderen Welten (1)"));
    const world = screen.getByLabelText("Welt des Gastes");
    await waitFor(() => {
      expect(within(world).queryByText("Nebelreich")).not.toBeNull();
    });
    expect(within(world).queryByText("Glasküste")).toBeNull();
    const list = await screen.findByRole("list", { name: "Gäste" });
    expect(await within(list).findByText("Mira aus Glasküste")).toBeDefined();
  });
});

describe("deleting a chapter (step 9.9, ADR-098)", () => {
  const BASE = `${STORIES}/ueberfahrt`;
  const SECOND = { ...CHAPTER, number: 2, title: "Sturm", text: "Wind." };
  const THIRD = { ...CHAPTER, number: 3, title: "Ankunft", text: "Land." };

  function routes() {
    return {
      "GET /api/models": ok(modelList(["x-ai/grok-4.7"])),
      "GET /api/worlds": ok([WORLD]),
      "GET /api/worlds/salzmark/entries": ok([ENTRY]),
      [`GET ${BASE}/chapters`]: ok([CHAPTER, SECOND, THIRD]),
    };
  }

  it("asks first, names the overall summary and opens the chapter that moved up", async () => {
    const confirm = vi.spyOn(window, "confirm").mockReturnValueOnce(false);
    const moved = { ...THIRD, number: 2 };
    const { calls } = fakeApi({
      ...routes(),
      [`DELETE ${BASE}/chapters/2`]: ok([CHAPTER, moved]),
    });
    const user = userEvent.setup();
    const onOpenChapter = vi.fn();
    render(
      <StoryPage story={STORY} chapter={2} onOpenChapter={onOpenChapter} />,
    );
    expect(await screen.findByLabelText("Kapiteltitel")).toHaveProperty(
      "value",
      "Sturm",
    );
    const remove = screen.getByRole("button", { name: "Kapitel löschen …" });

    await user.click(remove);
    expect(confirm.mock.calls[0]?.[0]).toContain("Kapitel 2 „Sturm“ löschen?");
    expect(confirm.mock.calls[0]?.[0]).toContain(
      "Die Gesamtzusammenfassung enthält dieses Kapitel noch",
    );
    expect(calls.some((c) => c.method === "DELETE")).toBe(false);

    confirm.mockReturnValueOnce(true);
    await user.click(remove);
    await waitFor(() => {
      expect(onOpenChapter).toHaveBeenCalledWith(2);
    });
    // The chapter that moved up gets a fresh editor right away.
    expect(screen.getByLabelText("Kapiteltitel")).toHaveProperty(
      "value",
      "Ankunft",
    );
  });

  it("opens the chapter before the last one, the story without chapters, and shows errors", async () => {
    vi.spyOn(window, "confirm").mockReturnValue(true);
    fakeApi({
      ...routes(),
      [`DELETE ${BASE}/chapters/3`]: ok([CHAPTER, SECOND]),
      [`DELETE ${BASE}/chapters/1`]: fail(404, "Kapitel weg"),
    });
    const user = userEvent.setup();
    const onOpenChapter = vi.fn();
    const { unmount } = render(
      <StoryPage story={STORY} chapter={3} onOpenChapter={onOpenChapter} />,
    );
    await screen.findByLabelText("Kapiteltitel");
    await user.click(screen.getByRole("button", { name: "Kapitel löschen …" }));
    await waitFor(() => {
      expect(onOpenChapter).toHaveBeenCalledWith(2);
    });
    unmount();

    render(
      <StoryPage story={STORY} chapter={1} onOpenChapter={onOpenChapter} />,
    );
    await screen.findByLabelText("Kapiteltitel");
    await user.click(screen.getByRole("button", { name: "Kapitel löschen …" }));
    expect(await screen.findByText("Kapitel weg")).toBeDefined();
  });

  it("goes to the story when the last chapter is gone", async () => {
    vi.spyOn(window, "confirm").mockReturnValue(true);
    fakeApi({
      ...routes(),
      [`GET ${BASE}/chapters`]: ok([CHAPTER]),
      [`DELETE ${BASE}/chapters/1`]: ok([]),
      [`GET ${STORIES}`]: ok([STORY]),
      [`GET ${BASE}/chapters/1/instructions`]: ok([]),
    });
    const user = userEvent.setup();
    renderShell("/welt/salzmark/geschichte/ueberfahrt/kapitel/1");
    await screen.findByLabelText("Kapiteltitel");
    await user.click(screen.getByRole("button", { name: "Kapitel löschen …" }));
    await waitFor(() => {
      expect(screen.getByLabelText("Adresse").textContent).toBe(
        "/welt/salzmark/geschichte/ueberfahrt",
      );
    });
  });
});
