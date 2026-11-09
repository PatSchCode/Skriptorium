import { useEffect, useState } from "react";
import { api, describeError, type ImageRecipe } from "../api";
import { ErrorText } from "./Common";
import { FORMATS } from "./imageGenerateText";

/**
 * "Bildrezepte" in the settings (step 11.6, ADR-126): rename a recipe, change its scene or remove
 * it; saved together. New recipes come from "Bild erzeugen" ("Als Rezept speichern"), where model,
 * format and LoRAs are chosen; they are not changed here. `models` names the models by their id.
 */
export function RecipeSettings({
  models,
}: {
  models: ReadonlyMap<string, string>;
}) {
  const [recipes, setRecipes] = useState<ImageRecipe[] | null>(null);
  const [open, setOpen] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [dirty, setDirty] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
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
          setError(describeError(reason));
        }
      });
    return () => {
      current = false;
    };
  }, []);

  function edit(id: string, change: Partial<ImageRecipe>) {
    setRecipes(
      (recipes ?? []).map((r) => (r.id === id ? { ...r, ...change } : r)),
    );
    setDirty(true);
  }

  async function save() {
    setBusy(true);
    setError(null);
    try {
      const saved = await api.setImageRecipes(
        (recipes ?? []).map(({ id, name, scene }) => ({ id, name, scene })),
      );
      setRecipes(saved.recipes);
      setDirty(false);
      setOpen(null);
    } catch (reason: unknown) {
      setError(describeError(reason));
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="card" aria-label="Bildrezepte">
      <h2>Bildrezepte</h2>
      <p className="note">
        Ein Rezept hält Modell, Zusätze mit Gewicht, Format und eine Szene mit
        der Stelle [Figur]. Es gilt für jede Figur in allen Welten. Neue Rezepte
        entstehen im Fenster „Bild erzeugen“ mit „Als Rezept speichern“.
      </p>
      {recipes !== null && recipes.length === 0 && (
        <p className="note">Noch keine Rezepte.</p>
      )}
      {(recipes ?? []).map((recipe) => (
        <div key={recipe.id} className="recipe-item">
          <div className="runware-row">
            <input
              aria-label={`Name des Rezepts ${recipe.name}`}
              value={recipe.name}
              maxLength={100}
              disabled={busy}
              onChange={(event) => {
                edit(recipe.id, { name: event.target.value });
              }}
            />
            <button
              type="button"
              className="ghost"
              aria-expanded={open === recipe.id}
              disabled={busy}
              onClick={() => {
                setOpen(open === recipe.id ? null : recipe.id);
              }}
            >
              Szene ändern
            </button>
            <span className="note">{summary(recipe, models)}</span>
            <button
              type="button"
              className="ghost"
              aria-label={`${recipe.name} entfernen`}
              disabled={busy}
              onClick={() => {
                setRecipes((recipes ?? []).filter((r) => r.id !== recipe.id));
                setDirty(true);
              }}
            >
              ✕
            </button>
          </div>
          {open === recipe.id && (
            <textarea
              aria-label={`Szene des Rezepts ${recipe.name}`}
              rows={4}
              maxLength={4000}
              value={recipe.scene}
              disabled={busy}
              onChange={(event) => {
                edit(recipe.id, { scene: event.target.value });
              }}
            />
          )}
        </div>
      ))}
      {dirty && (
        <div className="row">
          <button
            type="button"
            className="primary"
            disabled={busy}
            onClick={() => void save()}
          >
            Speichern
          </button>
        </div>
      )}
      <ErrorText message={error} />
    </section>
  );
}

/** "Krea 2 Turbo · 2 Zusätze · Hochformat" */
export function summary(
  recipe: ImageRecipe,
  models: ReadonlyMap<string, string>,
): string {
  const count = recipe.loras.length;
  return [
    models.get(recipe.model) ?? recipe.model,
    count === 0
      ? "ohne Zusätze"
      : `${String(count)} ${count === 1 ? "Zusatz" : "Zusätze"}`,
    FORMATS.find((f) => f.id === recipe.aspect_ratio)?.label ??
      recipe.aspect_ratio,
  ].join(" · ");
}
