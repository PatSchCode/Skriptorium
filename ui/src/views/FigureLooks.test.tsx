import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import { ENTRY, fail, fakeApi, modelList, ok, sseFeed } from "../../fake-api";
import type { CanonEntry } from "../api";
import { EntryArticle } from "./EntryArticle";
import { FigureLooks } from "./FigureLooks";

vi.mock("../files", () => ({
  GENERATED_SIDE: 4096,
  shrinkImage: vi.fn(() => Promise.resolve(new Blob(["klein"]))),
  base64: vi.fn(() => Promise.resolve("a2xlaW4=")),
}));

const STREAM = "POST /api/worlds/salzmark/entries/kael/figure-looks";
const ENTRY_GET = "GET /api/worlds/salzmark/entries/kael";
const PATCH = "PATCH /api/worlds/salzmark/entries/kael";
const DESCRIPTION = "a 34-year-old adult Northern European man, black hair";
const FIGURE: CanonEntry = {
  ...ENTRY,
  body: "Fährmann.\n\n## Wesen\n\nSchweigsam.",
};

afterEach(() => {
  vi.restoreAllMocks();
});

function open(
  entry: CanonEntry = FIGURE,
  onChanged = vi.fn(),
  onClose = vi.fn(),
) {
  render(<FigureLooks entry={entry} onChanged={onChanged} onClose={onClose} />);
  return { onChanged, onClose };
}

function finish(feed: ReturnType<typeof sseFeed>, text: string) {
  feed.send("text", { text });
  feed.send("done", {
    input_tokens: 400,
    output_tokens: 40,
    cost_usd: 0.006,
    finish_reason: "stop",
  });
  feed.close();
}

async function answerAndFormulate(user: ReturnType<typeof userEvent.setup>) {
  await user.type(screen.getByRole("textbox", { name: "Alter" }), "34");
  await user.click(screen.getByRole("button", { name: "Nordeuropa" }));
  await user.type(
    screen.getByRole("textbox", { name: "Haar (frei)" }),
    "schwarz",
  );
  await user.click(screen.getByRole("button", { name: "✨ Formulieren" }));
}

