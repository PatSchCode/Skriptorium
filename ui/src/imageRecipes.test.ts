import { describe, expect, it } from "vitest";
import { FIGURE, fillRecipe, hasOneFigure, sceneOf } from "./imageRecipes";

const ILKA = "a 27-year-old adult woman, grey eyes";

describe("image recipes (step 11.6, ADR-126)", () => {
  it("puts the figure in at [Figur]", () => {
    expect(fillRecipe("[Figur], in a cellar", ` ${ILKA} `)).toBe(
      `${ILKA}, in a cellar`,
    );
    expect(fillRecipe("a cellar", ILKA)).toBe("a cellar");
  });

  it("turns a description back into a scene", () => {
    expect(sceneOf(`${ILKA}, in a cellar`, ILKA)).toBe(
      `${FIGURE}, in a cellar`,
    );
    expect(sceneOf(`kneeling, ${ILKA}, ${ILKA}`, ILKA)).toBe(
      `kneeling, ${FIGURE}, ${ILKA}`,
    );
    expect(sceneOf("someone else", ILKA)).toBe("someone else");
    expect(sceneOf("[Figur] stays", ILKA)).toBe("[Figur] stays");
    expect(sceneOf("anything", "  ")).toBe("anything");
  });

  it("wants [Figur] exactly once", () => {
    expect(hasOneFigure("[Figur], cellar")).toBe(true);
    expect(hasOneFigure("cellar")).toBe(false);
    expect(hasOneFigure("[Figur] and [Figur]")).toBe(false);
  });
});
