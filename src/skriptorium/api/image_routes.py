"""Endpoints for generating images with the AI (roadmap steps 7.12, 9.8, 10.8, ADR-077, ADR-097,
ADR-115).

Nothing is stored here: ``generate`` returns the image for a preview. Taking it over goes the
way of an uploaded image (the browser shrinks it, the canon or manuscript routes check and store
it), so every check of steps 7.6, 7.10 and 7.11 applies unchanged. The delivered image is checked
by its first bytes before it reaches the browser; SVG and anything else is refused. An image to
build on is named by where it is stored; the server reads it itself (ADR-097).

Two providers serve images (ADR-115): OpenRouter for its catalog, Runware for the base models
and LoRAs in the owner's list. Which one serves a model follows from its identifier: Runware's
have the form ``source:model@version``, OpenRouter's ``vendor/model``. A model or LoRA goes into
the list only after Runware listed it.
"""

import base64
import logging
import secrets
from collections.abc import Container
from datetime import UTC, datetime
from typing import Annotated, Final, Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field, field_validator

from skriptorium.ai_gateway import (
    DEFAULT_IMAGE_MODEL,
    GatewayError,
    ImageOrder,
    ImageProvider,
    ImageReference,
    LoraChoice,
    ModelRefused,
    RateLimited,
    Usage,
    full_prompt,
)
from skriptorium.api.context import Services, ServicesDep, current_session
from skriptorium.api.runware_models import PATH as RUNWARE_PATH
from skriptorium.api.runware_models import START as RUNWARE_START
from skriptorium.api.runware_models import (
    Lora,
    RunwareModel,
    fits,
    identifier,
    is_runware,
)
from skriptorium.canon import ImageOrigin, OriginLora
from skriptorium.storage import InvalidInput, inspect_image

_log = logging.getLogger("skriptorium.api")

router = APIRouter(prefix="/api/images", dependencies=[Depends(current_session)])

# What a provider may deliver; the browser shrinks it before it is stored.
_MAX_DELIVERED_BYTES: Final = 40 * 1024 * 1024  # a 4K PNG (ADR-109)
_MAX_DELIVERED_SIDE: Final = 8192
_MEDIA_TYPES: Final = {"png": "image/png", "jpeg": "image/jpeg", "webp": "image/webp"}

AspectRatio = Literal["2:3", "1:1", "3:2", "16:9", "9:16", "3:4", "4:3"]


class ImageModelOut(BaseModel):
    """One image model; ``references`` is how many images it takes as a basis (ADR-097),
    ``resolutions`` and ``qualities`` the levels it offers, empty for none (ADR-109)."""

    id: str
    name: str
    references: int
    resolutions: list[str]
    qualities: list[str]
    # Whether it takes a start value (ADR-121); Runware models always do.
    seed: bool = False


class RunwareModelOut(BaseModel):
    """A base model at Runware (ADR-115); ``loras`` are the LoRAs of the list that fit it."""

    id: str
    name: str
    architecture: str
    addition: str
    loras: list[str]


class LoraOut(BaseModel):
    """A LoRA of the list (ADR-115)."""

    id: str
    name: str
    architecture: str
    trigger: str
    weight: float


class ImageModelList(BaseModel):
    """The image models, the preset one, and whether the list could be loaded."""

    default: str
    models: list[ImageModelOut]
    available: bool
    # False if no key is set up; generating then answers 503.
    ready: bool
    # The owner's models and LoRAs at Runware, and whether its key is set up (ADR-115).
    runware: list[RunwareModelOut] = []
    loras: list[LoraOut] = []
    runware_ready: bool = False


class RunwareListIn(BaseModel):
    """The edited list: order, names, additions, trigger words, weights; left out is removed."""

    models: Annotated[list[RunwareModelIn], Field(max_length=50)]
    loras: Annotated[list[LoraIn], Field(max_length=100)]


class RunwareAddIn(BaseModel):
    """A Runware identifier or a Civitai link with a version, to look up and add."""

    reference: Annotated[str, Field(min_length=1, max_length=500)]


class ImagePriceOut(BaseModel):
    """The price of one image; ``unit`` is image, megapixel or token, ``None`` if unknown.

    ``input_cost_usd`` and ``input_unit`` price an image given as the basis, if the provider
    names it (ADR-097).
    """

    cost_usd: float | None
    unit: str | None
    input_cost_usd: float | None = None
    input_unit: str | None = None


