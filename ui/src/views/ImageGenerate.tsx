import { useState, type ReactNode } from "react";
import {
  api,
  describeError,
  formatCost,
  type AspectRatio,
  type GeneratedImage,
  type ImageLevels,
  type ImageOrigin,
  type ImagePrice,
  type ImageTarget,
  type LoraChoice,
  type RunwareLora,
} from "../api";
import { ErrorText } from "./Common";
import type { Basis } from "./ImageOriginPanel";
import { useElapsed } from "./useElapsed";
import { useImageLevels } from "./useImageLevels";
import { useImageModels, type OfferedModel } from "./useImageModels";
import { useImagePrices } from "./useImagePrices";
import { useImageRequest } from "./useImageRequest";
import { WeightInput } from "./WeightInput";

const FORMATS: readonly { id: AspectRatio; label: string }[] = [
  { id: "2:3", label: "Hochformat" },
  { id: "1:1", label: "Quadrat" },
  { id: "3:2", label: "Quer" },
];

/** No levels chosen beforehand: the presets apply (step 10.5). */
const NO_LEVELS: ImageLevels = { resolution: null, quality: null };

/**
 * "Bild erzeugen" (step 7.12, ADR-077): a description from the canon to change, format and model
 * with the price beforehand; "Erzeugen" shows a preview with the real cost. Nothing is stored
 * until "Übernehmen", which hands the image and its origin (model, description, format, cost;
 * step 9.6, ADR-095) to the caller's usual upload. With a `basis` (step 9.8, ADR-097) a stored
 * image goes along to the model: the description says what should change, only models that take
 * a basis are offered, and the format follows the basis until the author picks one. The `target`
 * (world, and story for a cover) only files the request in the usage statistics (step 9.11).
 * Where the model offers them, resolution and quality are chosen too (step 10.5, ADR-109).
 * Models of the owner's list at Runware (step 10.8, ADR-115) come in a group of their own; for
 * them LoRAs that fit the model can be added, each with its weight.
 */
