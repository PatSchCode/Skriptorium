"""Endpoints for the image recipes (roadmap step 11.6, ADR-126).

A recipe is saved from "Bild erzeugen" by its name; the settings change names, scenes and the
order or remove one. Applying a recipe happens in the browser, which fills "Bild erzeugen" with it,
so nothing here generates an image. On saving, the model must be selectable and every LoRA must
be in the Runware list and fit the model, as when generating (ADR-115).
"""

from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from skriptorium.api.context import Services, ServicesDep, current_session
from skriptorium.api.image_recipes import (
    MAX_LORAS,
    MAX_NAME,
    MAX_RECIPES,
    MAX_SCENE,
    Recipe,
    RecipeLora,
)
from skriptorium.api.image_routes import AspectRatio
from skriptorium.api.runware_models import fits, is_runware
from skriptorium.storage import InvalidInput

router = APIRouter(prefix="/api/images/recipes", dependencies=[Depends(current_session)])

_Id = Annotated[str, Field(min_length=1, max_length=200)]
_Level = Annotated[str, Field(min_length=1, max_length=20)]


class RecipeLoraIo(BaseModel):
    """A LoRA of the Runware list with its weight."""

    id: _Id
    weight: Annotated[float, Field(ge=-2, le=2)]


class RecipeIn(BaseModel):
    """A recipe to save; one with the same name is replaced."""

    name: Annotated[str, Field(min_length=1, max_length=MAX_NAME)]
    model: _Id
    aspect_ratio: AspectRatio
    resolution: _Level | None = None
    quality: _Level | None = None
    loras: Annotated[list[RecipeLoraIo], Field(max_length=MAX_LORAS)] = []
    scene: Annotated[str, Field(min_length=1, max_length=MAX_SCENE)]


class RecipeOut(BaseModel):
    """A saved recipe."""

    id: str
    name: str
    model: str
    aspect_ratio: str
    resolution: str | None
    quality: str | None
    loras: list[RecipeLoraIo]
    scene: str


class RecipeEditIn(BaseModel):
    """A recipe of the list as edited in the settings: name and scene."""

    id: _Id
    name: Annotated[str, Field(min_length=1, max_length=MAX_NAME)]
    scene: Annotated[str, Field(min_length=1, max_length=MAX_SCENE)]


class RecipeListIn(BaseModel):
    """The edited list in its new order; a recipe left out is removed."""

    recipes: Annotated[list[RecipeEditIn], Field(max_length=MAX_RECIPES)]


class RecipeList(BaseModel):
    """The recipes in their order."""

    recipes: list[RecipeOut]


@router.get("")
async def list_recipes(found: ServicesDep) -> RecipeList:
    """The saved recipes."""
    return _list(found.image_recipes.recipes())


@router.post("")
async def save_recipe(body: RecipeIn, found: ServicesDep) -> RecipeOut:
    """Save a recipe by its name, after checking model, levels and LoRAs."""
    await _check_model(body, found)
    saved = found.image_recipes.save(
        Recipe(
            "",
            body.name,
            body.model,
            body.aspect_ratio,
            body.scene,
            body.resolution,
            body.quality,
            tuple(RecipeLora(lora.id, lora.weight) for lora in body.loras),
        )
    )
    return _out(saved)


@router.put("")
async def set_recipes(body: RecipeListIn, found: ServicesDep) -> RecipeList:
    """Save names, scenes and order as edited; left out is removed."""
    return _list(
        found.image_recipes.replace([(item.id, item.name, item.scene) for item in body.recipes])
    )


async def _check_model(body: RecipeIn, found: Services) -> None:
    """Refuse a model that cannot be chosen, levels it does not offer and LoRAs that do not fit.

    Raises:
        InvalidInput: What does not fit, in words for the author.
    """
    if is_runware(body.model):
        model = found.runware_models.model(body.model)
        if model is None:
            raise InvalidInput(f"Bildmodell nicht in der Runware-Liste: {body.model}")
        if body.resolution is not None or body.quality is not None:
            raise InvalidInput("Runware-Modelle haben keine Auflösung oder Qualität zur Wahl")
        for choice in body.loras:
            lora = found.runware_models.lora(choice.id)
            if lora is None:
                raise InvalidInput(f"LoRA nicht in der Liste: {choice.id}")
            if not fits(lora, model):
                raise InvalidInput(f"{lora.name} passt nicht zu {model.name}")
        return
    if body.loras:
        raise InvalidInput("LoRAs gibt es nur bei Modellen der Runware-Liste")
    await found.image_catalog.refresh()
    known = found.image_catalog.model(body.model)
    if known is None:
        raise InvalidInput(f"Unbekanntes Bildmodell: {body.model}")
    if body.resolution is not None and body.resolution not in known.resolutions:
        raise InvalidInput("Diese Auflösung bietet das Bildmodell nicht an")
    if body.quality is not None and body.quality not in known.qualities:
        raise InvalidInput("Diese Qualität bietet das Bildmodell nicht an")


def _out(recipe: Recipe) -> RecipeOut:
    return RecipeOut(
        id=recipe.id,
        name=recipe.name,
        model=recipe.model,
        aspect_ratio=recipe.aspect_ratio,
        resolution=recipe.resolution,
        quality=recipe.quality,
        loras=[RecipeLoraIo(id=lora.id, weight=lora.weight) for lora in recipe.loras],
        scene=recipe.scene,
    )


def _list(recipes: list[Recipe]) -> RecipeList:
    return RecipeList(recipes=[_out(recipe) for recipe in recipes])
