import { useState } from "react";
import type { LoraChoice, RunwareLora, RunwareModel } from "../api";
import { WeightInput } from "./WeightInput";

/** Weight per LoRA the author ticked (ADR-115). */
export type Ticked = Readonly<Record<string, number>>;

/**
 * The LoRAs the author ticks in "Bild erzeugen" (step 10.8, ADR-115): only those that fit the
 * chosen Runware model go along, each with its weight; for another model none.
 */
export function useLoraChoice(runware: RunwareModel | undefined) {
  const [ticked, setTicked] = useState<Ticked>({});
  const chosen: LoraChoice[] =
    runware === undefined
      ? []
      : runware.loras
          .filter((id) => id in ticked)
          .map((id) => ({ id, weight: ticked[id] ?? 1 }));
  return { ticked, setTicked, chosen };
}

/**
 * The LoRAs of the list that fit the chosen Runware model to tick and weigh, and a note on what
 * the server appends to the description: the model's addition and the ticked trigger words.
 */
export function RunwareExtras({
  runware,
  loras,
  ticked,
  busy,
  onTick,
}: {
  runware: RunwareModel | undefined;
  loras: readonly RunwareLora[];
  ticked: Ticked;
  busy: boolean;
  onTick: (ticked: Ticked) => void;
}) {
  const fitting = loras.filter((lora) => runware?.loras.includes(lora.id));
  const appended = [
    runware?.addition ?? "",
    ...fitting.filter((l) => l.id in ticked).map((l) => l.trigger),
  ].filter((text) => text.trim() !== "");
  return (
    <>
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
  ticked: Ticked;
  busy: boolean;
  onTick: (ticked: Ticked) => void;
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
