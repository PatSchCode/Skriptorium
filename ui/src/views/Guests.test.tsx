import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { CompletionContext } from "@codemirror/autocomplete";
import { EditorState } from "@codemirror/state";
import { EditorView } from "@codemirror/view";
import { afterEach, describe, expect, it, vi } from "vitest";
import {
  modelList,
  openStorySettings,
  CHAPTER,
  created,
  ENTRY,
  fail,
  fakeApi,
  ok,
  sseFeed,
  STORY,
  WORLD,
} from "../../fake-api";
import { loadStoryEntries } from "../storyEntries";
import { mentions } from "./InstructionEditor";
import { StoryPage } from "./StoryPage";
import { WritingPanel } from "./WritingPanel";

const BASE = "/api/worlds/salzmark/stories/ueberfahrt";
const NEBEL = { id: "nebelreich", name: "Nebelreich", description: "Nebel" };
const KING = {
  world: "nebelreich",
  id: "nebelkoenig",
  category: "figur" as const,
  name: "Nebelkönig",
  aliases: ["König"],
  status: null,
  images: [],
  body: "Trägt eine Krone aus Reif.",
};
const PALACE = {
  ...KING,
  id: "reifpalast",
  category: "ort" as const,
  name: "Reifpalast",
  aliases: [],
};
const LINK = { world: "nebelreich", entry: "nebelkoenig" };
const WITH_GUEST = { ...STORY, guest_links: [LINK] };

afterEach(() => {
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});

function storyRoutes() {
  return {
    "GET /api/models": ok(modelList(["x-ai/grok-4.7"])),
    "GET /api/worlds": ok([WORLD, NEBEL]),
    "GET /api/worlds/salzmark/entries": ok([ENTRY]),
    "GET /api/worlds/nebelreich/entries": ok([KING, PALACE]),
    "GET /api/worlds/nebelreich/entries/nebelkoenig": ok(KING),
    "GET /api/worlds/nebelreich/entries/reifpalast": ok(PALACE),
    [`GET ${BASE}/chapters`]: ok([CHAPTER]),
  };
}

