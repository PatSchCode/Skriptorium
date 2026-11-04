"""Archiving and deleting stories, deleting chapters (step 9.9, ADR-098, FR-036)."""

from datetime import UTC, datetime
from pathlib import Path

import pytest

from skriptorium.manuscript import (
    GuestLink,
    InstructionNote,
    InvalidInput,
    ManuscriptService,
    NotFound,
    StoryContents,
    StoryFact,
)
from skriptorium.storage import DocumentStore
from tests.image_samples import png

W = "salzmark"
AT = datetime(2026, 11, 4, 9, 0, tzinfo=UTC)


@pytest.fixture
def root(tmp_path: Path) -> Path:
    return tmp_path / "data"


@pytest.fixture
def store(root: Path) -> DocumentStore:
    return DocumentStore(root)


@pytest.fixture
def ms(store: DocumentStore) -> ManuscriptService:
    return ManuscriptService(store)


def _novel(ms: ManuscriptService, chapters: int) -> str:
    story = ms.create_story(W, "Die Überfahrt", "roman").id
    for number in range(1, chapters + 1):
        ms.save_chapter(W, story, number, title=f"Teil {number}", text=f"Text {number}.")
        ms.set_chapter_summary(W, story, number, f"Kurz {number}.", "geprüft")
    return story


def _note(text: str) -> InstructionNote:
    return InstructionNote(AT, f"Anweisung zu {text}", text, "x/m")


# --- archive -----------------------------------------------------------------------------


def test_archive_and_restore_leave_the_file_as_it_was(ms: ManuscriptService, root: Path) -> None:
    story = ms.create_story(W, "Am Ufer", "kurzgeschichte")
    file = root / "worlds" / W / "stories" / story.id / "story.md"
    before = file.read_bytes()
    assert ms.archive_story(W, story.id).archived is True
    assert [s.archived for s in ms.list_stories(W)] == [True]
    # Changing an archived story keeps it in the archive.
    assert ms.set_story_summary(W, story.id, "Neu.").archived is True
    ms.set_story_summary(W, story.id, "")
    assert ms.restore_story(W, story.id) == story
    assert file.read_bytes() == before


def test_archived_header_must_be_true_or_false(ms: ManuscriptService, root: Path) -> None:
    story = ms.create_story(W, "Am Ufer", "kurzgeschichte")
    file = root / "worlds" / W / "stories" / story.id / "story.md"
    file.write_text(
        file.read_text(encoding="utf-8").replace("---\n", "---\narchiviert: 1\n", 1),
        encoding="utf-8",
    )
    with pytest.raises(InvalidInput):
        ms.get_story(W, story.id)


def test_archive_needs_an_existing_story(ms: ManuscriptService) -> None:
    with pytest.raises(NotFound):
        ms.archive_story(W, "gibt-es-nicht")
    with pytest.raises(NotFound):
        ms.restore_story(W, "gibt-es-nicht")


# --- deleting a story for good -----------------------------------------------------------


def test_contents_name_chapters_facts_and_cover(ms: ManuscriptService) -> None:
    story = _novel(ms, 3)
    assert ms.story_contents(W, story) == StoryContents(chapters=3, facts=0, cover=False)
    ms.add_fact(W, story, "kael", "Kael fürchtet das Wasser.")
    ms.set_story_cover(W, story, png())
    assert ms.story_contents(W, story) == StoryContents(chapters=3, facts=1, cover=True)


def test_delete_only_an_archived_story_with_its_exact_title(ms: ManuscriptService) -> None:
    story = _novel(ms, 1)
    with pytest.raises(InvalidInput, match="archivierte"):
        ms.delete_story(W, story, "Die Überfahrt")
    ms.archive_story(W, story)
    for wrong in ("die überfahrt", " Die Überfahrt", "Am Ufer"):
        with pytest.raises(InvalidInput, match="Titel"):
            ms.delete_story(W, story, wrong)
    assert ms.get_story(W, story).archived is True
    with pytest.raises(NotFound):
        ms.delete_story(W, "gibt-es-nicht", "x")


def test_delete_removes_the_folder_and_its_index_rows(
    ms: ManuscriptService, store: DocumentStore, root: Path
) -> None:
    story = _novel(ms, 2)
    ms.create_story(W, "Am Ufer", "kurzgeschichte")
    ms.add_fact(W, story, "kael", "Kael fürchtet das Wasser.")
    ms.add_instruction(W, story, 1, _note("Der Nebel hob sich."))
    ms.set_story_cover(W, story, png())
    store.write("system/verbrauch/2026-11.md", {"eintraege": []}, "")
    assert store.search(W, "text", "fulltext") != []
    ms.archive_story(W, story)

    ms.delete_story(W, story, "Die Überfahrt")

    assert not (root / "worlds" / W / "stories" / story).exists()
    assert [s.id for s in ms.list_stories(W)] == ["am-ufer"]
    assert store.search(W, "text", "fulltext") == []
    assert store.search(W, "die über") == []
    assert (root / "system" / "verbrauch" / "2026-11.md").is_file()


# --- deleting a chapter ------------------------------------------------------------------


