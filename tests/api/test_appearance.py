"""Taking out the looks of a figure, a place or an item over the API (7.16, 10.3)."""

from pathlib import Path

from fastapi.testclient import TestClient

from tests.api.conftest import FakeProvider
from tests.api.test_writing import _events, writer

__all__ = ["writer"]

URL = "/api/worlds/die-salzmark/entries/kael/appearance"


def test_streams_the_looks_and_saves_nothing(
    writer: TestClient, provider: FakeProvider, data_dir: Path
) -> None:
    before = writer.get("/api/worlds/die-salzmark/entries/kael").json()

    response = writer.post(URL, json={})

    assert response.status_code == 200, response.text
    assert [name for name, _ in _events(response.text)] == ["start", "text", "text", "done"]
    system, user = provider.requests[0].messages
    assert "äußeres Erscheinungsbild" in system.content
    assert "Kael" in user.content
    assert provider.requests[0].temperature == 0.2
    assert writer.get("/api/worlds/die-salzmark/entries/kael").json() == before
    text = next((data_dir / "system" / "verbrauch").glob("*.md")).read_text(encoding="utf-8")
    assert "art: aussehen" in text


def test_unknown_model_and_entry(writer: TestClient, provider: FakeProvider) -> None:
    assert writer.post(URL, json={"model": "gibt/es-nicht"}).status_code == 422
    missing = writer.post("/api/worlds/die-salzmark/entries/niemand/appearance", json={})
    assert missing.status_code == 404
    assert provider.requests == []


def test_an_entry_too_large_for_the_budget_is_refused(
    writer: TestClient, provider: FakeProvider
) -> None:
    writer.post(
        "/api/worlds/die-salzmark/entries",
        json={"category": "figur", "name": "Riesenfigur", "body": "Narbe. " * 20_000},
    )

    response = writer.post("/api/worlds/die-salzmark/entries/riesenfigur/appearance", json={})

    assert response.status_code == 422
    assert "Eintrag (" in response.json()["detail"]
    assert provider.requests == []


def test_a_rule_is_refused(writer: TestClient, provider: FakeProvider) -> None:
    """Steps 8.4 and 10.3 (ADR-083, ADR-108): refused before anything is sent."""
    writer.post(
        "/api/worlds/die-salzmark/entries",
        json={"category": "regel", "name": "Salzrecht", "body": "Wer Salz stiehlt, zahlt."},
    )

    response = writer.post("/api/worlds/die-salzmark/entries/salzrecht/appearance", json={})

    assert response.status_code == 422
    assert "Figuren, Orten und Gegenständen" in response.json()["detail"]
    assert provider.requests == []


def test_a_place_streams_its_looks_without_its_location(
    writer: TestClient, provider: FakeProvider
) -> None:
    """Step 10.3 (ADR-108)."""
    writer.post(
        "/api/worlds/die-salzmark/entries",
        json={
            "category": "ort",
            "name": "Karst",
            "body": "Graue Mauern, grünes Licht.\n\n## Lage\n\nAuf der Klippe.",
        },
    )

    response = writer.post("/api/worlds/die-salzmark/entries/karst/appearance", json={})

    assert response.status_code == 200, response.text
    system, user = provider.requests[0].messages
    assert "eines Ortes" in system.content
    assert "Graue Mauern" in user.content
    assert "Klippe" not in user.content
