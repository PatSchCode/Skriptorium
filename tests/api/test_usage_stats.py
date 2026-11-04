"""Usage by world, story, kind and model (roadmap step 9.11, ADR-100)."""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from skriptorium.ai_gateway import Usage
from skriptorium.api.usage import UsageLog
from skriptorium.storage import DocumentStore, HeaderValue, InvalidInput
from tests.api.conftest import FakeClock, FakeImages, FakeProvider, services_of
from tests.api.test_writing import WRITE, writer

__all__ = ["writer"]

WORLD = "/api/worlds/die-salzmark"
STORY = f"{WORLD}/stories/am-ufer"
IMAGE = {"model": "black-forest-labs/flux.2-pro", "prompt": "Nebel am Hafen"}


def _log(tmp_path: Path, clock: FakeClock | None = None) -> tuple[UsageLog, DocumentStore]:
    store = DocumentStore(tmp_path / "data")
    return UsageLog(store, clock or FakeClock()), store


def _stored(data_dir: Path) -> list[dict[str, HeaderValue]]:
    """The items of September 2026 (the month of the fake clock)."""
    items = DocumentStore(data_dir).read("system/verbrauch/2026-09.md").header["anfragen"]
    assert isinstance(items, list)
    return [item for item in items if isinstance(item, dict)]


def _filed(data_dir: Path) -> list[tuple[HeaderValue, HeaderValue, HeaderValue]]:
    return [(item["art"], item["welt"], item["geschichte"]) for item in _stored(data_dir)]


# --- UsageLog ---------------------------------------------------------------------------------


def test_recorder_files_requests_under_world_and_story(tmp_path: Path) -> None:
    log, _ = _log(tmp_path)

    log.recorder("die-salzmark", "am-ufer")("schreiben", "m", Usage(10, 2, 0.1), "ok")
    log.recorder("die-salzmark")("weltenbau", "m", None, "abgebrochen")
    log.recorder(None)("bilderzeugung", "m", Usage(None, None, 0.04), "ok")

    assert _filed(tmp_path / "data") == [
        ("schreiben", "die-salzmark", "am-ufer"),
        ("weltenbau", "die-salzmark", None),
        ("bilderzeugung", None, None),
    ]


@pytest.mark.parametrize(
    ("world", "story"), [(None, "am-ufer"), ("Die Salzmark", None), ("die-salzmark", "../x")]
)
def test_recorder_refuses_bad_targets(tmp_path: Path, world: str | None, story: str | None) -> None:
    log, _ = _log(tmp_path)

    with pytest.raises(InvalidInput):
        log.recorder(world, story)


