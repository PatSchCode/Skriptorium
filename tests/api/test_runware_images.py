"""Tests of image generation through Runware and of the model list (roadmap step 10.8, ADR-115)."""

import base64
from pathlib import Path

import httpx
import pytest
from fastapi.testclient import TestClient

from skriptorium.api import create_app
from skriptorium.api.runware_models import (
    PATH,
    START,
    Lora,
    RunwareModel,
    RunwareModels,
    family,
    fits,
    identifier,
    is_runware,
)
from skriptorium.api.settings import Settings
from skriptorium.storage import DocumentStore, HeaderValue, InvalidInput
from tests.api.conftest import (
    ORIGIN,
    PASSWORD,
    FakeBreached,
    FakeImages,
    FakeRunware,
    cheap_hasher,
    services_of,
    set_up_password,
)
from tests.image_samples import png

EPIC = "civitai:277058@1405120"
PONY = "civitai:548016@861939"
CUFFS = "civitai:536201@596079"
FLUX_LORA = "civitai:1@2"


def _add(client: TestClient, reference: str) -> httpx.Response:
    response: httpx.Response = client.post("/api/images/runware", json={"reference": reference})
    return response


# --- the list ----------------------------------------------------------------------------------


def test_identifier_takes_identifiers_and_civitai_links() -> None:
    assert identifier(" civitai:277058@1405120 ") == EPIC
    assert identifier("runware:z-image@turbo") == "runware:z-image@turbo"
    link = "https://civitai.red/models/277058/epicrealism-xl?modelVersionId=1405120"
    assert identifier(link) == EPIC
    assert identifier("https://civitai.com/models/277058?foo=1&modelVersionId=1405120#x") == EPIC
    with pytest.raises(InvalidInput, match="Version"):
        identifier("https://civitai.com/models/277058/epicrealism-xl")
    with pytest.raises(InvalidInput, match="Keine Kennung"):
        identifier("https://example.com/models/1?modelVersionId=2")
    with pytest.raises(InvalidInput):
        identifier("black-forest-labs/flux.2-pro")


def test_is_runware_tells_the_providers_apart() -> None:
    assert is_runware(EPIC)
    assert not is_runware("black-forest-labs/flux.2-pro")


def test_families_decide_which_lora_fits() -> None:
    sdxl = RunwareModel(EPIC, "Epic", "sdxl")
    assert family("pony") == family("illustrious") == "sdxl"
    assert family("hidreamdev") == "hidreamdev"
    assert fits(Lora(CUFFS, "Cuffs", "pony", "", 1), sdxl)
    assert not fits(Lora(FLUX_LORA, "Flux", "flux1d", "", 1), sdxl)
    assert not fits(Lora(CUFFS, "?", "", "", 1), RunwareModel(EPIC, "?", ""))


def test_start_list_without_a_file(tmp_path: Path) -> None:
    models = RunwareModels(DocumentStore(tmp_path))
    assert models.models() == list(START)
    assert models.loras() == []
    assert models.model(EPIC) == START[3]
    assert models.lora(CUFFS) is None


def test_add_replace_and_bounds(tmp_path: Path) -> None:
    store = DocumentStore(tmp_path)
    models = RunwareModels(store)
    models.add_model(RunwareModel(PONY, "  Pony \n Mix ", "Pony"))
    models.add_model(RunwareModel(PONY, "Pony Mix 2", "pony", "score_9"))
    models.add_lora(Lora(CUFFS, "", "pony", "handcuffs", 0.8049))
    models.add_lora(Lora(CUFFS, "Cuffs", "pony", "handcuffs", 0.7))
    assert models.models()[-1] == RunwareModel(PONY, "Pony Mix 2", "pony", "score_9")
    assert len(models.models()) == len(START) + 1
    assert models.loras() == [Lora(CUFFS, "Cuffs", "pony", "handcuffs", 0.7)]
    models.add_lora(Lora(FLUX_LORA, "", "flux1d", "", 0.8049))
    assert models.lora(FLUX_LORA) == Lora(FLUX_LORA, FLUX_LORA, "flux1d", "", 0.8)
    with pytest.raises(InvalidInput, match="Gewicht"):
        models.add_lora(Lora(CUFFS, "x", "pony", "", 2.5))
    with pytest.raises(InvalidInput, match="Gewicht"):
        models.add_lora(Lora(CUFFS, "x", "pony", "", float("nan")))
    with pytest.raises(InvalidInput, match="Name"):
        models.add_model(RunwareModel(PONY, "x" * 201, "pony"))
    with pytest.raises(InvalidInput, match="Kennung"):
        models.add_model(RunwareModel("a/b", "x", "pony"))
    with pytest.raises(InvalidInput, match="Kennung"):
        models.add_lora(Lora("a/b", "x", "pony", "", 1))