_Id = Annotated[str, Field(min_length=1, max_length=200)]
# A level as the catalog names it, e.g. "2K" or "medium" (ADR-109).
_Level = Annotated[str, Field(min_length=1, max_length=20)]
# A start value every provider takes (ADR-121); the server draws one in this range itself.
MAX_SEED: Final = 2_147_483_647
_Seed = Annotated[int, Field(ge=1, le=MAX_SEED)]


class ReferenceIn(BaseModel):
    """A stored image as the basis: an image of an entry, a map or the cover of a story."""

    world: _Id
    entry: _Id | None = None
    image: _Id | None = None
    map_file: _Id | None = None
    story: _Id | None = None


class RunwareModelIn(BaseModel):
    """A base model of the list as edited."""

    id: _Id
    name: Annotated[str, Field(max_length=200)]
    addition: Annotated[str, Field(max_length=500)] = ""


class LoraIn(BaseModel):
    """A LoRA of the list as edited."""

    id: _Id
    name: Annotated[str, Field(max_length=200)]
    trigger: Annotated[str, Field(max_length=500)] = ""
    weight: Annotated[float, Field(ge=-2, le=2)]


class LoraChoiceIn(BaseModel):
    """A LoRA of the list chosen for one image, with its weight."""

    id: _Id
    weight: Annotated[float, Field(ge=-2, le=2)]


class GenerateIn(BaseModel):
    """What to generate."""

    model: str
    prompt: Annotated[str, Field(min_length=1, max_length=4000)]
    aspect_ratio: AspectRatio = "1:1"
    # One stored image to build on (ADR-097).
    reference: ReferenceIn | None = None
    # Levels the model offers (ADR-109); without them the model's own default.
    resolution: _Level | None = None
    quality: _Level | None = None
    # LoRAs of the list for a Runware model (ADR-115).
    loras: Annotated[list[LoraChoiceIn], Field(max_length=5)] = []
    # A fixed start value (ADR-121); without it the server draws one for models that take it.
    seed: _Seed | None = None
    # Where the image is meant to go, for the usage statistics (ADR-100): a world for an entry
    # image or a map, a world and a story for a cover.
    world: _Id | None = None
    story: _Id | None = None

    @field_validator("prompt")
    @classmethod
    def _not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Bildbeschreibung fehlt")
        return value.strip()


class GeneratedOut(BaseModel):
    """The generated image for the preview, base64-encoded, with the reported cost."""

    content: str
    media_type: str
    cost_usd: float | None
    model: str
    # The start value sent, or ``None`` for a model without one (ADR-121).
    seed: int | None = None
    # At Runware the model's addition and the trigger words the server appended (ADR-121).
    appended: str | None = None


class OriginLoraIn(BaseModel):
    """A LoRA that went along with a taken-over image (ADR-121)."""

    id: _Id
    name: Annotated[str, Field(max_length=200)]
    weight: Annotated[float, Field(ge=-2, le=2)]


class OriginLoraOut(BaseModel):
    """A LoRA of a stored origin."""

    id: str
    name: str
    weight: float


class ImageOriginIn(BaseModel):
    """How a taken-over image was generated; sent along by the browser (step 9.6, ADR-095)."""

    model: Annotated[str, Field(min_length=1, max_length=200)]
    prompt: Annotated[str, Field(min_length=1, max_length=4000)]
    aspect_ratio: AspectRatio
    cost_usd: Annotated[float | None, Field(ge=0)] = None
    # A short description of the image it was made from, e.g. "Bild 1 von Kael" (ADR-097).
    basis: Annotated[str | None, Field(min_length=1, max_length=200)] = None
    # The levels chosen, if the model offered any (ADR-109).
    resolution: _Level | None = None
    quality: _Level | None = None
    # Start value, LoRAs and the appended text (ADR-121).
    seed: _Seed | None = None
    loras: Annotated[list[OriginLoraIn], Field(max_length=5)] = []
    appended: Annotated[str | None, Field(max_length=4000)] = None
    # The name of the recipe it was made with (ADR-126).
    recipe: Annotated[str | None, Field(min_length=1, max_length=100)] = None


class ImageOriginOut(BaseModel):
    """The stored origin of an image, with the date it was taken over."""

    model: str
    prompt: str
    aspect_ratio: str
    cost_usd: float | None
    date: str
    basis: str | None
    resolution: str | None = None
    quality: str | None = None
    seed: int | None = None
    loras: list[OriginLoraOut] = []
    appended: str | None = None
    recipe: str | None = None


