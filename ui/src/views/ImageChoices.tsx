import { formatCost, type AspectRatio, type GeneratedImage } from "../api";
import { FORMATS, nearestFormat } from "./imageGenerateText";
import type { Basis } from "./ImageOriginPanel";
import type { OfferedModel } from "./useImageModels";

/** The models, in two groups as soon as the Runware list has any (ADR-115). */
export function ModelOptions({ models }: { models: readonly OfferedModel[] }) {
  const own = models.filter((m) => m.runware === undefined);
  const runware = models.filter((m) => m.runware !== undefined);
  const options = (list: readonly OfferedModel[]) =>
    list.map((entry) => (
      <option key={entry.id} value={entry.id}>
        {entry.name}
      </option>
    ));
  if (runware.length === 0) {
    return <>{options(own)}</>;
  }
  return (
    <>
      <optgroup label="OpenRouter">{options(own)}</optgroup>
      <optgroup label="Runware">{options(runware)}</optgroup>
    </>
  );
}

/** The stored image a new one is made from (step 9.8); reports its proportions once loaded. */
export function BasisPreview({
  basis,
  onProportions,
}: {
  basis: Basis;
  onProportions: (format: AspectRatio) => void;
}) {
  return (
    <div className="image-generate-basis">
      <img
        src={basis.src}
        alt=""
        onLoad={(event) => {
          const { naturalWidth, naturalHeight } = event.currentTarget;
          if (naturalWidth > 0 && naturalHeight > 0) {
            onProportions(nearestFormat(naturalWidth / naturalHeight));
          }
        }}
      />
      <div>
        <b>Grundlage</b>
        <span className="note">{basis.label} · geht mit an das Bildmodell</span>
      </div>
    </div>
  );
}

/** One level of the image the model offers: resolution or quality (step 10.5, ADR-109). */
export function LevelChoice({
  label,
  values,
  chosen,
  busy,
  onPick,
  describe,
}: {
  label: string;
  values: readonly string[];
  chosen: string | null;
  busy: boolean;
  onPick: (value: string) => void;
  describe: (value: string) => string;
}) {
  return (
    <div className="image-generate-field">
      {label}
      <div
        className="image-generate-formats"
        role="radiogroup"
        aria-label={label}
      >
        {values.map((value) => (
          <button
            key={value}
            type="button"
            role="radio"
            aria-checked={chosen === value}
            className={chosen === value ? "chosen" : undefined}
            disabled={busy}
            onClick={() => {
              onPick(value);
            }}
          >
            {describe(value)}
          </button>
        ))}
      </div>
    </div>
  );
}

/** Portrait, square or landscape. */
export function FormatChoice({
  format,
  busy,
  onPick,
}: {
  format: AspectRatio;
  busy: boolean;
  onPick: (format: AspectRatio) => void;
}) {
  return (
    <div
      className="image-generate-formats"
      role="radiogroup"
      aria-label="Format"
    >
      {FORMATS.map((entry) => (
        <button
          key={entry.id}
          type="button"
          role="radio"
          aria-checked={format === entry.id}
          className={format === entry.id ? "chosen" : undefined}
          disabled={busy}
          onClick={() => {
            onPick(entry.id);
          }}
        >
          {entry.label}
        </button>
      ))}
    </div>
  );
}

/**
 * The generated image before it is taken over, with the model, the real cost and the start value
 * with "Startwert behalten" (step 11.4, ADR-121).
 */
export function GeneratedPreview({
  result,
  name,
  onKeepSeed,
}: {
  result: GeneratedImage;
  name: string;
  onKeepSeed: (seed: number) => void;
}) {
  const seed = result.seed ?? null;
  return (
    <>
      <img
        className="image-generate-preview"
        src={`data:${result.media_type};base64,${result.content}`}
        alt="Vorschau des erzeugten Bildes"
      />
      <p className="note">
        {name} ·{" "}
        {result.cost_usd === null
          ? "Kosten nicht gemeldet"
          : `Kosten ${formatCost(result.cost_usd)}`}
        {seed !== null && (
          <>
            {` · Startwert ${String(seed)} `}
            <button
              type="button"
              className="ghost"
              onClick={() => {
                onKeepSeed(seed);
              }}
            >
              Startwert behalten
            </button>
          </>
        )}
      </p>
    </>
  );
}
