"""The owner's image recipes (roadmap step 11.6, ADR-126).

``system/bildrezepte.md`` holds one header field, ``rezepte``: a scene with the place of the
figure (``[Figur]``) together with the model, the format, the levels and the LoRAs it was made
with. A recipe holds for every figure of every world; the browser puts the figure's image
description in at ``[Figur]`` and fills "Bild erzeugen" with it, where everything stays
changeable. Whether the model and the LoRAs can be chosen is checked by the caller, which knows
the catalog and the Runware list.
"""

import math
import re
import secrets
import threading
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Final

from skriptorium.storage import DocumentStore, HeaderValue, InvalidInput, NotFound

PATH: Final = "system/bildrezepte.md"
FIGURE: Final = "[Figur]"
MAX_RECIPES: Final = 50
MAX_NAME: Final = 100
MAX_SCENE: Final = 4000
MAX_LORAS: Final = 5
MIN_WEIGHT: Final = -2.0
MAX_WEIGHT: Final = 2.0
ASPECT_RATIOS: Final = frozenset({"2:3", "1:1", "3:2", "16:9", "9:16", "3:4", "4:3"})

_ID: Final = re.compile(r"[0-9a-f]{8}")
_MODEL: Final = re.compile(r"[A-Za-z0-9._:@/-]{1,200}")
_LEVEL: Final = re.compile(r"[A-Za-z0-9._-]{1,20}")


@dataclass(frozen=True)
class RecipeLora:
    """A LoRA of the Runware list that goes along, with its weight."""

    id: str
    weight: float


@dataclass(frozen=True)
class Recipe:
    """A scene with ``[Figur]`` and how it is generated; ``id`` is empty before it is saved."""

    id: str
    name: str
    model: str
    aspect_ratio: str
    scene: str
    resolution: str | None = None
    quality: str | None = None
    loras: tuple[RecipeLora, ...] = ()


class ImageRecipes:
    """Reads and writes the list of recipes."""

    def __init__(self, store: DocumentStore) -> None:
        """Use ``store`` for ``system/bildrezepte.md``."""
        self._store = store
        self._lock = threading.Lock()

    def recipes(self) -> list[Recipe]:
        """The recipes in the chosen order; none if none were saved.

        Raises:
            InvalidInput: The file is broken.
        """
        try:
            header: Mapping[str, Any] = self._store.read(PATH).header
        except NotFound:
            return []
        value = header.get("rezepte", [])
        if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
            raise InvalidInput(f"{PATH}: Feld 'rezepte' muss eine Liste von Einträgen sein")
        return [_recipe(item) for item in value]

    def save(self, recipe: Recipe) -> Recipe:
        """Save ``recipe`` by its name: one of the same name (ignoring case) is replaced in place
        and keeps its identifier, else it is appended with a new one.

        Raises:
            InvalidInput: The list is full or a field is out of bounds.
        """
        checked = check(recipe)
        with self._lock:
            current = self.recipes()
            same = next((r for r in current if _key(r.name) == _key(checked.name)), None)
            if same is None:
                if len(current) >= MAX_RECIPES:
                    raise InvalidInput(f"Höchstens {MAX_RECIPES} Bildrezepte")
                taken = {r.id for r in current}
                saved = _with_id(checked, _new_id(taken))
                self._write([*current, saved])
            else:
                saved = _with_id(checked, same.id)
                self._write([saved if r.id == same.id else r for r in current])
            return saved

    def replace(self, edited: Sequence[tuple[str, str, str]]) -> list[Recipe]:
        """Save the list as edited: ``(id, name, scene)`` in the new order. Model, format,
        levels and LoRAs stay as saved; leaving a recipe out removes it.

        Raises:
            InvalidInput: An unknown or repeated identifier, a repeated name, or a field out of
                bounds.
        """
        with self._lock:
            known = {r.id: r for r in self.recipes()}
            ids = [recipe_id for recipe_id, _, _ in edited]
            if len(set(ids)) != len(ids):
                raise InvalidInput("Ein Rezept steht doppelt in der Liste")
            result = []
            for recipe_id, name, scene in edited:
                old = known.get(recipe_id)
                if old is None:
                    raise InvalidInput(f"Rezept nicht in der Liste: {recipe_id}")
                result.append(
                    check(
                        Recipe(
                            old.id,
                            name,
                            old.model,
                            old.aspect_ratio,
                            scene,
                            old.resolution,
                            old.quality,
                            old.loras,
                        )
                    )
                )
            names = [_key(r.name) for r in result]
            if len(set(names)) != len(names):
                raise InvalidInput("Zwei Rezepte haben denselben Namen")
            self._write(result)
            return result

    def _write(self, recipes: Sequence[Recipe]) -> None:
        self._store.write(PATH, {"rezepte": [_mapping(r) for r in recipes]}, "")