def origin_from(given: ImageOriginIn | None) -> ImageOrigin | None:
    """The origin to store, dated now; ``None`` for an uploaded image."""
    if given is None:
        return None
    now = datetime.now(UTC).isoformat(timespec="seconds")
    return ImageOrigin(
        given.model,
        given.prompt,
        given.aspect_ratio,
        given.cost_usd,
        now,
        given.basis,
        given.resolution,
        given.quality,
        given.seed,
        tuple(OriginLora(lora.id, lora.name, lora.weight) for lora in given.loras),
        given.appended,
        given.recipe,
    )


def origin_out(origin: ImageOrigin | None) -> ImageOriginOut | None:
    """The stored origin for the browser; ``None`` if the image has none."""
    if origin is None:
        return None
    return ImageOriginOut(
        model=origin.model,
        prompt=origin.prompt,
        aspect_ratio=origin.aspect_ratio,
        cost_usd=origin.cost_usd,
        date=origin.date,
        basis=origin.basis,
        resolution=origin.resolution,
        quality=origin.quality,
        seed=origin.seed,
        loras=[OriginLoraOut(id=x.id, name=x.name, weight=x.weight) for x in origin.loras],
        appended=origin.appended,
        recipe=origin.recipe,
    )


class Selectable(Container[str]):
    """The image models that can be chosen: OpenRouter's catalog and the Runware list."""

    def __init__(self, found: Services) -> None:
        """Ask ``found`` for both lists."""
        self._found = found

    def __contains__(self, model: object) -> bool:
        """Whether ``model`` can be chosen."""
        if not isinstance(model, str):
            return False
        if is_runware(model):
            try:
                return self._found.runware_models.model(model) is not None
            except InvalidInput:
                return False
        return model in self._found.image_catalog


@router.get("/models")
async def list_image_models(found: ServicesDep) -> ImageModelList:
    """The image models of the catalog (step 7.12) and of the Runware list (ADR-115);
    ``default`` is the saved one (ADR-096)."""
    await found.image_catalog.refresh()
    return ImageModelList(
        default=found.favorites.preset("bilderzeugung", Selectable(found), DEFAULT_IMAGE_MODEL),
        models=[
            ImageModelOut(
                id=m.id,
                name=m.name,
                references=m.references,
                resolutions=list(m.resolutions),
                qualities=list(m.qualities),
                seed=m.seed,
            )
            for m in found.image_catalog.models()
        ],
        available=found.image_catalog.available,
        ready=found.images is not None,
        **_runware_lists(found),
    )


@router.post("/runware")
async def add_runware_model(body: RunwareAddIn, found: ServicesDep) -> ImageModelList:
    """Look up a base model or LoRA at Runware and add it to the list (ADR-115).

    Only what Runware lists is added; a LoRA takes its trigger words and default weight.
    """
    if found.runware is None:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Runware nicht eingerichtet")
    air = identifier(body.reference)
    try:
        info = await found.runware.lookup(air)
    except GatewayError as error:
        raise _http_error(error) from None
    if info is None:
        raise InvalidInput(
            f"Runware führt {air} nicht. Nur Versionen, die Runware anbietet, sind nutzbar."
        )
    if info.kind == "checkpoint":
        found.runware_models.add_model(RunwareModel(air, info.name, info.architecture))
    else:
        weight = info.default_weight if info.default_weight is not None else 1.0
        found.runware_models.add_lora(
            Lora(air, info.name, info.architecture, info.trigger, max(-2.0, min(2.0, weight)))
        )
    return await list_image_models(found)


@router.put("/runware")
async def set_runware_models(body: RunwareListIn, found: ServicesDep) -> ImageModelList:
    """Save the edited list (order, names, additions, trigger words, weights) (ADR-115)."""
    found.runware_models.replace(
        [RunwareModel(m.id, m.name, "", m.addition) for m in body.models],
        [Lora(x.id, x.name, "", x.trigger, x.weight) for x in body.loras],
    )
    return await list_image_models(found)


