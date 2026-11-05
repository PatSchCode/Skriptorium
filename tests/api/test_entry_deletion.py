"""Deleting a canon entry with its traces in stories (step 10.1, ADR-106, V.43).

Deleting an entry used to leave facts, led characters and guest links with its identifier in
stories; a new entry with the same name would have inherited them. Now the preview names what
goes and the deletion takes it along, unless the identifier may also mean another entry of the
same story (the rule of ADR-098).
"""

import base64
from typing import Any

from fastapi.testclient import TestClient
from httpx import Response

from tests.image_samples import png

SALZ = "/api/worlds/die-salzmark"
NORD = "/api/worlds/nordland"
UFER = f"{SALZ}/stories/am-ufer"
EIS = f"{NORD}/stories/eisgang"


def _ok(response: Response, status: int = 200) -> Any:
    assert response.status_code == status, response.text
    return response.json() if response.content else None


def _set_up(client: TestClient) -> None:
    """Kael lives in the Salzmark: led, with facts, an image and a marker; a guest in Nordland."""
    _ok(client.post("/api/worlds", json={"name": "Die Salzmark"}), 201)
    _ok(client.post("/api/worlds", json={"name": "Nordland"}), 201)
    for name in ("Kael", "Mira"):
        _ok(client.post(f"{SALZ}/entries", json={"category": "figur", "name": name}), 201)
    _ok(
        client.post(
            f"{SALZ}/entries",
            json={"category": "ort", "name": "Hafen", "body": "Hier wartet @Kael."},
        ),
        201,
    )
    content = base64.b64encode(png()).decode()
    _ok(client.post(f"{SALZ}/entries/kael/images", json={"content": content}), 201)
    added = _ok(client.post(f"{SALZ}/maps", json={"name": "Inseln", "content": content}), 201)
    file = added["maps"][0]["file"]
    _ok(
        client.put(
            f"{SALZ}/maps/{file}/markers",
            json={
                "markers": [
                    {"entry": "kael", "x": 0.1, "y": 0.2},
                    {"entry": "mira", "x": 0.3, "y": 0.4},
                ]
            },
        )
    )
    _ok(client.post(f"{SALZ}/stories", json={"title": "Am Ufer", "form": "roman"}), 201)
    for fact in ("Kael rudert.", "Kael schweigt."):
        _ok(client.post(f"{UFER}/facts", json={"entry": "kael", "fact": fact}), 201)
    _ok(client.post(f"{UFER}/facts", json={"entry": "mira", "fact": "Mira lacht."}), 201)
    _ok(client.patch(UFER, json={"controlled_characters": ["kael", "mira"]}))
    _ok(client.post(f"{SALZ}/stories", json={"title": "Ohne Kael", "form": "fragment"}), 201)

    _ok(client.post(f"{NORD}/stories", json={"title": "Eisgang", "form": "kurzgeschichte"}), 201)
    _ok(client.post(f"{EIS}/guests", json={"world": "die-salzmark", "entry": "kael"}), 201)
    _ok(client.put(f"{EIS}/guests/die-salzmark/kael", json={"relation": "Kam übers Eis."}))
    _ok(client.post(f"{EIS}/facts", json={"entry": "kael", "fact": "Kael friert."}), 201)
    _ok(client.patch(EIS, json={"controlled_characters": ["kael"]}))


def test_preview_names_images_markers_and_every_story(logged_in: TestClient) -> None:
    _set_up(logged_in)

    preview = _ok(logged_in.get(f"{SALZ}/entries/kael/deletion-preview"))

    assert preview == {
        "name": "Kael",
        "images": 1,
        "markers": 1,
        "uses": [
            {
                "world": "die-salzmark",
                "world_name": "Die Salzmark",
                "story": "am-ufer",
                "story_title": "Am Ufer",
                "guest": False,
                "relation": False,
                "led": True,
                "facts": 2,
            },
            {
                "world": "nordland",
                "world_name": "Nordland",
                "story": "eisgang",
                "story_title": "Eisgang",
                "guest": True,
                "relation": True,
                "led": True,
                "facts": 1,
            },
        ],
    }
    # The preview changes nothing.
    assert _ok(logged_in.get(UFER))["controlled_characters"] == ["kael", "mira"]


