import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import { fail, fakeApi, ok } from "../../fake-api";
import type { ImageModelList, ImageOrigin, ImageRecipe } from "../api";
import { ImageGenerate } from "./ImageGenerate";
import { RecipeSettings, summary } from "./RecipeSettings";

const KREA = "krea:krea@2-turbo";
const ROPE = "skriptorium:2742699@3142259";
const GONE = "skriptorium:1@1";
const ILKA = "a 27-year-old adult woman, grey eyes";
const SCENE = "[Figur], kneeling in a dim cellar";

const LIST: ImageModelList = {
  default: "bytedance-seed/seedream-4.5",
  models: [
    {
      id: "bytedance-seed/seedream-4.5",
      name: "Seedream 4.5",
      references: 0,
      resolutions: ["1K", "2K"],
      qualities: ["auto", "high"],
    },
  ],
  available: true,
  ready: true,
  runware: [
    {
      id: KREA,
      name: "Krea 2 Turbo",
      architecture: "krea_oss_2_turbo",
      addition: "",
      loras: [ROPE],
    },
  ],
  loras: [
    {
      id: ROPE,
      name: "Rope Bondage",
      architecture: "krea_oss_2",
      trigger: "",
      weight: 0.6,
    },
  ],
  runware_ready: true,
};

const CELLAR: ImageRecipe = {
  id: "0a1b2c3d",
  name: "Kerker, Seil",
  model: KREA,
  aspect_ratio: "3:2",
  resolution: null,
  quality: null,
  loras: [
    { id: ROPE, weight: 0.8 },
    { id: GONE, weight: 1 },
  ],
  scene: SCENE,
};
const STUDIO: ImageRecipe = {
  id: "11111111",
  name: "Studio",
  model: "bytedance-seed/seedream-4.5",
  aspect_ratio: "2:3",
  resolution: "1K",
  quality: "high",
  loras: [],
  scene: "[Figur], plain studio",
};
const LOST: ImageRecipe = {
  ...STUDIO,
  id: "22222222",
  name: "Alt",
  model: "a/gone",
};

const IMAGE = ok({
  content: "iVBORw0KGgo=",
  media_type: "image/png",
  cost_usd: 0.003,
  model: KREA,
  seed: 7,
});

afterEach(() => {
  vi.restoreAllMocks();
});

function dialog(
  onTakeOver: (image: Blob, origin: ImageOrigin) => Promise<void> = () =>
    Promise.resolve(),
  figure: { name: string; text: string } | null = {
    name: "Ilka Varn",
    text: ILKA,
  },
) {
  return render(
    <ImageGenerate
      target={{ world: "salzmark" }}
      title="Bild erzeugen – Ilka Varn"
      initialPrompt={ILKA}
      initialFormat="2:3"
      figure={figure}
      onTakeOver={onTakeOver}
      onClose={() => undefined}
    />,
  );
}

