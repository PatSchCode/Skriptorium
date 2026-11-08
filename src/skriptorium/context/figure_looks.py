"""Request of the figure assistant: an English image description from the author's answers.

Step 11.5 (ADR-123). The author answers fixed questions about a figure's looks
(:data:`~skriptorium.canon.LOOKS_LABELS`); the interface writes the German lines of "Aussehen"
from them itself. The model only turns the answers (and the entry for what they leave open)
into one English paragraph for image models, in the form that carried in the image tests of
2026-11-07 (``docs/research/bildanbieter.md``): the age first, short visible phrases, no name,
clothing, pose, place or restraints; those belong to the image, not to the figure. Probe:
``spikes/figuren-assistent-11.5/README.md``. Nothing is stored here.
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


def check_answers(answers: Mapping[str, str]) -> dict[str, str]:
    """The answers in the order of the questions, trimmed; open questions as empty text.

    Raises:
        InvalidInput: An unknown question, an answer over 300 characters, or an age that is
            missing, not a whole number or under 18 (ADR-123: only adults).
    """
    unknown = sorted(set(answers) - set(LOOKS_LABELS))
    if unknown:
        raise InvalidInput(f"Unbekannte Frage zum Aussehen: {', '.join(unknown)}")
    checked = {label: " ".join(answers.get(label, "").split()) for label in LOOKS_LABELS}
    too_long = [label for label, text in checked.items() if len(text) > MAX_ANSWER_CHARS]
    if too_long:
        raise InvalidInput(
            f"Antwort zu lang (höchstens {MAX_ANSWER_CHARS} Zeichen): {', '.join(too_long)}"
        )
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