export function ImageGenerate({
  title,
  initialPrompt,
  initialFormat,
  initialModel = null,
  initialLevels = NO_LEVELS,
  takeOverLabel = "Übernehmen",
  hint = null,
  extra = null,
  basis = null,
  target,
  onTakeOver,
  onClose,
}: {
  title: string;
  initialPrompt: string;
  initialFormat: AspectRatio;
  /** The model to preselect, e.g. when generating anew from an origin (step 9.6). */
  initialModel?: string | null;
  /** The levels to preselect where the model offers them (step 10.5). */
  initialLevels?: ImageLevels;
  takeOverLabel?: string;
  /**
   * A note above the description, e.g. that an entry has no looks yet (step 7.16), with a button
   * to add them (step 9.5, ADR-094).
   */
  hint?: ReactNode;
  /** More choices above the description, e.g. the places of a map (step 9.5, ADR-094). */
  extra?: ReactNode;
  /** A stored image the new one is made from (step 9.8). */
  basis?: Basis | null;
  /** Where the image goes, for the usage statistics (step 9.11, ADR-100). */
  target: ImageTarget;
  onTakeOver: (image: Blob, origin: ImageOrigin) => Promise<void>;
  onClose: () => void;
}) {
  const request = useImageRequest(initialPrompt, initialFormat);
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState<GeneratedImage | null>(null);
  const [error, setError] = useState<string | null>(null);
  const choice = useImageModels(initialModel, basis !== null, setError);
  // Weight per LoRA the author ticked (ADR-115); only those that fit the model go along.
  const [ticked, setTicked] = useState<Readonly<Record<string, number>>>({});
  const runware = choice.chosen?.runware;
  const chosenLoras: LoraChoice[] =
    runware === undefined
      ? []
      : runware.loras
          .filter((id) => id in ticked)
          .map((id) => ({ id, weight: ticked[id] ?? 1 }));
  const levels = useImageLevels(
    choice.model,
    choice.models?.find((m) => m.id === choice.model),
    initialLevels,
  );
  const prices = useImagePrices(
    choice.model,
    levels.resolutions,
    levels.quality,
  );
  const elapsed = useElapsed(busy);
  const prompt = request.prompt.trim();
  // Only levels the model offers are sent and kept (ADR-109).
  const chosenLevels = {
    ...(levels.resolution === null ? {} : { resolution: levels.resolution }),
    ...(levels.quality === null ? {} : { quality: levels.quality }),
  };

  async function generate() {
    elapsed.start();
    setBusy(true);
    setError(null);
    setResult(null);
    try {
      setResult(
        await api.generateImage({
          model: choice.model,
          prompt,
          aspect_ratio: request.format,
          ...chosenLevels,
          ...target,
          ...(basis === null ? {} : { reference: basis.reference }),
          ...(chosenLoras.length === 0 ? {} : { loras: chosenLoras }),
        }),
      );
    } catch (reason: unknown) {
      setError(describeError(reason));
    } finally {
      setBusy(false);
    }
  }

  async function takeOver() {
    if (result === null) {
      return;
    }
    setBusy(true);
    setError(null);
    try {
      await onTakeOver(blobOf(result), {
        model: result.model,
        prompt,
        aspect_ratio: request.format,
        cost_usd: result.cost_usd,
        ...chosenLevels,
        ...(basis === null ? {} : { basis: shortLabel(basis.label) }),
      });
      onClose();
    } catch (reason: unknown) {
      setError(describeError(reason));
      setBusy(false);
    }
  }

  return (
    <div className="image-generate" role="group" aria-label={title}>
      <h3>{title}</h3>
      {!choice.ready && (
        <p className="note">
          {runware === undefined
            ? "Der KI-Anbieter ist nicht eingerichtet – Bilder erzeugen geht gerade nicht."
            : "Runware ist nicht eingerichtet – mit diesem Modell geht es gerade nicht."}
        </p>
      )}
      {result === null ? (
        <ImageGenerateForm
          hint={hint}
          extra={extra}
          basis={basis}
          request={request}
          choice={choice}
          initialModel={initialModel}
          levels={levels}
          priceOf={prices.priceOf}
          loras={choice.loras}
          ticked={ticked}
          onTick={setTicked}
          busy={busy}
          failed={error !== null}
        />
      ) : (
        <GeneratedPreview
          result={result}
          name={
            choice.models?.find((m) => m.id === choice.model)?.name ??
            choice.model
          }
        />
      )}
      {busy && result === null && (
        <p className="note">Bild wird erzeugt … {String(elapsed.seconds)} s</p>
      )}
      <ErrorText message={error} />
      <div className="row">
        {result === null ? (
          <button
            type="button"
            className="primary"
            disabled={
              busy || !choice.ready || choice.model === "" || prompt === ""
            }
            onClick={() => void generate()}
          >
            ✨ Erzeugen
          </button>
        ) : (
          <>
            <button
              type="button"
              className="primary"
              disabled={busy}
              onClick={() => void takeOver()}
            >
              {takeOverLabel}
            </button>
            <button
              type="button"
              className="ghost"
              disabled={busy}
              onClick={() => void generate()}
            >
              Neu erzeugen
            </button>
            <button
              type="button"
              className="ghost"
              disabled={busy}
              onClick={() => {
                setResult(null);
              }}
            >
              Beschreibung ändern
            </button>
          </>
        )}
        <button
          type="button"
          className="ghost"
          disabled={busy && result !== null}
          onClick={onClose}
        >
          {result === null ? "Abbrechen" : "Verwerfen"}
        </button>
      </div>
    </div>
  );
}

/**
 * What the author fills in before generating: hint and extra choices of the caller, the basis,
 * the description, format, model and the price beforehand.
 */
