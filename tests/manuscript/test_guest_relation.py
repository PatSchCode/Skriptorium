"""The relation of a guest to the world of the story (step 9.13, ADR-102)."""

from pathlib import Path

import pytest

from skriptorium.manuscript import RELATION_MAX, GuestLink, ManuscriptService
from skriptorium.storage import DocumentStore, InvalidInput, NotFound

W = "salzmark"
STORY = "worlds/salzmark/stories/begegnung/story.md"


@pytest.fixture
def root(tmp_path: Path) -> Path:
    return tmp_path / "data"


@pytest.fixture
def ms(root: Path) -> ManuscriptService:
    service = ManuscriptService(DocumentStore(root))
    service.create_story(W, "Begegnung", "kurzgeschichte")
    service.add_guest_link(W, "begegnung", "eisenmeer", "kael")
    service.add_guest_link(W, "begegnung", "nebelreich", "ragna")
    return service


def test_set_change_and_remove(ms: ManuscriptService, root: Path) -> None:
    before = (root / STORY).read_text(encoding="utf-8")
    assert "weltbezug" not in before

    story = ms.set_guest_relation(W, "begegnung", "eisenmeer", "kael", "  Kam mit dem Salz.\n")

    assert story.guest_links[0].relation == "Kam mit dem Salz."
    assert story.guest_links[1].relation == ""
    assert ms.get_story(W, "begegnung").guest_links == story.guest_links
    text = (root / STORY).read_text(encoding="utf-8")
    assert text.count("weltbezug") == 1
    assert "weltbezug: Kam mit dem Salz." in text
    # Equality is the pair: the link is still found, removed and refused twice.
    assert GuestLink("eisenmeer", "kael") in story.guest_links

    cleared = ms.set_guest_relation(W, "begegnung", "eisenmeer", "kael", "   ")

    assert cleared.guest_links[0].relation == ""
    assert (root / STORY).read_text(encoding="utf-8") == before


def test_relation_survives_other_changes(ms: ManuscriptService) -> None:
    ms.set_guest_relation(W, "begegnung", "nebelreich", "ragna", "Lebt im Turm.")

    ms.add_guest_link(W, "begegnung", "eisenmeer", "ysa")
    ms.update_story(W, "begegnung", perspective="Ich")
    story = ms.remove_guest_link(W, "begegnung", "eisenmeer", "kael")

    assert [(g.entry, g.relation) for g in story.guest_links] == [
        ("ragna", "Lebt im Turm."),
        ("ysa", ""),
    ]


def test_unknown_link_and_too_long_text(ms: ManuscriptService) -> None:
    with pytest.raises(NotFound):
        ms.set_guest_relation(W, "begegnung", "eisenmeer", "niemand", "x")
    with pytest.raises(NotFound):
        ms.set_guest_relation(W, "fehlt", "eisenmeer", "kael", "x")
    with pytest.raises(InvalidInput):
        ms.set_guest_relation(W, "begegnung", "eisenmeer", "kael", "x" * (RELATION_MAX + 1))
    assert ms.set_guest_relation(W, "begegnung", "eisenmeer", "kael", "x" * RELATION_MAX)


@pytest.mark.parametrize("value", ["3", "[a]", "{a: b}"])
def test_a_relation_that_is_no_text_is_refused(
    ms: ManuscriptService, root: Path, value: str
) -> None:
    path = root / STORY
    path.write_text(
        path.read_text(encoding="utf-8").replace(
            "eintrag: kael", f"eintrag: kael\n  weltbezug: {value}", 1
        ),
        encoding="utf-8",
    )
    with pytest.raises(InvalidInput):
        ms.get_story(W, "begegnung")


def test_an_empty_relation_written_by_hand_counts_as_none(
    ms: ManuscriptService, root: Path
) -> None:
    path = root / STORY
    path.write_text(
        path.read_text(encoding="utf-8").replace("eintrag: kael", "eintrag: kael\n  weltbezug:", 1),
        encoding="utf-8",
    )
    assert ms.get_story(W, "begegnung").guest_links[0].relation == ""
