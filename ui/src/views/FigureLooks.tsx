import { useCallback, useEffect, useRef, useState } from "react";
import { api, describeError, streamFigureLooks, type CanonEntry } from "../api";
import { describeWriteError } from "../api/writing";
import { base64, GENERATED_SIDE, shrinkImage } from "../files";
import {
  adultAge,
  AGE,
  answersFrom,
  answerTexts,
  chipsFor,
  looksLikeDescription,
  looksLines,
  MIN_AGE,
  parseSuggestions,
  type Answers,
  type Suggestions,
} from "../figureLooks";
import {
  APPEARANCE,
  IMAGE_DESCRIPTION,
  LOOKS_LABELS,
  putSectionAfter,
} from "../sections";
import type { LooksLabel } from "../sections";
import { ErrorText } from "./Common";
import { FigureDrafts, type ChosenDraft } from "./FigureDrafts";
import { blobOf } from "./imageGenerateText";
import { SectionConflict } from "./SectionConflict";
import { useSectionChoice } from "./useSectionChoice";
import { useTaskModel } from "./useTaskModel";
import { describeUsage, type Usage } from "./useWriteFlow";

/**
 * "✨ Aussehen festlegen" (step 11.5, ADR-123, ADR-124): fixed questions about a figure's looks,
 * each with a free field, preset from the lines already in "Aussehen". "Vorschläge machen" asks
 * a text model (task "Figuren-Assistent") for three answers per question from the entry and the
 * world; the author taps one (nothing is set before) and may add words. "Formulieren" asks the
 * model for an English image description from the answers; the German lines come from the answers.
 * Drafts with different start values let the author pick a main image. "Übernehmen" writes
 * "Aussehen" (asking before it replaces text) and "Bildbeschreibung" right after it, and adds the
 * picked draft as main image with its origin.
 */
