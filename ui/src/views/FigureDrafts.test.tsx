import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import { fail, fakeApi, ok } from "../../fake-api";
import { DRAFT_ADDITION, FigureDrafts } from "./FigureDrafts";

afterEach(() => {
  vi.restoreAllMocks();
});

const MODELS = {
  default: "a/ohne",
  models: [
    { id: "a/ohne", name: "Ohne Startwert", references: 0 },
    { id: "b/mit", name: "Mit Startwert", references: 0, seed: true },
  ],
  available: true,
  ready: true,
  runware: [
    {
      id: "runware:krea",
      name: "Krea 2 Turbo",
      architecture: "krea",
      addition: "",
      loras: [],
    },
  ],
  runware_ready: true,
};

function image(seed: number, cost: number | null = 0.004) {
  return {
    content: "aGFsbG8=",
    media_type: "image/png",
    cost_usd: cost,
    model: "b/mit",
    seed,
    appended: seed === 2 ? ", krea look" : null,
  };
}

describe("drafts of the figure assistant (step 11.5, ADR-123)", () => {
  it("offers only models with a start value and makes four drafts", async () => {
    let seed = 0;
    const { calls } = fakeApi({
      "GET /api/images/models": ok(MODELS),
      "POST /api/images/generate": () => {
        seed += 1;
        return seed === 4
          ? { status: 502, body: { detail: "Anbieter weg" } }
          : { status: 200, body: image(seed, seed === 3 ? null : 0.004) };
      },
    });
    const onPick = vi.fn();
    const user = userEvent.setup();
    render(
      <FigureDrafts world="salzmark" description=" a man " onPick={onPick} />,
    );
    const select = await screen.findByRole("combobox", { name: "Bildmodell" });
    expect(
      [...(select as HTMLSelectElement).options].map((o) => o.value),
    ).toEqual(["b/mit", "runware:krea"]);
    expect(screen.getByRole("textbox")).toHaveProperty("value", DRAFT_ADDITION);
    // Owner 2026-11-09: clothes hid the proportions, the drafts show plain underwear.
    expect(DRAFT_ADDITION).toContain("plain black underwear");
    expect(DRAFT_ADDITION).not.toContain("leggings");
    await user.clear(screen.getByRole("textbox"));
    await user.type(screen.getByRole("textbox"), "studio");
    await user.click(
      screen.getByRole("button", { name: "🎲 4 Entwürfe erzeugen" }),
    );

    expect(await screen.findByText("Anbieter weg")).toBeDefined();
    const drafts = screen.getAllByRole("radio");
    expect(drafts).toHaveLength(3);
    expect(screen.getByText(/Zusammen 0,008 \$/)).toBeDefined();
    const posts = calls.filter((c) => c.method === "POST");
    expect(posts).toHaveLength(4);
    expect(posts[0]?.body).toEqual({
      model: "b/mit",
      prompt: "a man, studio",
      aspect_ratio: "2:3",
      world: "salzmark",
    });
    expect(onPick).toHaveBeenLastCalledWith(null);

    await user.click(screen.getByRole("radio", { name: /Entwurf 2/ }));
    expect(onPick).toHaveBeenLastCalledWith({
      image: image(2),
      origin: {
        model: "b/mit",
        prompt: "a man, studio",
        aspect_ratio: "2:3",
        cost_usd: 0.004,
        seed: 2,
        appended: ", krea look",
      },
    });
    expect(
      screen
        .getByRole("radio", { name: /Entwurf 2/ })
        .getAttribute("aria-checked"),
    ).toBe("true");

    await user.selectOptions(select, "runware:krea");
    await user.click(
      screen.getByRole("button", { name: "🎲 4 Entwürfe erzeugen" }),
    );
    await waitFor(() => {
      expect(calls.filter((c) => c.method === "POST")).toHaveLength(8);
    });
    expect(calls.at(-1)?.body).toMatchObject({ model: "runware:krea" });
  });

  it("says so without a model that takes a start value, and on a failed list", async () => {
    fakeApi({
      "GET /api/images/models": ok({
        ...MODELS,
        models: [MODELS.models[0]],
        runware: [],
      }),
    });
    const { unmount } = render(
      <FigureDrafts world="salzmark" description="a man" onPick={vi.fn()} />,
    );
    expect(
      await screen.findByText(/Kein Bildmodell mit Startwert/),
    ).toBeDefined();
    expect(
      screen.getByRole("button", { name: "🎲 4 Entwürfe erzeugen" }),
    ).toHaveProperty("disabled", true);
    unmount();

    fakeApi({ "GET /api/images/models": fail(500, "Liste weg") });
    render(
      <FigureDrafts world="salzmark" description="a man" onPick={vi.fn()} />,
    );
    expect(await screen.findByText("Liste weg")).toBeDefined();
  });
});
