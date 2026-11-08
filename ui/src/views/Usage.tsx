import { useCallback, useState, type ReactNode } from "react";
import {
  api,
  FORMS,
  formatCost,
  type UsageGroup,
  type UsageTotals,
  type WorldUsage,
} from "../api";
import { shortName } from "../models";
import { useLoad } from "../useLoad";
import { ErrorText } from "./Common";

/** Names of the kinds of requests as the author knows them from the program. */
const KINDS: Record<string, string> = {
  schreiben: "Schreiben",
  kurzfassung: "Kurzfassung",
  gesamtzusammenfassung: "Gesamtzusammenfassung",
  weltenbau: "Weltenbauer",
  bildbeschreibung: "Bild beschreiben",
  bilderzeugung: "Bild erzeugen",
  aussehen: "Aussehen",
  figurenassistent: "Figuren-Assistent",
};

/** What the details below the table show: a world or one of its stories. */
interface Focus {
  world: string;
  story: string | null;
}

/** The month of today as the server counts it (UTC), e.g. "2026-11". */
function thisMonth(): string {
  return new Date().toISOString().slice(0, 7);
}

/** "November 2026" for "2026-11". */
function monthLabel(month: string): string {
  const [year, number] = month.split("-").map(Number);
  return new Date(
    Date.UTC(year ?? 2000, (number ?? 1) - 1, 1),
  ).toLocaleDateString("de-DE", {
    month: "long",
    year: "numeric",
    timeZone: "UTC",
  });
}

function count(value: number): string {
  return value.toLocaleString("de-DE");
}

function share(totals: UsageTotals): string {
  return totals.cache_share === null
    ? "–"
    : `${Math.round(totals.cache_share * 100).toString()} %`;
}

function worldName(world: WorldUsage): string {
  return world.name ?? `gelöschte Welt (${world.id})`;
}

/**
 * "Verbrauch" (step 9.11, ADR-100): requests, tokens, cost and the part of the input read from the
 * provider's cache, for a month or all months, by world. A world opens to its stories and the
 * work on the world itself; below the table the chosen world or story by kind and by model.
 * Requests from before step 9.11 carry no world and stay in "ohne Zuordnung", so the sum is the
 * whole month.
 */
export function Usage() {
  const [month, setMonth] = useState<string | null>(thisMonth);
  const [focus, setFocus] = useState<Focus | null>(null);
  const load = useCallback(() => api.usageStats(month), [month]);
  const { data, error } = useLoad(load);
  const loadModels = useCallback(
    () => Promise.all([api.models(), api.imageModels()]),
    [],
  );
  const models = useLoad(loadModels).data;

  const months = data?.months ?? [];
  const choices = months.includes(thisMonth())
    ? months
    : [thisMonth(), ...months];

  function modelName(id: string): string {
    if (models === undefined) {
      return id;
    }
    const [text, images] = models;
    const image = images.models.find((model) => model.id === id);
    if (image !== undefined) {
      return image.name;
    }
    return shortName(
      text.catalog.find((model) => model.id === id),
      id,
    );
  }

  const world = data?.worlds.find((item) => item.id === focus?.world);
  const story = world?.stories.find((item) => item.id === focus?.story);
  let detail: { title: string; group: UsageGroup } | null = null;
  if (world !== undefined) {
    detail =
      story === undefined
        ? { title: worldName(world), group: world.usage }
        : {
            title: story.title ?? `gelöschte Geschichte (${story.id})`,
            group: story.usage,
          };
  }

  return (
    <section className="card usage" aria-label="Verbrauch">
      <div className="usage-head">
        <h2>Verbrauch</h2>
        <label>
          Zeitraum{" "}
          <select
            value={month ?? ""}
            onChange={(event) => {
              setMonth(event.target.value === "" ? null : event.target.value);
              setFocus(null);
            }}
          >
            {choices.map((item) => (
              <option key={item} value={item}>
                {monthLabel(item)}
              </option>
            ))}
            <option value="">Alle Monate</option>
          </select>
        </label>
      </div>
      <ErrorText message={error} />
      {data !== undefined && (
        <>
          <Summary totals={data.total.totals} />
          <table className="usage-table">
            <thead>
              <tr>
                <th>Welt</th>
                <th>Anfragen</th>
                <th className="wide">Token ein</th>
                <th className="wide">Token aus</th>
                <th>Token gesamt</th>
                <th>Kosten</th>
                <th>Zwischen&shy;speicher</th>
              </tr>
            </thead>
            <tbody>
              {data.worlds.map((item) => {
                const open = focus?.world === item.id;
                return (
                  <WorldRows
                    key={item.id}
                    world={item}
                    open={open}
                    focusedStory={open ? focus.story : null}
                    onWorld={() => {
                      setFocus(
                        open && focus.story === null
                          ? null
                          : { world: item.id, story: null },
                      );
                    }}
                    onStory={(id) => {
                      setFocus({ world: item.id, story: id });
                    }}
                  />
                );
              })}
              {data.unassigned.totals.requests > 0 && (
                <Row
                  className="old"
                  label={
                    <>
                      ohne Zuordnung{" "}
                      <span className="note">(vor dem Umbau)</span>
                    </>
                  }
                  totals={data.unassigned.totals}
                />
              )}
              <Row className="sum" label="Summe" totals={data.total.totals} />
            </tbody>
          </table>
          {data.worlds.length === 0 &&
            data.unassigned.totals.requests === 0 && (
              <p className="note">Keine Anfragen in diesem Zeitraum.</p>
            )}
          {detail !== null && (
            <Detail
              title={detail.title}
              group={detail.group}
              modelName={modelName}
            />
          )}
        </>
      )}
    </section>
  );
}

