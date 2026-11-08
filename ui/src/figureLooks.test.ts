import { describe, expect, it } from "vitest";
import {
  adultAge,
  answersFrom,
  answerText,
  answerTexts,
  emptyAnswers,
  looksLikeDescription,
  looksLines,
} from "./figureLooks";

describe("the figure assistant's answers and lines (step 11.5, ADR-123)", () => {
  it("joins choice and addition and writes every line, open ones as –", () => {
    const answers = emptyAnswers();
    answers.Herkunft = { choice: "Nordeuropa", extra: " skandinavisch " };
    answers.Alter = { choice: null, extra: "26" };
    answers.Augen = { choice: "grün", extra: "" };
    expect(answerText(answers.Herkunft)).toBe("Nordeuropa, skandinavisch");
    expect(answerTexts(answers).Haar).toBe("");
    expect(looksLines(answers)).toBe(
      [
        "- **Herkunft:** Nordeuropa, skandinavisch",
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

  it("reads the lines of Aussehen back into answers, splitting off a choice", () => {
    const body =
      "Fährfrau.\n\n### Aussehen\n\n- **Herkunft:** Nordeuropa, skandinavisch\n" +
      "- **Alter:** 26\n- **Größe:** –\n- **Augen:** grün\n- **Haar:** kupferrot\n" +
      "- **Gesicht:** ovalförmig\n\n### Wesen\n\n- **Haut:** dunkel";
    const answers = answersFrom(body);
    expect(answers.Herkunft).toEqual({
      choice: "Nordeuropa",
      extra: "skandinavisch",
    });
    expect(answers.Alter).toEqual({ choice: null, extra: "26" });
    expect(answers.Größe).toEqual({ choice: null, extra: "" });
    expect(answers.Augen).toEqual({ choice: "grün", extra: "" });
    expect(answers.Haar).toEqual({ choice: null, extra: "kupferrot" });
    expect(answers.Gesicht).toEqual({ choice: null, extra: "ovalförmig" });
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
