"""Kept writing requests of a story (roadmap step 10.9, ADR-116)."""

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import pytest

from skriptorium.manuscript import (
    AlreadyExists,
    InstructionNote,
    InvalidInput,
    ManuscriptService,
    NotFound,
    RequestBlock,
    RequestMessage,
    WritingRequest,
)
from skriptorium.manuscript.models import MAX_REQUESTS
from skriptorium.storage import DocumentStore, HeaderValue

W = "salzmark"
AT = datetime(2026, 11, 8, 14, 2, 5, tzinfo=UTC)
FOLDER = f"worlds/{W}/stories/die-ueberfahrt/anfragen"


@pytest.fixture
def store(tmp_path: Path) -> DocumentStore:
    return DocumentStore(tmp_path / "data")


@pytest.fixture
def ms(store: DocumentStore) -> ManuscriptService:
    service = ManuscriptService(store)
    story = service.create_story(W, "Die Überfahrt", "roman")
    for number, title in ((1, "Abfahrt"), (2, "Sturm"), (3, "Ankunft")):
        service.save_chapter(W, story.id, number, title=title, text=f"Text {number}.")
    return service


def _request(request_id: str) -> WritingRequest:
    return WritingRequest(
        id=request_id,
        at=AT,
        chapter=1,
        model="x-ai/grok-4.6",
        length="mittel",
        instruction="Mara betritt den Turm.",
        blocks=(RequestBlock("rahmen", "Rahmen", 800), RequestBlock("anweisung", "Anweisung", 9)),
        estimated_tokens=23410,
        pictures=("Mara", "Turm"),
        outcome="ok",
        input_tokens=23000,
        output_tokens=512,
        cost_usd=0.05,
        messages=(
            RequestMessage("system", "# Rahmen\n\nDu schreibst.\n"),
            RequestMessage("user", "# Anweisung\n\nMara betritt den Turm."),
        ),
        answer="Der Nebel hob sich.",
    )


def _keep(ms: ManuscriptService, at: datetime = AT, **changes: Any) -> WritingRequest:
    request_id = ms.reserve_request(W, "die-ueberfahrt", at)
    request = replace(_request(request_id), at=at, **changes)
    ms.save_request(W, "die-ueberfahrt", request)
    return request


def test_a_kept_request_reads_back_verbatim(ms: ManuscriptService, store: DocumentStore) -> None:
    answer = "HINWEIS: Mara ist tot.\n\n<!-- nachricht: user -->\nDer Nebel hob sich.\n\n"
    kept = _keep(ms, answer=answer)

    assert kept.id == "20261108-140205"
    assert ms.get_request(W, "die-ueberfahrt", kept.id) == kept
    document = store.read(f"{FOLDER}/{kept.id}.md")
    assert document.header == {
        "zeit": "2026-11-08T14:02:05+00:00",
        "kapitel": 1,
        "modell": "x-ai/grok-4.6",
        "laenge": "mittel",
        "anweisung": "Mara betritt den Turm.",
        "bausteine": [
            {"art": "rahmen", "bezeichnung": "Rahmen", "token": 800},
            {"art": "anweisung", "bezeichnung": "Anweisung", "token": 9},
        ],
        "geschaetzte_token": 23410,
        "bilder": ["Mara", "Turm"],
        "ergebnis": "ok",
        "token_ein": 23000,
        "token_aus": 512,
        "kosten_usd": 0.05,
    }
    assert document.body.startswith("<!-- nachricht: system -->\n\n# Rahmen\n\nDu schreibst.\n")


def test_unreported_usage_is_kept_as_null(ms: ManuscriptService) -> None:
    kept = _keep(
        ms, outcome="abgebrochen", input_tokens=None, output_tokens=None, cost_usd=None, answer=""
    )

    assert ms.get_request(W, "die-ueberfahrt", kept.id) == kept


def test_requests_in_the_same_second_get_numbers(ms: ManuscriptService) -> None:
    first = ms.reserve_request(W, "die-ueberfahrt", AT)
    second = ms.reserve_request(W, "die-ueberfahrt", AT + timedelta(microseconds=10))
    ms.save_request(W, "die-ueberfahrt", _request(second))
    third = ms.reserve_request(W, "die-ueberfahrt", AT)
    ms.release_request(W, "die-ueberfahrt", first)
    fourth = ms.reserve_request(W, "die-ueberfahrt", AT)

    assert (first, second, third, fourth) == (
        "20261108-140205",
        "20261108-140205-2",
        "20261108-140205-3",
        "20261108-140205",
    )