def test_lists_are_bounded(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import skriptorium.api.runware_models as module

    monkeypatch.setattr(module, "MAX_MODELS", len(START))
    monkeypatch.setattr(module, "MAX_LORAS", 1)
    models = RunwareModels(DocumentStore(tmp_path))
    with pytest.raises(InvalidInput, match="Grundmodelle"):
        models.add_model(RunwareModel(PONY, "x", "pony"))
    models.add_lora(Lora(CUFFS, "x", "pony", "", 1))
    with pytest.raises(InvalidInput, match="LoRAs"):
        models.add_lora(Lora(FLUX_LORA, "x", "flux1d", "", 1))


def test_replace_keeps_the_looked_up_architecture(tmp_path: Path) -> None:
    models = RunwareModels(DocumentStore(tmp_path))
    models.add_lora(Lora(CUFFS, "Cuffs", "pony", "handcuffs", 0.8))
    models.replace(
        [RunwareModel(EPIC, "Epic", "gefälscht", "raw photo")],
        [Lora(CUFFS, "Fesseln", "gefälscht", "cuffs", 1.2)],
    )
    assert models.models() == [RunwareModel(EPIC, "Epic", "sdxl", "raw photo")]
    assert models.loras() == [Lora(CUFFS, "Fesseln", "pony", "cuffs", 1.2)]
    models.replace([], [])
    assert models.models() == []
    assert models.loras() == []


@pytest.mark.parametrize(
    ("given_models", "given_loras", "message"),
    [
        ([RunwareModel(PONY, "x", "")], [], "nicht in der Liste"),
        ([], [Lora(FLUX_LORA, "x", "", "", 1)], "nicht in der Liste"),
        ([RunwareModel(EPIC, "x", ""), RunwareModel(EPIC, "y", "")], [], "doppelt"),
    ],
)
def test_replace_refuses_unknown_and_repeated_entries(
    tmp_path: Path,
    given_models: list[RunwareModel],
    given_loras: list[Lora],
    message: str,
) -> None:
    models = RunwareModels(DocumentStore(tmp_path))
    with pytest.raises(InvalidInput, match=message):
        models.replace(given_models, given_loras)


@pytest.mark.parametrize(
    "header",
    [
        {"grundmodelle": "x"},
        {"grundmodelle": [{"kennung": 1}]},
        {"grundmodelle": [{"kennung": "a/b"}]},
        {"loras": [{"kennung": "a:b@c", "gewicht": "1"}]},
        {"loras": [{"kennung": "a/b"}]},
    ],
)
def test_a_broken_file_is_reported(tmp_path: Path, header: dict[str, HeaderValue]) -> None:
    store = DocumentStore(tmp_path)
    store.write(PATH, header, "")
    models = RunwareModels(store)
    with pytest.raises(InvalidInput):
        models.models()
        models.loras()


# --- the routes --------------------------------------------------------------------------------


def test_list_shows_the_start_list_and_fitting_loras(
    logged_in: TestClient, runware_server: FakeRunware
) -> None:
    body = logged_in.get("/api/images/models").json()
    assert body["runware_ready"] is True
    assert [m["id"] for m in body["runware"]] == [m.id for m in START]
    assert body["loras"] == []
    assert _add(logged_in, CUFFS).status_code == 200
    assert _add(logged_in, FLUX_LORA).status_code == 200
    body = logged_in.get("/api/images/models").json()
    epic = next(m for m in body["runware"] if m["id"] == EPIC)
    assert epic["loras"] == [CUFFS]
    assert body["loras"][0] == {
        "id": CUFFS,
        "name": "[PonyV6 XL] Handcuffs v1Pony",
        "architecture": "pony",
        "trigger": "handcuffs, cuffs",
        "weight": 0.8,
    }
    assert body["loras"][1]["weight"] == 1.0
    assert [t["taskType"] for t in runware_server.tasks] == ["modelSearch", "modelSearch"]


def test_add_takes_a_civitai_link_of_a_base_model(logged_in: TestClient) -> None:
    response = _add(logged_in, "https://civitai.com/models/548016/x?modelVersionId=861939")
    assert response.status_code == 200, response.text
    added = response.json()["runware"][-1]
    assert added == {
        "id": PONY,
        "name": "PonyXL MIX v2",
        "architecture": "pony",
        "addition": "",
        "loras": [],
    }


@pytest.mark.parametrize(
    ("reference", "status", "message"),
    [
        ("civitai:277058@1552721", 422, "führt civitai:277058@1552721 nicht"),
        ("civitai:3@4", 422, "führt"),
        ("https://civitai.red/models/277058", 422, "Version"),
    ],
)
def test_add_refuses_what_runware_does_not_list(
    logged_in: TestClient, reference: str, status: int, message: str
) -> None:
    response = _add(logged_in, reference)
    assert response.status_code == status
    assert message in response.json()["detail"]


def test_add_reports_a_failed_search(logged_in: TestClient, runware_server: FakeRunware) -> None:
    runware_server.status = 401
    runware_server.errors = [{"code": "invalidApiKey"}]
    response = _add(logged_in, EPIC)
    assert response.status_code == 502


def test_edit_the_list(logged_in: TestClient) -> None:
    _add(logged_in, CUFFS)
    response = logged_in.put(
        "/api/images/runware",
        json={
            "models": [{"id": EPIC, "name": "Epic", "addition": "raw photo"}],
            "loras": [{"id": CUFFS, "name": "Fesseln", "trigger": "cuffs", "weight": 1.1}],
        },
    )
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["runware"] == [
        {
            "id": EPIC,
            "name": "Epic",
            "architecture": "sdxl",
            "addition": "raw photo",
            "loras": [CUFFS],
        }
    ]
    assert body["loras"][0]["trigger"] == "cuffs"
    bad = logged_in.put(
        "/api/images/runware", json={"models": [{"id": PONY, "name": "x"}], "loras": []}
    )
    assert bad.status_code == 422


def test_generate_sends_model_loras_and_additions(
    logged_in: TestClient, runware_server: FakeRunware
) -> None:
    _add(logged_in, CUFFS)
    logged_in.put(
        "/api/images/runware",
        json={
            "models": [{"id": EPIC, "name": "Epic", "addition": "raw photo"}],
            "loras": [{"id": CUFFS, "name": "Cuffs", "trigger": "handcuffs", "weight": 0.8}],
        },
    )
    response = logged_in.post(
        "/api/images/generate",
        json={
            "model": EPIC,
            "prompt": "Kael am Fluss",
            "aspect_ratio": "2:3",
            "loras": [{"id": CUFFS, "weight": 0.6}],
            "world": "w",
        },
    )
    assert response.status_code == 200, response.text
    body = response.json()
    assert base64.b64decode(body["content"]) == png(832, 1216)
    assert body["media_type"] == "image/png"
    assert body["cost_usd"] == 0.0025
    task = runware_server.tasks[-1]
    assert task["positivePrompt"] == "Kael am Fluss, raw photo, handcuffs"
    assert task["lora"] == [{"model": CUFFS, "weight": 0.6}]
    assert task["safety"] == {"checkContent": False}
    stats = services_of(logged_in).usage.stats()
    assert EPIC in stats.total.models


@pytest.mark.parametrize(
    ("extra", "message"),
    [
        ({"model": PONY}, "Unbekanntes Bildmodell"),
        ({"loras": [{"id": FLUX_LORA, "weight": 1}]}, "Unbekannter Zusatz"),
        ({"loras": [{"id": CUFFS, "weight": 1}, {"id": CUFFS, "weight": 1}]}, "doppelt"),
        ({"resolution": "2K"}, "gibt es bei Runware"),
        ({"reference": {"world": "w", "map_file": "k.png"}}, "gibt es bei Runware"),
    ],
)
def test_generate_refuses_what_does_not_fit(
    logged_in: TestClient, extra: dict[str, object], message: str
) -> None:
    _add(logged_in, CUFFS)
    response = logged_in.post("/api/images/generate", json={"model": EPIC, "prompt": "x", **extra})
    assert response.status_code == 422
    assert message in response.json()["detail"]


def test_generate_refuses_a_lora_of_another_family(logged_in: TestClient) -> None:
    _add(logged_in, FLUX_LORA)
    response = logged_in.post(
        "/api/images/generate",
        json={"model": EPIC, "prompt": "x", "loras": [{"id": FLUX_LORA, "weight": 1}]},
    )
    assert response.status_code == 422
    assert "passt nicht" in response.json()["detail"]


def test_openrouter_models_take_no_loras(logged_in: TestClient) -> None:
    response = logged_in.post(
        "/api/images/generate",
        json={
            "model": "black-forest-labs/flux.2-pro",
            "prompt": "x",
            "loras": [{"id": CUFFS, "weight": 1}],
        },
    )
    assert response.status_code == 422
    assert "nur bei Modellen von Runware" in response.json()["detail"]


def test_generate_reports_a_refusal_and_records_it(
    logged_in: TestClient, runware_server: FakeRunware
) -> None:
    runware_server.status = 400
    runware_server.errors = [{"code": "nsfwContentDetected"}]
    response = logged_in.post("/api/images/generate", json={"model": EPIC, "prompt": "x"})
    assert response.status_code == 422
    assert "abgelehnt" in response.json()["detail"]
    assert services_of(logged_in).usage.month().requests == 1


def test_generate_refuses_an_unusable_image(
    logged_in: TestClient, runware_server: FakeRunware
) -> None:
    runware_server.image = b"<svg/>"
    response = logged_in.post("/api/images/generate", json={"model": EPIC, "prompt": "x"})
    assert response.status_code == 502


def test_price_of_a_runware_model_shows_after_generating(logged_in: TestClient) -> None:
    response = logged_in.get("/api/images/price", params={"model": EPIC})
    assert response.json() == {
        "cost_usd": None,
        "unit": None,
        "input_cost_usd": None,
        "input_unit": None,
    }
    assert logged_in.get("/api/images/price", params={"model": PONY}).status_code == 422


def test_a_runware_model_can_be_the_preset(logged_in: TestClient) -> None:
    response = logged_in.put("/api/models/aufgaben", json={"tasks": {"bilderzeugung": EPIC}})
    assert response.status_code == 200, response.text
    assert logged_in.get("/api/images/models").json()["default"] == EPIC
    refused = logged_in.put("/api/models/aufgaben", json={"tasks": {"bilderzeugung": PONY}})
    assert refused.status_code == 422


def test_without_key_runware_is_not_ready(data_dir: Path) -> None:
    app = create_app(
        Settings(data_dir=data_dir, ui_dir=data_dir / "no-ui"),
        hasher=cheap_hasher(),
        breached=FakeBreached(),
        provider_factory=lambda _: None,
        image_provider_factory=lambda _: FakeImages(image=png()),
        runware_factory=lambda: None,
    )
    with TestClient(app, base_url=ORIGIN, headers={"Origin": ORIGIN}) as client:
        services = services_of(client)
        assert services.runware is None
        set_up_password(client)
        client.post("/api/auth/login", json={"password": PASSWORD})
        assert client.get("/api/images/models").json()["runware_ready"] is False
        assert (
            client.post("/api/images/generate", json={"model": EPIC, "prompt": "x"}).status_code
            == 503
        )
        assert _add(client, EPIC).status_code == 503


def test_selectable_takes_only_text(logged_in: TestClient) -> None:
    from skriptorium.api.image_routes import Selectable

    selectable = Selectable(services_of(logged_in))
    assert EPIC in selectable
    assert not selectable.__contains__(1)


def test_runware_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    from skriptorium.api.app import _runware_from_environment

    monkeypatch.delenv("RUNWARE_API_KEY", raising=False)
    assert _runware_from_environment() is None
    monkeypatch.setenv("RUNWARE_API_KEY", "rw-test")
    assert _runware_from_environment() is not None


def test_a_broken_list_shows_the_start_list(
    logged_in: TestClient, caplog: pytest.LogCaptureFixture
) -> None:
    services_of(logged_in).runware_models._store.write(PATH, {"grundmodelle": "kaputt"}, "")
    response = logged_in.get("/api/images/models")
    assert response.status_code == 200
    body = response.json()
    assert [m["id"] for m in body["runware"]] == [m.id for m in START]
    assert body["loras"] == []
    assert "runware_liste_defekt" in caplog.text
    refused = logged_in.post("/api/images/generate", json={"model": EPIC, "prompt": "x"})
    assert refused.status_code == 422
    preset = logged_in.put("/api/models/aufgaben", json={"tasks": {"bilderzeugung": EPIC}})
    assert preset.status_code == 422