def _runware_lists(found: Services) -> dict[str, object]:
    """The Runware lists for the answer; a broken file (edited by hand) shows the start list and
    no LoRAs instead of blocking every image (finding 2 of the separate review of 10.8)."""
    try:
        models = found.runware_models.models()
        loras = found.runware_models.loras()
    except InvalidInput:
        _log.warning("runware_liste_defekt datei=%s", RUNWARE_PATH)
        models, loras = list(RUNWARE_START), []
    return {
        "runware": [
            RunwareModelOut(
                id=m.id,
                name=m.name,
                architecture=m.architecture,
                addition=m.addition,
                loras=[x.id for x in loras if fits(x, m)],
            )
            for m in models
        ],
        "loras": [
            LoraOut(
                id=x.id,
                name=x.name,
                architecture=x.architecture,
                trigger=x.trigger,
                weight=x.weight,
            )
            for x in loras
        ],
        "runware_ready": found.runware is not None,
    }


@router.get("/price")
async def image_price(
    model: str,
    found: ServicesDep,
    resolution: Annotated[str | None, Query(max_length=20)] = None,
    quality: Annotated[str | None, Query(max_length=20)] = None,
) -> ImagePriceOut:
    """The price of one image of ``model`` at its first provider, at the given levels (ADR-109)."""
    if is_runware(model):
        # Runware bills most models by compute time: the cost shows after generating.
        if found.runware_models.model(model) is None:
            raise InvalidInput(f"Unbekanntes Bildmodell: {model}")
        return ImagePriceOut(cost_usd=None, unit=None)
    await found.image_catalog.refresh()
    _check_levels(found, model, resolution, quality)
    price = await found.image_catalog.price(model, resolution, quality)
    given = await found.image_catalog.input_price(model)
    return ImagePriceOut(
        cost_usd=price.cost_usd if price else None,
        unit=price.unit if price else None,
        input_cost_usd=given.cost_usd if given else None,
        input_unit=given.unit if given else None,
    )


@router.post("/generate")
async def generate_image(body: GenerateIn, found: ServicesDep) -> GeneratedOut:
    """Generate one image for the preview; stores nothing (ADR-077, ADR-115)."""
    appended: str | None = None
    if is_runware(body.model):
        provider, order, appended = _runware_order(body, found)
    else:
        provider, order = await _openrouter_order(body, found)
    record = found.usage.recorder(body.world, body.story)
    try:
        image = await provider.generate(order)
    except GatewayError as error:
        record("bilderzeugung", body.model, None, _outcome(error))
        raise _http_error(error) from None
    record("bilderzeugung", body.model, Usage(None, None, image.cost_usd), "ok")
    try:
        info = inspect_image(
            image.data, max_bytes=_MAX_DELIVERED_BYTES, max_side=_MAX_DELIVERED_SIDE
        )
    except InvalidInput:
        raise HTTPException(
            status.HTTP_502_BAD_GATEWAY, "Das Modell hat kein verwendbares Bild geliefert"
        ) from None
    return GeneratedOut(
        content=base64.b64encode(image.data).decode("ascii"),
        media_type=_MEDIA_TYPES[info.kind],
        cost_usd=image.cost_usd,
        model=body.model,
        seed=order.seed,
        appended=appended,
    )


async def _openrouter_order(body: GenerateIn, found: Services) -> tuple[ImageProvider, ImageOrder]:
    """Provider and order for a model of OpenRouter's catalog.

    Raises:
        HTTPException: 503 without a key.
        InvalidInput: Unknown model, levels or basis it does not take, or LoRAs.
    """
    if found.images is None:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "KI-Anbieter nicht eingerichtet")
    await found.image_catalog.refresh()
    _check_levels(found, body.model, body.resolution, body.quality)
    if body.loras:
        raise InvalidInput("Zusätze (LoRAs) gibt es nur bei Modellen von Runware")
    catalog_model = found.image_catalog.model(body.model)
    takes_seed = catalog_model is not None and catalog_model.seed
    if body.seed is not None and not takes_seed:
        raise InvalidInput("Dieses Bildmodell nimmt keinen Startwert an")
    reference = None
    if body.reference is not None:
        if found.image_catalog.references(body.model) < 1:
            raise InvalidInput("Dieses Bildmodell nimmt kein Ausgangsbild an")
        reference = ImageReference(*_basis(body.reference, found))
    order = ImageOrder(
        body.model,
        body.prompt,
        body.aspect_ratio,
        reference,
        body.resolution,
        body.quality,
        seed=_seed(body.seed) if takes_seed else None,
    )
    return found.images, order