export function FigureLooks({
  entry,
  onChanged,
  onClose,
}: {
  entry: CanonEntry;
  onChanged: (entry: CanonEntry) => void;
  onClose: () => void;
}) {
  // The lines already in the entry stay tappable even when other suggestions are picked.
  const [own] = useState<Answers>(() => answersFrom(entry.body));
  const [answers, setAnswers] = useState<Answers>(own);
  const [suggestions, setSuggestions] = useState<Suggestions>({});
  const [suggesting, setSuggesting] = useState(false);
  const [lines, setLines] = useState<string | null>(null);
  const [description, setDescription] = useState("");
  const [running, setRunning] = useState(false);
  const [refused, setRefused] = useState(false);
  const [usage, setUsage] = useState<Usage | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [draft, setDraft] = useState<ChosenDraft | null>(null);
  const [saving, setSaving] = useState(false);
  const abort = useRef<AbortController | null>(null);
  const { place, asking } = useSectionChoice();
  const reportError = useCallback((message: string) => {
    setError(message);
  }, []);
  const { models, model, setModel } = useTaskModel(
    "figurenassistent",
    reportError,
  );

  useEffect(
    () => () => {
      abort.current?.abort();
    },
    [],
  );

  const age = answers.Alter.extra;
  const ageOk = adultAge(age);

  function answer(label: LooksLabel, change: Partial<Answers[LooksLabel]>) {
    setAnswers((before) => ({
      ...before,
      [label]: { ...before[label], ...change },
    }));
  }

  async function suggest() {
    const controller = new AbortController();
    abort.current = controller;
    setSuggesting(true);
    setUsage(null);
    setError(null);
    let text = "";
    try {
      await streamFigureLooks(
        api.figureLooksSuggestionsPath(entry.world, entry.id),
        model,
        answerTexts(answers),
        (event) => {
          if (event.type === "text") {
            text += event.text;
          } else if (event.type === "done") {
            setUsage(event);
            const found = parseSuggestions(text);
            if (Object.keys(found).length === 0) {
              setError(
                "Die KI hat keine Vorschläge in der erwarteten Form geliefert. " +
                  "Versuche es noch einmal oder wähle ein anderes Modell.",
              );
            } else {
              setSuggestions(found);
            }
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
      setSuggesting(false);
    }
  }

  async function formulate() {
    const controller = new AbortController();
    abort.current = controller;
    setRunning(true);
    setRefused(false);
    setDescription("");
    setUsage(null);
    setError(null);
    setDraft(null);
    setLines(looksLines(answers));
    let text = "";
    try {
      await streamFigureLooks(
        api.figureLooksPath(entry.world, entry.id),
        model,
        answerTexts(answers),
        (event) => {
          if (event.type === "text") {
            text += event.text;
            setDescription(text);
          } else if (event.type === "done") {
            setUsage(event);
            setRefused(!looksLikeDescription(text));
          } else if (event.type === "error") {
            setError(describeWriteError(event.kind));
            setRefused(event.kind === "abgelehnt");
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

  async function takeOver() {
    if (lines === null) {
      return;
    }
    setSaving(true);
    setError(null);
    try {
      // The current text, in case it changed elsewhere meanwhile.
      const fresh = await api.entry(entry.world, entry.id);
      const withLooks = await place(fresh.body, APPEARANCE, lines);
      if (withLooks === null) {
        setSaving(false);
        return;
      }
      const body = putSectionAfter(
        withLooks,
        IMAGE_DESCRIPTION,
        APPEARANCE,
        description,
      );
      let saved = await api.updateEntry(entry.world, entry.id, { body });
      if (draft !== null) {
        saved = await api.addImage(
          entry.world,
          entry.id,
          await base64(await shrinkImage(blobOf(draft.image), GENERATED_SIDE)),
          draft.origin,
        );
        const added = saved.images.at(-1);
        if (added !== undefined && saved.images[0] !== added) {
          saved = await api.setMainImage(entry.world, entry.id, added);
        }
      }
      onChanged(saved);
      onClose();
    } catch (reason: unknown) {
      setError(describeError(reason));
      setSaving(false);
    }
  }

  const showQuestions = lines === null || running || refused;
  const busy = running || suggesting;
  const formulated =
    lines !== null && !running && !refused && description.trim() !== "";
  return (
    <div className="image-description figure-looks">
      <h3>Aussehen von {entry.name}</h3>
      {showQuestions ? (
        <>
          <div className="row figure-looks-suggest">
            <button
              type="button"
              className="ghost"
              disabled={busy || model === ""}
              onClick={() => void suggest()}
            >
              ✨ Vorschläge machen
            </button>
            <span className="note">
              {Object.keys(suggestions).length === 0
                ? "aus Eintrag und Welt"
                : "aus Eintrag und Welt · noch einmal tippen für neue Vorschläge"}
            </span>
          </div>
          <Questions
            answers={answers}
            own={own}
            suggestions={suggestions}
            busy={busy}
            ageOk={ageOk || age.trim() === ""}
            onAnswer={answer}
          />
        </>
      ) : (
        <>
          <label>
            Aussehen (Deutsch)
            <textarea
              rows={10}
              value={lines}
              onChange={(event) => {
                setLines(event.target.value);
              }}
            />
          </label>
          <label>
            Bildbeschreibung (Englisch, für Bildmodelle)
            <textarea
              rows={4}
              value={description}
              onChange={(event) => {
                setDescription(event.target.value);
              }}
            />
          </label>
          <FigureDrafts
            world={entry.world}
            description={description}
            onPick={setDraft}
          />
        </>
      )}
      {running && (
        <p className="note">Die KI formuliert die Bildbeschreibung …</p>
      )}
      {suggesting && <p className="note">Die KI macht Vorschläge …</p>}
      {refused && !running && (
        <p className="note">
          Das Modell hat nicht wie verlangt geantwortet – vermutlich gesperrt.
          Wähle ein anderes Modell und formuliere neu.
        </p>
      )}
      {usage !== null && <p className="note">{describeUsage(usage)}</p>}
      <ErrorText message={error} />
      <div className="row">
        {showQuestions && models !== null && models.length > 0 && (
          <label className="image-description-model">
            Modell
            <select
              value={model}
              disabled={busy}
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
        {formulated ? (
          <>
            <button
              type="button"
              className="primary"
              disabled={saving || description.trim() === ""}
              onClick={() => void takeOver()}
            >
              Übernehmen
            </button>
            <button
              type="button"
              className="ghost"
              disabled={saving}
              onClick={() => {
                setLines(null);
                setDraft(null);
              }}
            >
              Zurück zu den Fragen
            </button>
          </>
        ) : (
          <button
            type="button"
            className="primary"
            disabled={busy || model === "" || !ageOk}
            onClick={() => void formulate()}
          >
            ✨ Formulieren
          </button>
        )}
        <button
          type="button"
          className="ghost"
          disabled={saving}
          onClick={() => {
            abort.current?.abort();
            // Stopping the suggestions keeps the window and the answers (owner, 2026-11-09).
            if (!suggesting) {
              onClose();
            }
          }}
        >
          {suggesting
            ? "Vorschläge abbrechen"
            : running
              ? "Abbrechen"
              : "Verwerfen"}
        </button>
      </div>
      <SectionConflict asking={asking} />
    </div>
  );
}

/**
 * The questions, each with the answers to tap (the line already in the entry, the pick, the
 * model's suggestions – a tap again takes the pick back) and a free field. The age is a number
 * field whose suggestions fill it.
 */
function Questions({
  answers,
  own,
  suggestions,
  busy,
  ageOk,
  onAnswer,
}: {
  answers: Answers;
  own: Answers;
  suggestions: Suggestions;
  busy: boolean;
  ageOk: boolean;
  onAnswer: (label: LooksLabel, change: Partial<Answers[LooksLabel]>) => void;
}) {
  return (
    <div className="figure-looks-questions">
      {LOOKS_LABELS.map((label) => {
        const proposed = suggestions[label] ?? [];
        return (
          <fieldset key={label} disabled={busy}>
            <legend>{label}</legend>
            {label === AGE ? (
              <>
                {proposed.length > 0 && (
                  <div className="figure-looks-chips">
                    {proposed.map((option) => (
                      <button
                        key={option.text}
                        type="button"
                        aria-pressed={
                          answers.Alter.extra.trim() === option.text
                        }
                        onClick={() => {
                          onAnswer(AGE, { extra: option.text });
                        }}
                      >
                        {option.text}
                        <Mark fromEntry={option.fromEntry} />
                      </button>
                    ))}
                  </div>
                )}
                <input
                  aria-label="Alter"
                  inputMode="numeric"
                  value={answers.Alter.extra}
                  onChange={(event) => {
                    onAnswer(AGE, { extra: event.target.value });
                  }}
                />
                <span className="note">
                  {ageOk
                    ? `Jahre, ab ${String(MIN_AGE)}`
                    : `Nur ganze Zahl ab ${String(MIN_AGE)}`}
                </span>
              </>
            ) : (
              <>
                <Chips
                  chips={chipsFor(
                    own[label].choice,
                    answers[label].choice,
                    proposed,
                  )}
                  picked={answers[label].choice}
                  onPick={(text) => {
                    onAnswer(label, {
                      choice: answers[label].choice === text ? null : text,
                    });
                  }}
                />
                <input
                  aria-label={`${label} (frei)`}
                  placeholder="Ergänzung"
                  value={answers[label].extra}
                  onChange={(event) => {
                    onAnswer(label, { extra: event.target.value });
                  }}
                />
              </>
            )}
          </fieldset>
        );
      })}
    </div>
  );
}

function Chips({
  chips,
  picked,
  onPick,
}: {
  chips: ReturnType<typeof chipsFor>;
  picked: string | null;
  onPick: (text: string) => void;
}) {
  if (chips.length === 0) {
    return null;
  }
  return (
    <div className="figure-looks-chips">
      {chips.map((chip) => (
        <button
          key={chip.text}
          type="button"
          aria-pressed={picked === chip.text}
          onClick={() => {
            onPick(chip.text);
          }}
        >
          {chip.text}
          <Mark fromEntry={chip.fromEntry} own={chip.own} />
        </button>
      ))}
    </div>
  );
}

/** Where a suggestion comes from, when that is worth saying. */
function Mark({
  fromEntry,
  own = false,
}: {
  fromEntry: boolean;
  own?: boolean;
}) {
  if (own) {
    return <small className="figure-looks-badge">{" bisher"}</small>;
  }
  return fromEntry ? (
    <small className="figure-looks-badge">{" aus Eintrag"}</small>
  ) : null;
}
