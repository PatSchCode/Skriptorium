"""HTTP tests of archiving and deleting worlds, stories and chapters (step 9.9, ADR-098, FR-036).

The cascade across the world border: deleting a world takes the guest links into it, and the
facts and led characters about those guests, out of the stories of other worlds.
"""

from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient
from httpx import Response

from skriptorium.storage import DocumentStore

SALZ = "/api/worlds/die-salzmark"
GLAS = "/api/worlds/glaskueste"


def _ok(response: Response, status: int = 200) -> Any:
    assert response.status_code == status, response.text
    return response.json() if response.content else None


def _set_up(client: TestClient) -> None:
    """Salzmark with a story that has guests from Glasküste; Glasküste with its own story."""
    _ok(client.post("/api/worlds", json={"name": "Die Salzmark"}), 201)
    _ok(client.post("/api/worlds", json={"name": "Glasküste"}), 201)
    for world, name in (
        (SALZ, "Kael"),
        (GLAS, "Mira"),
        (GLAS, "Kael"),
        (GLAS, "Vale"),
    ):
        _ok(client.post(f"{world}/entries", json={"category": "figur", "name": name}), 201)
    _ok(client.post(f"{SALZ}/stories", json={"title": "Die Überfahrt", "form": "roman"}), 201)
    story = f"{SALZ}/stories/die-ueberfahrt"
    for entry in ("mira", "kael", "vale"):
        _ok(client.post(f"{story}/guests", json={"world": "glaskueste", "entry": entry}), 201)
    for entry, fact in (("mira", "Mira lügt."), ("kael", "Kael rudert.")):
        _ok(client.post(f"{story}/facts", json={"entry": entry, "fact": fact}), 201)
    _ok(client.patch(story, json={"controlled_characters": ["mira", "kael"]}))
    _ok(client.post(f"{SALZ}/stories", json={"title": "Ohne Gast", "form": "fragment"}), 201)
    _ok(client.post(f"{GLAS}/stories", json={"title": "Glasnacht", "form": "kurzgeschichte"}), 201)
    _ok(client.put(f"{GLAS}/stories/glasnacht/chapters/1", json={"text": "Splitter im Sand."}))


def test_archive_and_restore_a_world(logged_in: TestClient) -> None:
    _set_up(logged_in)
    assert _ok(logged_in.post(f"{GLAS}/archive"))["archived"] is True
    listed = _ok(logged_in.get("/api/worlds"))
    assert [(w["id"], w["archived"]) for w in listed] == [
        ("die-salzmark", False),
        ("glaskueste", True),
    ]
    # Existing guests still resolve; a new guest link can still be made through the API.
    _ok(logged_in.get(f"{GLAS}/entries/mira"))
    assert _ok(logged_in.post(f"{GLAS}/restore"))["archived"] is False


def test_preview_names_the_consequences(logged_in: TestClient) -> None:
    _set_up(logged_in)
    preview = _ok(logged_in.get(f"{GLAS}/deletion-preview"))
    assert preview == {
        "name": "Glasküste",
        "entries": 3,
        "images": 0,
        "maps": 0,
        "stories": 1,
        "guest_uses": [
            {
                "world": "die-salzmark",
                "world_name": "Die Salzmark",
                "story": "die-ueberfahrt",
                "story_title": "Die Überfahrt",
                "guests": ["Mira", "Kael", "Vale"],
                # "kael" also names an entry of the Salzmark; its fact may mean that one.
                "facts": 1,
            }
        ],
    }
    assert _ok(logged_in.get(f"{SALZ}/deletion-preview")) == {
        "name": "Die Salzmark",
        "entries": 1,
        "images": 0,
        "maps": 0,
        "stories": 2,
        "guest_uses": [],
    }


def test_deleting_needs_the_archive_and_the_exact_name(logged_in: TestClient) -> None:
    _set_up(logged_in)
    refused = logged_in.request("DELETE", GLAS, json={"name": "Glasküste"})
    assert refused.status_code == 422
    assert "archiviert" in refused.json()["detail"]
    _ok(logged_in.post(f"{GLAS}/archive"))
    for wrong in ("glasküste", "Glaskueste", "Die Salzmark"):
        refused = logged_in.request("DELETE", GLAS, json={"name": wrong})
        assert refused.status_code == 422
        assert "Name" in refused.json()["detail"]
    assert logged_in.request("DELETE", GLAS, json={}).status_code == 422
    # Nothing changed in the other world.
    assert len(_ok(logged_in.get(f"{SALZ}/stories/die-ueberfahrt"))["guest_links"]) == 3
    missing = logged_in.request("DELETE", "/api/worlds/gibt-es-nicht", json={"name": "x"})
    assert missing.status_code == 404


