"""Resolution and quality of a generated image (step 10.5, ADR-109): catalog, price, request."""

import asyncio
import json

import httpx
import pytest

from skriptorium.ai_gateway import ImageCatalog, ImageOrder, ImagePrice, OpenRouterImageProvider
from skriptorium.ai_gateway.images import ImageEndpoint, level_price

KEY = "sk-or-test-key-not-real"


def _enum(*values: object) -> dict[str, object]:
    return {"type": "enum", "values": list(values)}


MODELS = {
    "data": [
        {
            "id": "seed/seedream",
            "name": "Seedream",
            "supported_parameters": {"resolution": _enum("1K", "2K", "1K")},
        },
        {
            "id": "x-ai/grok-imagine",
            "name": "Grok Imagine",
            "supported_parameters": {
                "resolution": _enum("1K", "2K"),
                "quality": _enum("low", "medium"),
            },
        },
        {
            "id": "google/gemini-image",
            "name": "Gemini",
            "supported_parameters": {"resolution": _enum("1K", "2K", "4K", "2K; drop", 7)},
        },
        {"id": "black-forest-labs/flux.2-pro", "name": "FLUX.2 Pro", "supported_parameters": {}},
        {
            "id": "seed/seedream-lite",
            "name": "Seedream Lite",
            "supported_parameters": {"resolution": _enum("2K", "4K")},
        },
    ]
}
PRICES: dict[str, list[object]] = {
    "seed/seedream": [
        {"unit": "image", "cost_usd": 0.045},
        {"variant": "high_resolution", "unit": "image", "cost_usd": 0.09},
        {"billable": "input_image", "unit": "image", "cost_usd": 0.003},
    ],
    "x-ai/grok-imagine": [
        {"billable": "input_image", "unit": "image", "cost_usd": 0.01},
        {"variant": "low_1k", "unit": "image", "cost_usd": 0.04},
        {"variant": "low_2k", "unit": "image", "cost_usd": 0.06},
        {"variant": "medium_2k", "unit": "image", "cost_usd": 0.08},
    ],
    "google/gemini-image": [{"unit": "token", "cost_usd": 0.00012}],
    "black-forest-labs/flux.2-pro": [{"unit": "megapixel", "cost_usd": 0.03}],
    "seed/seedream-lite": [
        {"unit": "image", "cost_usd": 0.035},
        {"billable": "input_image", "unit": "image", "cost_usd": 0.003},
    ],
}


def _setup(*answers: httpx.Response) -> tuple[ImageCatalog, OpenRouterImageProvider, list[object]]:
    sent: list[object] = []
    queue = list(answers)

    def handler(request: httpx.Request) -> httpx.Response:
        path = request.url.path
        if path == "/api/v1/images/models":
            return httpx.Response(200, json=MODELS)
        if path.startswith("/api/v1/images/models/"):
            model = path.removeprefix("/api/v1/images/models/").removesuffix("/endpoints")
            endpoint = {"provider_slug": "p", "pricing": PRICES.get(model, [])}
            return httpx.Response(200, json={"endpoints": [endpoint]})
        sent.append(json.loads(request.content))
        return queue.pop(0)

    transport = httpx.MockTransport(handler)
    catalog = ImageCatalog(transport=transport)
    asyncio.run(catalog.refresh())
    return catalog, OpenRouterImageProvider(KEY, catalog, transport=transport), sent


def test_the_catalog_keeps_the_offered_levels_once_and_drops_odd_ones() -> None:
    catalog, _, _ = _setup()
    seed = catalog.model("seed/seedream")
    grok = catalog.model("x-ai/grok-imagine")
    gemini = catalog.model("google/gemini-image")
    flux = catalog.model("black-forest-labs/flux.2-pro")
    assert seed is not None and grok is not None and gemini is not None and flux is not None
    assert (seed.resolutions, seed.qualities) == (("1K", "2K"), ())
    assert (grok.resolutions, grok.qualities) == (("1K", "2K"), ("low", "medium"))
    assert gemini.resolutions == ("1K", "2K", "4K")
    assert (flux.resolutions, flux.qualities) == ((), ())
    assert catalog.model("fehlt/ganz") is None