function ImageGenerateForm({
  hint,
  extra,
  basis,
  request,
  choice,
  initialModel,
  levels,
  priceOf,
  loras,
  ticked,
  onTick,
  busy,
  failed,
}: {
  hint: ReactNode;
  extra: ReactNode;
  basis: Basis | null;
  request: ReturnType<typeof useImageRequest>;
  choice: ReturnType<typeof useImageModels>;
  initialModel: string | null;
  levels: ReturnType<typeof useImageLevels>;
  priceOf: (resolution: string | null) => ImagePrice | null;
  loras: readonly RunwareLora[];
  ticked: Readonly<Record<string, number>>;
  onTick: (ticked: Readonly<Record<string, number>>) => void;
  busy: boolean;
  /** An error is shown already; then no note about missing models. */
  failed: boolean;
}) {
  const { models } = choice;
  const price = priceOf(levels.resolution);
  const runware = choice.chosen?.runware;
  const fitting = loras.filter((lora) => runware?.loras.includes(lora.id));
  const appended = [
    runware?.addition ?? "",
    ...fitting.filter((l) => l.id in ticked).map((l) => l.trigger),
  ].filter((text) => text.trim() !== "");
  return (
    <>
      {hint !== null && <div className="image-generate-hint">{hint}</div>}
      {extra}
      {basis !== null && (
        <BasisPreview basis={basis} onProportions={request.followBasis} />
      )}
      <label className="image-generate-field">
        {basis === null
          ? "Bildbeschreibung (änderbar)"
          : "Was soll sich ändern?"}
        <textarea
          rows={5}
          maxLength={4000}
          value={request.prompt}
          placeholder={
            basis === null
              ? undefined
              : "z. B. derselbe Mann im Winter, mit schwerem Wollmantel"
          }
          disabled={busy}
          onChange={(event) => {
            request.setPrompt(event.target.value);
          }}
        />
      </label>
      <FormatChoice
        format={request.format}
        busy={busy}
        onPick={request.pickFormat}
      />
      {models !== null && models.length > 0 && (
        <label className="image-generate-field">
          Modell
          <select
            value={choice.model}
            disabled={busy}
            onChange={(event) => {
              choice.setModel(event.target.value);
            }}
          >
            <ModelOptions models={models} />
          </select>
        </label>
      )}
      {models !== null && models.length > 0 && initialModel === null && (
        <p className="note">
          Aus den Einstellungen. Eine andere Wahl gilt nur für dieses Bild.
        </p>
      )}
      {models !== null && models.length === 0 && !failed && (
        <p className="note">
          {basis === null
            ? "Gerade sind keine Bildmodelle verfügbar."
            : "Gerade nimmt kein Bildmodell ein Ausgangsbild an."}
        </p>
      )}
      {levels.resolutions.length > 0 && (
        <LevelChoice
          label="Auflösung"
          values={levels.resolutions}
          chosen={levels.resolution}
          busy={busy}
          onPick={levels.pickResolution}
          describe={(resolution) => {
            const known = priceOf(resolution);
            return known?.unit === "image" && known.cost_usd !== null
              ? `${resolution} ${formatCost(known.cost_usd)}`
              : resolution;
          }}
        />
      )}
      {levels.qualities.length > 0 && (
        <LevelChoice
          label="Qualität"
          values={levels.qualities}
          chosen={levels.quality}
          busy={busy}
          onPick={levels.pickQuality}
          describe={(quality) => QUALITIES[quality] ?? quality}
        />
      )}
      {fitting.length > 0 && (
        <LoraChoices
          loras={fitting}
          ticked={ticked}
          busy={busy}
          onTick={onTick}
        />
      )}
      {appended.length > 0 && (
        <p className="note">
          Angehängt an die Beschreibung: {appended.join(", ")}
        </p>
      )}
      <p className="note">
        {runware === undefined
          ? describePrice(price, levels.resolution)
          : "Abrechnung nach Rechenzeit – die Kosten stehen nach dem Erzeugen da"}
        {basis !== null && price !== null && ` · ${describeBasisPrice(price)}`}
      </p>
    </>
  );
}

