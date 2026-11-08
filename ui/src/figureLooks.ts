/**
 * The figure assistant's questions and the text it writes (step 11.5, ADR-123): each question has
 * a few choices and a free addition; the lines `- **<label>:** …` of "Aussehen" come from the
 * answers here, without the AI. The AI only writes the English image description.
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

/** What the author answered: the picked choice (or `null`) and a free addition, per question. */
export type Answers = Record<
  LooksLabel,
  { choice: string | null; extra: string }
>;

/**
 * Choices offered per question; a question without choices has only the free field. The age is a
 * number field.
 */
export const CHOICES: Readonly<Record<LooksLabel, readonly string[]>> = {
  Herkunft: [
    "Nordeuropa",
    "Westeuropa",
    "Südeuropa",
    "Osteuropa",
    "Ostasien",
    "Südasien",
    "Naher Osten",
    "Afrika",
    "Lateinamerika",
    "gemischt",
  ],
  Alter: [],
  Größe: ["klein", "mittel", "groß"],
  Körperbau: [
    "zierlich",
    "schlank",
    "athletisch",
    "kurvig",
    "füllig",
    "kräftig",
  ],
  Proportionen: [],
  Gesicht: ["oval", "rund", "herzförmig", "kantig"],
  Haar: [],
  Augen: ["braun", "blau", "grün", "grau", "haselnuss"],
  Haut: ["hell", "mittel", "oliv", "dunkel"],
  "Besondere Merkmale": [],
};

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
 * The answers written in an entry's "Aussehen" as lines (rule 003: through `readLabelled`); a
 * text that starts with one of the choices is split into choice and addition. Without lines the
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
    const choice =
      CHOICES[label].find(
        (option) => text === option || text.startsWith(`${option}, `),
      ) ?? null;
    answers[label] = {
      choice,
      extra: choice === null ? text : text.slice(choice.length + 2),
    };
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
