import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { EditorView } from "@codemirror/view";
import { afterEach, describe, expect, it, vi } from "vitest";
import {
  catalogModel,
  ENTRY,
  fakeApi,
  modelList,
  ok,
  sseFeed,
} from "../../fake-api";
import { PictureSwitch, picturedEntries } from "./PictureSwitch";
import { describeUsage } from "./useWriteFlow";
import { WritingPanel } from "./WritingPanel";

const WRITE = "POST /api/worlds/salzmark/stories/ueberfahrt/chapters/1/write";
const KAEL = { ...ENTRY, images: ["kael-1.png", "kael-2.png"] };
const PLACE = {
  ...ENTRY,
  id: "grauwasser",
  category: "ort" as const,
  name: "Grauwasser",
  aliases: [],
  images: ["hafen.jpg"],
};
const MIRA = { ...ENTRY, id: "mira", name: "Mira", aliases: [], images: [] };

afterEach(() => {
  vi.restoreAllMocks();
});

function routes(feed: ReturnType<typeof sseFeed>, reads = true) {
  return {
    "GET /api/models": ok(
      modelList(
        ["x-ai/grok-4.7"],
        [catalogModel("x-ai/grok-4.7", { reads_images: reads })],
      ),
    ),
    "GET /api/worlds/salzmark/entries": ok([KAEL, PLACE, MIRA]),
    [WRITE]: () => ({ status: 200, stream: feed.stream }),
  };
}

function panel() {
  render(
    <WritingPanel
      world="salzmark"
      story="ueberfahrt"
      chapter={1}
      prepare={vi.fn(() => Promise.resolve(true))}
      onAccept={vi.fn(() => Promise.resolve())}
    />,
  );
}

async function typeInstruction(text: string) {
  const content = await screen.findByLabelText(/Anweisung an die KI/);
  const view = EditorView.findFromDOM(content);
  if (view === null) {
    throw new Error("instruction field without editor");
  }
  view.dispatch({
    changes: { from: 0, insert: text },
    userEvent: "input.type",
  });
}

describe("images along with writing (step 10.7, ADR-111)", () => {
  it("offers the main images of named entries, sends them once and names them", async () => {
    const feed = sseFeed();
    const { calls } = fakeApi(routes(feed));
    panel();
    const user = userEvent.setup();
    await screen.findByRole("option", { name: /grok-4\.7/ });

    await typeInstruction("@Kael trifft @Mira in @Grauwasser.");
    const box = await screen.findByLabelText("Bilder mitschicken");
    const line = box.closest("p");
    expect(line?.textContent).toContain(
      "2 Bilder, ca. +1,0 ct · ohne Bild: Mira",
    );
    const thumbs = within(line as HTMLElement).getAllByRole("img");
    expect(thumbs.map((image) => image.getAttribute("alt"))).toEqual([
      "Kael",
      "Grauwasser",
    ]);
    expect(thumbs[0]?.getAttribute("src")).toBe(
      "/api/worlds/salzmark/entries/kael/images/kael-1.png",
    );
    expect(box).toHaveProperty("checked", false);

    await user.click(box);
    await user.click(screen.getByRole("button", { name: "Weiterschreiben" }));

    await waitFor(() => {
      expect(calls.find((c) => c.method === "POST")?.body).toEqual({
        instruction: "@Kael trifft @Mira in @Grauwasser.",
        references: ["kael", "mira", "grauwasser"],
        model: "x-ai/grok-4.7",
        length: "mittel",
        scene: null,
        images: true,
      });
    });
    expect(screen.getByLabelText("Bilder mitschicken")).toHaveProperty(
      "checked",
      false,
    );
    feed.send("start", {
      model: "x-ai/grok-4.7",
      estimated_tokens: 6000,
      images: 2,
    });
    feed.send("text", { text: "Der Nebel hob sich." });
    feed.send("done", {
      input_tokens: 5800,
      output_tokens: 5,
      cost_usd: 0.012,
      finish_reason: "stop",
    });
    feed.close();
    expect(await screen.findByText(/· mit 2 Bildern$/)).toBeDefined();
  });

  it("sends no images unless ticked, and counts the place of a new scene", async () => {
    const feed = sseFeed();
    const { calls } = fakeApi(routes(feed));
    panel();
    const user = userEvent.setup();
    await screen.findByRole("option", { name: /grok-4\.7/ });

    expect(screen.queryByLabelText("Bilder mitschicken")).toBeNull();
    await user.click(screen.getByLabelText("Neue Szene"));
    await user.selectOptions(await screen.findByLabelText("Ort"), "grauwasser");
    const line = screen.getByLabelText("Bilder mitschicken").closest("p");
    expect(line?.textContent).toContain("1 Bild, ca. +0,5 ct");
    await user.click(screen.getByRole("button", { name: "Szene beginnen" }));

    await waitFor(() => {
      expect(calls.find((c) => c.method === "POST")?.body).toEqual({
        instruction: "",
        references: [],
        model: "x-ai/grok-4.7",
        length: "mittel",
        scene: { place: "grauwasser", characters: [], goal: "" },
      });
    });
    feed.close();
  });

  it("locks the switch for a model that does not read images", async () => {
    const feed = sseFeed();
    const { calls } = fakeApi(routes(feed, false));
    panel();
    const user = userEvent.setup();
    await screen.findByRole("option", { name: /grok-4\.7/ });

    await typeInstruction("@Kael wartet.");
    const box = await screen.findByLabelText("Bilder mitschicken");
    expect(box).toHaveProperty("disabled", true);
    expect(box.closest("p")?.textContent).toContain(
      "grok-4.7 kann keine Bilder lesen.",
    );
    await user.click(screen.getByRole("button", { name: "Weiterschreiben" }));
    await waitFor(() => {
      expect(calls.find((c) => c.method === "POST")?.body).not.toHaveProperty(
        "images",
      );
    });
    feed.close();
  });

  it("takes at most four, in the order named, and admits an unknown price", () => {
    const named = ["a", "b", "c", "d", "e"].map((id) => ({
      ...KAEL,
      id,
      name: id.toUpperCase(),
    }));
    expect(picturedEntries([MIRA, ...named]).map((entry) => entry.id)).toEqual([
      "a",
      "b",
      "c",
      "d",
    ]);
    render(
      <PictureSwitch
        named={named}
        model={catalogModel("x-ai/grok-4.7", {
          reads_images: true,
          input_price: null,
        })}
        modelId="x-ai/grok-4.7"
        checked={true}
        disabled={false}
        onChange={vi.fn()}
      />,
    );
    const line = screen.getByLabelText("Bilder mitschicken").closest("p");
    expect(line?.textContent).toContain("4 von 5 Bildern, Preis unbekannt");
    expect(within(line as HTMLElement).getAllByRole("img")).toHaveLength(4);
  });

  it("names a single image in the usage line", () => {
    const usage = {
      type: "done" as const,
      input_tokens: 1000,
      output_tokens: 10,
      cost_usd: null,
      finish_reason: "stop",
    };
    expect(describeUsage(usage, 1)).toBe(
      "Verbrauch: 1.000 Token ein, 10 aus · Kosten nicht gemeldet · mit 1 Bild",
    );
    expect(describeUsage(usage)).not.toContain("Bild");
  });
});
