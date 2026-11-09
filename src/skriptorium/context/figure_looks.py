"""Requests of the figure assistant (step 11.5, ADR-123, ADR-124).

Two requests, both without storing anything:

* **Image description** (ADR-123): the author answers fixed questions about a figure's looks
  (:data:`~skriptorium.canon.LOOKS_LABELS`); the interface writes the German lines of "Aussehen"
  from them itself. The model only turns the answers (and the entry for what they leave open)
  into one English paragraph for image models, in the form that carried in the image tests of
  2026-11-07 (``docs/research/bildanbieter.md``): the age first, short visible phrases, no name,
  clothing, pose, place or restraints; those belong to the image, not to the figure. Probe:
  ``spikes/figuren-assistent-11.5/README.md``.
* **Suggestions** (ADR-124): most entries tell little about the looks, so the model proposes
  three answers per question from the entry and the description of the world; the author picks.
  The reply is one line per question, ``Frage: a | b | c``; a suggestion taken from the entry
  ends in :data:`ENTRY_MARK`. The interface parses it (``ui/src/figureLooks.ts``).
"""

import re
from collections.abc import Mapping
from typing import Final

from skriptorium.canon import (
    IMAGE_DESCRIPTION,
    LOOKS_LABELS,
    CanonService,
    InvalidInput,
    drop_sections,
)
from skriptorium.context.parts import MAX_BUDGET, BuiltContext, Part, check_budget, fitted

AGE: Final = "Alter"
MIN_AGE: Final = 18
MAX_ANSWER_CHARS: Final = 300
# Suggestions per question and the mark of one taken from the entry (ADR-124); the interface
# parses the reply with the same values.
SUGGESTIONS_PER_QUESTION: Final = 3
ENTRY_MARK: Final = "[Eintrag]"

# Up to three digits: long-lived beings are fine, only adults are asked for (ADR-123).
_AGE_FORM: Final = re.compile(r"\d{1,3}")

_FRAME: Final = (
    "Du hilfst einem Autor, das Aussehen einer Figur aus seiner erzählten Welt für Bildmodelle "
    "festzuhalten. Alle Figuren sind erwachsen. Du bekommst seine Antworten auf feste Fragen "
    "und den Kanon-Eintrag der Figur. Die Antworten gelten; aus dem Eintrag nimmst du nur, was "
    "über das Äußere dort steht und die Antworten offenlassen. Erfinde keine Merkmale dazu.\n\n"
    "Schreibe nur die Bildbeschreibung, ohne Überschrift, ohne Einleitung und ohne Nachsatz: "
    "Englisch, ein einziger Absatz, höchstens 70 Wörter. Beginne genau mit "
    "„a <Alter>-year-old adult“, gefolgt von Herkunft und Geschlecht, dann „with mature adult "
    "facial features“. Danach Haut, Gesicht, Haar, Augen, besondere Merkmale und die Größe als "
    "„about … cm tall“ bzw. als Wort; Körperbau und Proportionen zuletzt in einer eigenen "
    "Wendung. Kurze, sichtbare Wendungen mit Kommas; keine Namen, keine Gefühle, keine "
    "Vorgeschichte, keine Kleidung, keine Pose, keine Umgebung und keine Fesseln, Ketten oder "
    "Halsbänder; die setzt der Autor beim Bild selbst dazu."
)


_SUGGEST_FRAME: Final = (
    "Du hilfst einem Autor, das Aussehen einer Figur aus seiner erzählten Welt für Bildmodelle "
    "festzulegen. Alle Figuren sind erwachsen. Du bekommst die Beschreibung der Welt, den "
    "Kanon-Eintrag der Figur und die Angaben, die der Autor schon gemacht hat.\n\n"
    f"Mache zu jeder der {len(LOOKS_LABELS)} Fragen genau {SUGGESTIONS_PER_QUESTION} Vorschläge, "
    "die zur Figur und zur Welt passen und sich deutlich voneinander unterscheiden. Lies zuerst "
    "den Eintrag: Alles, was er über das Äußere sagt (auch beiläufig, etwa Narben, Haarfarbe "
    "oder Wuchs), ist Kanon. Es steht als erster Vorschlag bei der passenden Frage, am Ende "
    f"gekennzeichnet mit „ {ENTRY_MARK}“; die beiden anderen weichen davon ab. Kein Vorschlag "
    "darf dem Eintrag widersprechen. Steht im Eintrag nichts zur Frage, denkst du dir alle drei "
    "passend zur Figur und zur Welt aus. Steht zu einer Frage schon eine Angabe des Autors, sind "
    "die drei Vorschläge Abwandlungen davon.\n\n"
    "„Herkunft“ beschreibt, wie die Figur aussieht („nordeuropäisch wirkend“), und nennt keinen "
    "Namen aus der Welt (kein Volk, Land oder Ort): Bildmodelle kennen die Welt nicht. „Alter“ "
    f"sind {SUGGESTIONS_PER_QUESTION} ganze Zahlen ab {MIN_AGE}, sonst nichts. „Größe“ nennt ein "
    "Wort und die Zentimeter. Alle anderen Antworten sind kurze, sichtbare Wendungen auf Deutsch, "
    "durch Kommas getrennt. Keine Namen, keine Gefühle, keine Vorgeschichte, keine Kleidung, "
    "keine Pose, keine Umgebung und keine Fesseln, Ketten oder Halsbänder.\n\n"
    "Antworte genau in dieser Form, eine Zeile je Frage, die Vorschläge durch „ | “ getrennt, und "
    "mit nichts davor oder danach:\n\n" + "\n".join(f"{label}: … | … | …" for label in LOOKS_LABELS)
)


