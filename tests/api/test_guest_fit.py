"""Relation of a guest and "Einpassen vorschlagen" over the API (step 9.13, ADR-102)."""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from tests.api.conftest import FakeProvider
from tests.api.test_writing import _events, writer

__all__ = ["writer"]

STORY = "/api/worlds/die-salzmark/stories/am-ufer"
GUEST = f"{STORY}/guests/nordland/ragna"


@pytest.fixture
def guest(writer: TestClient) -> TestClient:
    writer.post("/api/worlds", json={"name": "Nordland", "description": "Eis."})
    writer.post(
        "/api/worlds/nordland/entries",
        json={"category": "figur", "name": "Ragna", "body": "Jägerin.\n\n## Im Nordland\n\nAlt."},
    )
    assert writer.post(f"{STORY}/guests", json={"world": "nordland", "entry": "ragna"}).is_success
    return writer


def test_set_and_clear_the_relation(guest: TestClient) -> None:
    response = guest.put(GUEST, json={"relation": " Kam übers Eis. "})

    assert response.status_code == 200, response.text
    assert response.json()["guest_links"] == [
        {"world": "nordland", "entry": "ragna", "relation": "Kam übers Eis."}
    ]
    assert guest.get(STORY).json()["guest_links"][0]["relation"] == "Kam übers Eis."
    cleared = guest.put(GUEST, json={"relation": ""}).json()["guest_links"][0]
    assert cleared["relation"] == ""


def test_unknown_link_long_text_and_missing_field(guest: TestClient) -> None:
    assert guest.put(f"{STORY}/guests/nordland/niemand", json={"relation": "x"}).status_code == 404
    assert (
        guest.put(
            "/api/worlds/fehlt/stories/am-ufer/guests/nordland/ragna", json={"relation": "x"}
        ).status_code
        == 404
    )
    assert guest.put(GUEST, json={"relation": "x" * 4001}).status_code == 422
    assert guest.put(GUEST, json={}).status_code == 422


def test_writing_sees_the_relation_instead_of_the_home_world(
    guest: TestClient, provider: FakeProvider
) -> None:
    guest.put(GUEST, json={"relation": "Kam übers Eis."})

    response = guest.post(f"{STORY}/chapters/1/write", json={"instruction": "@Ragna kommt."})

    assert response.status_code == 200, response.text
    system = provider.requests[0].messages[0].content
    assert "### In dieser Welt („Die Salzmark“)\n\nKam übers Eis." in system
    assert "Im Nordland" not in system


def test_fit_streams_a_proposal_saves_nothing_and_counts_it(
    guest: TestClient, provider: FakeProvider, data_dir: Path
) -> None:
    guest.put(GUEST, json={"relation": "Kam übers Eis."})
    before = guest.get(STORY).json()

    response = guest.post(f"{GUEST}/fit", json={"wish": "soll fremd bleiben"})

    assert response.status_code == 200, response.text
    assert [name for name, _ in _events(response.text)] == ["start", "text", "text", "done"]
    system, user = provider.requests[0].messages
    assert "einzupassen" in system.content
    assert "# Neue Welt: Die Salzmark" in system.content
    assert "Jägerin." in user.content
    assert "# Bisher\n\nKam übers Eis." in user.content
    assert "soll fremd bleiben" in user.content
    assert provider.requests[0].temperature == 0.7
    assert guest.get(STORY).json() == before
    text = next((data_dir / "system" / "verbrauch").glob("*.md")).read_text(encoding="utf-8")
    assert "art: weltenbau" in text
    assert "welt: die-salzmark" in text
    assert "geschichte: am-ufer" in text


def test_fit_refuses_unknown_model_link_and_long_wish(
    guest: TestClient, provider: FakeProvider
) -> None:
    assert guest.post(f"{GUEST}/fit", json={"model": "gibt/es-nicht"}).status_code == 422
    assert guest.post(f"{STORY}/guests/nordland/niemand/fit", json={}).status_code == 404
    assert guest.post(f"{GUEST}/fit", json={"wish": "x" * 1001}).status_code == 422
    assert provider.requests == []


def test_fit_refuses_a_request_too_large_for_the_budget(
    guest: TestClient, provider: FakeProvider
) -> None:
    changed = guest.patch("/api/worlds/nordland/entries/ragna", json={"body": "Jägerin. " * 20_000})
    assert changed.status_code == 200, changed.text

    response = guest.post(f"{GUEST}/fit", json={})

    assert response.status_code == 422
    assert "Ragna (" in response.json()["detail"]
    assert provider.requests == []
