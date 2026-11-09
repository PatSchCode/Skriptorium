import { useEffect, useRef, useState } from "react";
import {
  describeError,
  formatCost,
  type AspectRatio,
  type ImageLevels,
  type ImageReference,
  type LoraChoice,
  type StoredImageOrigin,
} from "../api";

/**
 * A stored image as the basis of a new one (step 9.8, ADR-097): where it is stored, how the
 * origin names it, and its address for the thumbnail.
 */
export interface Basis {
  reference: ImageReference;
  label: string;
  src: string;
}

/**
 * What "Bild erzeugen" starts with when an image is generated anew from its origin, or from an
 * image as its basis (step 9.8).
 */
export interface GenerateSeed {
  prompt: string;
  format: AspectRatio;
  model: string | null;
  basis?: Basis;
  /** Resolution and quality of the origin (step 10.5, ADR-109). */
  levels?: ImageLevels;
  /** Start value (fixed) and LoRAs of the origin (step 11.4, ADR-121). */
  seed?: number | null;
  loras?: LoraChoice[];
}

const FORMATS: readonly string[] = ["2:3", "1:1", "3:2"];

/** The seed for generating anew; a format the dialog does not offer falls back to `format`. */
export function seedOf(
  origin: StoredImageOrigin,
  format: AspectRatio,
): GenerateSeed {
  return {
    prompt: origin.prompt,
    format: FORMATS.includes(origin.aspect_ratio)
      ? (origin.aspect_ratio as AspectRatio)
      : format,
    model: origin.model,
    levels: {
      resolution: origin.resolution ?? null,
      quality: origin.quality ?? null,
    },
    // Only what the origin has (step 11.4, ADR-121).
    ...(origin.seed == null ? {} : { seed: origin.seed }),
    ...((origin.loras ?? []).length === 0
      ? {}
      : {
          loras: (origin.loras ?? []).map(({ id, weight }) => ({ id, weight })),
        }),
  };
}

/**
 * "Herkunft" of a generated image (step 9.6, ADR-095): model, date, cost and description, folded
 * away; with `onRegenerate` a button opens "Bild erzeugen" with them. An uploaded image has no
 * origin and shows nothing. Remount with a `key` per image: the origin is loaded once.
 */
export function ImageOriginPanel({
  load,
  onRegenerate,
}: {
  load: () => Promise<StoredImageOrigin | null>;
  onRegenerate?: (origin: StoredImageOrigin) => void;
}) {
  const loader = useRef(load);
  const [origin, setOrigin] = useState<StoredImageOrigin | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let current = true;
    loader
      .current()
      .then((found) => {
        if (current) {
          setOrigin(found);
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

  if (error !== null) {
    return <p className="note">Herkunft nicht lesbar: {error}</p>;
  }
  if (origin === null) {
    return null;
  }
  return (
    <details className="image-origin">
      <summary>Herkunft</summary>
      <dl>
        <dt>Modell</dt>
        <dd>{origin.model}</dd>
        <dt>Übernommen</dt>
        <dd>{formatDate(origin.date)}</dd>
        <dt>Kosten</dt>
        <dd>
          {origin.cost_usd === null
            ? "nicht gemeldet"
            : formatCost(origin.cost_usd)}
        </dd>
        {origin.resolution != null && (
          <>
            <dt>Auflösung</dt>
            <dd>
              {origin.resolution}
              {origin.quality == null ? "" : ` · Qualität ${origin.quality}`}
            </dd>
          </>
        )}
        {origin.recipe != null && (
          <>
            <dt>Rezept</dt>
            <dd>{origin.recipe}</dd>
          </>
        )}
        {origin.seed != null && (
          <>
            <dt>Startwert</dt>
            <dd>{origin.seed}</dd>
          </>
        )}
        {(origin.loras ?? []).length > 0 && (
          <>
            <dt>LoRAs</dt>
            <dd>
              {(origin.loras ?? [])
                .map((lora) => `${lora.name} · Gewicht ${String(lora.weight)}`)
                .join(", ")}
            </dd>
          </>
        )}
        {origin.appended != null && origin.appended !== "" && (
          <>
            <dt>Angehängt</dt>
            <dd>{origin.appended}</dd>
          </>
        )}
        {origin.basis !== null && (
          <>
            <dt>Grundlage</dt>
            <dd>{origin.basis}</dd>
          </>
        )}
        <dt>Anweisung</dt>
        <dd className="image-origin-prompt">{origin.prompt}</dd>
      </dl>
      {onRegenerate !== undefined && (
        <button
          type="button"
          className="ghost"
          onClick={() => {
            onRegenerate(origin);
          }}
        >
          ✨ Mit dieser Anweisung neu erzeugen
        </button>
      )}
    </details>
  );
}

function formatDate(iso: string): string {
  const date = new Date(iso);
  return Number.isNaN(date.getTime())
    ? iso
    : date.toLocaleString("de-DE", { dateStyle: "medium", timeStyle: "short" });
}
