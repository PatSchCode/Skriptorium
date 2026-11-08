import { useCallback } from "react";
import {
  api,
  describeWriteError,
  formatCost,
  type RequestMessage,
  type RequestSummary,
  type WritingRequest,
} from "../api";
import { useLoad } from "../useLoad";
import { ErrorText } from "./Common";
import { shortModel } from "./InstructionHistory";

/** Token budget of one writing request (`MAX_BUDGET` of `context`); the estimate is shown against it. */
export const REQUEST_BUDGET = 30_000;
/** Characters of the instruction in a line of the list. */
const INSTRUCTION_START = 60;

const TIME = new Intl.DateTimeFormat("de-DE", {
  day: "2-digit",
  month: "2-digit",
  hour: "2-digit",
  minute: "2-digit",
});

/** Heading of each message by its role. */
const MESSAGE_TITLES: Record<RequestMessage["role"], string> = {
  system: "Wortlaut: Systemnachricht",
  user: "Wortlaut: Nutzernachricht",
  assistant: "Wortlaut: Antwort im Gespräch",
};

/**
 * The kept writing requests of the story (step 10.9, ADR-116), newest first: what went to the
 * AI, taken over or not. A click on a line shows the request with its blocks and, to open, the
 * messages and the AI's answer word for word. Only to look up: nothing here goes to the AI
 * again. `shown` is the request open below the list; `round` changes when a request may have
 * been added.
 */
export function WritingRequests({
  world,
  story,
  shown,
  onShow,
  round = 0,
}: {
  world: string;
  story: string;
  shown: string | null;
  onShow: (id: string) => void;
  round?: number;
}) {
  const load = useCallback(
    () => api.writingRequests(world, story),
    [world, story],
  );
  const { data, error } = useLoad(load, round);

  return (
    <section className="requests" aria-label="Anfragen an die KI">
      <p className="note">
        Was an die KI ging – die letzten 50 Anfragen dieser Geschichte, neueste
        oben. Nur zum Nachschlagen, geht nicht wieder an die KI.
      </p>
      <ErrorText message={error} />
      {data?.length === 0 && <p>Noch keine Anfragen in dieser Geschichte.</p>}
      {data !== undefined && data.length > 0 && (
        <div className="requests-scroll">
          <table className="requests-table">
            <thead>
              <tr>
                <th>Zeit</th>
                <th>Kapitel</th>
                <th>Modell</th>
                <th>Token</th>
                <th>Kosten</th>
                <th>Status</th>
                <th>Anweisung</th>
              </tr>
            </thead>
            <tbody>
              {data.map((request) => (
                <tr
                  key={request.id}
                  className={request.id === shown ? "shown" : undefined}
                >
                  <td>
                    <button
                      type="button"
                      className="link"
                      aria-pressed={request.id === shown}
                      onClick={() => {
                        onShow(request.id);
                      }}
                    >
                      {TIME.format(new Date(request.at))}
                    </button>
                  </td>
                  <td>Kap. {request.chapter}</td>
                  <td>{shortModel(request.model)}</td>
                  <td>{tokens(request.estimated_tokens)} Token</td>
                  <td>
                    {request.cost_usd === null
                      ? "–"
                      : formatCost(request.cost_usd)}
                  </td>
                  <td>
                    <RequestStatus request={request} />
                  </td>
                  <td className="instruction">
                    „{start(request.instruction)}“
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      {shown !== null && (
        <RequestDetail key={shown} world={world} story={story} id={shown} />
      )}
    </section>
  );
}

/** übernommen, verworfen, abgebrochen or Fehler (with the kind of error as its title). */
function RequestStatus({ request }: { request: RequestSummary }) {
  if (request.taken_over) {
    return <>übernommen</>;
  }
  if (request.outcome === "ok") {
    return <>verworfen</>;
  }
  if (request.outcome === "abgebrochen") {
    return <>abgebrochen</>;
  }
  return <span title={describeWriteError(request.outcome)}>Fehler</span>;
}

/** One kept request: model, length, images, estimate against the budget, blocks, texts. */
function RequestDetail({
  world,
  story,
  id,
}: {
  world: string;
  story: string;
  id: string;
}) {
  const load = useCallback(
    () => api.writingRequest(world, story, id),
    [world, story, id],
  );
  const { data, error } = useLoad(load);
  if (data === undefined) {
    return <ErrorText message={error} />;
  }
  const title = `Anfrage vom ${TIME.format(new Date(data.at))}`;
  return (
    <article className="card request-detail" aria-label={title}>
      <h3>{title}</h3>
      <p>
        Modell {shortModel(data.model)} · Länge {data.length} · {pictures(data)}{" "}
        · geschätzt {tokens(data.estimated_tokens)} / {tokens(REQUEST_BUDGET)}{" "}
        Token
      </p>
      <p className="note">{reported(data)}</p>
      <table className="request-blocks">
        <thead>
          <tr>
            <th>Baustein</th>
            <th>Token</th>
          </tr>
        </thead>
        <tbody>
          {data.blocks.map((block, index) => (
            <tr key={index}>
              <td>{block.label}</td>
              <td>{tokens(block.tokens)}</td>
            </tr>
          ))}
        </tbody>
      </table>
      {data.messages.map((message, index) => (
        <details key={index}>
          <summary>{MESSAGE_TITLES[message.role]}</summary>
          <pre className="request-text">{message.content}</pre>
        </details>
      ))}
      <details>
        <summary>Antwort der KI</summary>
        <pre className="request-text">
          {data.answer === "" ? "(keine Antwort)" : data.answer}
        </pre>
      </details>
    </article>
  );
}

function tokens(count: number): string {
  return count.toLocaleString("de-DE");
}

function start(instruction: string): string {
  return instruction.length > INSTRUCTION_START
    ? `${instruction.slice(0, INSTRUCTION_START).trimEnd()} …`
    : instruction;
}

/** "ohne Bilder" or the number of images with the names of their entries. */
function pictures(request: WritingRequest): string {
  const count = request.pictures.length;
  if (count === 0) {
    return "ohne Bilder";
  }
  const word = count === 1 ? "Bild" : "Bilder";
  return `${String(count)} ${word} (${request.pictures.join(", ")})`;
}

/** What the provider reported, or that it reported nothing (aborted or failed). */
function reported(request: WritingRequest): string {
  const cost =
    request.cost_usd === null
      ? "Kosten nicht gemeldet"
      : `Kosten ${formatCost(request.cost_usd)}`;
  if (request.input_tokens === null || request.output_tokens === null) {
    return `Gemeldet: keine Token · ${cost}`;
  }
  return `Gemeldet: ${tokens(request.input_tokens)} Token ein, ${tokens(request.output_tokens)} aus · ${cost}`;
}