/** Sums of the whole period above the table. */
function Summary({ totals }: { totals: UsageTotals }) {
  return (
    <>
      <p>
        {formatCost(totals.cost_usd)} für {count(totals.requests)}{" "}
        {totals.requests === 1 ? "Anfrage" : "Anfragen"} ·{" "}
        {count(totals.input_tokens)} Token ein, {count(totals.output_tokens)}{" "}
        aus
        {totals.cache_share !== null && (
          <>
            {" "}
            · <b>{share(totals)}</b> der Eingabe aus dem Zwischenspeicher
          </>
        )}
      </p>
      {totals.without_cost > 0 && (
        <p className="note">
          {count(totals.without_cost)}{" "}
          {totals.without_cost === 1 ? "Anfrage" : "Anfragen"} ohne gemeldete
          Kosten – die Abrechnung bei OpenRouter kann etwas höher liegen.
        </p>
      )}
    </>
  );
}

/** A world, and when open its stories and the work on the world itself. */
function WorldRows({
  world,
  open,
  focusedStory,
  onWorld,
  onStory,
}: {
  world: WorldUsage;
  open: boolean;
  focusedStory: string | null;
  onWorld: () => void;
  onStory: (id: string) => void;
}) {
  return (
    <>
      <Row
        label={
          <button
            type="button"
            className="link"
            aria-expanded={open}
            onClick={onWorld}
          >
            {open ? "▾" : "▸"} {worldName(world)}
            {world.archived && <span className="note"> (archiviert)</span>}
          </button>
        }
        totals={world.usage.totals}
      />
      {open &&
        world.stories.map((story) => (
          <Row
            key={story.id}
            className="sub"
            label={
              <>
                <button
                  type="button"
                  className="link"
                  aria-pressed={focusedStory === story.id}
                  onClick={() => {
                    onStory(story.id);
                  }}
                >
                  {story.title ?? `gelöschte Geschichte (${story.id})`}
                </button>{" "}
                <span className="note">
                  {FORMS.find((form) => form.id === story.form)?.label}
                  {story.archived && " (archiviert)"}
                </span>
              </>
            }
            totals={story.usage.totals}
          />
        ))}
      {open && world.own.totals.requests > 0 && (
        <Row
          className="sub"
          label={
            <>
              Welt selbst{" "}
              <span className="note">Weltenbauer, Bilder, Aussehen</span>
            </>
          }
          totals={world.own.totals}
        />
      )}
    </>
  );
}

/** One line of the table; on small screens a card with name and cost on top (styles.css). */
function Row({
  label,
  totals,
  className,
}: {
  label: ReactNode;
  totals: UsageTotals;
  className?: string;
}) {
  return (
    <tr className={className}>
      <td className="name">{label}</td>
      <td>
        {count(totals.requests)}
        <span className="unit"> Anfragen</span>
      </td>
      <td className="wide">{count(totals.input_tokens)}</td>
      <td className="wide">{count(totals.output_tokens)}</td>
      <td className="total">
        {count(totals.input_tokens + totals.output_tokens)}
        <span className="unit"> Token</span>
      </td>
      <td className="cost">{formatCost(totals.cost_usd)}</td>
      <td className="share">
        {share(totals)}
        <span className="unit"> Zwischenspeicher</span>
      </td>
    </tr>
  );
}

/** A world or story by kind and by model; models sortable by number or by token amount. */
function Detail({
  title,
  group,
  modelName,
}: {
  title: string;
  group: UsageGroup;
  modelName: (id: string) => string;
}) {
  const [byTokens, setByTokens] = useState(false);
  const most = Math.max(1, ...group.kinds.map((kind) => kind.requests));
  const tokens = (totals: UsageTotals) =>
    totals.input_tokens + totals.output_tokens;
  const models = byTokens
    ? [...group.models].sort((a, b) => tokens(b) - tokens(a))
    : group.models;
  return (
    <div className="usage-detail">
      <h3>{title} – nach Art</h3>
      <div className="usage-kinds">
        {group.kinds.map((kind) => (
          <div key={kind.kind} className="usage-kind">
            <span>{KINDS[kind.kind] ?? kind.kind}</span>
            <span
              className="bar"
              style={{
                width: `${Math.round((kind.requests / most) * 100).toString()}%`,
              }}
            />
            <span>
              {count(kind.requests)} · {formatCost(kind.cost_usd)}
            </span>
          </div>
        ))}
      </div>
      <div className="usage-head">
        <h3>{title} – Modelle</h3>
        <div className="segmented" role="group" aria-label="Sortierung">
          <button
            type="button"
            aria-pressed={!byTokens}
            onClick={() => {
              setByTokens(false);
            }}
          >
            nach Anzahl
          </button>
          <button
            type="button"
            aria-pressed={byTokens}
            onClick={() => {
              setByTokens(true);
            }}
          >
            nach Token
          </button>
        </div>
      </div>
      <table className="usage-models">
        <thead>
          <tr>
            <th>Modell</th>
            <th>Anfragen</th>
            <th>Token gesamt</th>
            <th>Kosten</th>
            <th>Zwischen&shy;speicher</th>
          </tr>
        </thead>
        <tbody>
          {models.map((model) => (
            <tr key={model.model}>
              <td>{modelName(model.model)}</td>
              <td>{count(model.requests)}</td>
              <td>{tokens(model) === 0 ? "–" : count(tokens(model))}</td>
              <td>{formatCost(model.cost_usd)}</td>
              <td>{share(model)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
