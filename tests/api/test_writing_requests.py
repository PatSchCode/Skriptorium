"""Writing requests are kept as they went to the AI, with the raw answer (step 10.9, ADR-116)."""

import asyncio
import logging
from datetime import UTC, datetime
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from skriptorium.ai_gateway import RateLimited
from skriptorium.api.flows import (
    PreparedRequest,
    RequestKeeper,
    WriteOrder,
    prepare_request,
    stream_events,
)
from skriptorium.context import CONFLICT_MARKER
from skriptorium.manuscript import ManuscriptService, WritingRequest
from skriptorium.storage import StorageError
from tests.api.conftest import FakeClock, FakeProvider, services_of
from tests.api.test_writing import WRITE, _builder, _events, writer

STORY = "/api/worlds/die-salzmark/stories/am-ufer"
REQUESTS = f"{STORY}/requests"
HISTORY = f"{STORY}/chapters/1/instructions"
AT = datetime(2026, 11, 8, 14, 2, 5, tzinfo=UTC)

__all__ = ["writer"]


def test_a_finished_request_is_kept_with_messages_and_raw_answer(
    writer: TestClient, provider: FakeProvider
) -> None:
    provider.chunks = (f"{CONFLICT_MARKER} Kael ist tot.\n", "Der Nebel hob sich.")

    response = writer.post(WRITE, json={"instruction": "Kael spricht.", "length": "kurz"})

    events = _events(response.text)
    start = events[0][1]
    assert start["request"] == "20260926-120000"
    assert [name for name, _ in events] == ["start", "hinweis", "text", "done"]
    kept = writer.get(f"{REQUESTS}/{start['request']}").json()
    sent = provider.requests[0]
    assert kept["messages"] == [
        {"role": message.role, "content": message.content} for message in sent.messages
    ]
    assert kept["answer"] == f"{CONFLICT_MARKER} Kael ist tot.\nDer Nebel hob sich."
    assert {key: kept[key] for key in ("chapter", "model", "length", "instruction")} == {
        "chapter": 1,
        "model": sent.model,
        "length": "kurz",
        "instruction": "Kael spricht.",
    }
    assert kept["estimated_tokens"] == start["estimated_tokens"]
    assert sum(block["tokens"] for block in kept["blocks"]) > 0
    assert {block["kind"] for block in kept["blocks"]} >= {"rahmen", "anweisung"}
    assert (kept["outcome"], kept["input_tokens"], kept["output_tokens"], kept["cost_usd"]) == (
        "ok",
        1200,
        40,
        0.0021,
    )
    assert (kept["pictures"], kept["at"]) == ([], "2026-09-26T12:00:00Z")


def test_failed_requests_are_kept_with_their_error_kind(
    writer: TestClient, provider: FakeProvider, clock: FakeClock
) -> None:
    writer.post(WRITE, json={})
    provider.error = RateLimited("zu viele")
    provider.chunks = ("Der Ne",)
    writer.post(WRITE, json={"scene": {"goal": "Ein Fremder kommt."}})

    listed = writer.get(REQUESTS).json()

    assert [(item["id"], item["outcome"]) for item in listed] == [
        ("20260926-120000-2", "zu_viele_anfragen"),
        ("20260926-120000", "ok"),
    ]
    failed = listed[0]
    assert failed["instruction"].startswith("Beginne hier eine neue Szene")
    assert (failed["input_tokens"], failed["cost_usd"], failed["taken_over"]) == (
        None,
        None,
        False,
    )
    assert "messages" not in failed
    assert writer.get(f"{REQUESTS}/{failed['id']}").json()["answer"] == "Der Ne"


def test_taking_over_names_the_request_in_the_history(writer: TestClient) -> None:
    request = _events(writer.post(WRITE, json={}).text)[0][1]["request"]
    noted = writer.post(
        HISTORY, json={"instruction": "Weiter", "text": "Der Nebel hob sich.", "request": request}
    )

    assert noted.status_code == 201, noted.text
    assert noted.json()[0]["request"] == request
    assert writer.get(REQUESTS).json()[0]["taken_over"] is True
    odd = writer.post(HISTORY, json={"instruction": "W", "text": "T", "request": "../story"})
    assert odd.status_code == 422