@pytest.mark.parametrize(
    ("model", "resolution", "quality", "price"),
    [
        # A variant naming the level wins, quality and resolution together first.
        ("x-ai/grok-imagine", "2K", "medium", ImagePrice(0.08, "image")),
        ("x-ai/grok-imagine", "1K", "low", ImagePrice(0.04, "image")),
        # Not named and above the smallest: "high_resolution"; at the smallest: the base price.
        ("seed/seedream", "2K", None, ImagePrice(0.09, "image")),
        ("seed/seedream", "1K", None, ImagePrice(0.045, "image")),
        # A price per token holds for every level.
        ("google/gemini-image", "4K", None, ImagePrice(0.00012, "token")),
        # So does the base price of a provider without any variant (probe 2026-11-05).
        ("seed/seedream-lite", "4K", None, ImagePrice(0.035, "image")),
        ("seed/seedream-lite", "2K", None, ImagePrice(0.035, "image")),
        # Nothing names it: unknown, the real cost comes after generating.
        ("x-ai/grok-imagine", "1K", "medium", None),
        # Without a level as before.
        ("seed/seedream", None, None, ImagePrice(0.045, "image")),
        ("black-forest-labs/flux.2-pro", None, None, ImagePrice(0.03, "megapixel")),
    ],
)
def test_prices_per_level(
    model: str, resolution: str | None, quality: str | None, price: ImagePrice | None
) -> None:
    catalog, _, _ = _setup()
    assert asyncio.run(catalog.price(model, resolution, quality)) == price


def test_level_price_of_a_provider_without_prices() -> None:
    bare = ImageEndpoint("p", frozenset(), None)
    assert level_price(bare, "1K", "2K", None) is None
    assert level_price(bare, "1K", "1K", None) is None
    quality_only = ImageEndpoint(
        "p", frozenset(), None, None, (("high", ImagePrice(0.2, "image")),)
    )
    assert level_price(quality_only, None, None, "HIGH") == ImagePrice(0.2, "image")


def test_odd_variant_entries_are_left_out() -> None:
    catalog, _, _ = _setup()
    endpoints = asyncio.run(catalog.endpoints("x-ai/grok-imagine"))
    assert [name for name, _ in endpoints[0].variants] == ["low_1k", "low_2k", "medium_2k"]
    PRICES["x-ai/grok-imagine"].extend(
        [
            {"variant": "", "unit": "image", "cost_usd": 1},
            {"variant": "x", "unit": "image", "cost_usd": True},
            {"variant": "y", "unit": "image", "cost_usd": -1},
            {"variant": "z", "cost_usd": 1},
            "kein Eintrag",
        ]
    )
    try:
        fresh, _, _ = _setup()
        endpoints = asyncio.run(fresh.endpoints("x-ai/grok-imagine"))
        assert [name for name, _ in endpoints[0].variants] == ["low_1k", "low_2k", "medium_2k"]
    finally:
        del PRICES["x-ai/grok-imagine"][-5:]


def test_the_request_names_the_levels_only_when_chosen() -> None:
    answer = httpx.Response(200, json={"data": [{"b64_json": "iVBORw==", "media_type": "x"}]})
    _, adapter, sent = _setup(answer, answer)
    asyncio.run(adapter.generate(ImageOrder("x-ai/grok-imagine", "Turm", "2:3", None, "2K", "low")))
    asyncio.run(adapter.generate(ImageOrder("black-forest-labs/flux.2-pro", "Turm", "2:3")))
    first, second = sent
    assert isinstance(first, dict) and isinstance(second, dict)
    assert (first["resolution"], first["quality"]) == ("2K", "low")
    assert "resolution" not in second and "quality" not in second
