/**
 * The figure assistant's questions and the text it writes (step 11.5, ADR-123, ADR-124): each
 * question has a picked answer, suggested by the AI from the entry and the world or written by the
 * author, and a free addition; the lines `- **<label>:** …` of "Aussehen" come from the answers
 * here, without the AI. The AI writes the suggestions and the English image description.
 */
import {
  LOOKS_LABELS,
  readLabelled,
  readSection,
  APPEARANCE,
} from "./sections";
import type { LooksLabel } from "./sections";

/** The youngest age the assistant takes; as `MIN_AGE` in `context/figure_looks.py`. */
export const MIN_AGE = 18;

/** The question of the age, which has a number field instead of free text. */
export const AGE: LooksLabel = "Alter";

/** Suggestions per question, as in `context/figure_looks.py` (ADR-124). */
export const SUGGESTIONS_PER_QUESTION = 3;

/** What the author answered: the picked choice (or `null`) and a free addition, per question. */
export type Answers = Record<
  LooksLabel,
  { choice: string | null; extra: string }
>;

/** Text of a line without an answer, as the probe wrote it. */
export const OPEN = "–";

/** No answer to any question. */
export function emptyAnswers(): Answers {
  return Object.fromEntries(
    LOOKS_LABELS.map((label) => [label, { choice: null, extra: "" }]),
  ) as Answers;
}

/** One answer as text: the choice, then the addition, joined by a comma. */
export function answerText(answer: Answers[LooksLabel]): string {
  return [answer.choice ?? "", answer.extra.trim()]
    .filter((part) => part !== "")
    .join(", ");
}

/** The answers as the server takes them: every question, open ones as empty text. */
export function answerTexts(answers: Answers): Record<LooksLabel, string> {
  return Object.fromEntries(
    LOOKS_LABELS.map((label) => [label, answerText(answers[label])]),
  ) as Record<LooksLabel, string>;
}

/**
 * The answers written in an entry's "Aussehen" as lines (rule 003: through `readLabelled`): each
 * line is the picked answer of its question, the age the text of the age field. Without lines the
 * answers are empty – a looks section in running text is not taken apart.
 */
export function answersFrom(body: string): Answers {
  const looks = readSection(body, APPEARANCE) ?? "";
  const answers = emptyAnswers();
  for (const label of LOOKS_LABELS) {
    const text = readLabelled(looks, label);
    if (text === null || text === OPEN) {
      continue;
    }
    answers[label] =
      label === AGE
        ? { choice: null, extra: text }
        : { choice: text, extra: "" };
  }
  return answers;
}

/** The lines of "Aussehen" from the answers, `–` where open (step 11.5, ADR-123). */
export function looksLines(answers: Answers): string {
  return LOOKS_LABELS.map((label) => {
    const text = answerText(answers[label]);
    return `- **${label}:** ${text === "" ? OPEN : text}`;
  }).join("\n");
}

/** Whether `age` is a whole number of at most three digits from 18 on, as the server checks. */
export function adultAge(age: string): boolean {
  return /^\d{1,3}$/.test(age.trim()) && Number(age.trim()) >= MIN_AGE;
}

/**
 * Whether the model's answer has the asked form – "a <age>-year-old adult …". Anything else
 * (an apology, a refusal in its own words) is treated like a refusal: the window offers another
 * model (V.58 (7)).
 */
export function looksLikeDescription(text: string): boolean {
  return /^an? \d{1,3}-year-old adult\b/i.test(text.trim());
}

/** One suggestion of the model; `fromEntry` when the entry already says so (ADR-124). */
export interface Suggestion {
  text: string;
  fromEntry: boolean;
}

/** The suggestions per question; a question the model skipped is missing. */
export type Suggestions = Partial<Record<LooksLabel, Suggestion[]>>;

/** What ends a suggestion taken from the entry, as `ENTRY_MARK` in `context/figure_looks.py`. */
const MARK_AT_END = /\s*\[Eintrag\]\s*$/i;

function suggestion(item: string): Suggestion {
  const text = item.replace(MARK_AT_END, "").trim();
  return { text, fromEntry: text.length < item.trim().length };
}

/**
 * The model's reply – one line `Frage: a | b | c` per question – as suggestions. Bullets and
 * bold around the question are tolerated; unknown questions, empty items and, for the age,
 * anything but an adult whole number are dropped; a question appears once, with at most three
 * suggestions. A reply without a single usable line gives an empty object.
 */
export function parseSuggestions(reply: string): Suggestions {
  const result: Suggestions = {};
  for (const line of reply.split("\n")) {
    const colon = line.indexOf(":");
    if (colon < 0) {
      continue;
    }
    const name = line
      .slice(0, colon)
      .replace(/[\s*>#-]+/g, " ")
      .trim();
    const label = LOOKS_LABELS.find((known) => known === name);
    if (label === undefined || result[label] !== undefined) {
      continue;
    }
    // `**Herkunft:** a | b` closes the bold after the colon.
    const items = line
      .slice(colon + 1)
      .replace(/^[\s*]+/, "")
      .split("|")
      .map(suggestion)
      .filter(
        (item) => item.text !== "" && (label !== AGE || adultAge(item.text)),
      )
      .slice(0, SUGGESTIONS_PER_QUESTION);
    if (items.length > 0) {
      result[label] = items;
    }
  }
  return result;
}

/** One answer to tap: the text, whether the entry says so, whether it is the author's own line. */
export interface Chip extends Suggestion {
  own: boolean;
}

/**
 * The chips of one question (not the age): the line already in the entry, the answer picked now
 * and then the suggestions – each text once, so a pick stays visible when new suggestions come.
 */
export function chipsFor(
  own: string | null,
  picked: string | null,
  suggestions: readonly Suggestion[],
): Chip[] {
  const chips: Chip[] = [];
  const add = (item: Suggestion, isOwn: boolean) => {
    const key = item.text.toLowerCase();
    if (
      item.text !== "" &&
      !chips.some((chip) => chip.text.toLowerCase() === key)
    ) {
      chips.push({ ...item, own: isOwn });
    }
  };
  add({ text: own ?? "", fromEntry: false }, true);
  add({ text: picked ?? "", fromEntry: false }, false);
  for (const item of suggestions) {
    add(item, false);
  }
  return chips;
}