def test_stats_group_by_world_story_kind_and_model(tmp_path: Path) -> None:
    clock = FakeClock()
    log, store = _log(tmp_path, clock)
    # Before step 9.11: no world, no cache counts.
    store.write(
        "system/verbrauch/2026-09.md",
        {
            "anfragen": [
                {
                    "zeit": "2026-09-01T10:00:00+00:00",
                    "art": "schreiben",
                    "modell": "x-ai/grok-4.6",
                    "ergebnis": "ok",
                    "token_ein": 1000,
                    "token_aus": 100,
                    "kosten_usd": 0.5,
                }
            ]
        },
        "",
    )
    story = log.recorder("die-salzmark", "am-ufer")
    story("schreiben", "x-ai/grok-4.6", Usage(2000, 200, 1.0, 1500, 0), "ok")
    story("kurzfassung", "x-ai/grok-4.7", Usage(1000, 50, 0.25, None, None), "ok")
    log.recorder("die-salzmark")("weltenbau", "x-ai/grok-4.6", None, "abgebrochen")
    log.recorder("glimmergrund", "kein-stein")(
        "schreiben", "x-ai/grok-4.6", Usage(400, 40, 0.1, 100, 0), "ok"
    )

    stats = log.stats("2026-09")

    assert stats.month == "2026-09"
    assert stats.months == ["2026-09"]
    month = log.month("2026-09")
    assert (stats.total.totals.requests, stats.total.totals.cost_usd) == (5, month.cost_usd)
    assert stats.total.totals.input_tokens == month.input_tokens == 4400
    assert stats.unassigned.totals.requests == 1
    salzmark = stats.worlds["die-salzmark"]
    assert salzmark.all.totals.requests == 3
    assert salzmark.own.totals.requests == 1
    assert salzmark.own.totals.without_cost == 1
    assert set(salzmark.stories) == {"am-ufer"}
    ufer = salzmark.stories["am-ufer"]
    assert ufer.totals.cost_usd == 1.25
    assert {kind: totals.requests for kind, totals in ufer.kinds.items()} == {
        "schreiben": 1,
        "kurzfassung": 1,
    }
    assert {model: totals.output_tokens for model, totals in ufer.models.items()} == {
        "x-ai/grok-4.6": 200,
        "x-ai/grok-4.7": 50,
    }
    # The cache share only counts requests that reported a cache: 1500 of 2000.
    assert ufer.totals.cache_read_tokens == 1500
    assert ufer.totals.cache_share == 0.75
    assert stats.unassigned.totals.cache_share is None
    assert stats.total.totals.cache_share == pytest.approx(1600 / 2400)
    # Worlds plus unassigned make up the total.
    parts = [world.all.totals.requests for world in stats.worlds.values()]
    assert sum(parts) + stats.unassigned.totals.requests == stats.total.totals.requests


def test_stats_over_all_months_and_bad_month(tmp_path: Path) -> None:
    clock = FakeClock()
    log, store = _log(tmp_path, clock)
    log.recorder("die-salzmark")("weltenbau", "m", Usage(1, 1, 0.5), "ok")
    clock.now = clock.now.replace(month=11)
    log.recorder("die-salzmark")("weltenbau", "m", Usage(1, 1, 0.25), "ok")
    store.write("system/verbrauch/notizen.md", {}, "kein Monat")

    every = log.stats()

    assert every.month is None
    assert every.months == ["2026-11", "2026-09"]
    assert every.worlds["die-salzmark"].all.totals.cost_usd == 0.75
    assert log.stats("2026-10").total.totals.requests == 0
    with pytest.raises(InvalidInput):
        log.stats("11-2026")


def test_values_of_the_wrong_type_count_as_nothing(tmp_path: Path) -> None:
    log, store = _log(tmp_path)
    item: dict[str, HeaderValue] = {
        "art": 3,
        "modell": None,
        "token_ein": "viel",
        "cache_gelesen": True,
        "welt": "",
        "geschichte": "am-ufer",
    }
    store.write("system/verbrauch/2026-09.md", {"anfragen": [item]}, "")

    stats = log.stats("2026-09")

    assert stats.unassigned.totals.requests == 1
    assert stats.unassigned.totals.cache_share is None
    assert set(stats.unassigned.kinds) == {"unbekannt"}
    assert set(stats.unassigned.models) == {"unbekannt"}


# --- every flow files its requests ------------------------------------------------------------


def test_writing_and_summaries_go_to_the_story(
    writer: TestClient, provider: FakeProvider, data_dir: Path
) -> None:
    assert writer.post(WRITE, json={}).status_code == 200
    assert writer.post(f"{STORY}/chapters/1/summarize").status_code == 200

    assert _filed(data_dir) == [
        ("schreiben", "die-salzmark", "am-ufer"),
        ("kurzfassung", "die-salzmark", "am-ufer"),
        ("gesamtzusammenfassung", "die-salzmark", "am-ufer"),
    ]


def test_world_builder_and_looks_go_to_the_world(
    writer: TestClient, provider: FakeProvider, data_dir: Path
) -> None:
    builder = {"messages": [{"role": "user", "content": "Ein Leuchtturm"}]}
    assert writer.post(f"{WORLD}/worldbuilder", json=builder).status_code == 200
    assert writer.post(f"{WORLD}/entries/kael/appearance", json={}).status_code == 200

    assert _filed(data_dir) == [
        ("weltenbau", "die-salzmark", None),
        ("aussehen", "die-salzmark", None),
    ]


