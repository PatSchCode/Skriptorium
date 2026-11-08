import { useState, type ReactNode } from "react";
import {
  api,
  describeError,
  type AspectRatio,
  type GeneratedImage,
  type ImageLevels,
  type ImageOrigin,
  type ImageTarget,
  type LoraChoice,
} from "../api";
import { ErrorText } from "./Common";
import { GeneratedPreview } from "./ImageChoices";
import { ImageGenerateForm } from "./ImageGenerateForm";
import { blobOf, shortLabel } from "./imageGenerateText";
import type { Basis } from "./ImageOriginPanel";
import { useLoraChoice } from "./RunwareLoras";
import { useSeedChoice } from "./SeedChoice";
import { useElapsed } from "./useElapsed";
import { useImageLevels } from "./useImageLevels";
import { useImageModels } from "./useImageModels";
import { useImagePrices } from "./useImagePrices";
import { useImageRequest } from "./useImageRequest";

// Helpers that callers and tests take from here since step 7.12 (moved in step 11.2).
export {
  describeBasisPrice,
  describePrice,
  nearestFormat,
  shortLabel,
} from "./imageGenerateText";

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
 * them LoRAs that fit the model can be added, each with its weight. Models that take a start
 * value offer it random or fixed (step 11.4, ADR-121); the origin keeps it with the LoRAs.
 */
export function ImageGenerate({
  title,
  initialPrompt,
  initialFormat,
  initialModel = null,
  initialLevels = NO_LEVELS,
  initialSeed = null,
  initialLoras = [],
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
  /** A fixed start value and the LoRAs to preselect, from an origin (step 11.4, ADR-121). */
  initialSeed?: number | null;
  initialLoras?: readonly LoraChoice[];
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
  const runware = choice.chosen?.runware;
  // Only ticked LoRAs that fit the model go along (ADR-115).
  const loras = useLoraChoice(runware, initialLoras);
  const seed = useSeedChoice(initialSeed);
  const takesSeed = choice.chosen?.seed === true;
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
          ...(loras.chosen.length === 0 ? {} : { loras: loras.chosen }),
          ...(takesSeed && seed.seed !== undefined ? { seed: seed.seed } : {}),
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
        ...(result.seed == null ? {} : { seed: result.seed }),
        ...(loras.chosen.length === 0
          ? {}
          : {
              loras: loras.chosen.map((lora) => ({
                ...lora,
                name:
                  choice.loras.find((l) => l.id === lora.id)?.name ?? lora.id,
              })),
            }),
        ...(result.appended == null ? {} : { appended: result.appended }),
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
          ticked={loras.ticked}
          onTick={loras.setTicked}
          seed={seed}
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
          onKeepSeed={seed.keep}
        />
      )}
      {busy && result === null && (
        <p className="note">Bild wird erzeugt … {String(elapsed.seconds)} s</p>
      )}
      <ErrorText message={error} />
      <GenerateActions
        generated={result !== null}
        busy={busy}
        canGenerate={
          choice.ready &&
          choice.model !== "" &&
          prompt !== "" &&
          (!takesSeed || seed.valid)
        }
        takeOverLabel={takeOverLabel}
        onGenerate={() => void generate()}
        onTakeOver={() => void takeOver()}
        onChange={() => {
          setResult(null);
        }}
        onClose={onClose}
      />
    </div>
  );
}

/**
 * The buttons under "Bild erzeugen": before generating "Erzeugen" and "Abbrechen"; with a preview
 * take over, generate anew, change the description or discard.
 */
function GenerateActions({
  generated,
  busy,
  canGenerate,
  takeOverLabel,
  onGenerate,
  onTakeOver,
  onChange,
  onClose,
}: {
  generated: boolean;
  busy: boolean;
  canGenerate: boolean;
  takeOverLabel: string;
  onGenerate: () => void;
  onTakeOver: () => void;
  onChange: () => void;
  onClose: () => void;
}) {
  return (
    <div className="row">
      {generated ? (
        <>
          <button
            type="button"
            className="primary"
            disabled={busy}
            onClick={onTakeOver}
          >
            {takeOverLabel}
          </button>
          <button
            type="button"
            className="ghost"
            disabled={busy}
            onClick={onGenerate}
          >
            Neu erzeugen
          </button>
          <button
            type="button"
            className="ghost"
            disabled={busy}
            onClick={onChange}
          >
            Beschreibung ändern
          </button>
        </>
      ) : (
        <button
          type="button"
          className="primary"
          disabled={busy || !canGenerate}
          onClick={onGenerate}
        >
          ✨ Erzeugen
        </button>
      )}
      <button
        type="button"
        className="ghost"
        disabled={busy && generated}
        onClick={onClose}
      >
        {generated ? "Verwerfen" : "Abbrechen"}
      </button>
    </div>
  );
}