/** The models, in two groups as soon as the Runware list has any (ADR-115). */
function ModelOptions({ models }: { models: readonly OfferedModel[] }) {
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

/** LoRAs that fit the chosen Runware model, each to tick and weigh (ADR-115). */
function LoraChoices({
  loras,
  ticked,
  busy,
  onTick,
}: {
  loras: readonly RunwareLora[];
  ticked: Readonly<Record<string, number>>;
  busy: boolean;
  onTick: (ticked: Readonly<Record<string, number>>) => void;
}) {
  return (
    <fieldset className="image-generate-field image-generate-loras">
      <legend>Zusätze (LoRAs)</legend>
      {loras.map((lora) => {
        const on = lora.id in ticked;
        return (
          <div key={lora.id} className="row">
            <label>
              <input
                type="checkbox"
                checked={on}
                disabled={busy}
                onChange={() => {
                  onTick(
                    on
                      ? Object.fromEntries(
                          Object.entries(ticked).filter(
                            ([id]) => id !== lora.id,
                          ),
                        )
                      : { ...ticked, [lora.id]: lora.weight },
                  );
                }}
              />{" "}
              {lora.name}
            </label>
            <WeightInput
              label={`Gewicht ${lora.name}`}
              value={ticked[lora.id] ?? lora.weight}
              disabled={busy || !on}
              onChange={(weight) => {
                onTick({ ...ticked, [lora.id]: weight });
              }}
            />
          </div>
        );
      })}
    </fieldset>
  );
}

/** The stored image a new one is made from (step 9.8); reports its proportions once loaded. */
function BasisPreview({
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

/** Names of the quality levels the catalog uses; others are shown as they come. */
const QUALITIES: Readonly<Record<string, string>> = {
  auto: "automatisch",
  low: "niedrig",
  medium: "mittel",
  high: "hoch",
  xhigh: "sehr hoch",
  max: "höchste",
};

/** One level of the image the model offers: resolution or quality (step 10.5, ADR-109). */
function LevelChoice({
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
function FormatChoice({
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

/** The generated image before it is taken over, with the model and the real cost. */
function GeneratedPreview({
  result,
  name,
}: {
  result: GeneratedImage;
  name: string;
}) {
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
      </p>
    </>
  );
}

/** The price shown before generating, at the chosen `resolution` if any (step 10.5). */
export function describePrice(
  price: ImagePrice | null,
  resolution: string | null = null,
): string {
  if (price === null) {
    return "Preis wird geladen …";
  }
  if (price.cost_usd === null || price.unit === null) {
    return resolution === null
      ? "Preis unbekannt"
      : `Preis für ${resolution} nicht ausgewiesen – die Kosten stehen nach dem Erzeugen da`;
  }
  if (price.unit === "image") {
    return `ca. ${formatCost(price.cost_usd)} je Bild${resolution === null ? "" : ` (${resolution})`}`;
  }
  if (price.unit === "megapixel") {
    return `ca. ${formatCost(price.cost_usd)} je Bild (1 Megapixel)`;
  }
  return "Abrechnung nach Verbrauch – die Kosten stehen nach dem Erzeugen da";
}

/** The server keeps at most this many characters of the basis's description (ADR-097). */
const MAX_BASIS_LABEL = 200;

/**
 * The description of the basis as the origin keeps it: a long entry name is cut with "…", so
 * taking over a paid image never fails on its length.
 */
export function shortLabel(label: string): string {
  return label.length <= MAX_BASIS_LABEL
    ? label
    : `${label.slice(0, MAX_BASIS_LABEL - 1)}…`;
}

/** What the basis costs, shown after the price of the new image (step 9.8). */
export function describeBasisPrice(price: ImagePrice): string {
  const cost = price.input_cost_usd ?? null;
  if (cost === null || price.input_unit == null) {
    return "Grundlage: Preis vom Anbieter nicht ausgewiesen";
  }
  if (cost === 0) {
    return "Grundlage ohne Aufpreis";
  }
  if (price.input_unit === "image") {
    return `Grundlage ${formatCost(cost)}`;
  }
  if (price.input_unit === "megapixel") {
    return `Grundlage ${formatCost(cost)} je Megapixel`;
  }
  return "Grundlage nach Verbrauch";
}

/** The offered format closest to the proportions `ratio` (width / height) of an image. */
export function nearestFormat(ratio: number): AspectRatio {
  const distance = (id: AspectRatio) => {
    const [width = 1, height = 1] = id.split(":").map(Number);
    return Math.abs(Math.log(ratio / (width / height)));
  };
  return FORMATS.map((entry) => entry.id).reduce((best, id) =>
    distance(id) < distance(best) ? id : best,
  );
}

function blobOf(image: GeneratedImage): Blob {
  const binary = atob(image.content);
  const bytes = new Uint8Array(binary.length);
  for (let at = 0; at < binary.length; at++) {
    bytes[at] = binary.charCodeAt(at);
  }
  return new Blob([bytes], { type: image.media_type });
}
