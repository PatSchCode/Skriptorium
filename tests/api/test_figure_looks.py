"""The figure assistant over the API (11.5, ADR-123)."""

from pathlib import Path

from fastapi.testclient import TestClient

from tests.api.conftest import FakeProvider
from tests.api.test_writing import _events, writer

__all__ = ["writer"]

URL = "/api/worlds/die-salzmark/entries/kael/figure-looks"
ANSWERS = {"Herkunft": "Nordeuropa", "Alter": "34", "Haar": "schwarz"}


def test_streams_the_description_and_saves_nothing(
    writer: TestClient, provider: FakeProvider, data_dir: Path
) -> None:
    before = writer.get("/api/worlds/die-salzmark/entries/kael").json()

    response = writer.post(URL, json={"answers": ANSWERS})

    assert response.status_code == 200, response.text
    assert [name for name, _ in _events(response.text)] == ["start", "text", "text", "done"]
    system, user = provider.requests[0].messages
    assert "year-old adult" in system.content
    assert "- Alter: 34" in user.content
    assert provider.requests[0].model == "x-ai/grok-4.6"
    assert provider.requests[0].temperature == 0.4
    assert writer.get("/api/worlds/die-salzmark/entries/kael").json() == before
    text = next((data_dir / "system" / "verbrauch").glob("*.md")).read_text(encoding="utf-8")
    assert "art: figurenassistent" in text


def test_the_saved_task_model_is_used(writer: TestClient, provider: FakeProvider) -> None:
    saved = writer.put(
        "/api/models/aufgaben", json={"tasks": {"figurenassistent": "x-ai/grok-4.7"}}
    )
    assert saved.status_code == 200, saved.text
    assert saved.json()["tasks"]["figurenassistent"] == "x-ai/grok-4.7"

    writer.post(URL, json={"answers": ANSWERS})

    assert provider.requests[0].model == "x-ai/grok-4.7"


def test_refused_before_anything_is_sent(writer: TestClient, provider: FakeProvider) -> None:
    young = writer.post(URL, json={"answers": {**ANSWERS, "Alter": "16"}})
    assert young.status_code == 422
    assert "ab 18" in young.json()["detail"]
    assert writer.post(URL, json={"answers": ANSWERS, "model": "gibt/es-nicht"}).status_code == 422
    assert writer.post(URL, json={}).status_code == 422
    missing = writer.post(
        "/api/worlds/die-salzmark/entries/niemand/figure-looks", json={"answers": ANSWERS}
    )
    assert missing.status_code == 404
    writer.post(
        "/api/worlds/die-salzmark/entries",
        json={"category": "ort", "name": "Karst", "body": "Mauern."},
    )
    place = writer.post(
        "/api/worlds/die-salzmark/entries/karst/figure-looks", json={"answers": ANSWERS}
    )
    assert place.status_code == 422
    assert provider.requests == []


def test_an_entry_too_large_for_the_budget_is_refused(
    writer: TestClient, provider: FakeProvider
) -> None:
    writer.post(
        "/api/worlds/die-salzmark/entries",
        json={"category": "figur", "name": "Riesenfigur", "body": "Narbe. " * 20_000},
    )

    response = writer.post(
        "/api/worlds/die-salzmark/entries/riesenfigur/figure-looks", json={"answers": ANSWERS}
    )

    assert response.status_code == 422
    assert provider.requests == []