def test_deleting_a_middle_chapter_moves_the_following_ones_up(
    ms: ManuscriptService, store: DocumentStore, root: Path
) -> None:
    story = _novel(ms, 4)
    for number in (1, 2, 3, 4):
        ms.add_instruction(W, story, number, _note(f"Verlauf {number}"))
    ms.complete_chapter(W, story, 3)
    folder = root / "worlds" / W / "stories" / story

    remaining = ms.delete_chapter(W, story, 2)

    assert [(c.number, c.title, c.text) for c in remaining] == [
        (1, "Teil 1", "Text 1."),
        (2, "Teil 3", "Text 3."),
        (3, "Teil 4", "Text 4."),
    ]
    assert remaining[1].status == "abgeschlossen"
    assert sorted(p.name for p in (folder / "chapters").iterdir()) == [
        "01-teil-1.md",
        "02-teil-3.md",
        "03-teil-4.md",
    ]
    assert sorted(p.name for p in (folder / "verlauf").iterdir()) == [
        "01.md",
        "02.md",
        "03.md",
    ]
    assert [n.text for n in ms.list_instructions(W, story, 2)] == ["Verlauf 3"]
    assert [n.text for n in ms.list_instructions(W, story, 3)] == ["Verlauf 4"]
    assert store.read(f"worlds/{W}/stories/{story}/verlauf/02.md").header["kapitel"] == 2
    chapters = f"worlds/{W}/stories/{story}/chapters"
    assert [hit.path for hit in store.search(W, "teil")] == [
        f"{chapters}/01-teil-1.md",
        f"{chapters}/02-teil-3.md",
        f"{chapters}/03-teil-4.md",
    ]
    with pytest.raises(NotFound):
        ms.get_chapter(W, story, 4)
    # The next new chapter takes the next free number again.
    assert ms.save_chapter(W, story, 4, title="Teil 5").number == 4


def test_deleting_a_chapter_marks_the_summaries_after_it_outdated(
    ms: ManuscriptService, root: Path
) -> None:
    """A chapter that moves up keeps its summary but as ``veraltet``; a missing one stays
    missing, the chapters before keep theirs (step 9.9, ADR-098)."""
    story = _novel(ms, 5)
    ms.set_chapter_summary(W, story, 3, "Kurz 3.", "erzeugt")
    ms.set_chapter_summary(W, story, 4, "", "fehlt")

    remaining = ms.delete_chapter(W, story, 2)

    assert [(c.number, c.summary, c.summary_status) for c in remaining] == [
        (1, "Kurz 1.", "geprüft"),
        (2, "Kurz 3.", "veraltet"),
        (3, "", "fehlt"),
        (4, "Kurz 5.", "veraltet"),
    ]
    # The value is written into the file and read back by a new service.
    again = ManuscriptService(DocumentStore(root))
    assert again.get_chapter(W, story, 2).summary_status == "veraltet"
    assert "kurzfassung_status: veraltet" in next(
        (root / "worlds" / W / "stories" / story / "chapters").glob("02-*.md")
    ).read_text(encoding="utf-8")
    # Moving up again leaves an outdated summary outdated.
    assert [c.summary_status for c in ms.delete_chapter(W, story, 1)] == [
        "veraltet",
        "fehlt",
        "veraltet",
    ]
    # Creating it again and checking it work as before.
    assert ms.set_chapter_summary(W, story, 1, "Neu 3.", "erzeugt").summary_status == "erzeugt"
    assert ms.set_chapter_summary(W, story, 1, "Neu 3.", "geprüft").summary_status == "geprüft"
    assert ms.set_chapter_summary(W, story, 3, "Kurz 5.", "veraltet").summary_status == "veraltet"


def test_deleting_chapters_without_history(ms: ManuscriptService) -> None:
    story = _novel(ms, 3)
    ms.add_instruction(W, story, 3, _note("Nur am letzten"))
    assert [c.title for c in ms.delete_chapter(W, story, 3)] == ["Teil 1", "Teil 2"]
    assert ms.list_instructions(W, story, 2) == []
    assert [c.title for c in ms.delete_chapter(W, story, 1)] == ["Teil 2"]
    assert ms.get_chapter(W, story, 1).summary == "Kurz 2."


def test_deleting_a_missing_chapter(ms: ManuscriptService) -> None:
    story = _novel(ms, 1)
    with pytest.raises(NotFound):
        ms.delete_chapter(W, story, 2)
    with pytest.raises(NotFound):
        ms.delete_chapter(W, "gibt-es-nicht", 1)


# --- guests of a world that is deleted ---------------------------------------------------


def test_remove_guest_world_takes_links_facts_and_led_characters(ms: ManuscriptService) -> None:
    story = ms.create_story(W, "Die Überfahrt", "roman").id
    for world, entry in (("glaskueste", "mira"), ("glaskueste", "kael"), ("nebelreich", "vale")):
        ms.add_guest_link(W, story, world, entry)
    facts = (("mira", "Mira lügt."), ("vale", "Vale schläft."), ("kael", "Kael rudert."))
    for entry, fact in facts:
        ms.add_fact(W, story, entry, fact)
    ms.update_story(W, story, controlled_characters=["mira", "vale", "kael"])

    changed = ms.remove_guest_world(W, story, "glaskueste", {"mira"})

    assert changed.guest_links == (GuestLink("nebelreich", "vale"),)
    assert changed.facts == (StoryFact("vale", "Vale schläft."), StoryFact("kael", "Kael rudert."))
    assert changed.controlled_characters == ("vale", "kael")
    assert changed.title == "Die Überfahrt"


def test_remove_guest_world_without_links_changes_nothing(
    ms: ManuscriptService, root: Path
) -> None:
    story = ms.create_story(W, "Am Ufer", "kurzgeschichte")
    file = root / "worlds" / W / "stories" / story.id / "story.md"
    before = file.read_bytes()
    assert ms.remove_guest_world(W, story.id, "glaskueste", set()) == story
    assert file.read_bytes() == before
    assert not (file.parent / "facts.md").exists()