def _clean(answers: Mapping[str, str]) -> dict[str, str]:
    """The answers in the order of the questions, trimmed; unknown or too long ones refused."""
    unknown = sorted(set(answers) - set(LOOKS_LABELS))
    if unknown:
        raise InvalidInput(f"Unbekannte Frage zum Aussehen: {', '.join(unknown)}")
    checked = {label: " ".join(answers.get(label, "").split()) for label in LOOKS_LABELS}
    too_long = [label for label, text in checked.items() if len(text) > MAX_ANSWER_CHARS]
    if too_long:
        raise InvalidInput(
            f"Antwort zu lang (höchstens {MAX_ANSWER_CHARS} Zeichen): {', '.join(too_long)}"
        )
    return checked


def check_answers(answers: Mapping[str, str]) -> dict[str, str]:
    """The answers in the order of the questions, trimmed; open questions as empty text.

    Raises:
        InvalidInput: An unknown question, an answer over 300 characters, or an age that is
            missing, not a whole number or under 18 (ADR-123: only adults).
    """
    checked = _clean(answers)
    age = checked[AGE]
    if _AGE_FORM.fullmatch(age) is None or int(age) < MIN_AGE:
        raise InvalidInput(f"Das Alter muss eine ganze Zahl ab {MIN_AGE} sein.")
    return checked


def build_figure_looks(
    canon: CanonService,
    world_id: str,
    entry_id: str,
    answers: Mapping[str, str],
    budget: int = MAX_BUDGET,
) -> BuiltContext:
    """Request for the English image description of a figure from the author's answers.

    Raises:
        NotFound: The world or the entry does not exist.
        InvalidInput: Budget outside 1-30,000, the entry is not a figure, or the answers do not
            pass :func:`check_answers`.
        ContextTooLarge: The entry does not fit the budget.
    """
    check_budget(budget)
    entry = canon.get_entry(world_id, entry_id)
    if entry.category != "figur":
        raise InvalidInput("Der Figuren-Assistent ist nur für Figuren da.")
    checked = check_answers(answers)
    lines = "\n".join(f"- {label}: {text or '(keine Angabe)'}" for label, text in checked.items())
    body = drop_sections(entry.body, IMAGE_DESCRIPTION).strip()
    return fitted(
        [Part("rahmen", "Rahmen", _FRAME)],
        [
            Part("anweisung", "Antworten", f"Antworten des Autors:\n\n{lines}"),
            Part("eintraege", "Eintrag", f"Kanon-Eintrag:\n\n# {entry.name}\n\n{body}".strip()),
        ],
        budget,
    )


def build_looks_suggestions(
    canon: CanonService,
    world_id: str,
    entry_id: str,
    answers: Mapping[str, str],
    budget: int = MAX_BUDGET,
) -> BuiltContext:
    """Request for three suggestions per question about a figure's looks (ADR-124).

    ``answers`` are what the author has so far (the lines already in "Aussehen" or typed in the
    window); they may be partial or empty and need no age: the suggestions are variations of
    them. The entry comes without its "Bildbeschreibung"; the world's description comes along.

    Raises:
        NotFound: The world or the entry does not exist.
        InvalidInput: Budget outside 1-30,000, the entry is not a figure, or an answer is for an
            unknown question or too long.
        ContextTooLarge: World description and entry do not fit the budget.
    """
    check_budget(budget)
    world = canon.get_world(world_id)
    entry = canon.get_entry(world_id, entry_id)
    if entry.category != "figur":
        raise InvalidInput("Der Figuren-Assistent ist nur für Figuren da.")
    checked = _clean(answers)
    lines = "\n".join(
        f"- {label}: {text or '(noch keine Angabe)'}" for label, text in checked.items()
    )
    body = drop_sections(entry.body, IMAGE_DESCRIPTION).strip()
    return fitted(
        [Part("rahmen", "Rahmen", _SUGGEST_FRAME)],
        [
            Part("welt", world.name, f"# Welt: {world.name}\n\n{world.description}".strip()),
            Part("eintraege", "Eintrag", f"Kanon-Eintrag der Figur:\n\n# {entry.name}\n\n{body}"),
            Part("anweisung", "Angaben", f"Angaben des Autors bisher:\n\n{lines}"),
        ],
        budget,
    )