def test_kept_requests_never_reach_the_ai(writer: TestClient, provider: FakeProvider) -> None:
    provider.chunks = ("Die Laterne erlosch.",)
    writer.post(WRITE, json={"instruction": "Mira bringt die Laterne."})
    provider.chunks = ("Kael schwieg.",)

    writer.post(WRITE, json={"instruction": "Kael schweigt."})

    system, user = (message.content for message in provider.requests[1].messages)
    assert "Laterne" not in system + user


def test_read_routes_refuse_unknown_worlds_stories_and_requests(writer: TestClient) -> None:
    assert writer.get(REQUESTS).json() == []
    assert writer.get("/api/worlds/fehlt/stories/am-ufer/requests").status_code == 404
    assert writer.get("/api/worlds/die-salzmark/stories/fehlt/requests").status_code == 404
    assert writer.get(f"{REQUESTS}/20260926-120000").status_code == 404
    assert writer.get(f"{REQUESTS}/kaputt").status_code == 404
    assert writer.get("/api/worlds/fehlt/stories/am-ufer/requests/x").status_code == 404


def test_a_storage_failure_never_breaks_the_stream(
    writer: TestClient, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    manuscripts = services_of(writer).manuscript

    def broken(world: str, story: str, request: WritingRequest) -> None:
        raise StorageError("Platte voll")

    monkeypatch.setattr(manuscripts, "save_request", broken)
    with caplog.at_level(logging.WARNING, logger="skriptorium.api.flows.writing"):
        response = writer.post(WRITE, json={"instruction": "Mira kommt mit der Laterne."})

    assert [name for name, _ in _events(response.text)] == ["start", "text", "text", "done"]
    assert "Anfrage nicht gespeichert: StorageError" in caplog.text
    assert "Laterne" not in caplog.text
    assert "Platte" not in caplog.text


# The flow on its own: aborted requests and requests closed before they were sent.


def _prepared(tmp_path: Path) -> tuple[ManuscriptService, PreparedRequest]:
    canon, manuscripts, builder = _builder(tmp_path)
    order = WriteOrder("die-salzmark", "am-ufer", 1, "Mira kommt.")
    return manuscripts, prepare_request(canon, manuscripts, builder, order)


def test_an_aborted_request_is_kept_with_what_came_so_far(tmp_path: Path) -> None:
    manuscripts, prepared = _prepared(tmp_path)
    keeper = RequestKeeper(manuscripts, lambda: AT)
    provider = FakeProvider(chunks=("Mira ", "kam ", "herein."))

    async def read_two_then_abort() -> None:
        stream = stream_events(provider, prepared, keeper=keeper)
        await anext(stream)
        await anext(stream)
        await stream.aclose()  # type: ignore[attr-defined]  # async generator

    asyncio.run(read_two_then_abort())

    kept = manuscripts.get_request("die-salzmark", "am-ufer", "20261108-140205")
    assert (kept.outcome, kept.answer, kept.input_tokens) == ("abgebrochen", "Mira ", None)


def test_a_request_closed_before_sending_is_neither_counted_nor_kept(tmp_path: Path) -> None:
    manuscripts, prepared = _prepared(tmp_path)
    keeper = RequestKeeper(manuscripts, lambda: AT)
    provider = FakeProvider()
    counted: list[str] = []

    async def read_start_then_close() -> str:
        stream = stream_events(
            provider, prepared, lambda *args: counted.append(args[3]), keeper=keeper
        )
        start = await anext(stream)
        await stream.aclose()  # type: ignore[attr-defined]  # async generator
        return start

    start = asyncio.run(read_start_then_close())

    assert '"request": "20261108-140205"' in start
    assert (provider.requests, counted) == ([], [])
    assert manuscripts.list_requests("die-salzmark", "am-ufer") == []
    # The identifier was given back.
    assert manuscripts.reserve_request("die-salzmark", "am-ufer", AT) == "20261108-140205"


def test_other_requests_are_not_kept(tmp_path: Path) -> None:
    manuscripts, prepared = _prepared(tmp_path)
    keeper = RequestKeeper(manuscripts, lambda: AT)
    plain = PreparedRequest(prepared.completion, prepared.estimated_tokens)

    async def read_all() -> list[str]:
        return [event async for event in stream_events(FakeProvider(), plain, keeper=keeper)]

    events = asyncio.run(read_all())

    assert '"request": null' in events[0]
    assert manuscripts.list_requests("die-salzmark", "am-ufer") == []
