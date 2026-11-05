"""A guest with a relation to the world of the story, and the proposal to fit it in
(step 9.13, ADR-102)."""

from pathlib import Path

import pytest

from skriptorium.canon import CanonService, NotFound
from skriptorium.context import ContextBuilder
from skriptorium.context.parts import Known, render, render_known
from skriptorium.manuscript import ManuscriptService
from skriptorium.storage import DocumentStore

WORLD = "die-salzmark"
HOME = "nebelreich"
STORY = "am-ufer"
BODY = (
    "Herrscher über den Nebel.\n\n"
    "## Wesen\n\nKühl.\n\n"
    "## Im Nebelreich\n\nThront im Reifpalast, Vater von Ysa.\n"
)

Services = tuple[CanonService, ManuscriptService]


@pytest.fixture
def services(tmp_path: Path) -> Services:
    store = DocumentStore(tmp_path / "data")
    canon = CanonService(store)
    manuscripts = ManuscriptService(store)
    canon.create_world("Die Salzmark", "Sieben Inseln nach der Flut.")
    canon.create_world("Nebelreich", "Eine Welt aus Nebel.")
    canon.create_entry(WORLD, "figur", "Ilka Varn", body="Fischerin, 19.")
    canon.create_entry(WORLD, "regel", "Salzgesetz", body="Salz bricht jeden Bann.")
    canon.create_entry(HOME, "figur", "Nebelkönig", body=BODY)
    canon.create_entry(HOME, "regel", "Nebelgesetz", body="Nebel lügt nie.")
    manuscripts.create_story(WORLD, "Am Ufer", "kurzgeschichte")
    manuscripts.save_chapter(WORLD, STORY, 1, text="Nebel.")
    manuscripts.add_guest_link(WORLD, STORY, HOME, "nebelkoenig")
    return canon, manuscripts


def system_of(services: Services) -> str:
    built = ContextBuilder(*services).build(WORLD, STORY, 1, "Weiter.", ["nebelkoenig"])
    return built.messages[0].content


def test_without_relation_the_guest_stays_as_it_was(services: Services) -> None:
    canon, _ = services
    entry = canon.get_entry(HOME, "nebelkoenig")
    expected = render(entry, "Nebelreich")

    assert render_known(Known(entry, "Nebelreich", "", "Die Salzmark")) == expected
    assert render_known(Known(entry, "Nebelreich", "  \n", "Die Salzmark")) == expected
    assert expected in system_of(services)
    assert "In dieser Welt" not in system_of(services)


def test_with_relation_it_stands_below_and_the_home_world_is_left_out(
    services: Services,
) -> None:
    _, manuscripts = services
    manuscripts.set_guest_relation(
        WORLD, STORY, HOME, "nebelkoenig", "Strandete nach der Flut.\n\n## Besitz\n\nEine Krone."
    )

    system = system_of(services)

    assert "## Nebelkönig (Figur, Gast aus der Welt „Nebelreich“)" in system
    assert "### Wesen\n\nKühl." in system
    assert "Reifpalast" not in system
    assert "Im Nebelreich" not in system
    assert (
        "### In dieser Welt („Die Salzmark“)\n\nStrandete nach der Flut.\n\n#### Besitz\n\n"
        "Eine Krone."
    ) in system


def test_an_own_entry_never_gets_a_relation(services: Services) -> None:
    canon, _ = services
    entry = canon.get_entry(WORLD, "ilka-varn")
    assert render(entry, None, "Gilt nicht.", "Die Salzmark") == render(entry)


def test_the_fit_request_holds_guest_world_rules_relation_and_wish(services: Services) -> None:
    _, manuscripts = services
    builder = ContextBuilder(*services)
    plain = builder.build_guest_fit(WORLD, STORY, HOME, "nebelkoenig")
    system, user = plain.messages

    assert "in die Welt seiner Geschichte einzupassen" in system.content
    assert "# Neue Welt: Die Salzmark\n\nSieben Inseln nach der Flut." in system.content
    assert "- Ilka Varn (Figur)" in system.content
    assert "Salz bricht jeden Bann." in system.content
    assert "Nebel lügt nie." not in system.content
    assert "Eine Welt aus Nebel." not in system.content
    assert user.content.startswith("## Nebelkönig (Figur, Gast aus der Welt „Nebelreich“)")
    assert "Reifpalast" in user.content
    assert "# Bisher" not in user.content
    assert "# Wunsch" not in user.content

    manuscripts.set_guest_relation(WORLD, STORY, HOME, "nebelkoenig", "Strandete.")
    _, user = builder.build_guest_fit(WORLD, STORY, HOME, "nebelkoenig", " fremd bleiben ").messages
    assert "# Bisher\n\nStrandete." in user.content
    assert user.content.endswith("# Wunsch des Autors\n\nfremd bleiben")


def test_unknown_links_and_entries(services: Services) -> None:
    canon, _ = services
    builder = ContextBuilder(*services)
    with pytest.raises(NotFound):
        builder.build_guest_fit(WORLD, STORY, HOME, "nebelgesetz")
    with pytest.raises(NotFound):
        builder.build_guest_fit(WORLD, "fehlt", HOME, "nebelkoenig")
    canon.delete_entry(HOME, "nebelkoenig")
    with pytest.raises(NotFound):
        builder.build_guest_fit(WORLD, STORY, HOME, "nebelkoenig")
