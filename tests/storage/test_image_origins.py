"""Tests for the origin of generated images in a companion file (steps 9.6, 10.5)."""

import os
from dataclasses import replace
from pathlib import Path

import pytest

from skriptorium.storage import (
    DocumentStore,
    ImageOrigin,
    InvalidInput,
    NotFound,
    OriginLora,
    StorageError,
)
from skriptorium.storage.frontmatter import HeaderValue
from skriptorium.storage.origins import origin_from_mapping, origin_to_mapping
from tests.image_samples import png

IMAGE = "worlds/salzmark/bilder/kael-0a1b2c.png"
COMPANION = IMAGE + ".herkunft.yml"
ORIGIN = ImageOrigin(
    "openai/gpt-image-1",
    "Kael am Hafen, Abendlicht.\nZweite Zeile: „Mantel“ in Grau.",
    "2:3",
    0.04,
    "2026-10-25T18:00:00+00:00",
)


@pytest.fixture
def store(tmp_path: Path) -> DocumentStore:
    return DocumentStore(tmp_path / "data")


def test_writes_and_reads_the_origin_next_to_the_image(
    store: DocumentStore, tmp_path: Path
) -> None:
    store.write_image(IMAGE, png(), origin=ORIGIN)
    assert store.read_image_origin(IMAGE) == ORIGIN
    text = (tmp_path / "data" / COMPANION).read_text(encoding="utf-8")
    assert text.startswith("modell: openai/gpt-image-1\n")
    assert "„Mantel“ in Grau" in text  # readable, not escaped
    # Not a Markdown document: neither listed nor indexed.
    assert store.list_paths() == []
    store.rebuild_index()
    assert store.search("salzmark", "Kael", "fulltext") == []


def test_an_image_without_companion_has_no_origin(store: DocumentStore) -> None:
    store.write_image(IMAGE, png())
    assert store.read_image_origin(IMAGE) is None


def test_deleting_the_image_deletes_its_origin(store: DocumentStore, tmp_path: Path) -> None:
    store.write_image(IMAGE, png(), origin=ORIGIN)
    store.delete_image(IMAGE)
    assert not (tmp_path / "data" / COMPANION).exists()
    assert store.read_image_origin(IMAGE) is None


def test_a_companion_left_without_image_is_removed_on_delete(
    store: DocumentStore, tmp_path: Path
) -> None:
    store.write_image(IMAGE, png(), origin=ORIGIN)
    (tmp_path / "data" / IMAGE).unlink()  # image deleted by hand
    with pytest.raises(NotFound):
        store.delete_image(IMAGE)
    assert not (tmp_path / "data" / COMPANION).exists()


