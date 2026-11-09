"""The figure assistant over the API (11.5, ADR-123, ADR-124)."""

from pathlib import Path

from fastapi.testclient import TestClient

from tests.api.conftest import FakeProvider
from tests.api.test_writing import _events, writer

__all__ = ["writer"]

URL = "/api/worlds/die-salzmark/entries/kael/figure-looks"
SUGGESTIONS_URL = URL + "/suggestions"
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


def test_suggestions_stream_and_save_nothing(
    writer: TestClient, provider: FakeProvider, data_dir: Path
) -> None:
    before = writer.get("/api/worlds/die-salzmark/entries/kael").json()

    response = writer.post(SUGGESTIONS_URL, json={"answers": {"Haar": "schwarz"}})

    assert response.status_code == 200, response.text
    assert response.headers["cache-control"] == "no-store"
    assert [name for name, _ in _events(response.text)] == ["start", "text", "text", "done"]
    request = provider.requests[0]
    system, user = request.messages
    assert "genau 3 Vorschläge" in system.content
    assert "- Haar: schwarz" in user.content
    assert "- Alter: (noch keine Angabe)" in user.content
    assert request.model == "x-ai/grok-4.6"
    assert request.temperature == 0.8
    assert request.max_tokens == 4000
    assert writer.get("/api/worlds/die-salzmark/entries/kael").json() == before
    text = next((data_dir / "system" / "verbrauch").glob("*.md")).read_text(encoding="utf-8")
    assert "art: figurenassistent" in text


def test_suggestions_work_without_any_answer_and_use_the_saved_task_model(
    writer: TestClient, provider: FakeProvider
) -> None:
    writer.put("/api/models/aufgaben", json={"tasks": {"figurenassistent": "x-ai/grok-4.7"}})

    response = writer.post(SUGGESTIONS_URL, json={"answers": {}})

    assert response.status_code == 200, response.text
    assert provider.requests[0].model == "x-ai/grok-4.7"


def test_suggestions_are_refused_before_anything_is_sent(
    writer: TestClient, provider: FakeProvider
) -> None:
    unknown = writer.post(SUGGESTIONS_URL, json={"answers": {"Kleidung": "Mantel"}})
    assert unknown.status_code == 422
    assert "Kleidung" in unknown.json()["detail"]
    assert (
        writer.post(SUGGESTIONS_URL, json={"answers": {}, "model": "gibt/es-nicht"}).status_code
        == 422
    )
    assert writer.post(SUGGESTIONS_URL, json={}).status_code == 422
    missing = writer.post(
        "/api/worlds/die-salzmark/entries/niemand/figure-looks/suggestions",
        json={"answers": {}},
    )
    assert missing.status_code == 404
    writer.post(
        "/api/worlds/die-salzmark/entries",
        json={"category": "ort", "name": "Karst", "body": "Mauern."},
    )
    place = writer.post(
        "/api/worlds/die-salzmark/entries/karst/figure-looks/suggestions", json={"answers": {}}
    )
    assert place.status_code == 422
    assert provider.requests == []


def test_suggestions_for_an_entry_too_large_for_the_budget_are_refused(
    writer: TestClient, provider: FakeProvider
) -> None:
    writer.post(
        "/api/worlds/die-salzmark/entries",
        json={"category": "figur", "name": "Riesenfigur", "body": "Narbe. " * 20_000},
    )

    response = writer.post(
        "/api/worlds/die-salzmark/entries/riesenfigur/figure-looks/suggestions",
        json={"answers": {}},
    )

    assert response.status_code == 422
    assert provider.requests == []
