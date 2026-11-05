import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import { fakeApi, ok } from "../../fake-api";
import { describePrice, ImageGenerate } from "./ImageGenerate";
import { ImageOriginPanel } from "./ImageOriginPanel";

const MODELS = ok({
  default: "seed/seedream",
  models: [
    {
      id: "seed/seedream",
      name: "Seedream",
      references: 0,
      resolutions: ["1K", "2K"],
      qualities: [],
    },
    {
      id: "x-ai/grok",
      name: "Grok",
      references: 0,
      resolutions: ["1K", "2K"],
      qualities: ["low", "medium", "fein"],
    },
    {
      id: "g/gemini",
      name: "Gemini",
      references: 0,
      resolutions: ["1K", "4K"],
      qualities: ["auto", "high"],
    },
    { id: "bfl/flux", name: "FLUX", references: 0 },
  ],
  available: true,
  ready: true,
});
const IMAGE = ok({
  content: "iVBORw0KGgo=",
  media_type: "image/png",
  cost_usd: 0.09,
  model: "seed/seedream",
});

/** Prices by query, as the server names them per level. */
function price(_body: unknown, path: string) {
  const query = new URLSearchParams(path.split("?")[1]);
  const key = `${query.get("model") ?? ""}|${query.get("resolution") ?? ""}|${query.get("quality") ?? ""}`;
  const known: Record<
    string,
    { cost_usd: number | null; unit: string | null }
  > = {
    "seed/seedream|1K|": { cost_usd: 0.045, unit: "image" },
    "seed/seedream|2K|": { cost_usd: 0.09, unit: "image" },
    "x-ai/grok|1K|low": { cost_usd: 0.04, unit: "image" },
    "x-ai/grok|2K|low": { cost_usd: 0.06, unit: "image" },
    "x-ai/grok|2K|medium": { cost_usd: 0.08, unit: "image" },
    "bfl/flux||": { cost_usd: 0.03, unit: "megapixel" },
  };
  return { status: 200, body: known[key] ?? { cost_usd: null, unit: null } };
}

