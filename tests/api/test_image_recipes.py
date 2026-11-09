"""Tests of the image recipes (roadmap step 11.6, ADR-126)."""

import base64
from dataclasses import replace
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from skriptorium.api.image_recipes import PATH, ImageRecipes, Recipe, RecipeLora, check
from skriptorium.storage import DocumentStore, HeaderValue, InvalidInput
from skriptorium.storage.origins import ImageOrigin, origin_from_mapping, origin_to_mapping
from tests.api.conftest import FakeRunware
from tests.image_samples import png

EPIC = "civitai:277058@1405120"
CUFFS = "civitai:536201@596079"
FLUX_LORA = "civitai:1@2"
SCENE = "[Figur], kneeling in a dim cellar, torch light"
WORLD = "/api/worlds/die-salzmark"
ENTRY = f"{WORLD}/entries/gunda"


def _recipe(name: str = "Kerker", **change: Any) -> Recipe:
    base = Recipe("", name, EPIC, "2:3", SCENE, loras=(RecipeLora(CUFFS, 0.6),))
    return replace(base, **change)


# --- the list ----------------------------------------------------------------------------------


def test_no_recipes_without_a_file(tmp_path: Path) -> None:
    assert ImageRecipes(DocumentStore(tmp_path)).recipes() == []


def test_save_appends_and_replaces_by_name(tmp_path: Path) -> None:
    recipes = ImageRecipes(DocumentStore(tmp_path))
    first = recipes.save(_recipe("  Kerker,\n Seil "))
    assert first.name == "Kerker, Seil"
    assert len(first.id) == 8
    second = recipes.save(_recipe("Studio", loras=(), model="black-forest-labs/flux.2-pro"))
    again = recipes.save(_recipe("kerker, seil", scene="a cellar, [Figur]", loras=()))
    assert again.id == first.id
    assert [r.name for r in recipes.recipes()] == ["kerker, seil", "Studio"]
    assert recipes.recipes()[0].scene == "a cellar, [Figur]"
    assert recipes.recipes()[1] == second


def test_the_file_holds_german_fields(tmp_path: Path) -> None:
    store = DocumentStore(tmp_path)
    saved = ImageRecipes(store).save(_recipe(resolution="2K", quality="high"))
    assert store.read(PATH).header == {
        "rezepte": [
            {
                "kennung": saved.id,
                "name": "Kerker",
                "modell": EPIC,
                "seitenverhaeltnis": "2:3",
                "aufloesung": "2K",
                "qualitaet": "high",
                "loras": [{"kennung": CUFFS, "gewicht": 0.6}],
                "szene": SCENE,
            }
        ]
    }


@pytest.mark.parametrize(
    ("change", "message"),
    [
        ({"name": "  "}, "Namen"),
        ({"name": "x" * 101}, "Name"),
        ({"scene": "a cellar"}, r"\[Figur\] genau einmal"),
        ({"scene": "[Figur] and [Figur]"}, r"\[Figur\] genau einmal"),
        ({"scene": "[Figur]" + "x" * 4000}, "Szene"),
        ({"model": "a b"}, "Modell"),
        ({"aspect_ratio": "5:4"}, "Format"),
        ({"resolution": "2 K"}, "Auflösung"),
        ({"loras": tuple(RecipeLora(f"a:b@{i}", 1) for i in range(6))}, "Höchstens 5"),
        ({"loras": (RecipeLora(CUFFS, 1), RecipeLora(CUFFS, 0.5))}, "doppelt"),
        ({"loras": (RecipeLora(CUFFS, float("nan")),)}, "Gewicht"),
        ({"loras": (RecipeLora(CUFFS, 2.5),)}, "Gewicht"),
    ],
)
def test_check_refuses_what_is_out_of_bounds(change: dict[str, Any], message: str) -> None:
    with pytest.raises(InvalidInput, match=message):
        check(_recipe(**change))


def test_check_rounds_weights() -> None:
    assert check(_recipe(loras=(RecipeLora(CUFFS, 0.6049),))).loras == (RecipeLora(CUFFS, 0.6),)