describe("guests from other worlds on the story page (step 3.7)", () => {
  it("binds in an entry of another world and lists it with its world", async () => {
    const { calls } = fakeApi({
      ...storyRoutes(),
      [`POST ${BASE}/guests`]: created(WITH_GUEST),
    });
    const user = userEvent.setup();
    render(<StoryPage story={STORY} />);
    await openStorySettings(user);
    await user.click(await screen.findByText("Gäste aus anderen Welten (0)"));

    const world = screen.getByLabelText("Welt des Gastes");
    await waitFor(() => {
      expect(within(world).queryByText("Nebelreich")).not.toBeNull();
    });
    expect(within(world).queryByText("Die Salzmark")).toBeNull();
    await user.selectOptions(world, "nebelreich");
    const entry = screen.getByLabelText("Gast-Eintrag");
    await within(entry).findByText("Nebelkönig");
    await user.selectOptions(entry, "nebelkoenig");
    await user.click(
      screen.getByRole("button", { name: "Als Gast einbinden" }),
    );

    expect(calls.find((c) => c.method === "POST")?.body).toEqual(LINK);
    const list = await screen.findByRole("list", { name: "Gäste" });
    expect(
      await within(list).findByText("Nebelkönig aus Nebelreich"),
    ).toBeDefined();
    expect(screen.getByText("Gäste aus anderen Welten (1)")).toBeDefined();
    // Already bound, so no longer offered.
    await waitFor(() => {
      expect(within(entry).queryByText("Nebelkönig")).toBeNull();
    });
  });

  it("removes a guest, but not one the author leads", async () => {
    const { calls } = fakeApi({
      ...storyRoutes(),
      [`DELETE ${BASE}/guests/nebelreich/nebelkoenig`]: ok(STORY),
    });
    const user = userEvent.setup();
    const { unmount } = render(
      <StoryPage
        story={{ ...WITH_GUEST, controlled_characters: ["nebelkoenig"] }}
      />,
    );
    await openStorySettings(user);
    await user.click(await screen.findByText("Gäste aus anderen Welten (1)"));
    await user.click(
      await screen.findByRole("button", { name: "Nebelkönig entfernen" }),
    );
    expect(
      await screen.findByText(
        "Nebelkönig führst du selbst – erst in der Figuren-Schreibweise abwählen.",
      ),
    ).toBeDefined();
    expect(calls.some((c) => c.method === "DELETE")).toBe(false);
    unmount();

    render(<StoryPage story={WITH_GUEST} />);
    await openStorySettings(user);
    await user.click(await screen.findByText("Gäste aus anderen Welten (1)"));
    await user.click(
      await screen.findByRole("button", { name: "Nebelkönig entfernen" }),
    );
    expect(
      await screen.findByText("Gäste aus anderen Welten (0)"),
    ).toBeDefined();
    expect(calls.some((c) => c.method === "DELETE")).toBe(true);
  });

  it("marks a guest whose entry is gone and shows refusals", async () => {
    fakeApi({
      ...storyRoutes(),
      "GET /api/worlds/nebelreich/entries/nebelkoenig": fail(404, "fehlt"),
      [`POST ${BASE}/guests`]: fail(422, "Unbekannter Kanon-Eintrag"),
    });
    const user = userEvent.setup();
    render(<StoryPage story={WITH_GUEST} />);
    await openStorySettings(user);
    await user.click(await screen.findByText("Gäste aus anderen Welten (1)"));

    expect(
      await screen.findByText(
        "nebelkoenig aus Nebelreich – Eintrag fehlt in seiner Welt",
      ),
    ).toBeDefined();
    await user.selectOptions(
      screen.getByLabelText("Welt des Gastes"),
      "nebelreich",
    );
    const entry = screen.getByLabelText("Gast-Eintrag");
    await within(entry).findByText("Reifpalast");
    await user.selectOptions(entry, "reifpalast");
    await user.click(
      screen.getByRole("button", { name: "Als Gast einbinden" }),
    );
    expect(await screen.findByText("Unbekannter Kanon-Eintrag")).toBeDefined();
  });

  it("offers guest characters in the writing mode", async () => {
    const { calls } = fakeApi({
      ...storyRoutes(),
      [`PATCH ${BASE}`]: (body) => ({
        status: 200,
        body: { ...WITH_GUEST, ...(body as object) },
      }),
    });
    const user = userEvent.setup();
    render(<StoryPage story={WITH_GUEST} />);
    await user.click(
      await screen.findByRole("button", {
        name: "Figuren-Schreibweise ändern",
      }),
    );
    const group = await screen.findByRole("group", {
      name: "Figuren, die du selbst führst",
    });
    await user.click(await within(group).findByLabelText("Nebelkönig (Gast)"));
    await user.click(
      screen.getByRole("button", { name: "Schreibweise speichern" }),
    );

    await waitFor(() => {
      expect(calls.find((c) => c.method === "PATCH")?.body).toEqual({
        perspective: "ich",
        controlled_characters: ["nebelkoenig"],
      });
    });
  });
});

