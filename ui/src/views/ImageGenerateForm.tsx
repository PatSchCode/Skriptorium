import type { ReactNode } from "react";
import { formatCost, type ImagePrice, type RunwareLora } from "../api";
import {
  BasisPreview,
  FormatChoice,
  LevelChoice,
  ModelOptions,
} from "./ImageChoices";
import {
  QUALITIES,
  describeBasisPrice,
  describePrice,
} from "./imageGenerateText";
import type { Basis } from "./ImageOriginPanel";
import { RunwareExtras, type Ticked } from "./RunwareLoras";
import { SeedField, type useSeedChoice } from "./SeedChoice";
import type { useImageLevels } from "./useImageLevels";
import type { useImageModels } from "./useImageModels";
import type { useImageRequest } from "./useImageRequest";

type Choice = ReturnType<typeof useImageModels>;
type Levels = ReturnType<typeof useImageLevels>;
type PriceOf = (resolution: string | null) => ImagePrice | null;

/**
 * What the author fills in before generating: hint and extra choices of the caller, the basis,
 * the description, format, model, levels, LoRAs and the price beforehand.
 */
export function ImageGenerateForm({
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
  seed,
  busy,
  failed,
}: {
  hint: ReactNode;
  extra: ReactNode;
  basis: Basis | null;
  request: ReturnType<typeof useImageRequest>;
  choice: Choice;
  initialModel: string | null;
  levels: Levels;
  priceOf: PriceOf;
  loras: readonly RunwareLora[];
  ticked: Ticked;
  onTick: (ticked: Ticked) => void;
  /** The start value; shown only for a model that takes one (step 11.4, ADR-121). */
  seed: ReturnType<typeof useSeedChoice>;
  busy: boolean;
  /** An error is shown already; then no note about missing models. */
  failed: boolean;
}) {
  const runware = choice.chosen?.runware;
  return (
    <>
      {hint !== null && <div className="image-generate-hint">{hint}</div>}
      {extra}
      {basis !== null && (
        <BasisPreview basis={basis} onProportions={request.followBasis} />
      )}
      <PromptField request={request} basis={basis} busy={busy} />
      <FormatChoice
        format={request.format}
        busy={busy}
        onPick={request.pickFormat}
      />
      <ModelField
        choice={choice}
        initialModel={initialModel}
        withBasis={basis !== null}
        busy={busy}
        failed={failed}
      />
      {choice.chosen?.seed === true && <SeedField choice={seed} busy={busy} />}
      <LevelFields levels={levels} priceOf={priceOf} busy={busy} />
      <RunwareExtras
        runware={runware}
        loras={loras}
        ticked={ticked}
        busy={busy}
        onTick={onTick}
      />
      <p className="note">
        <PriceNote
          price={priceOf(levels.resolution)}
          resolution={levels.resolution}
          runware={runware !== undefined}
          withBasis={basis !== null}
        />
      </p>
    </>
  );
}

/** The description to change, or with a basis what should change. */
function PromptField({
  request,
  basis,
  busy,
}: {
  request: ReturnType<typeof useImageRequest>;
  basis: Basis | null;
  busy: boolean;
}) {
  return (
    <label className="image-generate-field">
      {basis === null ? "Bildbeschreibung (änderbar)" : "Was soll sich ändern?"}
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
  );
}

/** The model to pick, with a note where it comes from or that none is offered. */
function ModelField({
  choice,
  initialModel,
  withBasis,
  busy,
  failed,
}: {
  choice: Choice;
  initialModel: string | null;
  withBasis: boolean;
  busy: boolean;
  failed: boolean;
}) {
  const { models } = choice;
  if (models === null) {
    return null;
  }
  if (models.length === 0) {
    return failed ? null : (
      <p className="note">
        {withBasis
          ? "Gerade nimmt kein Bildmodell ein Ausgangsbild an."
          : "Gerade sind keine Bildmodelle verfügbar."}
      </p>
    );
  }
  return (
    <>
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
      {initialModel === null && (
        <p className="note">
          Aus den Einstellungen. Eine andere Wahl gilt nur für dieses Bild.
        </p>
      )}
    </>
  );
}

/** Resolution and quality, where the model offers them (step 10.5, ADR-109). */
function LevelFields({
  levels,
  priceOf,
  busy,
}: {
  levels: Levels;
  priceOf: PriceOf;
  busy: boolean;
}) {
  return (
    <>
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
    </>
  );
}

/** The price beforehand; Runware bills by compute time, so its cost shows afterwards. */
function PriceNote({
  price,
  resolution,
  runware,
  withBasis,
}: {
  price: ImagePrice | null;
  resolution: string | null;
  runware: boolean;
  withBasis: boolean;
}) {
  return (
    <>
      {runware
        ? "Abrechnung nach Rechenzeit – die Kosten stehen nach dem Erzeugen da"
        : describePrice(price, resolution)}
      {withBasis && price !== null && ` · ${describeBasisPrice(price)}`}
    </>
  );
}
