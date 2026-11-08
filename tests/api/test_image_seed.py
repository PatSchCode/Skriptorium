"""A fixed start value when generating images, and the full origin (step 11.4, ADR-121)."""

import base64

import pytest
from fastapi.testclient import TestClient

from skriptorium.api.image_routes import MAX_SEED
from tests.api.conftest import FakeImages, FakeRunware
from tests.image_samples import png

FLEX = "black-forest-labs/flux.2-flex"
PRO = "black-forest-labs/flux.2-pro"
EPIC = "civitai:277058@1405120"
CUFFS = "civitai:536201@596079"
WORLD = "/api/worlds/die-salzmark"
ENTRY = f"{WORLD}/entries/gunda"


def _order(model: str, **extra: object) -> dict[str, object]:
    return {"model": model, "prompt": "Eine Wirtin", "aspect_ratio": "2:3", **extra}


def test_the_list_names_the_models_that_take_a_start_value(logged_in: TestClient) -> None:
    models = {m["id"]: m["seed"] for m in logged_in.get("/api/images/models").json()["models"]}
    assert models[FLEX] is True
    assert models[PRO] is False


def test_without_a_start_value_the_server_draws_one(
    logged_in: TestClient, images: FakeImages
) -> None:
    body = logged_in.post("/api/images/generate", json=_order(FLEX)).json()
    (order,) = images.orders
    assert order.seed is not None and 1 <= order.seed <= MAX_SEED
    assert body["seed"] == order.seed
    assert body["appended"] is None


def test_a_fixed_start_value_goes_along(logged_in: TestClient, images: FakeImages) -> None:
    body = logged_in.post("/api/images/generate", json=_order(FLEX, seed=42)).json()
    assert images.orders[-1].seed == 42
    assert body["seed"] == 42


def test_a_model_without_start_value_gets_none(logged_in: TestClient, images: FakeImages) -> None:
    body = logged_in.post("/api/images/generate", json=_order(PRO)).json()
    assert images.orders[-1].seed is None
    assert body["seed"] is None
    refused = logged_in.post("/api/images/generate", json=_order(PRO, seed=42))
    assert refused.status_code == 422
    assert "keinen Startwert" in refused.text


@pytest.mark.parametrize("seed", [0, MAX_SEED + 1, -3, "7x"])
def test_the_start_value_is_bounded(logged_in: TestClient, seed: object) -> None:
    response = logged_in.post("/api/images/generate", json=_order(FLEX, seed=seed))
    assert response.status_code == 422


def test_runware_always_gets_a_start_value_and_names_the_appended_text(
    logged_in: TestClient, runware_server: FakeRunware
) -> None:
    logged_in.post("/api/images/runware", json={"reference": CUFFS})
    logged_in.put(
        "/api/images/runware",
        json={
            "models": [{"id": EPIC, "name": "Epic", "addition": "raw photo"}],
            "loras": [{"id": CUFFS, "name": "Cuffs", "trigger": "handcuffs", "weight": 0.8}],
        },
    )
    drawn = logged_in.post("/api/images/generate", json=_order(EPIC)).json()
    seed = runware_server.tasks[-1]["seed"]
    assert isinstance(seed, int) and 1 <= seed <= MAX_SEED
    assert drawn["seed"] == seed
    assert drawn["appended"] == "raw photo"

    fixed = logged_in.post(
        "/api/images/generate",
        json=_order(EPIC, seed=seed, loras=[{"id": CUFFS, "weight": 0.6}]),
    ).json()
    assert runware_server.tasks[-1]["seed"] == seed
    assert fixed["appended"] == "raw photo, handcuffs"


def test_the_origin_keeps_start_value_loras_and_appended_text(logged_in: TestClient) -> None:
    logged_in.post("/api/worlds", json={"name": "Die Salzmark", "description": ""})
    logged_in.post(f"{WORLD}/entries", json={"category": "figur", "name": "Gunda"})
    origin = {
        "model": EPIC,
        "prompt": "Gunda am Salzhafen",
        "aspect_ratio": "2:3",
        "cost_usd": 0.0031,
        "seed": 1834072215,
        "loras": [{"id": CUFFS, "name": "Cuffs", "weight": 0.6}],
        "appended": "raw photo, handcuffs",
    }
    content = base64.b64encode(png()).decode()
    added = logged_in.post(f"{ENTRY}/images", json={"content": content, "herkunft": origin})
    assert added.status_code in (200, 201), added.text
    image = added.json()["images"][-1]
    found = logged_in.get(f"{ENTRY}/images/{image}/origin").json()
    assert {k: found[k] for k in origin} == origin

    without = {k: v for k, v in origin.items() if k not in ("seed", "loras", "appended")}
    plain = logged_in.post(f"{ENTRY}/images", json={"content": content, "herkunft": without})
    old = logged_in.get(f"{ENTRY}/images/{plain.json()['images'][-1]}/origin").json()
    assert (old["seed"], old["loras"], old["appended"]) == (None, [], None)


@pytest.mark.parametrize(
    "change",
    [
        {"seed": 0},
        {"loras": [{"id": CUFFS, "name": "Cuffs", "weight": 3}]},
        {"loras": [{"id": f"a:b@{i}", "name": "x", "weight": 1} for i in range(6)]},
        {"appended": "x" * 4001},
    ],
)
def test_the_origin_refuses_odd_values(logged_in: TestClient, change: dict[str, object]) -> None:
    logged_in.post("/api/worlds", json={"name": "Die Salzmark", "description": ""})
    logged_in.post(f"{WORLD}/entries", json={"category": "figur", "name": "Gunda"})
    origin = {"model": EPIC, "prompt": "Gunda", "aspect_ratio": "2:3", **change}
    content = base64.b64encode(png()).decode()
    response = logged_in.post(f"{ENTRY}/images", json={"content": content, "herkunft": origin})
    assert response.status_code == 422