def check(recipe: Recipe) -> Recipe:
    """``recipe`` with its name on one line and its scene trimmed.

    Raises:
        InvalidInput: A field is out of bounds, or the scene does not hold ``[Figur]`` exactly once.
    """
    name = " ".join(recipe.name.split())
    if not name:
        raise InvalidInput("Das Rezept braucht einen Namen")
    if len(name) > MAX_NAME:
        raise InvalidInput(f"Name: höchstens {MAX_NAME} Zeichen")
    scene = recipe.scene.strip()
    if len(scene) > MAX_SCENE:
        raise InvalidInput(f"Szene: höchstens {MAX_SCENE} Zeichen")
    if scene.count(FIGURE) != 1:
        raise InvalidInput(f"Die Szene muss {FIGURE} genau einmal enthalten - dort steht die Figur")
    if not _MODEL.fullmatch(recipe.model):
        raise InvalidInput("Ungültiges Modell")
    if recipe.aspect_ratio not in ASPECT_RATIOS:
        raise InvalidInput("Ungültiges Format")
    for level in (recipe.resolution, recipe.quality):
        if level is not None and not _LEVEL.fullmatch(level):
            raise InvalidInput("Ungültige Auflösung oder Qualität")
    if len(recipe.loras) > MAX_LORAS:
        raise InvalidInput(f"Höchstens {MAX_LORAS} LoRAs je Rezept")
    if len({lora.id for lora in recipe.loras}) != len(recipe.loras):
        raise InvalidInput("Eine LoRA steht doppelt im Rezept")
    for lora in recipe.loras:
        if not math.isfinite(lora.weight) or not MIN_WEIGHT <= lora.weight <= MAX_WEIGHT:
            raise InvalidInput(f"Gewicht zwischen {MIN_WEIGHT} und {MAX_WEIGHT}")
    return Recipe(
        recipe.id,
        name,
        recipe.model,
        recipe.aspect_ratio,
        scene,
        recipe.resolution,
        recipe.quality,
        tuple(RecipeLora(lora.id, round(lora.weight, 2)) for lora in recipe.loras),
    )


def _key(name: str) -> str:
    return " ".join(name.split()).casefold()


def _new_id(taken: set[str]) -> str:
    while True:
        candidate = secrets.token_hex(4)
        if candidate not in taken:
            return candidate


def _with_id(recipe: Recipe, recipe_id: str) -> Recipe:
    return Recipe(
        recipe_id,
        recipe.name,
        recipe.model,
        recipe.aspect_ratio,
        recipe.scene,
        recipe.resolution,
        recipe.quality,
        recipe.loras,
    )


def _mapping(recipe: Recipe) -> HeaderValue:
    mapping: dict[str, HeaderValue] = {
        "kennung": recipe.id,
        "name": recipe.name,
        "modell": recipe.model,
        "seitenverhaeltnis": recipe.aspect_ratio,
    }
    if recipe.resolution is not None:
        mapping["aufloesung"] = recipe.resolution
    if recipe.quality is not None:
        mapping["qualitaet"] = recipe.quality
    mapping["loras"] = [{"kennung": lora.id, "gewicht": lora.weight} for lora in recipe.loras]
    mapping["szene"] = recipe.scene
    return mapping


def _text(item: Mapping[str, object], name: str) -> str:
    value = item.get(name, "")
    if not isinstance(value, str):
        raise InvalidInput(f"{PATH}: Feld '{name}' muss Text sein")
    return value


def _level(item: Mapping[str, object], name: str) -> str | None:
    value = item.get(name)
    if value is not None and not isinstance(value, str):
        raise InvalidInput(f"{PATH}: Feld '{name}' muss Text sein")
    return value


def _recipe(item: Mapping[str, object]) -> Recipe:
    loras = item.get("loras", [])
    if not isinstance(loras, list) or not all(isinstance(lora, dict) for lora in loras):
        raise InvalidInput(f"{PATH}: Feld 'loras' muss eine Liste von Einträgen sein")
    chosen = []
    for lora in loras:
        weight = lora.get("gewicht", 1.0)
        if not isinstance(weight, int | float) or isinstance(weight, bool):
            raise InvalidInput(f"{PATH}: Feld 'gewicht' muss eine Zahl sein")
        chosen.append(RecipeLora(_text(lora, "kennung"), float(weight)))
    recipe_id = _text(item, "kennung")
    if not _ID.fullmatch(recipe_id):
        raise InvalidInput(f"{PATH}: ungültige Kennung")
    try:
        return check(
            Recipe(
                recipe_id,
                _text(item, "name"),
                _text(item, "modell"),
                _text(item, "seitenverhaeltnis"),
                _text(item, "szene"),
                _level(item, "aufloesung"),
                _level(item, "qualitaet"),
                tuple(chosen),
            )
        )
    except InvalidInput as error:
        raise InvalidInput(f"{PATH}: {error}") from error
