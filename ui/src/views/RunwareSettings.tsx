import { useState } from "react";
import {
  api,
  describeError,
  type ImageModelList,
  type RunwareLora,
  type RunwareModel,
} from "../api";
import { ErrorText } from "./Common";
import { WeightInput } from "./WeightInput";

/**
 * "Bildmodelle bei Runware" in the settings (step 10.8, ADR-115): the base models and LoRAs the
 * image dialog offers. A model or LoRA is added by its identifier or a Civitai link with a
 * version; the server looks it up at Runware first and takes only what Runware lists. Names,
 * additions to the prompt, trigger words and weights are edited here and saved together;
 * removing is saved the same way.
 */
export function RunwareSettings({
  list,
  onChange,
}: {
  list: ImageModelList;
  onChange: (list: ImageModelList) => void;
}) {
  const [models, setModels] = useState<RunwareModel[]>(list.runware ?? []);
  const [loras, setLoras] = useState<RunwareLora[]>(list.loras ?? []);
  const [shown, setShown] = useState(list);
  const [reference, setReference] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [dirty, setDirty] = useState(false);
  if (list !== shown) {
    setShown(list);
    setModels(list.runware ?? []);
    setLoras(list.loras ?? []);
    setDirty(false);
  }
  const ready = list.runware_ready ?? false;

  async function run(action: () => Promise<ImageModelList>) {
    setBusy(true);
    setError(null);
    try {
      onChange(await action());
      return true;
    } catch (reason: unknown) {
      setError(describeError(reason));
      return false;
    } finally {
      setBusy(false);
    }
  }

  async function add() {
    if (await run(() => api.addRunwareModel(reference.trim()))) {
      setReference("");
    }
  }

  function save() {
    void run(() =>
      api.setRunwareModels({
        models: models.map((m) => ({
          id: m.id,
          name: m.name,
          addition: m.addition,
        })),
        loras: loras.map((l) => ({
          id: l.id,
          name: l.name,
          trigger: l.trigger,
          weight: l.weight,
        })),
      }),
    );
  }

  function editModel(id: string, change: Partial<RunwareModel>) {
    setModels(models.map((m) => (m.id === id ? { ...m, ...change } : m)));
    setDirty(true);
  }

  function editLora(id: string, change: Partial<RunwareLora>) {
    setLoras(loras.map((l) => (l.id === id ? { ...l, ...change } : l)));
    setDirty(true);
  }

  return (
    <section className="card" aria-label="Bildmodelle bei Runware">
      <h2>Bildmodelle bei Runware</h2>
      {!ready && (
        <p className="note">
          Runware ist nicht eingerichtet (Schlüssel fehlt) – die Liste lässt
          sich ansehen, aber nichts hinzufügen, und Bilder damit erzeugen geht
          nicht.
        </p>
      )}
      <h3>Grundmodelle</h3>
      {models.length === 0 && <p className="note">Keine Grundmodelle.</p>}
      {models.map((model) => (
        <div key={model.id} className="runware-row">
          <input
            aria-label={`Name ${model.id}`}
            value={model.name}
            maxLength={200}
            disabled={busy}
            onChange={(event) => {
              editModel(model.id, { name: event.target.value });
            }}
          />
          <input
            aria-label={`Zusatz zur Beschreibung ${model.name}`}
            placeholder="Zusatz zur Beschreibung, z. B. score_9"
            value={model.addition}
            maxLength={500}
            disabled={busy}
            onChange={(event) => {
              editModel(model.id, { addition: event.target.value });
            }}
          />
          <span className="note">
            {model.id} · {model.architecture || "Basis unbekannt"}
          </span>
          <button
            type="button"
            className="ghost"
            aria-label={`${model.name} entfernen`}
            disabled={busy}
            onClick={() => {
              setModels(models.filter((m) => m.id !== model.id));
              setDirty(true);
            }}
          >
            ✕
          </button>
        </div>
      ))}
      <h3>Zusätze (LoRAs)</h3>
      {loras.length === 0 && <p className="note">Keine LoRAs.</p>}
      {loras.map((lora) => (
        <div key={lora.id} className="runware-row">
          <input
            aria-label={`Name ${lora.id}`}
            value={lora.name}
            maxLength={200}
            disabled={busy}
            onChange={(event) => {
              editLora(lora.id, { name: event.target.value });
            }}
          />
          <input
            aria-label={`Auslösewort ${lora.name}`}
            placeholder="Auslösewort"
            value={lora.trigger}
            maxLength={500}
            disabled={busy}
            onChange={(event) => {
              editLora(lora.id, { trigger: event.target.value });
            }}
          />
          <WeightInput
            label={`Gewicht ${lora.name}`}
            value={lora.weight}
            disabled={busy}
            onChange={(weight) => {
              editLora(lora.id, { weight });
            }}
          />
          <span className="note">
            {lora.id} · {lora.architecture || "Basis unbekannt"}
          </span>
          <button
            type="button"
            className="ghost"
            aria-label={`${lora.name} entfernen`}
            disabled={busy}
            onClick={() => {
              setLoras(loras.filter((l) => l.id !== lora.id));
              setDirty(true);
            }}
          >
            ✕
          </button>
        </div>
      ))}
      {dirty && (
        <p>
          <button
            type="button"
            className="primary"
            disabled={busy}
            onClick={save}
          >
            Änderungen speichern
          </button>
        </p>
      )}
      <h3>Hinzufügen</h3>
      <div className="row">
        <input
          aria-label="Kennung oder Civitai-Link"
          placeholder="civitai:277058@1405120 oder Civitai-Link mit Version"
          value={reference}
          maxLength={500}
          disabled={busy || !ready}
          onChange={(event) => {
            setReference(event.target.value);
          }}
        />
        <button
          type="button"
          disabled={busy || !ready || reference.trim() === ""}
          onClick={() => void add()}
        >
          Prüfen und hinzufügen
        </button>
      </div>
      <p className="note">
        Nur Versionen, die Runware anbietet, lassen sich nutzen. Grundmodell
        oder LoRA erkennt der Server selbst; eine LoRA zeigt der Dialog nur bei
        Grundmodellen derselben Basis.
      </p>
      <ErrorText message={error} />
    </section>
  );
}
