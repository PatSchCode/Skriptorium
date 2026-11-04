"""Request that fits a guest into the world of a story (step 9.13, ADR-102).

The world builder reads the guest's entry from its home world, the description, rules and entry
names of the story's world and, if there is one, the relation written so far and a wish of the
author. It proposes how the guest fits in: how it came there or where it comes from there, whom
it knows, what it has with it and its role. Nothing is stored; the author takes the text over
into the guest's relation and saves it.
"""

from typing import Final

from skriptorium.canon import CanonService, NotFound
from skriptorium.context.parts import (
    MAX_BUDGET,
    BuiltContext,
    Part,
    check_budget,
    fitted,
    in_category_order,
    render,
)
from skriptorium.context.worldbuilder import entry_index
from skriptorium.manuscript import ManuscriptService

_FRAME: Final = (
    "Du hilfst einem Autor, eine Figur oder einen Eintrag aus einer anderen erzählten Welt in "
    "die Welt seiner Geschichte einzupassen. Du bekommst den Kanon-Eintrag aus der Heimatwelt, "
    "die Beschreibung, die Regeln und die Namen der Einträge der neuen Welt. Schlage vor, wie "
    "der Gast in die neue Welt passt: wie er dorthin kam oder woher er dort stammt, wen er dort "
    "kennt (Einträge der neuen Welt mit @Name), was er bei sich hat und welche Rolle er dort "
    "spielt. Ändere nichts an Wesen, Aussehen und Fähigkeiten; erfinde nur, was für den Bezug "
    "zur neuen Welt nötig ist, und widersprich weder der Weltbeschreibung noch den Regeln. "
    "Schreibe auf Deutsch, als Fließtext ohne Überschrift und ohne Einleitung, höchstens etwa "
    "150 Wörter, nur den Text, den der Autor übernehmen kann."
)


def build_guest_fit(
    canon: CanonService,
    manuscripts: ManuscriptService,
    world_id: str,
    story_id: str,
    guest_world: str,
    entry_id: str,
    wish: str = "",
    budget: int = MAX_BUDGET,
) -> BuiltContext:
    """Request for a proposal of the guest's relation to the world of the story.

    Raises:
        NotFound: The world, the story, the guest link or the guest's entry does not exist.
        InvalidInput: Budget outside 1-30,000.
        ContextTooLarge: Frame, world and entry do not fit the budget.
    """
    check_budget(budget)
    world = canon.get_world(world_id)
    story = manuscripts.get_story(world_id, story_id)
    link = next(
        (g for g in story.guest_links if (g.world, g.entry) == (guest_world, entry_id)), None
    )
    if link is None:
        raise NotFound(f"{guest_world}/{entry_id}")
    entry = canon.get_entry(guest_world, entry_id)
    home = canon.get_world(guest_world).name
    entries = canon.list_entries(world_id)
    rules = [
        Part("regel", rule.name, render(rule))
        for rule in in_category_order(entries)
        if rule.category == "regel"
    ]
    system = [
        Part("rahmen", "Rahmen", _FRAME),
        Part("welt", world.name, f"# Neue Welt: {world.name}\n\n{world.description}".strip()),
        Part("eintraege", "Einträge der Welt", entry_index(entries)),
        *rules,
    ]
    user = [Part("gast", entry.name, render(entry, home))]
    if link.relation:
        user.append(Part("anweisung", "Bisheriger Weltbezug", f"# Bisher\n\n{link.relation}"))
    if wish.strip():
        user.append(Part("anweisung", "Wunsch", f"# Wunsch des Autors\n\n{wish.strip()}"))
    return fitted(system, user, budget)