def test_generated_images_go_to_their_target(
    writer: TestClient, images: FakeImages, data_dir: Path
) -> None:
    assert writer.post("/api/images/generate", json=IMAGE).status_code == 200
    world = {**IMAGE, "world": "die-salzmark"}
    assert writer.post("/api/images/generate", json=world).status_code == 200
    cover = {**world, "story": "am-ufer"}
    assert writer.post("/api/images/generate", json=cover).status_code == 200

    assert _filed(data_dir) == [
        ("bilderzeugung", None, None),
        ("bilderzeugung", "die-salzmark", None),
        ("bilderzeugung", "die-salzmark", "am-ufer"),
    ]


def test_image_target_needs_a_world_and_valid_identifiers(
    writer: TestClient, images: FakeImages
) -> None:
    story_only = {**IMAGE, "story": "am-ufer"}
    assert writer.post("/api/images/generate", json=story_only).status_code == 422
    bad = {**IMAGE, "world": "Die Salzmark"}
    assert writer.post("/api/images/generate", json=bad).status_code == 422
    assert images.orders == []


# --- endpoint ---------------------------------------------------------------------------------


def test_stats_endpoint_names_worlds_and_stories(
    writer: TestClient, provider: FakeProvider
) -> None:
    usage = services_of(writer).usage
    assert writer.post(WRITE, json={}).status_code == 200
    usage.recorder("die-salzmark")("weltenbau", "x-ai/grok-4.6", Usage(10, 5, 0.5), "ok")
    usage.recorder("die-salzmark", "geloescht")(
        "schreiben", "x-ai/grok-4.6", Usage(1, 1, 0.01), "ok"
    )
    usage.recorder("verschwunden")("weltenbau", "x-ai/grok-4.6", Usage(1, 1, 2.0), "ok")
    usage.record("aussehen", "x-ai/grok-4.6", None, "abgelehnt")

    response = writer.get("/api/usage/stats", params={"month": "2026-09"})

    assert response.status_code == 200, response.text
    body = response.json()
    assert body["month"] == "2026-09"
    assert body["months"] == ["2026-09"]
    assert body["total"]["totals"]["requests"] == 5
    assert body["unassigned"]["totals"]["requests"] == 1
    # By cost, highest first: the deleted world spent 2 $.
    assert [(world["id"], world["name"], world["deleted"]) for world in body["worlds"]] == [
        ("verschwunden", None, True),
        ("die-salzmark", "Die Salzmark", False),
    ]
    salzmark = body["worlds"][1]
    assert salzmark["own"]["totals"]["requests"] == 1
    assert [
        (story["id"], story["title"], story["form"], story["deleted"])
        for story in salzmark["stories"]
    ] == [
        ("geloescht", None, None, True),
        ("am-ufer", "Am Ufer", "kurzgeschichte", False),
    ]
    assert salzmark["usage"]["kinds"][0]["kind"] == "schreiben"
    assert salzmark["usage"]["models"] == [
        {
            "model": "x-ai/grok-4.6",
            "requests": 3,
            "input_tokens": 1211,
            "output_tokens": 46,
            "cost_usd": 0.5121,
            "without_cost": 0,
            "cache_read_tokens": 0,
            "cache_share": None,
        }
    ]
    assert writer.get("/api/usage/stats").json()["month"] is None
    assert writer.get("/api/usage/stats", params={"month": "9-2026"}).status_code == 422


def test_stats_mark_archived_worlds_and_stories(writer: TestClient, provider: FakeProvider) -> None:
    assert writer.post(WRITE, json={}).status_code == 200
    assert writer.post(f"{STORY}/archive").status_code == 200
    assert writer.post(f"{WORLD}/archive").status_code == 200

    world = writer.get("/api/usage/stats").json()["worlds"][0]

    assert (world["archived"], world["stories"][0]["archived"]) == (True, True)