def test_an_entry_without_traces_shows_nothing_else(logged_in: TestClient) -> None:
    _set_up(logged_in)
    preview = _ok(logged_in.get(f"{SALZ}/entries/hafen/deletion-preview"))
    assert preview == {"name": "Hafen", "images": 0, "markers": 0, "uses": []}


def test_delete_takes_the_traces_along_and_a_new_entry_starts_clean(
    logged_in: TestClient,
) -> None:
    _set_up(logged_in)

    _ok(logged_in.delete(f"{SALZ}/entries/kael"), 204)

    ufer = _ok(logged_in.get(UFER))
    assert ufer["controlled_characters"] == ["mira"]
    assert ufer["facts"] == [{"entry": "mira", "fact": "Mira lacht."}]
    eis = _ok(logged_in.get(EIS))
    assert (eis["guest_links"], eis["facts"], eis["controlled_characters"]) == ([], [], [])
    world = _ok(logged_in.get(SALZ))
    assert [m["entry"] for m in world["maps"][0]["markers"]] == ["mira"]
    # The mention in another entry stays as text.
    assert _ok(logged_in.get(f"{SALZ}/entries/hafen"))["body"] == "Hier wartet @Kael."

    _ok(logged_in.post(f"{SALZ}/entries", json={"category": "figur", "name": "Kael"}), 201)
    again = _ok(logged_in.get(f"{SALZ}/entries/kael/deletion-preview"))
    assert again["uses"] == []


def test_traces_that_may_mean_another_entry_stay(logged_in: TestClient) -> None:
    _set_up(logged_in)
    # Nordland has its own "Kael", so the fact and the led character in Eisgang may mean it.
    _ok(logged_in.post(f"{NORD}/entries", json={"category": "figur", "name": "Kael"}), 201)
    # A story of the Salzmark binds in Nordland's Kael as a guest with the same identifier.
    _ok(logged_in.post(f"{SALZ}/stories", json={"title": "Zwei Kael", "form": "fragment"}), 201)
    zwei = f"{SALZ}/stories/zwei-kael"
    _ok(logged_in.post(f"{zwei}/guests", json={"world": "nordland", "entry": "kael"}), 201)
    _ok(logged_in.post(f"{zwei}/facts", json={"entry": "kael", "fact": "Kael ist fremd."}), 201)

    preview = _ok(logged_in.get(f"{SALZ}/entries/kael/deletion-preview"))
    assert [(u["story"], u["guest"], u["led"], u["facts"]) for u in preview["uses"]] == [
        ("am-ufer", False, True, 2),
        ("eisgang", True, False, 0),
    ]

    _ok(logged_in.delete(f"{SALZ}/entries/kael"), 204)

    eis = _ok(logged_in.get(EIS))
    assert eis["guest_links"] == []
    assert eis["facts"] == [{"entry": "kael", "fact": "Kael friert."}]
    assert eis["controlled_characters"] == ["kael"]
    zwei_kael = _ok(logged_in.get(zwei))
    assert zwei_kael["guest_links"] == [{"world": "nordland", "entry": "kael", "relation": ""}]
    assert zwei_kael["facts"] == [{"entry": "kael", "fact": "Kael ist fremd."}]


def test_unknown_entries(logged_in: TestClient) -> None:
    _set_up(logged_in)
    assert logged_in.get(f"{SALZ}/entries/niemand/deletion-preview").status_code == 404
    assert logged_in.delete(f"{SALZ}/entries/niemand").status_code == 404
    assert logged_in.get("/api/worlds/fehlt/entries/kael/deletion-preview").status_code == 404
    assert _ok(logged_in.get(UFER))["controlled_characters"] == ["kael", "mira"]


def test_several_stories_of_another_world_with_the_guest(logged_in: TestClient) -> None:
    _set_up(logged_in)
    schnee = f"{NORD}/stories/schnee"
    _ok(logged_in.post(f"{NORD}/stories", json={"title": "Schnee", "form": "fragment"}), 201)
    _ok(logged_in.post(f"{schnee}/guests", json={"world": "die-salzmark", "entry": "kael"}), 201)

    preview = _ok(logged_in.get(f"{SALZ}/entries/kael/deletion-preview"))
    assert [(u["story"], u["relation"]) for u in preview["uses"]] == [
        ("am-ufer", False),
        ("eisgang", True),
        ("schnee", False),
    ]
    _ok(logged_in.delete(f"{SALZ}/entries/kael"), 204)
    assert _ok(logged_in.get(schnee))["guest_links"] == []
