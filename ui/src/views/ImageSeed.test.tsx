import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import { fakeApi, ok } from "../../fake-api";
import type {
  ImageModelList,
  ImageOrigin,
  LoraChoice,
  StoredImageOrigin,
} from "../api";
import { ImageGenerate } from "./ImageGenerate";
import { ImageOriginPanel, seedOf } from "./ImageOriginPanel";

const FLEX = "black-forest-labs/flux.2-flex";
const PRO = "black-forest-labs/flux.2-pro";
const EPIC = "civitai:277058@1405120";
const CUFFS = "civitai:536201@596079";

const LIST: ImageModelList = {
  default: FLEX,
  models: [
    { id: FLEX, name: "FLUX.2 Flex", references: 0, seed: true },
    { id: PRO, name: "FLUX.2 Pro", references: 1 },
  ],
  available: true,
  ready: true,
  runware: [
    {
      id: EPIC,
      name: "epiCRealism XL VXIV",
      architecture: "sdxl",
      addition: "raw photo",
      loras: [CUFFS],
    },
  ],
  loras: [
    {
      id: CUFFS,
      name: "Handcuffs",
      architecture: "pony",
      trigger: "handcuffs",
      weight: 0.8,
    },
  ],
  runware_ready: true,
};

function image(model: string, seed: number | null, appended: string | null) {
  return ok({
    content: "iVBORw0KGgo=",
    media_type: "image/png",
    cost_usd: 0.003,
    model,
    seed,
    appended,
  });
}

afterEach(() => {
  vi.restoreAllMocks();
});

function dialog({
  initialModel = null,
  initialSeed = null,
  initialLoras = [],
  onTakeOver = () => Promise.resolve(),
}: {
  initialModel?: string | null;
  initialSeed?: number | null;
  initialLoras?: LoraChoice[];
  onTakeOver?: (image: Blob, origin: ImageOrigin) => Promise<void>;
} = {}) {
  return render(
    <ImageGenerate
      target={{ world: "die-salzmark" }}
      title="Bild erzeugen"
      initialPrompt="Mira am Kai"
      initialFormat="2:3"
      initialModel={initialModel}
      initialSeed={initialSeed}
      initialLoras={initialLoras}
      onTakeOver={onTakeOver}
      onClose={() => undefined}
    />,
  );
}

function posts(calls: { method: string; body: unknown }[]) {
  return calls.filter((c) => c.method === "POST").map((c) => c.body);
}