def test_the_list_is_bounded(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import skriptorium.api.image_recipes as module

    monkeypatch.setattr(module, "MAX_RECIPES", 1)
    recipes = ImageRecipes(DocumentStore(tmp_path))
    recipes.save(_recipe("A"))
    recipes.save(_recipe("a"))
    with pytest.raises(InvalidInput, match="Höchstens 1"):
        recipes.save(_recipe("B"))


def test_new_identifiers_do_not_repeat(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:

    drawn = iter(["aaaaaaaa", "aaaaaaaa", "bbbbbbbb"])
    monkeypatch.setattr("skriptorium.api.image_recipes.secrets.token_hex", lambda _: next(drawn))
    recipes = ImageRecipes(DocumentStore(tmp_path))
    assert recipes.save(_recipe("A")).id == "aaaaaaaa"
    assert recipes.save(_recipe("B")).id == "bbbbbbbb"


def test_replace_renames_reorders_and_removes(tmp_path: Path) -> None:
    recipes = ImageRecipes(DocumentStore(tmp_path))
    a = recipes.save(_recipe("A", resolution="2K"))
    b = recipes.save(_recipe("B"))
    recipes.save(_recipe("C"))
    result = recipes.replace([(b.id, "Bett", "[Figur] in bed"), (a.id, "A", SCENE)])
    assert [(r.name, r.scene) for r in result] == [("Bett", "[Figur] in bed"), ("A", SCENE)]
    assert recipes.recipes() == result
    assert result[1].resolution == "2K"
    assert result[1].loras == (RecipeLora(CUFFS, 0.6),)


@pytest.mark.parametrize(
    ("edited", "message"),
    [
        ([("ffffffff", "X", SCENE)], "nicht in der Liste"),
        ([("A", "A", SCENE), ("A", "B", SCENE)], "doppelt"),
        ([("A", "Gleich", SCENE), ("B", "gleich", SCENE)], "denselben Namen"),
        ([("A", "A", "no figure")], r"\[Figur\]"),
    ],
)
def test_replace_refuses_odd_lists(
    tmp_path: Path, edited: list[tuple[str, str, str]], message: str
) -> None:
    recipes = ImageRecipes(DocumentStore(tmp_path))
    ids = {"A": recipes.save(_recipe("A")).id, "B": recipes.save(_recipe("B")).id}
    with pytest.raises(InvalidInput, match=message):
        recipes.replace([(ids.get(i, i), name, scene) for i, name, scene in edited])


@pytest.mark.parametrize(
    "header",
    [
        {"rezepte": "x"},
        {"rezepte": ["x"]},
        {"rezepte": [{"kennung": "zz", "name": "A", "modell": EPIC, "seitenverhaeltnis": "2:3"}]},
        {"rezepte": [{"kennung": "aaaaaaaa", "name": 1}]},
        {"rezepte": [{"kennung": "aaaaaaaa", "aufloesung": 2}]},
        {"rezepte": [{"kennung": "aaaaaaaa", "loras": "x"}]},
        {"rezepte": [{"kennung": "aaaaaaaa", "loras": [{"kennung": CUFFS, "gewicht": "1"}]}]},
        {
            "rezepte": [
                {
                    "kennung": "aaaaaaaa",
                    "name": "A",
                    "modell": EPIC,
                    "seitenverhaeltnis": "2:3",
                    "szene": "without",
                }
            ]
        },
    ],
)
def test_a_broken_file_is_reported(tmp_path: Path, header: dict[str, HeaderValue]) -> None:
    store = DocumentStore(tmp_path)
    store.write(PATH, header, "")
    with pytest.raises(InvalidInput, match="bildrezepte"):
        ImageRecipes(store).recipes()


# --- the endpoints -----------------------------------------------------------------------------


def _save(client: TestClient, **change: object) -> dict[str, object]:
    body: dict[str, object] = {
        "name": "Kerker",
        "model": EPIC,
        "aspect_ratio": "2:3",
        "loras": [{"id": CUFFS, "weight": 0.6}],
        "scene": SCENE,
    }
    body.update(change)
    response = client.post("/api/images/recipes", json=body)
    result: dict[str, object] = {"status": response.status_code, **response.json()}
    return result


def test_save_list_and_edit_recipes(logged_in: TestClient, runware_server: FakeRunware) -> None:
    assert logged_in.get("/api/images/recipes").json() == {"recipes": []}
    assert logged_in.post("/api/images/runware", json={"reference": CUFFS}).status_code == 200
    saved = _save(logged_in)
    assert saved["status"] == 200
    assert saved["loras"] == [{"id": CUFFS, "weight": 0.6}]
    flux = _save(
        logged_in, name="Studio", model="bytedance-seed/seedream-4.5", loras=[], resolution="2K"
    )
    assert (flux["status"], flux["resolution"], flux["quality"]) == (200, "2K", None)
    listed = logged_in.get("/api/images/recipes").json()["recipes"]
    assert [r["name"] for r in listed] == ["Kerker", "Studio"]
    edited = logged_in.put(
        "/api/images/recipes",
        json={"recipes": [{"id": flux["id"], "name": "Atelier", "scene": "[Figur], studio"}]},
    )
    assert edited.status_code == 200
    assert edited.json()["recipes"] == [
        {
            "id": flux["id"],
            "name": "Atelier",
            "model": "bytedance-seed/seedream-4.5",
            "aspect_ratio": "2:3",
            "resolution": "2K",
            "quality": None,
            "loras": [],
            "scene": "[Figur], studio",
        }
    ]
    assert len(runware_server.tasks) == 1


@pytest.mark.parametrize(
    ("change", "message"),
    [
        ({"model": "civitai:9@9"}, "nicht in der Runware-Liste"),
        ({"resolution": "2K"}, "keine Auflösung"),
        ({"loras": [{"id": "civitai:3@4", "weight": 1}]}, "LoRA nicht in der Liste"),
        ({"loras": [{"id": FLUX_LORA, "weight": 1}]}, "passt nicht"),
        ({"model": "black-forest-labs/flux.2-pro"}, "nur bei Modellen der Runware-Liste"),
        ({"model": "a/unknown", "loras": []}, "Unbekanntes Bildmodell"),
        (
            {"model": "bytedance-seed/seedream-4.5", "loras": [], "resolution": "8K"},
            "Auflösung",
        ),
        (
            {"model": "bytedance-seed/seedream-4.5", "loras": [], "quality": "low"},
            "Qualität",
        ),
        ({"scene": "no figure"}, "[Figur]"),
    ],
)
def test_save_refuses_what_does_not_fit(
    logged_in: TestClient, runware_server: FakeRunware, change: dict[str, object], message: str
) -> None:
    logged_in.post("/api/images/runware", json={"reference": CUFFS})
    logged_in.post("/api/images/runware", json={"reference": FLUX_LORA})
    saved = _save(logged_in, **change)
    assert saved["status"] == 422
    assert message in str(saved["detail"])
    assert logged_in.get("/api/images/recipes").json() == {"recipes": []}


def test_the_origin_keeps_the_recipe(logged_in: TestClient) -> None:
    logged_in.post("/api/worlds", json={"name": "Die Salzmark", "description": ""})
    logged_in.post(f"{WORLD}/entries", json={"category": "figur", "name": "Gunda"})
    origin = {"model": EPIC, "prompt": "Gunda", "aspect_ratio": "2:3", "recipe": "Kerker"}
    content = base64.b64encode(png()).decode()
    added = logged_in.post(f"{ENTRY}/images", json={"content": content, "herkunft": origin})
    image = added.json()["images"][-1]
    assert logged_in.get(f"{ENTRY}/images/{image}/origin").json()["recipe"] == "Kerker"
    plain = {k: v for k, v in origin.items() if k != "recipe"}
    added = logged_in.post(f"{ENTRY}/images", json={"content": content, "herkunft": plain})
    image = added.json()["images"][-1]
    assert logged_in.get(f"{ENTRY}/images/{image}/origin").json()["recipe"] is None


def test_the_companion_file_names_the_recipe() -> None:
    origin = ImageOrigin("m", "p", "2:3", None, "2026-11-09", recipe="Kerker")
    mapping = origin_to_mapping(origin)
    assert mapping["rezept"] == "Kerker"
    assert origin_from_mapping(mapping) == origin
    with pytest.raises(InvalidInput, match="Rezept"):
        origin_from_mapping({**mapping, "rezept": 3})
