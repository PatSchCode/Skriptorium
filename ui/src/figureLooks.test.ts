import { describe, expect, it } from "vitest";
import {
  adultAge,
  answersFrom,
  answerText,
  answerTexts,
  chipsFor,
  emptyAnswers,
  looksLikeDescription,
  looksLines,
  parseSuggestions,
} from "./figureLooks";

describe("the figure assistant's answers and lines (step 11.5, ADR-123)", () => {
  it("joins choice and addition and writes every line, open ones as –", () => {
    const answers = emptyAnswers();
    answers.Herkunft = {
      choice: "nordeuropäisch wirkend",
      extra: " skandinavisch ",
    };
    answers.Alter = { choice: null, extra: "26" };
    answers.Augen = { choice: "grün", extra: "" };
    expect(answerText(answers.Herkunft)).toBe(
      "nordeuropäisch wirkend, skandinavisch",
    );
    expect(answerTexts(answers).Haar).toBe("");
    expect(looksLines(answers)).toBe(
      [
        "- **Herkunft:** nordeuropäisch wirkend, skandinavisch",
        "- **Alter:** 26",
        "- **Größe:** –",
        "- **Körperbau:** –",
        "- **Proportionen:** –",
        "- **Gesicht:** –",
        "- **Haar:** –",
        "- **Augen:** grün",
        "- **Haut:** –",
        "- **Besondere Merkmale:** –",
      ].join("\n"),
    );
  });

  it("reads the lines of Aussehen back as the picked answers", () => {
    const body =
      "Fährfrau.\n\n### Aussehen\n\n- **Herkunft:** Nordeuropa, skandinavisch\n" +
      "- **Alter:** 26\n- **Größe:** –\n- **Augen:** grün\n- **Haar:** kupferrot\n" +
      "\n### Wesen\n\n- **Haut:** dunkel";
    const answers = answersFrom(body);
    expect(answers.Herkunft).toEqual({
      choice: "Nordeuropa, skandinavisch",
      extra: "",
    });
    expect(answers.Alter).toEqual({ choice: null, extra: "26" });
    expect(answers.Größe).toEqual({ choice: null, extra: "" });
    expect(answers.Augen).toEqual({ choice: "grün", extra: "" });
    expect(answers.Haar).toEqual({ choice: "kupferrot", extra: "" });
    expect(answers.Haut).toEqual({ choice: null, extra: "" });
    expect(answersFrom("## Aussehen\n\nGroß und hager.")).toEqual(
      emptyAnswers(),
    );
    expect(answersFrom("Ohne.")).toEqual(emptyAnswers());
  });

  it("takes only adults, as the server does", () => {
    for (const age of ["18", " 26 ", "340"]) {
      expect(adultAge(age)).toBe(true);
    }
    for (const age of ["", "17", "1000", "26 Jahre", "-20", "zwanzig"]) {
      expect(adultAge(age)).toBe(false);
    }
  });

  it("recognizes the asked form; anything else counts as a refusal", () => {
    expect(looksLikeDescription(" a 26-year-old adult woman, red hair")).toBe(
      true,
    );
    expect(looksLikeDescription("An 80-year-old adult man")).toBe(true);
    expect(looksLikeDescription("I can't help with that.")).toBe(false);
    expect(looksLikeDescription("a 26-year-old woman")).toBe(false);
  });
});

describe("the suggestions of the model (step 11.5, ADR-124)", () => {
  it("reads one line per question, with the mark of the entry", () => {
    const found = parseSuggestions(
      [
        "Herkunft: nordeuropäisch wirkend | keltisch wirkend | slawisch wirkend",
        "Alter: 34 | 42 | 51",
        "Haar: kupferrot, glatt [Eintrag] | hellrot | dunkelblond",
        "Besondere Merkmale: Narben an den Handgelenken [eintrag]",
      ].join("\n"),
    );
    expect(found.Herkunft?.map((item) => item.text)).toEqual([
      "nordeuropäisch wirkend",
      "keltisch wirkend",
      "slawisch wirkend",
    ]);
    expect(found.Alter?.map((item) => item.text)).toEqual(["34", "42", "51"]);
    expect(found.Haar).toEqual([
      { text: "kupferrot, glatt", fromEntry: true },
      { text: "hellrot", fromEntry: false },
      { text: "dunkelblond", fromEntry: false },
    ]);
    expect(found["Besondere Merkmale"]).toEqual([
      { text: "Narben an den Handgelenken", fromEntry: true },
    ]);
    expect(found.Größe).toBeUndefined();
  });

  it("tolerates bullets and bold, and drops what it cannot use", () => {
    const found = parseSuggestions(
      [
        "- **Herkunft:** a | | b | c | d",
        "Alter: 17 | zwanzig | 40 | 41 | 42 | 43",
        "Kleidung: Mantel | Hut",
        "Haar: erstes | zweites",
        "Haar: doppelt | wird ignoriert",
        "Größe:",
        "Gesicht: |  | ",
        "Eine Zeile ohne Doppelpunkt",
      ].join("\n"),
    );
    expect(found.Herkunft?.map((item) => item.text)).toEqual(["a", "b", "c"]);
    expect(found.Alter?.map((item) => item.text)).toEqual(["40", "41", "42"]);
    expect(found.Haar?.map((item) => item.text)).toEqual(["erstes", "zweites"]);
    expect(Object.keys(found).sort()).toEqual(["Alter", "Haar", "Herkunft"]);
  });

  it("gives nothing for a reply that is not in the asked form", () => {
    expect(parseSuggestions("")).toEqual({});
    expect(parseSuggestions("I can't help with that.")).toEqual({});
    expect(parseSuggestions("Hinweis: nichts dazu")).toEqual({});
  });

  it("lists the line in the entry, the pick and the suggestions, each text once", () => {
    const chips = chipsFor("kupferrot", "hellrot", [
      { text: "Kupferrot", fromEntry: false },
      { text: "hellrot", fromEntry: true },
      { text: "schwarz", fromEntry: false },
    ]);
    expect(chips).toEqual([
      { text: "kupferrot", fromEntry: false, own: true },
      { text: "hellrot", fromEntry: false, own: false },
      { text: "schwarz", fromEntry: false, own: false },
    ]);
    expect(chipsFor(null, null, [])).toEqual([]);
    expect(chipsFor("", "", [{ text: "grau", fromEntry: true }])).toEqual([
      { text: "grau", fromEntry: true, own: false },
    ]);
  });
});