describe("start value when generating (step 11.4, ADR-121)", () => {
  it("is random first, then kept from the preview and sent", async () => {
    const { calls } = fakeApi({
      "GET /api/images/models": ok(LIST),
      "GET /api/images/price": ok({ cost_usd: 0.02, unit: "image" }),
      "POST /api/images/generate": image(FLEX, 1834072215, null),
    });
    const user = userEvent.setup();
    dialog();
    const random = await screen.findByRole("radio", { name: "zufällig" });
    expect(random.getAttribute("aria-checked")).toBe("true");
    expect(screen.getByLabelText("Fester Startwert")).toHaveProperty(
      "disabled",
      true,
    );
    await user.click(screen.getByRole("button", { name: "✨ Erzeugen" }));
    expect(await screen.findByText(/Startwert 1834072215/)).toBeDefined();
    await user.click(
      screen.getByRole("button", { name: "Startwert behalten" }),
    );
    await user.click(
      screen.getByRole("button", { name: "Beschreibung ändern" }),
    );
    expect(
      screen.getByRole("radio", { name: "fest" }).getAttribute("aria-checked"),
    ).toBe("true");
    expect(screen.getByLabelText("Fester Startwert")).toHaveProperty(
      "value",
      "1834072215",
    );
    await user.click(screen.getByRole("button", { name: "✨ Erzeugen" }));
    await screen.findByAltText("Vorschau des erzeugten Bildes");
    const [first, second] = posts(calls);
    expect(first).not.toHaveProperty("seed");
    expect(second).toEqual({
      model: FLEX,
      prompt: "Mira am Kai",
      aspect_ratio: "2:3",
      world: "die-salzmark",
      seed: 1834072215,
    });
  });

  it("refuses a fixed value out of range and hides the line for other models", async () => {
    fakeApi({
      "GET /api/images/models": ok(LIST),
      "GET /api/images/price": ok({ cost_usd: 0.02, unit: "image" }),
    });
    const user = userEvent.setup();
    dialog();
    await user.click(await screen.findByRole("radio", { name: "fest" }));
    const field = screen.getByLabelText("Fester Startwert");
    await user.type(field, "0");
    expect(screen.getByText(/ganze Zahl von 1 bis/)).toBeDefined();
    const go = screen.getByRole("button", { name: "✨ Erzeugen" });
    expect(go).toHaveProperty("disabled", true);
    await user.clear(field);
    await user.type(field, "2147483648");
    expect(go).toHaveProperty("disabled", true);
    await user.clear(field);
    await user.type(field, "12");
    expect(go).toHaveProperty("disabled", false);
    await user.selectOptions(screen.getByLabelText("Modell"), PRO);
    expect(screen.queryByRole("radio", { name: "fest" })).toBeNull();
    expect(go).toHaveProperty("disabled", false);
  });

  it("takes over start value, LoRAs and the appended text into the origin", async () => {
    fakeApi({
      "GET /api/images/models": ok(LIST),
      "GET /api/images/price": ok({ cost_usd: null, unit: null }),
      "POST /api/images/generate": image(EPIC, 42, "raw photo, handcuffs"),
    });
    const user = userEvent.setup();
    const onTakeOver = vi.fn<
      (image: Blob, origin: ImageOrigin) => Promise<void>
    >(() => Promise.resolve());
    dialog({
      initialModel: EPIC,
      initialSeed: 42,
      initialLoras: [{ id: CUFFS, weight: 0.6 }],
      onTakeOver,
    });
    const cuffs = await screen.findByRole("checkbox", { name: "Handcuffs" });
    expect(cuffs).toHaveProperty("checked", true);
    expect(screen.getByLabelText("Fester Startwert")).toHaveProperty(
      "value",
      "42",
    );
    await user.click(screen.getByRole("button", { name: "✨ Erzeugen" }));
    await user.click(await screen.findByRole("button", { name: "Übernehmen" }));
    await waitFor(() => {
      expect(onTakeOver).toHaveBeenCalled();
    });
    expect(onTakeOver.mock.calls[0]?.[1]).toEqual({
      model: EPIC,
      prompt: "Mira am Kai",
      aspect_ratio: "2:3",
      cost_usd: 0.003,
      seed: 42,
      loras: [{ id: CUFFS, name: "Handcuffs", weight: 0.6 }],
      appended: "raw photo, handcuffs",
    });
  });

  it("takes over no LoRAs when none went along", async () => {
    const without = { ...LIST, loras: [] };
    fakeApi({
      "GET /api/images/models": ok({
        ...without,
        runware: (LIST.runware ?? []).map((m) => ({ ...m, loras: [] })),
      }),
      "GET /api/images/price": ok({ cost_usd: null, unit: null }),
      "POST /api/images/generate": image(EPIC, 7, "raw photo"),
    });
    const user = userEvent.setup();
    const onTakeOver = vi.fn<
      (image: Blob, origin: ImageOrigin) => Promise<void>
    >(() => Promise.resolve());
    dialog({ initialModel: EPIC, onTakeOver });
    await user.click(
      await screen.findByRole("button", { name: "✨ Erzeugen" }),
    );
    await user.click(await screen.findByRole("button", { name: "Übernehmen" }));
    await waitFor(() => {
      expect(onTakeOver).toHaveBeenCalled();
    });
    expect(onTakeOver.mock.calls[0]?.[1]).not.toHaveProperty("loras");
  });
});

describe("full origin (step 11.4, ADR-121)", () => {
  const ORIGIN: StoredImageOrigin = {
    model: EPIC,
    prompt: "Mira am Kai",
    aspect_ratio: "2:3",
    cost_usd: 0.003,
    date: "2026-11-08T18:00:00+00:00",
    basis: null,
    seed: 1834072215,
    loras: [{ id: CUFFS, name: "Handcuffs", weight: 0.6 }],
    appended: "raw photo, handcuffs",
  };

  it("shows start value, LoRAs and the appended text", async () => {
    render(<ImageOriginPanel load={() => Promise.resolve(ORIGIN)} />);
    expect(await screen.findByText("1834072215")).toBeDefined();
    expect(screen.getByText("Handcuffs · Gewicht 0.6")).toBeDefined();
    expect(screen.getByText("raw photo, handcuffs")).toBeDefined();
  });

  it("starts anew with the start value fixed and the LoRAs ticked", () => {
    expect(seedOf(ORIGIN, "2:3")).toEqual({
      prompt: "Mira am Kai",
      format: "2:3",
      model: EPIC,
      levels: { resolution: null, quality: null },
      seed: 1834072215,
      loras: [{ id: CUFFS, weight: 0.6 }],
    });
  });
});