describe("the figure assistant (step 11.5, ADR-123)", () => {
  it("is offered on a figure and says what is missing", async () => {
    fakeApi({ "GET /api/models": ok(modelList(["x-ai/grok-4.6"])) });
    const user = userEvent.setup();
    const { rerender } = render(
      <EntryArticle
        world="salzmark"
        current={FIGURE}
        compact={false}
        onEdit={vi.fn()}
        onSaved={vi.fn()}
      />,
    );
    expect(screen.getByText("– noch kein Abschnitt „Aussehen“")).toBeDefined();
    rerender(
      <EntryArticle
        world="salzmark"
        current={{ ...FIGURE, body: "## Aussehen\n\n- **Alter:** 30" }}
        compact={false}
        onEdit={vi.fn()}
        onSaved={vi.fn()}
      />,
    );
    expect(screen.getByText("– noch keine Bildbeschreibung")).toBeDefined();
    rerender(
      <EntryArticle
        world="salzmark"
        current={{
          ...FIGURE,
          body: "## Aussehen\n\n- **Alter:** 30\n\n## Bildbeschreibung\n\na man",
        }}
        compact={false}
        onEdit={vi.fn()}
        onSaved={vi.fn()}
      />,
    );
    expect(screen.queryByText(/– noch/)).toBeNull();
    await user.click(
      screen.getByRole("button", { name: "✨ Aussehen festlegen" }),
    );
    expect(screen.getByRole("textbox", { name: "Alter" })).toHaveProperty(
      "value",
      "30",
    );
    await user.click(screen.getByRole("button", { name: "Verwerfen" }));
    expect(
      screen.getByRole("button", { name: "✨ Aussehen festlegen" }),
    ).toBeDefined();
  });

  it("asks for an adult age before it formulates", async () => {
    fakeApi({ "GET /api/models": ok(modelList(["x-ai/grok-4.6"])) });
    const user = userEvent.setup();
    open();
    const formulate = await screen.findByRole("button", {
      name: "✨ Formulieren",
    });
    await waitFor(() => {
      expect(screen.getByRole("combobox", { name: "Modell" })).toBeDefined();
    });
    expect(formulate).toHaveProperty("disabled", true);
    expect(screen.getByText("Jahre, ab 18")).toBeDefined();
    await user.type(screen.getByRole("textbox", { name: "Alter" }), "16");
    expect(screen.getByText("Nur ganze Zahl ab 18")).toBeDefined();
    expect(formulate).toHaveProperty("disabled", true);
    await user.clear(screen.getByRole("textbox", { name: "Alter" }));
    await user.type(screen.getByRole("textbox", { name: "Alter" }), "18");
    expect(formulate).toHaveProperty("disabled", false);
  });

  it("formulates, writes Aussehen and Bildbeschreibung and keeps the rest", async () => {
    const feed = sseFeed();
    const { calls } = fakeApi({
      "GET /api/models": ok(modelList(["x-ai/grok-4.6"])),
      [STREAM]: () => ({ status: 200, stream: feed.stream }),
      [ENTRY_GET]: ok(FIGURE),
      [PATCH]: ok({ ...FIGURE, body: "neu" }),
      "GET /api/images/models": ok({
        default: "x/y",
        models: [{ id: "x/y", name: "Y", references: 0 }],
        available: true,
        ready: true,
      }),
    });
    const user = userEvent.setup();
    const { onChanged, onClose } = open();
    await waitFor(() => {
      expect(screen.getByRole("combobox", { name: "Modell" })).toBeDefined();
    });
    await answerAndFormulate(user);
    expect(calls.find((c) => c.method === "POST")?.body).toEqual({
      model: "x-ai/grok-4.6",
      answers: {
        Herkunft: "Nordeuropa",
        Alter: "34",
        Größe: "",
        Körperbau: "",
        Proportionen: "",
        Gesicht: "",
        Haar: "schwarz",
        Augen: "",
        Haut: "",
        "Besondere Merkmale": "",
      },
    });
    finish(feed, DESCRIPTION);
    const description = await screen.findByRole("textbox", {
      name: "Bildbeschreibung (Englisch, für Bildmodelle)",
    });
    expect(description).toHaveProperty("value", DESCRIPTION);
    expect(
      screen.getByRole("textbox", { name: "Aussehen (Deutsch)" }),
    ).toHaveProperty(
      "value",
      expect.stringContaining("- **Herkunft:** Nordeuropa\n- **Alter:** 34\n"),
    );
    expect(
      await screen.findByText(/Kein Bildmodell mit Startwert/),
    ).toBeDefined();
    await user.type(description, ", beard");
    await user.click(screen.getByRole("button", { name: "Übernehmen" }));
    await waitFor(() => {
      expect(onChanged).toHaveBeenCalled();
    });
    expect(onClose).toHaveBeenCalled();
    const body = (calls.at(-1)?.body as { body: string }).body;
    expect(body).toBe(
      "Fährmann.\n\n## Wesen\n\nSchweigsam.\n\n## Aussehen\n\n" +
        "- **Herkunft:** Nordeuropa\n- **Alter:** 34\n- **Größe:** –\n" +
        "- **Körperbau:** –\n- **Proportionen:** –\n- **Gesicht:** –\n" +
        "- **Haar:** schwarz\n- **Augen:** –\n- **Haut:** –\n" +
        "- **Besondere Merkmale:** –\n\n## Bildbeschreibung\n\n" +
        `${DESCRIPTION}, beard\n`,
    );
  });

  it("offers another model when the answer is not a description", async () => {
    const feed = sseFeed();
    fakeApi({
      "GET /api/models": ok(modelList(["x-ai/grok-4.6", "qwen/qwen3.8-max"])),
      [STREAM]: () => ({ status: 200, stream: feed.stream }),
    });
    const user = userEvent.setup();
    open();
    await waitFor(() => {
      expect(screen.getByRole("combobox", { name: "Modell" })).toBeDefined();
    });
    await answerAndFormulate(user);
    finish(feed, "I can't help with that.");
    expect(await screen.findByText(/vermutlich gesperrt/)).toBeDefined();
    expect(screen.getByRole("combobox", { name: "Modell" })).toBeDefined();
    expect(
      screen.getByRole("button", { name: "✨ Formulieren" }),
    ).toBeDefined();
    expect(screen.queryByRole("button", { name: "Übernehmen" })).toBeNull();
  });

  it("treats a refusal of the provider the same way", async () => {
    const feed = sseFeed();
    fakeApi({
      "GET /api/models": ok(modelList(["x-ai/grok-4.6"])),
      [STREAM]: () => ({ status: 200, stream: feed.stream }),
    });
    const user = userEvent.setup();
    open();
    await waitFor(() => {
      expect(screen.getByRole("combobox", { name: "Modell" })).toBeDefined();
    });
    await answerAndFormulate(user);
    feed.send("error", { kind: "abgelehnt" });
    feed.close();
    expect(
      await screen.findByText("Das Modell hat die Anfrage abgelehnt."),
    ).toBeDefined();
    expect(screen.getByText(/vermutlich gesperrt/)).toBeDefined();
  });

  it("reports a refusal before streaming and a failed model list", async () => {
    fakeApi({
      "GET /api/models": ok(modelList(["x-ai/grok-4.6"])),
      [STREAM]: fail(422, "Das Alter muss eine ganze Zahl ab 18 sein."),
    });
    const user = userEvent.setup();
    open();
    await waitFor(() => {
      expect(screen.getByRole("combobox", { name: "Modell" })).toBeDefined();
    });
    await answerAndFormulate(user);
    expect(
      await screen.findByText("Das Alter muss eine ganze Zahl ab 18 sein."),
    ).toBeDefined();
  });

  it("says so when the model list cannot be loaded", async () => {
    fakeApi({ "GET /api/models": fail(500, "kaputt") });
    open();
    expect(await screen.findByText("kaputt")).toBeDefined();
    expect(screen.queryByRole("combobox", { name: "Modell" })).toBeNull();
  });

  it("asks before it replaces looks, and back to the questions keeps the answers", async () => {
    const feeds: ReturnType<typeof sseFeed>[] = [];
    const withLooks = {
      ...FIGURE,
      body: "## Aussehen\n\nGroß und hager.\n\n## Wesen\n\nSchweigsam.",
    };
    const { calls } = fakeApi({
      "GET /api/models": ok(modelList(["x-ai/grok-4.6"])),
      [STREAM]: () => {
        const feed = sseFeed();
        feeds.push(feed);
        return { status: 200, stream: feed.stream };
      },
      [ENTRY_GET]: ok(withLooks),
      [PATCH]: ok(withLooks),
      "GET /api/images/models": ok({
        default: "x/y",
        models: [],
        available: true,
        ready: true,
      }),
    });
    const user = userEvent.setup();
    const { onChanged } = open(withLooks);
    await waitFor(() => {
      expect(screen.getByRole("combobox", { name: "Modell" })).toBeDefined();
    });
    await answerAndFormulate(user);
    await waitFor(() => {
      expect(feeds).toHaveLength(1);
    });
    finish(feeds[0] ?? sseFeed(), DESCRIPTION);
    await user.click(
      await screen.findByRole("button", { name: "Zurück zu den Fragen" }),
    );
    expect(screen.getByRole("textbox", { name: "Alter" })).toHaveProperty(
      "value",
      "34",
    );
    await user.click(screen.getByRole("button", { name: "✨ Formulieren" }));
    await waitFor(() => {
      expect(feeds).toHaveLength(2);
    });
    finish(feeds[1] ?? sseFeed(), DESCRIPTION);
    await user.click(await screen.findByRole("button", { name: "Übernehmen" }));
    await user.click(await screen.findByRole("button", { name: "Abbrechen" }));
    expect(calls.some((c) => c.method === "PATCH")).toBe(false);
    expect(onChanged).not.toHaveBeenCalled();
  });
  it("adds the picked draft as main image with its origin", async () => {
    const feed = sseFeed();
    const withImage = { ...FIGURE, images: ["alt.webp"] };
    const { calls } = fakeApi({
      "GET /api/models": ok(modelList(["x-ai/grok-4.6"])),
      [STREAM]: () => ({ status: 200, stream: feed.stream }),
      [ENTRY_GET]: ok(withImage),
      [PATCH]: ok(withImage),
      "GET /api/images/models": ok({
        default: "b/mit",
        models: [{ id: "b/mit", name: "Mit", references: 0, seed: true }],
        available: true,
        ready: true,
      }),
      "POST /api/images/generate": ok({
        content: "aGFsbG8=",
        media_type: "image/png",
        cost_usd: 0.004,
        model: "b/mit",
        seed: 505,
      }),
      "POST /api/worlds/salzmark/entries/kael/images": ok({
        ...withImage,
        images: ["alt.webp", "neu.webp"],
      }),
      "POST /api/worlds/salzmark/entries/kael/images/neu.webp/main": ok({
        ...withImage,
        images: ["neu.webp", "alt.webp"],
      }),
    });
    const user = userEvent.setup();
    const { onChanged } = open(withImage);
    await waitFor(() => {
      expect(screen.getByRole("combobox", { name: "Modell" })).toBeDefined();
    });
    await answerAndFormulate(user);
    finish(feed, DESCRIPTION);
    await user.click(
      await screen.findByRole("button", { name: "🎲 4 Entwürfe erzeugen" }),
    );
    await user.click((await screen.findAllByRole("radio"))[0] as HTMLElement);
    await user.click(screen.getByRole("button", { name: "Übernehmen" }));
    await waitFor(() => {
      expect(onChanged).toHaveBeenCalledWith({
        ...withImage,
        images: ["neu.webp", "alt.webp"],
      });
    });
    const upload = calls.find(
      (c) => c.path === "/api/worlds/salzmark/entries/kael/images",
    );
    expect(upload?.body).toMatchObject({
      content: "a2xlaW4=",
      herkunft: { model: "b/mit", seed: 505, aspect_ratio: "2:3" },
    });
  });
  it("keeps the window when saving fails, with edited lines", async () => {
    const feed = sseFeed();
    fakeApi({
      "GET /api/models": ok(modelList(["x-ai/grok-4.6"])),
      [STREAM]: () => ({ status: 200, stream: feed.stream }),
      [ENTRY_GET]: ok(FIGURE),
      [PATCH]: fail(409, "Eintrag geändert"),
      "GET /api/images/models": ok({
        default: "x/y",
        models: [],
        available: true,
        ready: true,
      }),
    });
    const user = userEvent.setup();
    const { onChanged, onClose } = open();
    await waitFor(() => {
      expect(screen.getByRole("combobox", { name: "Modell" })).toBeDefined();
    });
    await answerAndFormulate(user);
    finish(feed, DESCRIPTION);
    const lines = await screen.findByRole("textbox", {
      name: "Aussehen (Deutsch)",
    });
    await user.type(lines, "!");
    expect((lines as HTMLTextAreaElement).value.endsWith("–!")).toBe(true);
    await user.click(screen.getByRole("button", { name: "Übernehmen" }));
    expect(await screen.findByText("Eintrag geändert")).toBeDefined();
    expect(onChanged).not.toHaveBeenCalled();
    expect(onClose).not.toHaveBeenCalled();
    expect(screen.getByRole("button", { name: "Übernehmen" })).toHaveProperty(
      "disabled",
      false,
    );
  });

  it("stops the request on Abbrechen and closes", async () => {
    const feed = sseFeed();
    fakeApi({
      "GET /api/models": ok(modelList(["x-ai/grok-4.6", "b/zwei"])),
      [STREAM]: () => ({ status: 200, stream: feed.stream }),
    });
    const user = userEvent.setup();
    const { onClose } = open();
    const select = await screen.findByRole("combobox", { name: "Modell" });
    await user.selectOptions(select, "b/zwei");
    await answerAndFormulate(user);
    expect(
      await screen.findByText("Die KI formuliert die Bildbeschreibung …"),
    ).toBeDefined();
    await user.click(screen.getByRole("button", { name: "Abbrechen" }));
    expect(onClose).toHaveBeenCalled();
  });
});
