"""Archiving a world and deleting it for good (step 9.9, ADR-098, FR-036)."""

from pathlib import Path

import pytest

from skriptorium.canon import CanonService, InvalidInput, NotFound, WorldContents
from skriptorium.storage import DocumentStore, ImageOrigin
from tests.image_samples import jpeg, png

WORLD = "die-salzmark"


@pytest.fixture
def root(tmp_path: Path) -> Path:
    return tmp_path / "data"


@pytest.fixture
def store(root: Path) -> DocumentStore:
    return DocumentStore(root)


@pytest.fixture
def canon(store: DocumentStore) -> CanonService:
    service = CanonService(store)
    service.create_world("Die Salzmark", "Sieben Inseln.")
    service.create_world("Nebelreich")
    service.create_entry(WORLD, "figur", "Kael", body="Fährmann am Salzhafen.")
    service.create_entry("nebelreich", "figur", "Nebelkönig", body="Herr über den Salzhafen.")
    return service


def test_archive_and_restore_leave_the_file_as_it_was(canon: CanonService, root: Path) -> None:
    file = root / "worlds" / WORLD / "world.md"
    before = file.read_bytes()
    archived = canon.archive_world(WORLD)
    assert archived.archived is True
    assert "archiviert: true" in file.read_text(encoding="utf-8")
    assert [(w.id, w.archived) for w in canon.list_worlds()] == [
        (WORLD, True),
        ("nebelreich", False),
    ]
    assert canon.restore_world(WORLD).archived is False
    assert file.read_bytes() == before


def test_an_archived_world_keeps_working(canon: CanonService) -> None:
    canon.archive_world(WORLD)
    changed = canon.update_world(WORLD, description="Acht Inseln.")
    assert changed.archived is True
    assert canon.get_entry(WORLD, "kael").name == "Kael"


def test_archive_needs_an_existing_world(canon: CanonService) -> None:
    with pytest.raises(NotFound):
        canon.archive_world("gibt-es-nicht")
    with pytest.raises(NotFound):
        canon.restore_world("gibt-es-nicht")


def test_archived_header_must_be_true_or_false(canon: CanonService, root: Path) -> None:
    file = root / "worlds" / WORLD / "world.md"
    file.write_text("---\nname: Die Salzmark\narchiviert: ja\n---\n", encoding="utf-8")
    with pytest.raises(InvalidInput):
        canon.get_world(WORLD)
    file.write_text("---\nname: Die Salzmark\narchiviert: false\n---\n", encoding="utf-8")
    assert canon.get_world(WORLD).archived is False


def test_contents_count_entries_images_and_maps(canon: CanonService) -> None:
    canon.create_entry(WORLD, "ort", "Hafen")
    canon.add_entry_image(WORLD, "kael", png())
    canon.add_entry_image(WORLD, "kael", jpeg())
    canon.add_entry_image(WORLD, "hafen", png())
    canon.add_world_map(WORLD, "Seekarte", png())
    assert canon.world_contents(WORLD) == WorldContents(entries=2, images=3, maps=1)
    assert canon.world_contents("nebelreich") == WorldContents(entries=1, images=0, maps=0)


def test_delete_only_an_archived_world_with_its_exact_name(canon: CanonService) -> None:
    with pytest.raises(InvalidInput, match="archivierte"):
        canon.delete_world(WORLD, "Die Salzmark")
    canon.archive_world(WORLD)
    for wrong in ("die salzmark", "Die Salzmark ", "", "Nebelreich"):
        with pytest.raises(InvalidInput, match="Name"):
            canon.delete_world(WORLD, wrong)
    assert canon.check_world_deletion(WORLD, "Die Salzmark").id == WORLD
    assert canon.get_world(WORLD).archived is True
    with pytest.raises(NotFound):
        canon.delete_world("gibt-es-nicht", "x")


def test_delete_removes_the_whole_folder_and_its_index_rows(
    canon: CanonService, store: DocumentStore, root: Path
) -> None:
    origin = ImageOrigin("bild/modell", "Ein Hafen", "1:1", 0.04, "2026-11-04")
    canon.add_entry_image(WORLD, "kael", png(), origin)
    canon.add_world_map(WORLD, "Seekarte", jpeg(), origin)
    assert len(list((root / "worlds" / WORLD).rglob("*.herkunft.yml"))) == 2
    store.write(f"worlds/{WORLD}/stories/flucht/story.md", {"titel": "Flucht"}, "Salzhafen.")
    store.write("system/verbrauch/2026-11.md", {"eintraege": []}, "")
    assert store.search(WORLD, "salzhafen", "fulltext") != []
    canon.archive_world(WORLD)

    canon.delete_world(WORLD, "Die Salzmark")

    assert not (root / "worlds" / WORLD).exists()
    assert [p.name for p in root.iterdir() if p.name.startswith(".")] == []
    assert [w.id for w in canon.list_worlds()] == ["nebelreich"]
    assert store.search(WORLD, "salzhafen", "fulltext") == []
    assert store.search(WORLD, "kael") == []
    assert store.search("nebelreich", "salzhafen", "fulltext") != []
    assert (root / "system" / "verbrauch" / "2026-11.md").is_file()
    with pytest.raises(NotFound):
        canon.get_world(WORLD)
