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
const SUGGEST = `${STREAM}/suggestions`;
const REPLY = [
  "Herkunft: nordeuropäisch wirkend | keltisch wirkend | slawisch wirkend",
  "Alter: 24 | 26 | 28",
  "Haar: kupferrot, glatt, taillenlang [Eintrag] | hellrot | dunkelblond",
].join("\n");
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
  await user.type(
    screen.getByRole("textbox", { name: "Herkunft (frei)" }),
    "Nordeuropa",
  );
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
    expect(
      screen.getByRole("button", { name: "✨ Vorschläge machen" }),
    ).toHaveProperty("disabled", true);
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

describe("the suggestions for the questions (step 11.5, ADR-124)", () => {
  const withLooks: CanonEntry = {
    ...FIGURE,
    body: "## Aussehen\n\n- **Alter:** 26\n- **Haar:** kupferrot, glatt\n\n## Wesen\n\nSchweigsam.",
  };

  // The badge follows the text; the accessible name may or may not put a space between them.
  const OWN = /^kupferrot, glatt\s*bisher$/;
  const FROM_ENTRY = /^kupferrot, glatt, taillenlang\s*aus Eintrag$/;

  function feedsOf() {
    const feeds: ReturnType<typeof sseFeed>[] = [];
    const handler = () => {
      const feed = sseFeed();
      feeds.push(feed);
      return { status: 200, stream: feed.stream };
    };
    return { feeds, handler };
  }

  function pressed(name: string | RegExp): string | null {
    return screen.getByRole("button", { name }).getAttribute("aria-pressed");
  }

  async function ready() {
    await waitFor(() => {
      expect(screen.getByRole("combobox", { name: "Modell" })).toBeDefined();
    });
  }

  it("asks with the answers so far, taps to pick and keeps the pick for new suggestions", async () => {
    const { feeds, handler } = feedsOf();
    const { calls } = fakeApi({
      "GET /api/models": ok(modelList(["x-ai/grok-4.6"])),
      [SUGGEST]: handler,
    });
    const user = userEvent.setup();
    open(withLooks);
    await ready();
    expect(screen.getByText("aus Eintrag und Welt")).toBeDefined();
    // The line already in the entry is the picked answer until the author taps another.
    expect(pressed(OWN)).toBe("true");

    await user.click(
      screen.getByRole("button", { name: "✨ Vorschläge machen" }),
    );
    expect(await screen.findByText("Die KI macht Vorschläge …")).toBeDefined();
    await waitFor(() => {
      expect(feeds).toHaveLength(1);
    });
    expect(calls.find((c) => c.method === "POST")?.body).toMatchObject({
      model: "x-ai/grok-4.6",
      answers: { Alter: "26", Haar: "kupferrot, glatt", Herkunft: "" },
    });
    finish(feeds[0] ?? sseFeed(), REPLY);
    expect(
      await screen.findByText(/noch einmal tippen für neue Vorschläge/),
    ).toBeDefined();
    expect(screen.getByText(/Verbrauch: 400 Token ein/)).toBeDefined();

    expect(pressed("nordeuropäisch wirkend")).toBe("false");
    expect(pressed(FROM_ENTRY)).toBe("false");
    await user.click(screen.getByRole("button", { name: "hellrot" }));
    expect(pressed("hellrot")).toBe("true");
    expect(pressed(OWN)).toBe("false");
    await user.click(screen.getByRole("button", { name: "hellrot" }));
    expect(pressed("hellrot")).toBe("false");
    await user.click(screen.getByRole("button", { name: "hellrot" }));
    await user.click(screen.getByRole("button", { name: "28" }));
    expect(screen.getByRole("textbox", { name: "Alter" })).toHaveProperty(
      "value",
      "28",
    );
    expect(pressed("28")).toBe("true");
    expect(pressed("24")).toBe("false");
    await user.type(
      screen.getByRole("textbox", { name: "Haar (frei)" }),
      "zum Zopf",
    );

    // New suggestions do not take the pick away.
    await user.click(
      screen.getByRole("button", { name: "✨ Vorschläge machen" }),
    );
    await waitFor(() => {
      expect(feeds).toHaveLength(2);
    });
    expect(calls.filter((c) => c.method === "POST").at(-1)?.body).toMatchObject(
      { answers: { Alter: "28", Haar: "hellrot, zum Zopf" } },
    );
    finish(feeds[1] ?? sseFeed(), "Haar: schwarz | grau | weiß");
    expect(
      await screen.findByRole("button", { name: "schwarz" }),
    ).toBeDefined();
    expect(pressed("hellrot")).toBe("true");
    expect(screen.queryByRole("button", { name: "dunkelblond" })).toBeNull();
    expect(screen.queryByRole("button", { name: "24" })).toBeNull();
  });

  it("says so when the reply has no suggestions in the asked form", async () => {
    const { feeds, handler } = feedsOf();
    fakeApi({
      "GET /api/models": ok(modelList(["x-ai/grok-4.6"])),
      [SUGGEST]: handler,
    });
    const user = userEvent.setup();
    open();
    await ready();
    await user.click(
      screen.getByRole("button", { name: "✨ Vorschläge machen" }),
    );
    await waitFor(() => {
      expect(feeds).toHaveLength(1);
    });
    finish(feeds[0] ?? sseFeed(), "Dazu kann ich nichts sagen.");
    expect(
      await screen.findByText(/keine Vorschläge in der erwarteten Form/),
    ).toBeDefined();
    expect(screen.queryByText(/noch einmal tippen/)).toBeNull();
  });

  it("reports a refusal of the provider and a refusal before streaming", async () => {
    const { feeds, handler } = feedsOf();
    let before = false;
    fakeApi({
      "GET /api/models": ok(modelList(["x-ai/grok-4.6"])),
      [SUGGEST]: () =>
        before ? { status: 422, body: { detail: "Keine Figur." } } : handler(),
    });
    const user = userEvent.setup();
    open();
    await ready();
    await user.click(
      screen.getByRole("button", { name: "✨ Vorschläge machen" }),
    );
    await waitFor(() => {
      expect(feeds).toHaveLength(1);
    });
    feeds[0]?.send("error", { kind: "abgelehnt" });
    feeds[0]?.close();
    expect(
      await screen.findByText("Das Modell hat die Anfrage abgelehnt."),
    ).toBeDefined();

    before = true;
    await user.click(
      screen.getByRole("button", { name: "✨ Vorschläge machen" }),
    );
    expect(await screen.findByText("Keine Figur.")).toBeDefined();
  });

  it("stops only the suggestions and keeps the window with the answers", async () => {
    const { feeds, handler } = feedsOf();
    fakeApi({
      "GET /api/models": ok(modelList(["x-ai/grok-4.6"])),
      [SUGGEST]: handler,
    });
    const user = userEvent.setup();
    const { onClose } = open();
    await ready();
    await user.type(
      screen.getByRole("textbox", { name: "Haar (frei)" }),
      "rot",
    );
    await user.click(
      screen.getByRole("button", { name: "✨ Vorschläge machen" }),
    );
    await waitFor(() => {
      expect(feeds).toHaveLength(1);
    });
    expect(
      screen.getByRole("button", { name: "✨ Vorschläge machen" }),
    ).toHaveProperty("disabled", true);
    await user.click(
      screen.getByRole("button", { name: "Vorschläge abbrechen" }),
    );
    await waitFor(() => {
      expect(
        screen.getByRole("button", { name: "✨ Vorschläge machen" }),
      ).toHaveProperty("disabled", false);
    });
    expect(onClose).not.toHaveBeenCalled();
    expect(screen.queryByText("Die KI macht Vorschläge …")).toBeNull();
    expect(screen.getByRole("textbox", { name: "Haar (frei)" })).toHaveProperty(
      "value",
      "rot",
    );
    expect(screen.getByRole("button", { name: "Verwerfen" })).toBeDefined();
  });
});
