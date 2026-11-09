import { useCallback, useEffect, useState } from "react";
import { api, describeError, type ImageRecipe, type RecipeOrder } from "../api";
import { hasOneFigure, sceneOf } from "../imageRecipes";
import { ErrorText } from "./Common";

/**
 * The saved image recipes for "Bild erzeugen" (step 11.6, ADR-126), loaded once when `enabled`;
 * a failed list ends up in `onError`. `reload` loads them anew after saving.
 */
export function useRecipes(
  enabled: boolean,
  onError: (message: string) => void,
) {
  const [recipes, setRecipes] = useState<ImageRecipe[]>([]);
  const [loads, setLoads] = useState(0);
  const reload = useCallback(() => {
    setLoads((count) => count + 1);
  }, []);
  useEffect(() => {
    if (!enabled) {
      return;
    }
    let current = true;
    api
      .imageRecipes()
      .then((list) => {
        if (current) {
          setRecipes(list.recipes);
        }
      })
      .catch((reason: unknown) => {
        if (current) {
          onError(describeError(reason));
        }
      });
    return () => {
      current = false;
    };
  }, [enabled, loads, onError]);
  return { recipes, reload };
}

/** The recipe to apply; "Kein Rezept" leaves the window as it is. */
export function RecipeField({
  recipes,
  chosen,
  figureName,
  busy,
  onPick,
}: {
  recipes: readonly ImageRecipe[];
  chosen: string | null;
  figureName: string;
  busy: boolean;
  onPick: (recipe: ImageRecipe | null) => void;
}) {
  if (recipes.length === 0) {
    return null;
  }
  return (
    <>
      <label className="image-generate-field">
        Rezept
        <select
          value={chosen ?? ""}
          disabled={busy}
          onChange={(event) => {
            onPick(recipes.find((r) => r.id === event.target.value) ?? null);
          }}
        >
          <option value="">Kein Rezept</option>
          {recipes.map((recipe) => (
            <option key={recipe.id} value={recipe.id}>
              {recipe.name}
            </option>
          ))}
        </select>
      </label>
      <p className="note">
        Übernimmt Modell, Zusätze, Format und Szene. Die Bildbeschreibung von{" "}
        {figureName} steht an der Stelle von [Figur]. Alles bleibt änderbar.
      </p>
    </>
  );
}

/**
 * "Als Rezept speichern" (ADR-126): what the window holds now, with the figure's text replaced by
 * `[Figur]` in the scene; a recipe of the same name is replaced. `order` gives model, format,
 * levels and LoRAs; `described` names them for the note.
 */
export function SaveRecipe({
  prompt,
  figure,
  figureName,
  initialName,
  recipes,
  order,
  described,
  onSaved,
  onClose,
}: {
  prompt: string;
  figure: string;
  figureName: string;
  initialName: string;
  recipes: readonly ImageRecipe[];
  order: Omit<RecipeOrder, "name" | "scene">;
  described: string;
  onSaved: (recipe: ImageRecipe) => void;
  onClose: () => void;
}) {
  const [name, setName] = useState(initialName);
  const [scene, setScene] = useState(() => sceneOf(prompt, figure));
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const replaced = recipes.find(
    (r) => key(r.name) === key(name) && key(name) !== "",
  );
  const valid = name.trim() !== "" && hasOneFigure(scene);

  async function save() {
    setBusy(true);
    setError(null);
    try {
      onSaved(await api.saveImageRecipe({ ...order, name, scene }));
    } catch (reason: unknown) {
      setError(describeError(reason));
      setBusy(false);
    }
  }

  return (
    <fieldset className="recipe-save">
      <legend>Als Rezept speichern</legend>
      <label className="image-generate-field">
        Name
        <input
          value={name}
          maxLength={100}
          disabled={busy}
          onChange={(event) => {
            setName(event.target.value);
          }}
        />
      </label>
      <label className="image-generate-field">
        Szene (die Figur steht bei [Figur])
        <textarea
          rows={4}
          maxLength={4000}
          value={scene}
          disabled={busy}
          onChange={(event) => {
            setScene(event.target.value);
          }}
        />
      </label>
      <p className="note">
        Gespeichert werden: {described}.{" "}
        {scene.includes("[Figur]") && sceneOf(prompt, figure) === scene
          ? `Die Bildbeschreibung von ${figureName} ist durch [Figur] ersetzt. `
          : ""}
        Das Rezept gilt in allen Welten.
      </p>
      {!hasOneFigure(scene) && (
        <p className="note">
          Setze [Figur] genau einmal dort ein, wo die Figur stehen soll.
        </p>
      )}
      {replaced !== undefined && (
        <p className="note">Ersetzt das Rezept „{replaced.name}“.</p>
      )}
      <ErrorText message={error} />
      <div className="row">
        <button
          type="button"
          className="primary"
          disabled={busy || !valid}
          onClick={() => void save()}
        >
          Rezept speichern
        </button>
        <button
          type="button"
          className="ghost"
          disabled={busy}
          onClick={onClose}
        >
          Abbrechen
        </button>
      </div>
    </fieldset>
  );
}

function key(name: string): string {
  return name.trim().split(/\s+/).join(" ").toLowerCase();
}