def _runware_order(
    body: GenerateIn, found: Services
) -> tuple[ImageProvider, ImageOrder, str | None]:
    """Provider, order and the appended text for a base model of the Runware list (ADR-115).

    The model's addition and the trigger words of the chosen LoRAs are appended to the prompt;
    every Runware model takes a start value (ADR-121).

    Raises:
        HTTPException: 503 without a key.
        InvalidInput: A model or LoRA not in the list, a LoRA that does not fit the model, a
            basis image or levels.
    """
    if found.runware is None:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Runware nicht eingerichtet")
    model = found.runware_models.model(body.model)
    if model is None:
        raise InvalidInput(f"Unbekanntes Bildmodell: {body.model}")
    if body.reference is not None or body.resolution is not None or body.quality is not None:
        raise InvalidInput("Ausgangsbild, Auflösung und Qualität gibt es bei Runware hier nicht")
    if len({choice.id for choice in body.loras}) != len(body.loras):
        raise InvalidInput("Ein Zusatz ist doppelt gewählt")
    chosen: list[Lora] = []
    for choice in body.loras:
        lora = found.runware_models.lora(choice.id)
        if lora is None:
            raise InvalidInput(f"Unbekannter Zusatz: {choice.id}")
        if not fits(lora, model):
            raise InvalidInput(f"{lora.name} passt nicht zu {model.name}")
        chosen.append(lora)
    additions = (model.addition, *(lora.trigger for lora in chosen))
    order = ImageOrder(
        model.id,
        full_prompt(body.prompt, *additions),
        body.aspect_ratio,
        loras=tuple(
            LoraChoice(lora.id, choice.weight)
            for lora, choice in zip(chosen, body.loras, strict=True)
        ),
        seed=_seed(body.seed),
    )
    return found.runware, order, full_prompt("", *additions) or None


def _seed(given: int | None) -> int:
    """The start value to send: the fixed one, else one drawn here (ADR-121)."""
    return given if given is not None else secrets.randbelow(MAX_SEED) + 1


def _check_levels(found: Services, model: str, resolution: str | None, quality: str | None) -> None:
    """Refuse an unknown model and levels it does not offer (ADR-109).

    Raises:
        InvalidInput: Unknown model, or a resolution or quality it does not offer.
    """
    known = found.image_catalog.model(model)
    if known is None:
        raise InvalidInput(f"Unbekanntes Bildmodell: {model}")
    if resolution is not None and resolution not in known.resolutions:
        raise InvalidInput("Diese Auflösung bietet das Bildmodell nicht an")
    if quality is not None and quality not in known.qualities:
        raise InvalidInput("Diese Qualität bietet das Bildmodell nicht an")


def _basis(reference: ReferenceIn, found: Services) -> tuple[bytes, str]:
    """Bytes and media type of the stored image to build on.

    Raises:
        InvalidInput: Not exactly one of entry image, map or cover named.
        NotFound: World, entry, image, map, story or cover does not exist.
    """
    named = [
        reference.entry is not None or reference.image is not None,
        reference.map_file is not None,
        reference.story is not None,
    ]
    if sum(named) != 1:
        raise InvalidInput("Grundlage: genau ein Eintragsbild, eine Karte oder ein Titelbild")
    if reference.map_file is not None:
        return found.canon.world_map(reference.world, reference.map_file)
    if reference.story is not None:
        return found.manuscript.story_cover(reference.world, reference.story)
    if reference.entry is None or reference.image is None:
        raise InvalidInput("Grundlage: Eintrag und Bild angeben")
    return found.canon.entry_image(reference.world, reference.entry, reference.image)


def _outcome(error: GatewayError) -> str:
    if isinstance(error, ModelRefused):
        return "abgelehnt"
    if isinstance(error, RateLimited):
        return "zu_viele_anfragen"
    return "fehler"


def _http_error(error: GatewayError) -> HTTPException:
    """A refusal or failure as an answer the interface shows; it names no prompt."""
    if isinstance(error, ModelRefused):
        return HTTPException(
            status.HTTP_422_UNPROCESSABLE_CONTENT,
            "Das Modell hat das Bild abgelehnt. Probier ein anderes Modell oder ändere die "
            "Beschreibung. Abgelehnte Bilder kosten nichts.",
        )
    if isinstance(error, RateLimited):
        return HTTPException(
            status.HTTP_429_TOO_MANY_REQUESTS,
            "Der Anbieter meldet zu viele Anfragen. Bitte kurz warten.",
        )
    return HTTPException(
        status.HTTP_502_BAD_GATEWAY,
        f"{error}. Probier ein anderes Modell oder ändere die Beschreibung.",
    )


RunwareListIn.model_rebuild()
