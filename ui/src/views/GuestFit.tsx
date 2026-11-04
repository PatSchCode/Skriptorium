import { useEffect, useRef, useState } from "react";
import {
  api,
  describeError,
  streamGuestFit,
  type GuestLink,
  type Story,
} from "../api";
import { describeWriteError } from "../api/writing";
import { taskModel } from "../models";
import { ErrorText } from "./Common";
import { describeUsage, type Usage } from "./useWriteFlow";

/**
 * "✨ Einpassen vorschlagen" (step 9.13, ADR-102): the world builder reads the guest's entry and
 * the world of the story and proposes how the guest fits in. Nothing is saved; "In das Feld
 * übernehmen" hands the text to the guest's field, which the author saves.
 */
export function GuestFit({
  story,
  link,
  name,
  onTake,
  onClose,
}: {
  story: Story;
  link: GuestLink;
  name: string;
  onTake: (text: string) => void;
  onClose: () => void;
}) {
  const [models, setModels] = useState<{ id: string; name: string }[] | null>(
    null,
  );
  const [model, setModel] = useState("");
  const [wish, setWish] = useState("");
  const [text, setText] = useState("");
  const [running, setRunning] = useState(false);
  const [usage, setUsage] = useState<Usage | null>(null);
  const [error, setError] = useState<string | null>(null);
  const abort = useRef<AbortController | null>(null);

  useEffect(() => {
    let current = true;
    api
      .models()
      .then((list) => {
        if (!current) {
          return;
        }
        const names = new Map(list.catalog.map((m) => [m.id, m.name]));
        const saved = taskModel(list, "weltenbau");
        const offered =
          saved === null || list.favorites.includes(saved)
            ? list.favorites
            : [saved, ...list.favorites];
        setModels(offered.map((id) => ({ id, name: names.get(id) ?? id })));
        setModel(
          saved ??
            (list.favorites.includes(list.default)
              ? list.default
              : (list.favorites[0] ?? "")),
        );
      })
      .catch((reason: unknown) => {
        if (current) {
          setError(describeError(reason));
          setModels([]);
        }
      });
    return () => {
      current = false;
      abort.current?.abort();
    };
  }, []);

  async function propose() {
    const controller = new AbortController();
    abort.current = controller;
    setRunning(true);
    setText("");
    setUsage(null);
    setError(null);
    try {
      await streamGuestFit(
        api.fitGuestPath(story.world, story.id, link),
        model,
        wish,
        (event) => {
          if (event.type === "text") {
            setText((before) => before + event.text);
          } else if (event.type === "done") {
            setUsage(event);
          } else if (event.type === "error") {
            setError(describeWriteError(event.kind));
          }
        },
        controller.signal,
      );
    } catch (reason: unknown) {
      if (!controller.signal.aborted) {
        setError(describeError(reason));
      }
    } finally {
      setRunning(false);
    }
  }

  const done = !running && text.trim() !== "";

  return (
    <div className="image-description guest-fit">
      <h3>Vorschlag des Weltenbauers für {name}</h3>
      {models !== null && models.length > 0 && (
        <label className="image-description-model">
          Modell
          <select
            value={model}
            disabled={running}
            onChange={(event) => {
              setModel(event.target.value);
            }}
          >
            {models.map((option) => (
              <option key={option.id} value={option.id}>
                {option.name}
              </option>
            ))}
          </select>
        </label>
      )}
      <label className="image-description-model">
        Wunsch (frei, z. B. „soll fremd bleiben“)
        <input
          value={wish}
          maxLength={1000}
          disabled={running}
          onChange={(event) => {
            setWish(event.target.value);
          }}
        />
      </label>
      {(running || done) && (
        <textarea
          aria-label="Vorschlag"
          rows={6}
          value={text}
          readOnly={running}
          onChange={(event) => {
            setText(event.target.value);
          }}
        />
      )}
      {running && <p className="note">Der Weltenbauer liest …</p>}
      {usage !== null && <p className="note">{describeUsage(usage)}</p>}
      <ErrorText message={error} />
      <div className="row">
        {done ? (
          <>
            <button
              type="button"
              className="primary"
              onClick={() => {
                onTake(text.trim());
              }}
            >
              In das Feld übernehmen
            </button>
            <button
              type="button"
              className="ghost"
              onClick={() => void propose()}
            >
              Neuer Vorschlag
            </button>
          </>
        ) : (
          <button
            type="button"
            className="primary"
            disabled={running || model === ""}
            onClick={() => void propose()}
          >
            Vorschlagen
          </button>
        )}
        <button
          type="button"
          className="ghost"
          onClick={() => {
            abort.current?.abort();
            onClose();
          }}
        >
          {running ? "Abbrechen" : "Verwerfen"}
        </button>
      </div>
      <p className="note">
        Übernehmen ersetzt den Text im Feld; gespeichert wird erst mit
        „Speichern“.
      </p>
    </div>
  );
}