describe("recipes in Bild erzeugen (step 11.6, ADR-126)", () => {
  it("fills the window from a recipe and names it in the origin", async () => {
    const { calls } = fakeApi({
      "GET /api/images/models": ok(LIST),
      "GET /api/images/recipes": ok({ recipes: [CELLAR, STUDIO, LOST] }),
      "GET /api/images/price": ok({ cost_usd: null, unit: null }),
      "POST /api/images/generate": IMAGE,
    });
    const onTakeOver = vi.fn(() => Promise.resolve());
    const user = userEvent.setup();
    dialog(onTakeOver);
    const recipe = await screen.findByRole("combobox", { name: "Rezept" });
    await screen.findByRole("option", { name: "Seedream 4.5" });
    await user.selectOptions(recipe, "0a1b2c3d");

    expect(
      screen.getByRole("textbox", { name: "Bildbeschreibung (änderbar)" }),
    ).toHaveProperty("value", `${ILKA}, kneeling in a dim cellar`);
    expect(screen.getByRole("combobox", { name: "Modell" })).toHaveProperty(
      "value",
      KREA,
    );
    expect(
      screen.getByRole("checkbox", { name: "Rope Bondage" }),
    ).toHaveProperty("checked", true);
    expect(screen.getByLabelText("Gewicht Rope Bondage")).toHaveProperty(
      "value",
      "0.8",
    );
    expect(screen.getByText(/weggelassen: skriptorium:1@1/)).toBeDefined();
    expect(
      screen.getByText(/Bildbeschreibung von Ilka Varn steht an der Stelle/),
    ).toBeDefined();

    await user.click(screen.getByRole("button", { name: "✨ Erzeugen" }));
    await user.click(await screen.findByRole("button", { name: "Übernehmen" }));
    const order = calls.find((c) => c.method === "POST")?.body;
    expect(order).toMatchObject({
      model: KREA,
      aspect_ratio: "3:2",
      loras: [{ id: ROPE, weight: 0.8 }],
    });
    expect(onTakeOver).toHaveBeenCalledWith(
      expect.any(Blob),
      expect.objectContaining({ recipe: "Kerker, Seil", aspect_ratio: "3:2" }),
    );
  });

  it("takes the levels of a recipe and says when its model is gone", async () => {
    fakeApi({
      "GET /api/images/models": ok(LIST),
      "GET /api/images/recipes": ok({ recipes: [CELLAR, STUDIO, LOST] }),
      "GET /api/images/price": ok({ cost_usd: 0.04, unit: "image" }),
    });
    const user = userEvent.setup();
    dialog();
    const recipe = await screen.findByRole("combobox", { name: "Rezept" });
    await screen.findByRole("option", { name: "Seedream 4.5" });
    await user.selectOptions(recipe, "11111111");
    expect(screen.getByRole("combobox", { name: "Modell" })).toHaveProperty(
      "value",
      "bytedance-seed/seedream-4.5",
    );
    await user.selectOptions(recipe, "22222222");
    expect(screen.getByText(/nicht mehr verfügbar: a\/gone/)).toBeDefined();
    await user.selectOptions(recipe, "");
    expect(screen.queryByText(/nicht mehr verfügbar/)).toBeNull();
  });

  it("saves what the window holds as a recipe, with [Figur] for the figure", async () => {
    const { calls } = fakeApi({
      "GET /api/images/models": ok(LIST),
      "GET /api/images/recipes": ok({ recipes: [CELLAR] }),
      "GET /api/images/price": ok({ cost_usd: null, unit: null }),
      "POST /api/images/recipes": (body) =>
        ok({ ...(body as object), id: "33333333" })(),
    });
    const user = userEvent.setup();
    dialog();
    const recipe = await screen.findByRole("combobox", { name: "Rezept" });
    await screen.findByRole("option", { name: "Seedream 4.5" });
    await user.selectOptions(recipe, "0a1b2c3d");
    await user.click(
      screen.getByRole("button", { name: "Als Rezept speichern …" }),
    );
    expect(
      screen.queryByRole("button", { name: "Als Rezept speichern …" }),
    ).toBeNull();
    expect(screen.getByRole("textbox", { name: "Name" })).toHaveProperty(
      "value",
      "Kerker, Seil",
    );
    const scene = screen.getByRole("textbox", {
      name: "Szene (die Figur steht bei [Figur])",
    });
    expect(scene).toHaveProperty("value", SCENE);
    expect(screen.getByText(/Ersetzt das Rezept „Kerker, Seil“/)).toBeDefined();
    expect(
      screen.getByText(/Krea 2 Turbo, Quer, Rope Bondage 0,8/),
    ).toBeDefined();
    expect(screen.getByText(/durch \[Figur\] ersetzt/)).toBeDefined();

    await user.clear(scene);
    await user.type(scene, "a cellar");
    expect(screen.getByText(/genau einmal/)).toBeDefined();
    expect(
      screen.getByRole("button", { name: "Rezept speichern" }),
    ).toHaveProperty("disabled", true);
    await user.type(scene, ", [[Figur]");
    const name = screen.getByRole("textbox", { name: "Name" });
    await user.clear(name);
    await user.type(name, "Keller");
    expect(screen.queryByText(/Ersetzt das Rezept/)).toBeNull();
    await user.click(screen.getByRole("button", { name: "Rezept speichern" }));

    expect(
      await screen.findByText("Rezept „Keller“ gespeichert."),
    ).toBeDefined();
    expect(calls.find((c) => c.method === "POST")?.body).toEqual({
      name: "Keller",
      model: KREA,
      aspect_ratio: "3:2",
      loras: [{ id: ROPE, weight: 0.8 }],
      scene: "a cellar, [Figur]",
    });
    await waitFor(() => {
      expect(
        calls.filter((c) => c.path === "/api/images/recipes"),
      ).toHaveLength(3);
    });
  });

  it("shows a refused save and closes the form on Abbrechen", async () => {
    fakeApi({
      "GET /api/images/models": ok(LIST),
      "GET /api/images/recipes": ok({ recipes: [] }),
      "GET /api/images/price": ok({ cost_usd: null, unit: null }),
      "POST /api/images/recipes": fail(422, "Höchstens 50 Bildrezepte"),
    });
    const user = userEvent.setup();
    dialog();
    await user.click(
      await screen.findByRole("button", { name: "Als Rezept speichern …" }),
    );
    expect(screen.queryByRole("combobox", { name: "Rezept" })).toBeNull();
    await user.type(screen.getByRole("textbox", { name: "Name" }), "Neu");
    await user.click(screen.getByRole("button", { name: "Rezept speichern" }));
    expect(await screen.findByText("Höchstens 50 Bildrezepte")).toBeDefined();
    const buttons = screen.getAllByRole("button", { name: "Abbrechen" });
    await user.click(buttons[buttons.length - 1] as HTMLElement);
    expect(screen.queryByRole("textbox", { name: "Name" })).toBeNull();
  });

  it("offers no recipes without a figure and reports a failed list", async () => {
    const { calls } = fakeApi({
      "GET /api/images/models": ok(LIST),
      "GET /api/images/price": ok({ cost_usd: null, unit: null }),
    });
    const { unmount } = dialog(undefined, null);
    await screen.findByRole("combobox", { name: "Modell" });
    expect(
      screen.queryByRole("button", { name: "Als Rezept speichern …" }),
    ).toBeNull();
    expect(calls.some((c) => c.path === "/api/images/recipes")).toBe(false);
    unmount();

    fakeApi({
      "GET /api/images/models": ok(LIST),
      "GET /api/images/recipes": fail(500, "Rezepte weg"),
      "GET /api/images/price": ok({ cost_usd: null, unit: null }),
    });
    dialog();
    expect(await screen.findByText("Rezepte weg")).toBeDefined();
  });
});