def test_a_failing_origin_write_leaves_no_image(
    store: DocumentStore, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls = 0
    real_fsync = os.fsync

    def fail_third(descriptor: int) -> None:
        nonlocal calls
        calls += 1
        if calls == 3:  # file and directory of the image succeed, the companion fails
            raise OSError("Datenträger voll")
        real_fsync(descriptor)

    monkeypatch.setattr(os, "fsync", fail_third)
    with pytest.raises(StorageError, match="Datenträger voll"):
        store.write_image(IMAGE, png(), origin=ORIGIN)
    monkeypatch.undo()
    assert [p for p in (tmp_path / "data" / "worlds").rglob("*") if p.is_file()] == []


def test_an_unreadable_companion_is_invalid_input(store: DocumentStore, tmp_path: Path) -> None:
    store.write_image(IMAGE, png())
    (tmp_path / "data" / COMPANION).write_text("modell: [offen\n", encoding="utf-8")
    with pytest.raises(InvalidInput):
        store.read_image_origin(IMAGE)


def test_reads_origins_only_of_image_paths(store: DocumentStore) -> None:
    with pytest.raises(InvalidInput):
        store.read_image_origin("worlds/w/canon/figur/kael.md")


def test_mapping_round_trip_and_missing_cost() -> None:
    assert origin_from_mapping(origin_to_mapping(ORIGIN)) == ORIGIN
    without_cost = ImageOrigin("m", "p", "1:1", None, "2026-10-25T18:00:00+00:00")
    assert origin_from_mapping(origin_to_mapping(without_cost)) == without_cost
    whole = origin_to_mapping(ORIGIN) | {"kosten_usd": 1}
    assert origin_from_mapping(whole).cost_usd == 1.0


@pytest.mark.parametrize(
    "change",
    [
        {"modell": None},
        {"anweisung": 3},
        {"seitenverhaeltnis": None},
        {"datum": None},
        {"kosten_usd": "teuer"},
        {"kosten_usd": True},
    ],
)
def test_refuses_incomplete_or_wrong_fields(change: dict[str, HeaderValue]) -> None:
    with pytest.raises(InvalidInput):
        origin_from_mapping(origin_to_mapping(ORIGIN) | change)


def test_a_failing_image_delete_after_the_origin_is_a_storage_error(
    store: DocumentStore, monkeypatch: pytest.MonkeyPatch
) -> None:
    store.write_image(IMAGE, png(), origin=ORIGIN)
    real_unlink = Path.unlink

    def refuse_image(self: Path, missing_ok: bool = False) -> None:
        if self.suffix == ".png":
            raise PermissionError("gesperrt")
        real_unlink(self, missing_ok=missing_ok)

    monkeypatch.setattr(Path, "unlink", refuse_image)
    with pytest.raises(StorageError, match="gesperrt"):
        store.delete_image(IMAGE)
    monkeypatch.undo()
    assert store.read_image(IMAGE)[0] == png()


def test_the_basis_of_an_image_made_from_another_round_trips(store: DocumentStore) -> None:
    """Step 9.8, ADR-097: ``grundlage`` names the image it was made from; old files lack it."""
    made = ImageOrigin("m", "p", "1:1", None, "2026-10-26T10:00:00+00:00", "Bild 1 von Kael")
    store.write_image(IMAGE, png(), origin=made)
    assert store.read_image_origin(IMAGE) == made
    assert origin_to_mapping(made)["grundlage"] == "Bild 1 von Kael"
    assert "grundlage" not in origin_to_mapping(ORIGIN)
    with pytest.raises(InvalidInput, match="Grundlage"):
        origin_from_mapping({**origin_to_mapping(ORIGIN), "grundlage": 3})


def test_resolution_and_quality_round_trip(store: DocumentStore) -> None:
    """Step 10.5, ADR-109: both are kept when chosen; older files lack them."""
    made = ImageOrigin("m", "p", "2:3", 0.09, "2026-11-05T10:00:00+00:00", None, "2K", "medium")
    store.write_image(IMAGE, png(), origin=made)
    assert store.read_image_origin(IMAGE) == made
    mapping = origin_to_mapping(made)
    assert (mapping["aufloesung"], mapping["qualitaet"]) == ("2K", "medium")
    assert "aufloesung" not in origin_to_mapping(ORIGIN)
    assert "qualitaet" not in origin_to_mapping(ORIGIN)
    assert origin_from_mapping(origin_to_mapping(ORIGIN)).resolution is None
    for field in ("aufloesung", "qualitaet"):
        with pytest.raises(InvalidInput, match="Auflösung oder Qualität"):
            origin_from_mapping({**origin_to_mapping(ORIGIN), field: 2})


def test_start_value_loras_and_appended_text_round_trip(
    store: DocumentStore, tmp_path: Path
) -> None:
    # Step 11.4 (ADR-121).
    full = replace(
        ORIGIN,
        seed=1834072215,
        loras=(OriginLora("civitai:536201@596079", "Nebelstimmung", 0.8),),
        appended="fog, misty harbour",
    )
    store.write_image(IMAGE, png(), origin=full)
    assert store.read_image_origin(IMAGE) == full
    text = (tmp_path / "data" / COMPANION).read_text(encoding="utf-8")
    assert "startwert: 1834072215\n" in text
    assert "angehaengt: fog, misty harbour\n" in text
    # Without them the file looks as before.
    assert set(origin_to_mapping(ORIGIN)) == {
        "modell",
        "anweisung",
        "seitenverhaeltnis",
        "kosten_usd",
        "datum",
    }


@pytest.mark.parametrize(
    "change",
    [
        {"startwert": "7"},
        {"startwert": True},
        {"angehaengt": 3},
        {"loras": "civitai:1@2"},
        {"loras": [{"kennung": "a:b@c", "name": "x"}]},
        {"loras": [{"kennung": "a:b@c", "name": "x", "gewicht": True}]},
        {"loras": ["a:b@c"]},
    ],
)
def test_refuses_a_wrong_start_value_or_lora(change: dict[str, HeaderValue]) -> None:
    with pytest.raises(InvalidInput):
        origin_from_mapping(origin_to_mapping(ORIGIN) | change)