def test_deleting_a_world_removes_its_guests_in_other_worlds(
    logged_in: TestClient, data_dir: Path
) -> None:
    _set_up(logged_in)
    store_root = data_dir
    index = DocumentStore(data_dir)
    usage = store_root / "system" / "verbrauch"
    usage.mkdir(parents=True, exist_ok=True)
    (usage / "2026-11.md").write_text("---\neintraege: []\n---\n", encoding="utf-8")
    usage_before = sorted((p.name, p.read_bytes()) for p in usage.iterdir())
    assert index.search("glaskueste", "mi") != []
    assert index.search("glaskueste", "splitter", "fulltext") != []
    _ok(logged_in.post(f"{GLAS}/archive"))

    _ok(logged_in.request("DELETE", GLAS, json={"name": "Glasküste"}), 204)

    assert not (store_root / "worlds" / "glaskueste").exists()
    assert [w["id"] for w in _ok(logged_in.get("/api/worlds"))] == ["die-salzmark"]
    story = _ok(logged_in.get(f"{SALZ}/stories/die-ueberfahrt"))
    assert story["guest_links"] == []
    # "kael" stays: it names the Salzmark's own Kael as well.
    assert story["facts"] == [{"entry": "kael", "fact": "Kael rudert."}]
    assert story["controlled_characters"] == ["kael"]
    assert logged_in.get(f"{GLAS}/entries/mira").status_code == 404
    assert index.search("glaskueste", "mi") == []
    assert index.search("glaskueste", "splitter", "fulltext") == []
    assert sorted((p.name, p.read_bytes()) for p in usage.iterdir()) == usage_before


def test_archive_restore_and_delete_a_story(logged_in: TestClient, data_dir: Path) -> None:
    _set_up(logged_in)
    story = f"{GLAS}/stories/glasnacht"
    assert _ok(logged_in.get(f"{story}/deletion-preview")) == {
        "title": "Glasnacht",
        "chapters": 1,
        "facts": 0,
        "cover": False,
    }
    refused = logged_in.request("DELETE", story, json={"title": "Glasnacht"})
    assert refused.status_code == 422
    assert _ok(logged_in.post(f"{story}/archive"))["archived"] is True
    assert _ok(logged_in.post(f"{story}/restore"))["archived"] is False
    _ok(logged_in.post(f"{story}/archive"))
    assert logged_in.request("DELETE", story, json={"title": "glasnacht"}).status_code == 422

    _ok(logged_in.request("DELETE", story, json={"title": "Glasnacht"}), 204)

    assert _ok(logged_in.get(f"{GLAS}/stories")) == []
    assert not (data_dir / "worlds" / "glaskueste" / "stories" / "glasnacht").exists()
    assert logged_in.get(f"{story}/chapters").status_code == 404


def test_story_routes_need_the_world(logged_in: TestClient) -> None:
    missing = "/api/worlds/gibt-es-nicht/stories/x"
    for method, path in (
        ("POST", f"{missing}/archive"),
        ("POST", f"{missing}/restore"),
        ("GET", f"{missing}/deletion-preview"),
        ("DELETE", f"{missing}/chapters/1"),
    ):
        assert logged_in.request(method, path).status_code == 404
    assert logged_in.request("DELETE", missing, json={"title": "x"}).status_code == 404


def test_delete_a_middle_chapter(logged_in: TestClient) -> None:
    _set_up(logged_in)
    story = f"{SALZ}/stories/die-ueberfahrt"
    for number, title in ((1, "Aufbruch"), (2, "Sturm"), (3, "Ankunft")):
        _ok(logged_in.put(f"{story}/chapters/{number}", json={"title": title, "text": title}))
        _ok(
            logged_in.post(
                f"{story}/chapters/{number}/instructions",
                json={"instruction": "Weiter", "text": f"Verlauf {title}"},
            ),
            201,
        )

    remaining = _ok(logged_in.delete(f"{story}/chapters/2"))

    assert [(c["number"], c["title"]) for c in remaining] == [
        (1, "Aufbruch"),
        (2, "Ankunft"),
    ]
    notes = _ok(logged_in.get(f"{story}/chapters/2/instructions"))
    assert [n["text"] for n in notes] == ["Verlauf Ankunft"]
    assert logged_in.get(f"{story}/chapters/3").status_code == 404
    assert logged_in.delete(f"{story}/chapters/3").status_code == 404


def test_preview_and_delete_with_several_stories_and_a_vanished_guest(
    logged_in: TestClient,
) -> None:
    _set_up(logged_in)
    second = f"{SALZ}/stories/ohne-gast"
    _ok(logged_in.post(f"{second}/guests", json={"world": "glaskueste", "entry": "mira"}), 201)
    _ok(logged_in.post(f"{second}/facts", json={"entry": "mira", "fact": "Mira wartet."}), 201)
    # An entry deleted on its own leaves its guest link behind; the preview names its identifier.
    _ok(logged_in.delete(f"{GLAS}/entries/vale"), 204)

    preview = _ok(logged_in.get(f"{GLAS}/deletion-preview"))
    assert [(u["story"], u["guests"], u["facts"]) for u in preview["guest_uses"]] == [
        ("die-ueberfahrt", ["Mira", "Kael", "vale"], 1),
        ("ohne-gast", ["Mira"], 1),
    ]
    _ok(logged_in.post(f"{GLAS}/archive"))
    _ok(logged_in.request("DELETE", GLAS, json={"name": "Glasküste"}), 204)
    for story in (f"{SALZ}/stories/die-ueberfahrt", second):
        assert _ok(logged_in.get(story))["guest_links"] == []
    assert _ok(logged_in.get(second))["facts"] == []