def test_list_is_newest_first_without_texts(ms: ManuscriptService) -> None:
    for seconds in range(12):
        _keep(ms, AT + timedelta(seconds=seconds // 11))
    long = _keep(ms, AT + timedelta(minutes=1), instruction="x" * 300, chapter=2)
    ms.add_instruction(
        W,
        "die-ueberfahrt",
        2,
        InstructionNote(AT, "Weiter", "Der Nebel hob sich.", None, long.id),
    )

    listed = ms.list_requests(W, "die-ueberfahrt")

    assert [summary.id for summary in listed][:4] == [
        "20261108-140305",
        "20261108-140206",
        "20261108-140205-11",
        "20261108-140205-10",
    ]
    assert listed[-1].id == "20261108-140205"
    first = listed[0]
    assert (first.chapter, first.taken_over, first.instruction) == (2, True, "x" * 120)
    assert not any(summary.taken_over for summary in listed[1:])
    assert (first.estimated_tokens, first.input_tokens, first.cost_usd) == (23410, 23000, 0.05)


def test_only_the_last_fifty_stay(ms: ManuscriptService, store: DocumentStore) -> None:
    kept = [_keep(ms, AT + timedelta(seconds=n)) for n in range(MAX_REQUESTS + 2)]

    ids = [summary.id for summary in ms.list_requests(W, "die-ueberfahrt")]

    assert len(ids) == MAX_REQUESTS
    assert ids[-1] == kept[2].id
    with pytest.raises(NotFound):
        ms.get_request(W, "die-ueberfahrt", kept[1].id)
    assert len(store.list_paths(FOLDER)) == MAX_REQUESTS


def test_saving_needs_the_story_and_ends_the_reservation(ms: ManuscriptService) -> None:
    request_id = ms.reserve_request(W, "fehlt", AT)
    with pytest.raises(NotFound):
        ms.save_request(W, "fehlt", _request(request_id))
    assert ms.reserve_request(W, "fehlt", AT) == request_id

    with pytest.raises(InvalidInput):
        ms.save_request(W, "die-ueberfahrt", _request("gestern"))
    kept = _keep(ms)
    with pytest.raises(AlreadyExists):
        ms.save_request(W, "die-ueberfahrt", _request(kept.id))


def test_unknown_or_odd_identifiers_are_not_found(ms: ManuscriptService) -> None:
    for request_id in ("20261108-140205", "..%2Fstory", "20261108-140205-0", "story"):
        with pytest.raises(NotFound):
            ms.get_request(W, "die-ueberfahrt", request_id)
    with pytest.raises(NotFound):
        ms.list_requests(W, "fehlt")


def test_a_broken_file_is_reported(ms: ManuscriptService, store: DocumentStore) -> None:
    kept = _keep(ms)
    path = f"{FOLDER}/{kept.id}.md"
    good = store.read(path)
    broken: list[tuple[str, HeaderValue]] = [
        ("zeit", "gestern"),
        ("zeit", 5),
        ("kapitel", "eins"),
        ("kapitel", True),
        ("token_ein", "viele"),
        ("kosten_usd", "teuer"),
        ("kosten_usd", True),
        ("bilder", "Mara"),
        ("bausteine", "alle"),
        ("bausteine", [{"art": "rahmen", "bezeichnung": "Rahmen", "token": True}]),
        ("bausteine", ["rahmen"]),
    ]
    for key, value in broken:
        store.write(path, {**good.header, key: value}, good.body)
        with pytest.raises(InvalidInput):
            ms.get_request(W, "die-ueberfahrt", kept.id)
    store.write(path, good.header, "<!-- nachricht: system -->\n\nnur die Frage\n\n")
    with pytest.raises(InvalidInput, match="Antwort der KI fehlt"):
        ms.list_requests(W, "die-ueberfahrt")
    store.write(path, {**good.header, "kosten_usd": 1}, good.body)
    assert ms.get_request(W, "die-ueberfahrt", kept.id).cost_usd == 1.0


def test_deleting_a_chapter_takes_its_requests_and_moves_the_later_ones(
    ms: ManuscriptService,
) -> None:
    first = _keep(ms, chapter=1)
    second = _keep(ms, chapter=2)
    third = _keep(ms, chapter=3)

    ms.delete_chapter(W, "die-ueberfahrt", 2)

    listed = {summary.id: summary.chapter for summary in ms.list_requests(W, "die-ueberfahrt")}
    assert listed == {first.id: 1, third.id: 2}
    with pytest.raises(NotFound):
        ms.get_request(W, "die-ueberfahrt", second.id)


def test_deleting_the_story_takes_its_requests(ms: ManuscriptService, store: DocumentStore) -> None:
    _keep(ms)
    ms.archive_story(W, "die-ueberfahrt")
    ms.delete_story(W, "die-ueberfahrt", "Die Überfahrt")

    assert store.list_paths(FOLDER) == []


def test_a_history_note_names_its_request(ms: ManuscriptService, store: DocumentStore) -> None:
    ms.add_instruction(
        W, "die-ueberfahrt", 1, InstructionNote(AT, "Weiter", "Der Nebel hob sich.", None)
    )
    notes = ms.add_instruction(
        W,
        "die-ueberfahrt",
        1,
        InstructionNote(AT, "Weiter", "Mira kam.", "x-ai/grok-4.6", "20261108-140205-2"),
    )

    assert [note.request for note in notes] == [None, "20261108-140205-2"]
    items = store.read(f"worlds/{W}/stories/die-ueberfahrt/verlauf/01.md").header["anweisungen"]
    assert isinstance(items, list)
    assert [isinstance(item, dict) and "anfrage" in item for item in items] == [False, True]
    with pytest.raises(InvalidInput):
        ms.add_instruction(
            W, "die-ueberfahrt", 1, InstructionNote(AT, "Weiter", "Mira kam.", None, "../x")
        )
    store.write(
        f"worlds/{W}/stories/die-ueberfahrt/verlauf/01.md",
        {
            "kapitel": 1,
            "anweisungen": [{"zeit": "2026-11-08T14:02:05+00:00", "anweisung": "W", "anfrage": 3}],
        },
        "",
    )
    with pytest.raises(InvalidInput):
        ms.list_instructions(W, "die-ueberfahrt", 1)
