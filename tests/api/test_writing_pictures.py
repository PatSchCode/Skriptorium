"""Main images of named entries go along when writing, on request (step 10.7, ADR-111)."""

import base64
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from skriptorium.api.flows import WriteOrder, prepare_request
from skriptorium.api.flows.writing import MAX_PICTURES, PICTURE_TOKENS
from skriptorium.storage import InvalidInput
from tests.api.conftest import FakeProvider
from tests.api.test_writing import WRITE, _builder, _events, _guest, writer
from tests.image_samples import jpeg, png

__all__ = ["writer"]

MODEL = "x-ai/grok-4.6"


def _picture(client: TestClient, entry: str, data: bytes, world: str = "die-salzmark") -> None:
    response = client.post(
        f"/api/worlds/{world}/entries/{entry}/images",
        json={"content": base64.b64encode(data).decode()},
    )
    assert response.status_code == 201, response.text


def test_without_the_switch_the_request_stays_the_same(
    writer: TestClient, provider: FakeProvider
) -> None:
    _picture(writer, "kael", png())
    order = {"instruction": "Kael rudert.", "references": ["kael"], "model": MODEL}

    plain = writer.post(WRITE, json=order)
    off = writer.post(WRITE, json={**order, "images": False})
    _picture(writer, "kael", jpeg())
    unpictured = writer.post(WRITE, json={**order, "references": ["runenklinge"]})
    unpictured_on = writer.post(
        WRITE, json={**order, "references": ["runenklinge"], "images": True}
    )

    first, second, third, fourth = provider.requests
    assert first.messages == second.messages
    assert third.messages == fourth.messages
    assert all(m.images == () for r in provider.requests for m in r.messages)
    assert "# Bilder" not in third.messages[1].content
    for response in (plain, off, unpictured_on):
        assert _events(response.text)[0][1]["images"] == 0
    assert unpictured.status_code == 200


def test_main_images_of_named_entries_go_along_in_order_at_most_four(
    writer: TestClient, provider: FakeProvider
) -> None:
    _guest(writer)
    _picture(writer, "kael", png())
    _picture(writer, "kael", jpeg())
    _picture(writer, "mira", jpeg())
    _picture(writer, "hafen-von-grauwasser", png())
    _picture(writer, "nebelkoenig", jpeg(), world="nebelreich")
    _picture(writer, "reifpalast", png(), world="nebelreich")
    order = {
        "instruction": "Alle treffen sich.",
        "references": ["kael", "runenklinge", "mira", "hafen-von-grauwasser", "nebelkoenig"],
        "model": MODEL,
    }
    without = writer.post(WRITE, json=order)

    response = writer.post(
        WRITE, json={**order, "images": True, "scene": {"place": "reifpalast", "goal": "Treffen"}}
    )

    assert response.status_code == 200, response.text
    request = provider.requests[1]
    system, user = request.messages
    assert system.images == ()
    assert [(part.media_type, part.data) for part in user.images] == [
        ("image/png", png()),
        ("image/jpeg", jpeg()),
        ("image/png", png()),
        ("image/jpeg", jpeg()),
    ]
    assert len(user.images) == MAX_PICTURES
    pictures = user.content.split("# Bilder\n\n")[1].split("\n\n# Anweisung")[0]
    assert "- Bild 1: Kael\n- Bild 2: Mira\n- Bild 3: Hafen von Grauwasser\n" in pictures
    assert "- Bild 4: Nebelkönig\n\n" in pictures
    assert "Reifpalast" not in pictures and "Runenklinge" not in pictures
    assert "gilt der Text" in pictures
    start = _events(response.text)[0][1]
    base = _events(without.text)[0][1]["estimated_tokens"]
    assert start["images"] == MAX_PICTURES
    assert start["estimated_tokens"] >= base + MAX_PICTURES * PICTURE_TOKENS


def test_the_place_and_characters_of_a_new_scene_count_as_named(
    writer: TestClient, provider: FakeProvider
) -> None:
    _guest(writer)
    _picture(writer, "reifpalast", png(), world="nebelreich")
    _picture(writer, "kael", jpeg())

    response = writer.post(
        WRITE,
        json={
            "model": MODEL,
            "images": True,
            "scene": {"place": "reifpalast", "characters": ["kael"], "goal": "Ankunft"},
        },
    )

    assert response.status_code == 200, response.text
    user = provider.requests[0].messages[1]
    assert [part.data for part in user.images] == [png(), jpeg()]
    assert "- Bild 1: Reifpalast\n- Bild 2: Kael" in user.content


def test_only_models_that_read_images_take_them(
    writer: TestClient, provider: FakeProvider, tmp_path: Path
) -> None:
    _picture(writer, "kael", png())
    order = {"references": ["kael"], "images": True}

    blind = writer.post(WRITE, json={**order, "model": "deepseek/deepseek-v3.2"})

    assert blind.status_code == 422
    assert "keine Bilder" in blind.text
    assert provider.requests == []
    canon, manuscripts, builder = _builder(tmp_path)
    with pytest.raises(InvalidInput, match="keine Bilder"):
        prepare_request(
            canon, manuscripts, builder, WriteOrder("die-salzmark", "am-ufer", 1, images=True)
        )