describe("relation of a guest to the world of the story (step 9.13)", () => {
  const guestList = () => within(screen.getByRole("list", { name: "Gäste" }));

  async function openGuests(user: ReturnType<typeof userEvent.setup>) {
    await openStorySettings(user);
    await user.click(await screen.findByText("Gäste aus anderen Welten (1)"));
    return screen.findByLabelText(/In dieser Welt \(„Die Salzmark“\)/);
  }

  it("saves the relation trimmed, and only when it changed", async () => {
    const { calls } = fakeApi({
      ...storyRoutes(),
      [`PUT ${BASE}/guests/nebelreich/nebelkoenig`]: (body) => ({
        status: 200,
        body: {
          ...WITH_GUEST,
          guest_links: [
            { ...LINK, relation: (body as { relation: string }).relation },
          ],
        },
      }),
    });
    const user = userEvent.setup();
    render(
      <StoryPage
        story={{
          ...WITH_GUEST,
          guest_links: [{ ...LINK, relation: "Kam übers Eis." }],
        }}
      />,
    );
    const field = await openGuests(user);
    const save = guestList().getByRole("button", { name: "Speichern" });

    expect((field as HTMLTextAreaElement).value).toBe("Kam übers Eis.");
    expect((save as HTMLButtonElement).disabled).toBe(true);
    await user.clear(field);
    await user.type(field, "  Strandete nach der Flut. ");
    await user.click(save);

    await waitFor(() => {
      expect(calls.find((c) => c.method === "PUT")?.body).toEqual({
        relation: "Strandete nach der Flut.",
      });
    });
    expect(
      screen.getByText(/Abschnitte über Nebelreich \(„In …“\)/),
    ).toBeDefined();
  });

  it("takes over the world builder's proposal into the field", async () => {
    const feed = sseFeed();
    const { calls } = fakeApi({
      ...storyRoutes(),
      [`POST ${BASE}/guests/nebelreich/nebelkoenig/fit`]: () => ({
        status: 200,
        stream: feed.stream,
      }),
      [`PUT ${BASE}/guests/nebelreich/nebelkoenig`]: ok(WITH_GUEST),
    });
    const user = userEvent.setup();
    render(<StoryPage story={WITH_GUEST} />);
    const field = await openGuests(user);

    await user.click(
      screen.getByRole("button", { name: "✨ Einpassen vorschlagen" }),
    );
    expect(
      screen.getByRole("heading", {
        name: "Vorschlag des Weltenbauers für Nebelkönig",
      }),
    ).toBeDefined();
    await user.type(screen.getByLabelText(/Wunsch/), "soll fremd bleiben");
    await user.click(
      await screen.findByRole("button", { name: "Vorschlagen" }),
    );
    expect(calls.find((c) => c.path.endsWith("/fit"))?.body).toEqual({
      model: "x-ai/grok-4.7",
      wish: "soll fremd bleiben",
    });
    feed.send("text", { text: "Strandete nach der Flut " });
    feed.send("text", { text: "auf den Inseln." });
    feed.send("done", {
      input_tokens: 900,
      output_tokens: 40,
      cost_usd: 0.002,
      finish_reason: "stop",
    });
    feed.close();
    await user.click(
      await screen.findByRole("button", { name: "In das Feld übernehmen" }),
    );

    expect((field as HTMLTextAreaElement).value).toBe(
      "Strandete nach der Flut auf den Inseln.",
    );
    expect(screen.queryByLabelText("Vorschlag")).toBeNull();
    await user.click(guestList().getByRole("button", { name: "Speichern" }));
    await waitFor(() => {
      expect(calls.find((c) => c.method === "PUT")?.body).toEqual({
        relation: "Strandete nach der Flut auf den Inseln.",
      });
    });
  });

  it("discards a proposal, shows refusals and offers no field without entry", async () => {
    const feed = sseFeed();
    fakeApi({
      ...storyRoutes(),
      [`POST ${BASE}/guests/nebelreich/nebelkoenig/fit`]: () => ({
        status: 200,
        stream: feed.stream,
      }),
      [`PUT ${BASE}/guests/nebelreich/nebelkoenig`]: fail(
        422,
        "Weltbezug darf höchstens 4000 Zeichen lang sein",
      ),
    });
    const user = userEvent.setup();
    const { unmount } = render(<StoryPage story={WITH_GUEST} />);
    const field = await openGuests(user);

    await user.click(
      screen.getByRole("button", { name: "✨ Einpassen vorschlagen" }),
    );
    await user.click(
      await screen.findByRole("button", { name: "Vorschlagen" }),
    );
    feed.send("text", { text: "Etwas." });
    feed.send("error", { kind: "abgelehnt", message: "nein" });
    feed.close();
    expect(await screen.findByText(/abgelehnt|lehnt/i)).toBeDefined();
    await user.click(screen.getByRole("button", { name: "Verwerfen" }));
    expect((field as HTMLTextAreaElement).value).toBe("");
    await user.type(field, "Zu lang.");
    await user.click(guestList().getByRole("button", { name: "Speichern" }));
    expect(
      await screen.findByText(
        "Weltbezug darf höchstens 4000 Zeichen lang sein",
      ),
    ).toBeDefined();
    unmount();

    fakeApi({
      ...storyRoutes(),
      "GET /api/worlds/nebelreich/entries/nebelkoenig": fail(404, "fehlt"),
    });
    render(<StoryPage story={WITH_GUEST} />);
    await openStorySettings(user);
    await user.click(await screen.findByText("Gäste aus anderen Welten (1)"));
    await screen.findByText(/Eintrag fehlt in seiner Welt/);
    expect(screen.queryByLabelText(/In dieser Welt/)).toBeNull();
  });
});

