"""Resolution and quality over the API (step 10.5, ADR-109): list, price, order, origin."""

import base64

from fastapi.testclient import TestClient

from tests.api.conftest import FakeImages
from tests.image_samples import png

SEED = "bytedance-seed/seedream-4.5"
FLUX = "black-forest-labs/flux.2-pro"
ORDER = {"model": SEED, "prompt": "Ein Turm", "aspect_ratio": "2:3"}


def test_the_list_names_the_levels_of_each_model(logged_in: TestClient) -> None:
    models = {m["id"]: m for m in logged_in.get("/api/images/models").json()["models"]}
    assert (models[SEED]["resolutions"], models[SEED]["qualities"]) == (
        ["1K", "2K"],
        ["auto", "high"],
    )
    assert (models[FLUX]["resolutions"], models[FLUX]["qualities"]) == ([], [])


def test_the_price_follows_the_level(logged_in: TestClient) -> None:
    def price(**levels: str) -> object:
        answer = logged_in.get("/api/images/price", params={"model": SEED, **levels})
        assert answer.status_code == 200, answer.text
        return answer.json()["cost_usd"]

    assert price() == 0.04
    assert price(resolution="1K") == 0.04
    assert price(resolution="2K") == 0.08
    assert price(resolution="2K", quality="high") == 0.08
    for levels in ({"resolution": "4K"}, {"quality": "low"}, {"resolution": "x" * 21}):
        answer = logged_in.get("/api/images/price", params={"model": SEED, **levels})
        assert answer.status_code == 422
    flux = logged_in.get("/api/images/price", params={"model": FLUX, "resolution": "2K"})
    assert flux.status_code == 422


def test_an_order_carries_the_levels_the_model_offers(
    logged_in: TestClient, images: FakeImages
) -> None:
    answer = logged_in.post(
        "/api/images/generate", json={**ORDER, "resolution": "2K", "quality": "high"}
    )
    assert answer.status_code == 200, answer.text
    answer = logged_in.post("/api/images/generate", json=ORDER)
    assert answer.status_code == 200, answer.text
    first, second = images.orders
    assert (first.resolution, first.quality) == ("2K", "high")
    assert (second.resolution, second.quality) == (None, None)


def test_an_order_with_a_level_the_model_lacks_is_refused(
    logged_in: TestClient, images: FakeImages
) -> None:
    for wrong in (
        {**ORDER, "resolution": "4K"},
        {**ORDER, "quality": "max"},
        {**ORDER, "model": FLUX, "resolution": "2K"},
        {**ORDER, "model": "gibt/es-nicht"},
    ):
        answer = logged_in.post("/api/images/generate", json=wrong)
        assert answer.status_code == 422, wrong
    assert images.orders == []


def test_the_origin_keeps_the_levels(logged_in: TestClient) -> None:
    world = "/api/worlds/die-salzmark"
    logged_in.post("/api/worlds", json={"name": "Die Salzmark", "description": ""})
    logged_in.post(f"{world}/entries", json={"category": "ort", "name": "Turm"})
    origin = {"model": SEED, "prompt": "Ein Turm", "aspect_ratio": "3:2", "cost_usd": 0.08}
    content = base64.b64encode(png()).decode()
    added = logged_in.post(
        f"{world}/entries/turm/images",
        json={"content": content, "herkunft": {**origin, "resolution": "2K", "quality": "high"}},
    )
    assert added.status_code == 201, added.text
    plain = logged_in.post(
        f"{world}/entries/turm/images", json={"content": content, "herkunft": origin}
    )
    with_levels, without = plain.json()["images"]
    found = logged_in.get(f"{world}/entries/turm/images/{with_levels}/origin").json()
    assert (found["resolution"], found["quality"]) == ("2K", "high")
    found = logged_in.get(f"{world}/entries/turm/images/{without}/origin").json()
    assert (found["resolution"], found["quality"]) == (None, None)
