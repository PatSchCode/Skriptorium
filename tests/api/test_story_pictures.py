"""Pictures of a story over HTTP (step 10.6, ADR-110): upload, read, origin."""

import base64

from fastapi.testclient import TestClient

from tests.image_samples import jpeg, png

WORLD = "/api/worlds/die-salzmark"
STORY = f"{WORLD}/stories/das-salz"
ORIGIN = {"model": "m/x", "prompt": "Hafen im Nebel", "aspect_ratio": "3:2", "cost_usd": 0.035}


def _setup(client: TestClient) -> None:
    client.post("/api/worlds", json={"name": "Die Salzmark", "description": ""})
    client.post(f"{WORLD}/stories", json={"title": "Das Salz", "form": "kurzgeschichte"})


def _content(data: bytes) -> str:
    return base64.b64encode(data).decode()


def test_stores_and_serves_a_picture_with_its_origin(logged_in: TestClient) -> None:
    _setup(logged_in)
    made = logged_in.post(f"{STORY}/images", json={"content": _content(jpeg()), "herkunft": ORIGIN})
    assert made.status_code == 201, made.text
    file = made.json()["file"]
    assert file.startswith("bild-") and file.endswith(".jpg")
    served = logged_in.get(f"{STORY}/images/{file}")
    assert served.status_code == 200
    assert served.content == jpeg()
    assert served.headers["content-type"] == "image/jpeg"
    origin = logged_in.get(f"{STORY}/images/{file}/origin").json()
    assert {k: origin[k] for k in ORIGIN} == ORIGIN
    uploaded = logged_in.post(f"{STORY}/images", json={"content": _content(png())}).json()["file"]
    assert logged_in.get(f"{STORY}/images/{uploaded}/origin").json() is None


def test_refuses_unreadable_content_and_unknown_pictures(logged_in: TestClient) -> None:
    _setup(logged_in)
    assert logged_in.post(f"{STORY}/images", json={"content": "%%%"}).status_code == 422
    svg = _content(b"<svg/>")
    assert logged_in.post(f"{STORY}/images", json={"content": svg}).status_code == 422
    missing = f"{WORLD}/stories/gibt-es-nicht/images"
    assert logged_in.post(missing, json={"content": _content(jpeg())}).status_code == 404
    for name in ("bild-0123456789ab.jpg", "story.md", "titelbild-0123456789ab.jpg"):
        assert logged_in.get(f"{STORY}/images/{name}").status_code == 404
        assert logged_in.get(f"{STORY}/images/{name}/origin").status_code == 404


def test_pictures_need_a_session(client: TestClient) -> None:
    assert client.get(f"{STORY}/images/bild-0123456789ab.jpg").status_code == 401
