"""Tests of the Runware adapter (roadmap step 10.8, ADR-115)."""

import asyncio
import base64
import json
import logging
from collections.abc import Callable

import httpx
import pytest

from skriptorium.ai_gateway import (
    ImageOrder,
    ImageReference,
    InvalidRequest,
    LoraChoice,
    ModelRefused,
    ProviderUnavailable,
    RateLimited,
    RunwareImageProvider,
    full_prompt,
)
from skriptorium.ai_gateway.runware import CHECK_CONTENT, MAX_PROMPT_CHARS, SIZES
from tests.image_samples import png

KEY = "rw-test-schluessel"

Handler = Callable[[httpx.Request], httpx.Response]


def _row(request: httpx.Request, **fields: object) -> httpx.Response:
    task = json.loads(request.content)[0]
    return httpx.Response(200, json={"data": [{"taskUUID": task["taskUUID"], **fields}]})


def _adapter(handler: Handler) -> RunwareImageProvider:
    return RunwareImageProvider(KEY, transport=httpx.MockTransport(handler))


def _image_handler(seen: list[httpx.Request], **extra: object) -> Handler:
    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        fields: dict[str, object] = {
            "imageBase64Data": base64.b64encode(png(832, 1216)).decode("ascii"),
            "cost": 0.0025,
        }
        fields.update(extra)
        return _row(request, **fields)

    return handler


def test_generate_sends_the_fixed_settings_and_returns_the_image() -> None:
    seen: list[httpx.Request] = []
    adapter = _adapter(_image_handler(seen))
    order = ImageOrder(
        "civitai:277058@1405120",
        "Kael am Fluss",
        "2:3",
        loras=(LoraChoice("civitai:536201@596079", 0.8),),
    )
    image = asyncio.run(adapter.generate(order))
    asyncio.run(adapter.aclose())
    assert image.data == png(832, 1216)
    assert image.cost_usd == 0.0025
    request = seen[0]
    assert request.url == "https://api.runware.ai/v1"
    assert request.headers["authorization"] == f"Bearer {KEY}"
    task = json.loads(request.content)[0]
    assert task["taskType"] == "imageInference"
    assert task["model"] == "civitai:277058@1405120"
    assert task["positivePrompt"] == "Kael am Fluss"
    assert (task["width"], task["height"]) == SIZES["2:3"]
    assert task["outputType"] == "base64Data"
    assert task["includeCost"] is True
    assert task["safety"] == {"checkContent": False}
    assert CHECK_CONTENT is False
    assert task["lora"] == [{"model": "civitai:536201@596079", "weight": 0.8}]


def test_generate_without_loras_sends_none_and_bounds_the_prompt() -> None:
    seen: list[httpx.Request] = []
    adapter = _adapter(_image_handler(seen))
    asyncio.run(adapter.generate(ImageOrder("runware:400@1", "x" * 5000, "1:1")))
    task = json.loads(seen[0].content)[0]
    assert "lora" not in task
    assert len(task["positivePrompt"]) == MAX_PROMPT_CHARS


@pytest.mark.parametrize(
    "order",
    [
        ImageOrder("runware:400@1", "x", "5:4"),
        ImageOrder("runware:400@1", "x", "1:1", reference=ImageReference(b"x", "image/png")),
        ImageOrder("runware:400@1", "x", "1:1", resolution="2K"),
        ImageOrder("runware:400@1", "x", "1:1", quality="high"),
        ImageOrder(
            "runware:400@1", "x", "1:1", loras=tuple(LoraChoice(f"a:b@{i}", 1) for i in range(6))
        ),
    ],
)
def test_generate_refuses_what_runware_does_not_take_here(order: ImageOrder) -> None:
    seen: list[httpx.Request] = []
    with pytest.raises(InvalidRequest):
        asyncio.run(_adapter(_image_handler(seen)).generate(order))
    assert seen == []


@pytest.mark.parametrize(
    ("cost", "expected"),
    [(0.01, 0.01), (None, None), (float("nan"), None), (-1, None), (True, None), ("1", None)],
)
def test_generate_takes_only_a_sensible_cost(cost: object, expected: float | None) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        task = json.loads(request.content)[0]
        row = {
            "taskUUID": task["taskUUID"],
            "imageBase64Data": base64.b64encode(png()).decode("ascii"),
            "cost": cost,
        }
        return httpx.Response(200, content=json.dumps({"data": [row]}).encode())

    image = asyncio.run(_adapter(handler).generate(ImageOrder("runware:400@1", "x", "1:1")))
    assert image.cost_usd == expected


@pytest.mark.parametrize(
    ("fields", "message"),
    [
        ({}, "kein Bild"),
        ({"imageBase64Data": "nicht base64!"}, "nicht lesbar"),
        ({"status": "processing"}, "zwei Minuten"),
    ],
)
def test_generate_without_a_usable_image(fields: dict[str, object], message: str) -> None:
    adapter = _adapter(lambda request: _row(request, **fields))
    with pytest.raises(ProviderUnavailable, match=message):
        asyncio.run(adapter.generate(ImageOrder("runware:400@1", "x", "1:1")))


@pytest.mark.parametrize(
    "body",
    [
        b"kein json",
        json.dumps({"data": []}).encode(),
        json.dumps({"data": [{"taskUUID": "fremd"}]}).encode(),
        json.dumps([1]).encode(),
    ],
)
def test_generate_with_an_unreadable_answer(body: bytes) -> None:
    adapter = _adapter(lambda _: httpx.Response(200, content=body))
    with pytest.raises(ProviderUnavailable):
        asyncio.run(adapter.generate(ImageOrder("runware:400@1", "x", "1:1")))


