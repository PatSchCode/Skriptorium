/**
 * Image recipes in "Bild erzeugen" (step 11.6, ADR-126): the figure goes in at `[Figur]`, and a
 * description becomes a scene again by putting `[Figur]` where the figure stands.
 */

/** The place of the figure in a scene; as `FIGURE` in `api/image_recipes.py`. */
export const FIGURE = "[Figur]";

/** The description of `scene` for a figure: `figure` at the place of `[Figur]`. */
export function fillRecipe(scene: string, figure: string): string {
  return scene.replace(FIGURE, figure.trim());
}

/**
 * The scene of a description: where `figure` stands, `[Figur]` instead (the first time). Without
 * it the description stays as it is; the author then puts `[Figur]` in by hand.
 */
export function sceneOf(prompt: string, figure: string): string {
  const wanted = figure.trim();
  if (wanted === "" || prompt.includes(FIGURE)) {
    return prompt;
  }
  const at = prompt.indexOf(wanted);
  return at < 0
    ? prompt
    : prompt.slice(0, at) + FIGURE + prompt.slice(at + wanted.length);
}

/** Whether `scene` holds `[Figur]` exactly once, as the server demands. */
export function hasOneFigure(scene: string): boolean {
  return scene.split(FIGURE).length === 2;
}
