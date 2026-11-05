"""Request that takes the looks of a figure, a place or an item out of its canon entry.

Step 7.16 (ADR-078) for figures, step 10.3 (ADR-108) for places and items. The model reads the
entry once and writes only what can be seen, with its own frame per category: a figure's face,
hair, build and clothing; a place's buildings, material, light and ground; an item's form,
material and decoration. Everything else stays out. It invents nothing; without any statement
about looks it answers with the fixed marker :data:`NO_APPEARANCE`. A place goes without its
section "Lage"; an image gets that on top of the looks anyway (ADR-094). Nothing is stored; the
author takes the text over as the section "Aussehen".
"""

from typing import Final

from skriptorium.canon import LOCATION, CanonService, Category, InvalidInput, take_section
from skriptorium.context.parts import MAX_BUDGET, BuiltContext, Part, check_budget, fitted

NO_APPEARANCE: Final = "KEIN AUSSEHEN"

_RULES: Final = (
    "Übernimm nur, was im Eintrag steht, und erfinde nichts dazu. Schreibe auf Deutsch in "
    "ganzen Sätzen, als Fließtext ohne Überschrift, ohne Einleitung, höchstens etwa 120 Wörter. "
    f"Steht im Eintrag nichts über das Äußere, antworte genau: {NO_APPEARANCE}"
)

_FRAMES: Final[dict[Category, str]] = {
    "figur": (
        "Du liest den Kanon-Eintrag einer Figur aus einer erzählten Welt und schreibst nur ihr "
        "äußeres Erscheinungsbild heraus: Gesicht, Haare, Augen, Statur, Größe, sichtbares "
        "Alter, Kleidung, typische Haltung und sichtbare Merkmale wie Narben, Tätowierungen oder "
        "Schmuck. Lass Wesen, Gedanken, Gewohnheiten, Fähigkeiten, Vorgeschichte und "
        "Beziehungen weg. "
    ),
    "ort": (
        "Du liest den Kanon-Eintrag eines Ortes aus einer erzählten Welt und schreibst nur "
        "heraus, wie er aussieht: Bauweise, Größe, Material, Farben, Licht, Gelände und "
        "Pflanzen, sichtbare Spuren von Alter oder Zerstörung. Lass Lage und Weg dorthin, "
        "Bewohner, Geschichte, Bedeutung und Ereignisse weg. "
    ),
    "gegenstand": (
        "Du liest den Kanon-Eintrag eines Gegenstands aus einer erzählten Welt und schreibst "
        "nur heraus, wie er aussieht: Form, Größe, Material, Farbe, Oberfläche, Verzierungen, "
        "Inschriften und Zustand. Lass Zweck, Verwendung, Wirkung, Herkunft und Besitzer weg. "
    ),
}


def build_appearance(
    canon: CanonService, world_id: str, entry_id: str, budget: int = MAX_BUDGET
) -> BuiltContext:
    """Request to write out the looks of a figure, a place or an item from its entry.

    Raises:
        NotFound: The world or the entry does not exist.
        InvalidInput: Budget outside 1-30,000, or the entry is neither a figure, a place nor an
            item (ADR-083, ADR-108: the interface offers it only for those; the server checks
            it too).
        ContextTooLarge: The entry does not fit the budget.
    """
    check_budget(budget)
    entry = canon.get_entry(world_id, entry_id)
    frame = _FRAMES.get(entry.category)
    if frame is None:
        raise InvalidInput(
            "Das Aussehen lässt sich nur bei Figuren, Orten und Gegenständen herauslösen."
        )
    body = entry.body
    if entry.category == "ort":
        _, body = take_section(body, LOCATION)
    text = f"# {entry.name}\n\n{body.strip()}".strip()
    return fitted(
        [Part("rahmen", "Rahmen", frame + _RULES)],
        [Part("eintraege", "Eintrag", text)],
        budget,
    )