@pytest.mark.parametrize(
    ("status", "code", "kind"),
    [
        (429, "tooManyRequests", RateLimited),
        (400, "nsfwContentDetected", ModelRefused),
        (401, "invalidApiKey", ProviderUnavailable),
        (402, "insufficientCredits", ProviderUnavailable),
        (400, "invalidModel", InvalidRequest),
        (400, "missingPrompt", InvalidRequest),
        (500, "internalError", ProviderUnavailable),
        (400, "nicht erlaubt <script>", ProviderUnavailable),
    ],
)
def test_errors_of_the_answer_map_to_kinds(status: int, code: str, kind: type[Exception]) -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(status, json={"errors": [{"code": code, "message": "Prompt X"}]})

    with pytest.raises(kind) as raised:
        asyncio.run(_adapter(handler).generate(ImageOrder("runware:400@1", "geheim", "1:1")))
    assert "geheim" not in str(raised.value)
    assert "<script>" not in str(raised.value)


@pytest.mark.parametrize(("status", "kind"), [(429, RateLimited), (503, ProviderUnavailable)])
def test_status_without_error_list(status: int, kind: type[Exception]) -> None:
    adapter = _adapter(lambda _: httpx.Response(status, content=b""))
    with pytest.raises(kind):
        asyncio.run(adapter.generate(ImageOrder("runware:400@1", "x", "1:1")))


def test_connection_failure_hides_the_request() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("weg", request=request)

    with pytest.raises(ProviderUnavailable) as raised:
        asyncio.run(_adapter(handler).generate(ImageOrder("runware:400@1", "x", "1:1")))
    assert raised.value.__context__ is None
    assert raised.value.__cause__ is None


def test_log_line_names_no_prompt_and_no_key(caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.INFO, logger="skriptorium.ai_gateway")
    asyncio.run(
        _adapter(_image_handler([])).generate(ImageOrder("civitai:1@2 \n x", "Kael geheim", "1:1"))
    )
    line = caplog.records[-1].getMessage()
    assert "anbieter=runware" in line
    assert "modell=civitai:1@2___x" in line
    assert "Kael" not in line
    assert KEY not in line


def test_key_is_required_and_not_shown() -> None:
    with pytest.raises(ProviderUnavailable):
        RunwareImageProvider.from_environment({})
    adapter = RunwareImageProvider.from_environment({"RUNWARE_API_KEY": KEY})
    assert KEY not in repr(adapter)


def test_lookup_reports_a_lora_with_trigger_words_and_weight() -> None:
    seen: list[dict[str, object]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(json.loads(request.content)[0])
        return _row(
            request,
            results=[
                {"air": "civitai:536201@1", "category": "lora"},
                {
                    "air": "civitai:536201@596079",
                    "name": "Handcuffs",
                    "version": "v1Pony",
                    "category": "lora",
                    "architecture": "Pony",
                    "positiveTriggerWords": ["handcuffs", "cuffs", 3],
                    "defaultWeight": 0.8,
                },
            ],
        )

    info = asyncio.run(_adapter(handler).lookup("civitai:536201@596079"))
    assert info is not None
    assert info.kind == "lora"
    assert info.name == "Handcuffs v1Pony"
    assert info.architecture == "pony"
    assert info.trigger == "handcuffs, cuffs"
    assert info.default_weight == 0.8
    assert seen[0]["taskType"] == "modelSearch"
    assert seen[0]["search"] == "civitai:536201@596079"


def test_lookup_reports_a_base_model_without_extras() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return _row(
            request,
            results=[
                {
                    "air": "runware:400@1",
                    "name": "FLUX.2 [dev] 2.0",
                    "version": "2.0",
                    "category": "checkpoint",
                    "architecture": None,
                    "positiveTriggerWords": None,
                    "defaultWeight": "1",
                }
            ],
        )

    info = asyncio.run(_adapter(handler).lookup("runware:400@1"))
    assert info is not None
    assert (info.kind, info.name, info.architecture, info.trigger) == (
        "checkpoint",
        "FLUX.2 [dev] 2.0",
        "",
        "",
    )
    assert info.default_weight is None


@pytest.mark.parametrize(
    "results",
    [[], [{"air": "a:b@c", "category": "controlnet"}], [{"air": "a:b@d", "category": "lora"}]],
)
def test_lookup_finds_nothing(results: list[object]) -> None:
    adapter = _adapter(lambda request: _row(request, results=results))
    assert asyncio.run(adapter.lookup("a:b@c")) is None


def test_lookup_needs_an_identifier_and_a_readable_answer() -> None:
    with pytest.raises(InvalidRequest):
        asyncio.run(_adapter(lambda r: _row(r, results=[])).lookup("keine kennung"))
    with pytest.raises(ProviderUnavailable):
        asyncio.run(_adapter(lambda r: _row(r, results="x")).lookup("a:b@c"))


def test_full_prompt_appends_non_empty_additions() -> None:
    assert full_prompt(" Kael ", "", " score_9 ", "handcuffs") == "Kael, score_9, handcuffs"
    assert full_prompt("", "a") == "a"
    assert len(full_prompt("x" * 5000, "y")) == MAX_PROMPT_CHARS
