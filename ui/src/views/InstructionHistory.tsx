import { useCallback } from "react";
import { api } from "../api";
import { useLoad } from "../useLoad";
import { ErrorText } from "./Common";

const TIME = new Intl.DateTimeFormat("de-DE", {
  dateStyle: "medium",
  timeStyle: "short",
});

/**
 * The taken-over exchanges of a chapter, oldest first, laid out like a chat (step 5.13,
 * FR-027, ADR-056): the author's instruction on the right, the AI's text as it went into the
 * manuscript on the left. Only to look up: never part of the manuscript, never sent to the AI.
 * `round` changes when a new exchange was noted. An AI text whose request is still kept offers
 * "Anfrage ansehen", which goes to `onRequest` (step 10.9, ADR-116).
 */
export function InstructionHistory({
  world,
  story,
  chapter,
  round = 0,
  onRequest,
}: {
  world: string;
  story: string;
  chapter: number;
  round?: number;
  onRequest?: (id: string) => void;
}) {
  const load = useCallback(
    () => api.instructions(world, story, chapter),
    [world, story, chapter],
  );
  const { data, error } = useLoad(load, round);
  // Which requests are still kept; without that list no note offers its request.
  const loadKept = useCallback(
    () =>
      api
        .writingRequests(world, story)
        .then((requests) => new Set(requests.map((request) => request.id))),
    [world, story],
  );
  const kept = useLoad(loadKept, round).data;

  return (
    <section className="history" aria-label="Verlauf der Anweisungen">
      <p className="note">
        Was du angewiesen und übernommen hast – nur zum Nachschlagen, geht nicht
        an die KI.
      </p>
      <ErrorText message={error} />
      {data?.length === 0 && (
        <p>Noch keine übernommenen Vorschläge in diesem Kapitel.</p>
      )}
      {data !== undefined && data.length > 0 && (
        <ol className="history-list">
          {data.map((note, index) => (
            <li key={index}>
              <div className="history-in" aria-label="Deine Anweisung">
                <time dateTime={note.at}>{TIME.format(new Date(note.at))}</time>
                <p>{note.instruction}</p>
              </div>
              <div className="history-out" aria-label="Text der KI">
                <p className="who">
                  KI{note.model !== null && ` · ${shortModel(note.model)}`}
                </p>
                <p>{note.text}</p>
                {note.request !== null &&
                  onRequest !== undefined &&
                  kept?.has(note.request) === true && (
                    <RequestLink id={note.request} onRequest={onRequest} />
                  )}
              </div>
            </li>
          ))}
        </ol>
      )}
    </section>
  );
}

/** "Anfrage ansehen": opens the kept request of an AI text (step 10.9, ADR-116). */
function RequestLink({
  id,
  onRequest,
}: {
  id: string;
  onRequest: (id: string) => void;
}) {
  return (
    <button
      type="button"
      className="link"
      onClick={() => {
        onRequest(id);
      }}
    >
      Anfrage ansehen
    </button>
  );
}

/** Model identifier without the provider, e.g. "x-ai/grok-4.6" → "grok-4.6". */
export function shortModel(model: string): string {
  return model.slice(model.lastIndexOf("/") + 1);
}
