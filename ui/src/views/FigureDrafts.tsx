import { useCallback, useState } from "react";
import {
  api,
  describeError,
  formatCost,
  type GeneratedImage,
  type ImageOrigin,
} from "../api";
import { ErrorText } from "./Common";
import { ModelOptions } from "./ImageChoices";
import { useImageModels } from "./useImageModels";

/** How many drafts one click makes (V.58: 3–4; mockup 11.5). */
export const DRAFTS = 4;

/**
 * What the drafts add to the image description, changeable before generating (owner, ADR-123:
 * "Zusatz frei"): the whole figure from head to feet in skimpy underwear before a neutral
 * background, so build, proportions and face can be compared (owner after the trials of
 * 2026-11-09: clothes, then plain underwear and a cropped frame hid the proportions; ADR-123,
 * addendum). The framing words keep Krea 2 Turbo from cutting at the thighs (probe 2026-11-09).
 */
export const DRAFT_ADDITION =
  "wide full-length photo, the entire body from head to bare feet visible in frame, space above the head and below the feet, standing straight, facing the camera, arms held slightly away from the body, wearing only a skimpy black string thong and a minimal black triangle bra, barefoot, plain light grey studio background, soft even light, camera at hip height";

/** A draft the author picked, with what is kept as its origin (step 9.6, ADR-095; 11.4). */
export interface ChosenDraft {
  image: GeneratedImage;
  origin: ImageOrigin;
}

/**
 * Drafts of the figure assistant (step 11.5, ADR-123): `DRAFTS` images of `description` plus the
 * addition, each with its own start value drawn by the server (ADR-121), only from models that
 * take one. A tap picks one; `onPick` gets it (or `null`). Nothing is stored here.
 */
export function FigureDrafts({
  world,
  description,
  onPick,
}: {
  world: string;
  description: string;
  onPick: (draft: ChosenDraft | null) => void;
}) {
  const [error, setError] = useState<string | null>(null);
  const reportError = useCallback((message: string) => {
    setError(message);
  }, []);
  const { models, model, setModel, ready } = useImageModels(
    null,
    false,
    reportError,
  );
  const [addition, setAddition] = useState(DRAFT_ADDITION);
  const [drafts, setDrafts] = useState<GeneratedImage[]>([]);
  const [picked, setPicked] = useState<number | null>(null);
  const [busy, setBusy] = useState(false);
  const seeded = (models ?? []).filter((m) => m.seed === true);
  const chosenModel = seeded.some((m) => m.id === model)
    ? model
    : (seeded[0]?.id ?? "");
  const prompt = [description.trim(), addition.trim()]
    .filter((part) => part !== "")
    .join(", ");

  async function generate() {
    setBusy(true);
    setError(null);
    setPicked(null);
    onPick(null);
    setDrafts([]);
    // Each draft on its own: a failed one does not throw away the others (they are paid for).
    const results = await Promise.allSettled(
      Array.from({ length: DRAFTS }, () =>
        api.generateImage({
          model: chosenModel,
          prompt,
          aspect_ratio: "2:3",
          world,
        }),
      ),
    );
    setDrafts(
      results.flatMap((result) =>
        result.status === "fulfilled" ? [result.value] : [],
      ),
    );
    const failed = results.find((result) => result.status === "rejected");
    if (failed !== undefined) {
      setError(describeError(failed.reason));
    }
    setBusy(false);
  }

  function pick(at: number) {
    const image = drafts[at];
    if (image === undefined) {
      return;
    }
    setPicked(at);
    onPick({
      image,
      origin: {
        model: image.model,
        prompt,
        aspect_ratio: "2:3",
        cost_usd: image.cost_usd,
        ...(image.seed == null ? {} : { seed: image.seed }),
        ...(image.appended == null ? {} : { appended: image.appended }),
      },
    });
  }

  const cost = drafts.reduce((sum, image) => sum + (image.cost_usd ?? 0), 0);
  return (
    <div className="figure-drafts">
      <label>
        Zusatz für die Entwürfe (Kleidung, Hintergrund, Licht)
        <textarea
          rows={2}
          value={addition}
          disabled={busy}
          onChange={(event) => {
            setAddition(event.target.value);
          }}
        />
      </label>
      <div className="row">
        {seeded.length > 0 && (
          <label>
            Bildmodell{" "}
            <select
              value={chosenModel}
              disabled={busy}
              onChange={(event) => {
                setModel(event.target.value);
              }}
            >
              <ModelOptions models={seeded} />
            </select>
          </label>
        )}
        <button
          type="button"
          className="ghost"
          disabled={busy || chosenModel === "" || !ready || prompt === ""}
          onClick={() => void generate()}
        >
          🎲 {DRAFTS} Entwürfe erzeugen
        </button>
      </div>
      {models !== null && seeded.length === 0 && (
        <p className="note">Kein Bildmodell mit Startwert eingerichtet.</p>
      )}
      {busy && <p className="note">Die Entwürfe entstehen …</p>}
      {drafts.length > 0 && (
        <>
          <div
            className="figure-drafts-grid"
            role="radiogroup"
            aria-label="Entwürfe"
          >
            {drafts.map((image, at) => (
              <button
                key={`${String(image.seed)}-${String(at)}`}
                type="button"
                role="radio"
                aria-checked={picked === at}
                className={picked === at ? "chosen" : undefined}
                onClick={() => {
                  pick(at);
                }}
              >
                <img
                  src={`data:${image.media_type};base64,${image.content}`}
                  alt={`Entwurf ${String(at + 1)}`}
                />
                <span>
                  {image.seed == null ? "" : `Startwert ${String(image.seed)}`}
                </span>
              </button>
            ))}
          </div>
          <p className="note">
            {cost > 0 ? `Zusammen ${formatCost(cost)}. ` : ""}
            Der gewählte Entwurf wird Hauptbild der Figur.
          </p>
        </>
      )}
      <ErrorText message={error} />
    </div>
  );
}