function open(
  taken = vi.fn(() => Promise.resolve()),
  initialLevels?: { resolution: string | null; quality: string | null },
) {
  render(
    <ImageGenerate
      target={{ world: "die-salzmark" }}
      title="Bild erzeugen – Turm"
      initialPrompt="Ein Turm"
      initialFormat="3:2"
      initialLevels={initialLevels}
      onTakeOver={taken}
      onClose={vi.fn()}
    />,
  );
  return taken;
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe("resolution and quality (step 10.5, ADR-109)", () => {
  it("presets 2K with its price, sends and keeps the levels", async () => {
    const { calls } = fakeApi({
      "GET /api/images/models": MODELS,
      "GET /api/images/price": price,
      "POST /api/images/generate": IMAGE,
    });
    const user = userEvent.setup();
    const taken = open();
    expect(await screen.findByText("ca. 0,09 $ je Bild (2K)")).toBeDefined();
    expect(screen.getByRole("radio", { name: "2K 0,09 $" })).toHaveProperty(
      "ariaChecked",
      "true",
    );
    expect(screen.getByRole("radio", { name: "1K 0,045 $" })).toBeDefined();
    expect(screen.queryByRole("radiogroup", { name: "Qualität" })).toBeNull();

    await user.click(screen.getByRole("button", { name: "✨ Erzeugen" }));
    await user.click(await screen.findByRole("button", { name: "Übernehmen" }));
    expect(calls.find((c) => c.method === "POST")?.body).toEqual({
      model: "seed/seedream",
      prompt: "Ein Turm",
      aspect_ratio: "3:2",
      resolution: "2K",
      world: "die-salzmark",
    });
    await waitFor(() => {
      expect(taken).toHaveBeenCalledWith(expect.any(Blob), {
        model: "seed/seedream",
        prompt: "Ein Turm",
        aspect_ratio: "3:2",
        cost_usd: 0.09,
        resolution: "2K",
      });
    });
  });

  it("offers quality with names, follows each model and shows unknown prices honestly", async () => {
    const { calls } = fakeApi({
      "GET /api/images/models": MODELS,
      "GET /api/images/price": price,
      "POST /api/images/generate": IMAGE,
    });
    const user = userEvent.setup();
    open();
    await screen.findByText("ca. 0,09 $ je Bild (2K)");

    await user.selectOptions(screen.getByLabelText("Modell"), "x-ai/grok");
    expect(await screen.findByText("ca. 0,06 $ je Bild (2K)")).toBeDefined();
    const quality = screen.getByRole("radiogroup", { name: "Qualität" });
    expect(quality.textContent).toBe("niedrigmittelfein");
    await user.click(screen.getByRole("radio", { name: "mittel" }));
    expect(await screen.findByText("ca. 0,08 $ je Bild (2K)")).toBeDefined();
    await user.click(screen.getByRole("radio", { name: "1K" }));
    expect(
      await screen.findByText(
        "Preis für 1K nicht ausgewiesen – die Kosten stehen nach dem Erzeugen da",
      ),
    ).toBeDefined();

    await user.selectOptions(screen.getByLabelText("Modell"), "g/gemini");
    expect(screen.getByRole("radio", { name: "1K" })).toHaveProperty(
      "ariaChecked",
      "true",
    );
    expect(screen.getByRole("radio", { name: "automatisch" })).toHaveProperty(
      "ariaChecked",
      "true",
    );
    await user.click(screen.getByRole("radio", { name: "hoch" }));

    await user.selectOptions(screen.getByLabelText("Modell"), "bfl/flux");
    expect(
      await screen.findByText("ca. 0,03 $ je Bild (1 Megapixel)"),
    ).toBeDefined();
    expect(screen.queryByRole("radiogroup", { name: "Auflösung" })).toBeNull();
    await user.click(screen.getByRole("button", { name: "✨ Erzeugen" }));
    const sent = calls.find((c) => c.method === "POST")?.body;
    expect(sent).not.toHaveProperty("resolution");
    expect(sent).not.toHaveProperty("quality");
  });

  it("starts from the levels of an origin where the model offers them", async () => {
    fakeApi({
      "GET /api/images/models": MODELS,
      "GET /api/images/price": price,
    });
    open(undefined, { resolution: "1K", quality: "teuer" });
    expect(await screen.findByText("ca. 0,045 $ je Bild (1K)")).toBeDefined();
  });

  it("counts a failed price request as unknown", async () => {
    fakeApi({
      "GET /api/images/models": MODELS,
      "GET /api/images/price": () => ({ status: 500, body: { detail: "weg" } }),
    });
    open();
    expect(
      await screen.findByText(
        "Preis für 2K nicht ausgewiesen – die Kosten stehen nach dem Erzeugen da",
      ),
    ).toBeDefined();
    expect(screen.getByRole("radio", { name: "2K" })).toBeDefined();
  });

  it("names the price of a level", () => {
    expect(describePrice({ cost_usd: 0.09, unit: "image" }, "2K")).toBe(
      "ca. 0,09 $ je Bild (2K)",
    );
    expect(describePrice({ cost_usd: null, unit: null })).toBe(
      "Preis unbekannt",
    );
  });

  it("shows the levels in the origin of an image", async () => {
    render(
      <ImageOriginPanel
        load={() =>
          Promise.resolve({
            model: "x-ai/grok",
            prompt: "Ein Turm",
            aspect_ratio: "3:2",
            cost_usd: 0.08,
            date: "2026-11-05T10:00:00+00:00",
            basis: null,
            resolution: "2K",
            quality: "medium",
          })
        }
      />,
    );
    expect(await screen.findByText("2K · Qualität medium")).toBeDefined();
  });
});