describe("guests in the writing panel (step 3.7)", () => {
  it("sends a guest named with @ and offers guests for a new scene", async () => {
    const feed = sseFeed();
    const { calls } = fakeApi({
      ...storyRoutes(),
      [`POST ${BASE}/chapters/1/write`]: () => ({
        status: 200,
        stream: feed.stream,
      }),
    });
    const user = userEvent.setup();
    render(
      <WritingPanel
        world="salzmark"
        story="ueberfahrt"
        chapter={1}
        guests={[LINK, { world: "nebelreich", entry: "reifpalast" }]}
        prepare={() => Promise.resolve(true)}
        onAccept={() => Promise.resolve()}
      />,
    );
    const content = await screen.findByLabelText(/Anweisung an die KI/);
    const view = EditorView.findFromDOM(content);
    view?.dispatch({ changes: { from: 0, insert: "@König tritt ein." } });

    expect(
      await screen.findByText("Herangezogen: Nebelkönig (Gast)"),
    ).toBeDefined();
    await user.click(screen.getByLabelText("Neue Szene"));
    expect(
      screen.getByRole("option", { name: "Reifpalast (Gast)" }),
    ).toBeDefined();
    const figures = screen.getByRole("group", { name: "Figuren" });
    expect(within(figures).getByLabelText("Nebelkönig (Gast)")).toBeDefined();
    expect(within(figures).getByLabelText("Kael")).toBeDefined();
    await user.click(screen.getByLabelText("Neue Szene"));
    await user.click(screen.getByRole("button", { name: "Weiterschreiben" }));

    await waitFor(() => {
      expect(calls.find((c) => c.method === "POST")?.body).toMatchObject({
        references: ["nebelkoenig"],
      });
    });
    feed.close();
  });
});

describe("mentions and story entries with guests", () => {
  it("marks guests in the @ menu", () => {
    const state = EditorState.create({ doc: "@" });
    const result = mentions(
      new CompletionContext(state, 1, false),
      [ENTRY, KING],
      "salzmark",
    );
    expect(result?.options).toMatchObject([
      { label: "Kael", detail: "Figur" },
      { label: "Nebelkönig", detail: "Figur · Gast" },
    ]);
  });

  it("puts guests over entries of the world with the same identifier", async () => {
    const own = { ...ENTRY, id: "nebelkoenig", name: "Salz-König" };
    fakeApi({
      "GET /api/worlds/salzmark/entries": ok([ENTRY, own]),
      "GET /api/worlds/nebelreich/entries/nebelkoenig": ok(KING),
      "GET /api/worlds/nebelreich/entries/fehlt": fail(404, "fehlt"),
    });

    const entries = await loadStoryEntries("salzmark", [
      LINK,
      { world: "nebelreich", entry: "fehlt" },
    ]);

    expect(entries.map((e) => `${e.world}/${e.name}`)).toEqual([
      "salzmark/Kael",
      "nebelreich/Nebelkönig",
    ]);
  });

  it("passes other errors on", async () => {
    fakeApi({
      "GET /api/worlds/salzmark/entries": ok([]),
      "GET /api/worlds/nebelreich/entries/nebelkoenig": fail(500, "kaputt"),
    });

    await expect(loadStoryEntries("salzmark", [LINK])).rejects.toThrow();
  });
});

describe("guests named under Herangezogen (step 5.16)", () => {
  it("shows the guest's entry in the bar of the story", async () => {
    fakeApi(storyRoutes());
    const user = userEvent.setup();
    render(<StoryPage story={WITH_GUEST} />);
    const content = await screen.findByLabelText(/Anweisung an die KI/);
    EditorView.findFromDOM(content)?.dispatch({
      changes: { from: 0, insert: "@König tritt ein." },
    });
    await user.click(
      await screen.findByRole("button", { name: "Nebelkönig (Gast)" }),
    );
    const side = screen.getByRole("complementary", {
      name: "Kanon und Geschichte",
    });
    expect(
      await within(side).findByRole("heading", { name: "Nebelkönig" }),
    ).toBeDefined();
    expect(within(side).getByText("Trägt eine Krone aus Reif.")).toBeDefined();
    expect(
      within(side).getByText(
        "Gast aus einer anderen Welt – nur in deren Kanon zu ändern.",
      ),
    ).toBeDefined();
  });
});