describe("Bildrezepte in the settings (step 11.6, ADR-126)", () => {
  const MODELS = new Map([[KREA, "Krea 2 Turbo"]]);

  it("renames, changes a scene, removes and saves", async () => {
    const { calls } = fakeApi({
      "GET /api/images/recipes": ok({ recipes: [CELLAR, STUDIO] }),
      "PUT /api/images/recipes": (body) =>
        ok({
          recipes: (body as { recipes: ImageRecipe[] }).recipes.map((r) => ({
            ...CELLAR,
            ...r,
          })),
        })(),
    });
    const user = userEvent.setup();
    render(<RecipeSettings models={MODELS} />);
    expect(
      await screen.findByText("Krea 2 Turbo · 2 Zusätze · Quer"),
    ).toBeDefined();
    expect(
      screen.getByText(
        "bytedance-seed/seedream-4.5 · ohne Zusätze · Hochformat",
      ),
    ).toBeDefined();
    expect(screen.queryByRole("button", { name: "Speichern" })).toBeNull();

    const name = screen.getByRole("textbox", {
      name: "Name des Rezepts Kerker, Seil",
    });
    await user.clear(name);
    await user.type(name, "Keller");
    const opens = screen.getAllByRole("button", { name: "Szene ändern" });
    await user.click(opens[0] as HTMLElement);
    const scene = screen.getByRole("textbox", {
      name: "Szene des Rezepts Keller",
    });
    await user.type(scene, ", torch");
    await user.click(screen.getByRole("button", { name: "Studio entfernen" }));
    await user.click(screen.getByRole("button", { name: "Speichern" }));

    await waitFor(() => {
      expect(screen.queryByRole("button", { name: "Speichern" })).toBeNull();
    });
    expect(calls.find((c) => c.method === "PUT")?.body).toEqual({
      recipes: [{ id: CELLAR.id, name: "Keller", scene: `${SCENE}, torch` }],
    });
    expect(
      screen.queryByRole("textbox", { name: /Szene des Rezepts/ }),
    ).toBeNull();
  });

  it("says when there are none, toggles a scene and reports errors", async () => {
    fakeApi({ "GET /api/images/recipes": ok({ recipes: [] }) });
    const { unmount } = render(<RecipeSettings models={MODELS} />);
    expect(await screen.findByText("Noch keine Rezepte.")).toBeDefined();
    unmount();

    fakeApi({ "GET /api/images/recipes": fail(500, "Liste kaputt") });
    const second = render(<RecipeSettings models={MODELS} />);
    expect(await screen.findByText("Liste kaputt")).toBeDefined();
    second.unmount();

    fakeApi({
      "GET /api/images/recipes": ok({ recipes: [CELLAR] }),
      "PUT /api/images/recipes": fail(
        422,
        "Zwei Rezepte haben denselben Namen",
      ),
    });
    const user = userEvent.setup();
    render(<RecipeSettings models={MODELS} />);
    const open = await screen.findByRole("button", { name: "Szene ändern" });
    await user.click(open);
    expect(open.getAttribute("aria-expanded")).toBe("true");
    await user.click(open);
    expect(
      screen.queryByRole("textbox", { name: /Szene des Rezepts/ }),
    ).toBeNull();
    await user.type(
      screen.getByRole("textbox", { name: /Name des Rezepts/ }),
      "!",
    );
    await user.click(screen.getByRole("button", { name: "Speichern" }));
    expect(
      await screen.findByText("Zwei Rezepte haben denselben Namen"),
    ).toBeDefined();
  });

  it("names one addition in the singular", () => {
    expect(
      summary({ ...CELLAR, loras: [{ id: ROPE, weight: 1 }] }, new Map()),
    ).toBe(`${KREA} · 1 Zusatz · Quer`);
  });
});
