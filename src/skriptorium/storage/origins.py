"""Origin of a generated image, kept in a companion file next to it (steps 9.6, 9.8, 10.5,
11.4, 11.6, ADR-095, ADR-097, ADR-109, ADR-121, ADR-126).

The companion ``<image>.herkunft.yml`` holds plain YAML, not a Markdown document, so the
search index (which reads every ``.md`` file) never sees it. Images without a companion
(uploaded, or generated before step 9.6) simply have no origin.
"""

from dataclasses import dataclass
from typing import Final

from skriptorium.storage.errors import InvalidInput
from skriptorium.storage.frontmatter import HeaderValue

ORIGIN_SUFFIX: Final = ".herkunft.yml"


@dataclass(frozen=True)
class OriginLora:
    """A LoRA that went along with the image, with its name and weight (ADR-121)."""

    id: str
    name: str
    weight: float


@dataclass(frozen=True)
class ImageOrigin:
    """How an image was generated: model, prompt, aspect ratio, reported cost, date taken over,
    if it was made from another image a short description of that basis, and the resolution and
    quality chosen (ADR-109; ``None`` when the model offers none or for older origins), and
    since step 11.4 (ADR-121) the start value, the LoRAs with their weights and the text the
    server appended to the prompt (``None`` or empty when there were none, or for older ones)."""

    model: str
    prompt: str
    aspect_ratio: str
    cost_usd: float | None
    date: str
    basis: str | None = None
    resolution: str | None = None
    quality: str | None = None
    seed: int | None = None
    loras: tuple[OriginLora, ...] = ()
    appended: str | None = None
    # The name of the recipe it was made with (step 11.6, ADR-126); ``None`` without one.
    recipe: str | None = None


def origin_to_mapping(origin: ImageOrigin) -> dict[str, HeaderValue]:
    """The fields as written to the companion file."""
    mapping: dict[str, HeaderValue] = {
        "modell": origin.model,
        "anweisung": origin.prompt,
        "seitenverhaeltnis": origin.aspect_ratio,
        "kosten_usd": origin.cost_usd,
        "datum": origin.date,
    }
    if origin.basis is not None:
        mapping["grundlage"] = origin.basis
    if origin.resolution is not None:
        mapping["aufloesung"] = origin.resolution
    if origin.quality is not None:
        mapping["qualitaet"] = origin.quality
    if origin.seed is not None:
        mapping["startwert"] = origin.seed
    if origin.loras:
        mapping["loras"] = [
            {"kennung": lora.id, "name": lora.name, "gewicht": lora.weight} for lora in origin.loras
        ]
    if origin.appended is not None:
        mapping["angehaengt"] = origin.appended
    if origin.recipe is not None:
        mapping["rezept"] = origin.recipe
    return mapping


def origin_from_mapping(mapping: dict[str, HeaderValue]) -> ImageOrigin:
    """Read the fields of a companion file.

    Raises:
        InvalidInput: A field is missing or has the wrong type.
    """
    model = mapping.get("modell")
    prompt = mapping.get("anweisung")
    aspect_ratio = mapping.get("seitenverhaeltnis")
    cost = mapping.get("kosten_usd")
    date = mapping.get("datum")
    basis = mapping.get("grundlage")
    resolution = mapping.get("aufloesung")
    quality = mapping.get("qualitaet")
    seed = mapping.get("startwert")
    appended = mapping.get("angehaengt")
    recipe = mapping.get("rezept")
    if not (
        isinstance(model, str)
        and isinstance(prompt, str)
        and isinstance(aspect_ratio, str)
        and isinstance(date, str)
    ):
        raise InvalidInput("Herkunft des Bildes unvollständig")
    if cost is not None and (isinstance(cost, bool) or not isinstance(cost, int | float)):
        raise InvalidInput("Kosten in der Herkunft des Bildes keine Zahl")
    if basis is not None and not isinstance(basis, str):
        raise InvalidInput("Grundlage in der Herkunft des Bildes kein Text")
    if not all(value is None or isinstance(value, str) for value in (resolution, quality)):
        raise InvalidInput("Auflösung oder Qualität in der Herkunft des Bildes kein Text")
    if seed is not None and (isinstance(seed, bool) or not isinstance(seed, int)):
        raise InvalidInput("Startwert in der Herkunft des Bildes keine ganze Zahl")
    if appended is not None and not isinstance(appended, str):
        raise InvalidInput("Angehängter Text in der Herkunft des Bildes kein Text")
    if recipe is not None and not isinstance(recipe, str):
        raise InvalidInput("Rezept in der Herkunft des Bildes kein Text")
    return ImageOrigin(
        model,
        prompt,
        aspect_ratio,
        None if cost is None else float(cost),
        date,
        basis,
        resolution if isinstance(resolution, str) else None,
        quality if isinstance(quality, str) else None,
        seed if isinstance(seed, int) else None,
        _loras(mapping.get("loras")),
        appended if isinstance(appended, str) else None,
        recipe if isinstance(recipe, str) else None,
    )


def _loras(value: HeaderValue) -> tuple[OriginLora, ...]:
    """The LoRAs of a companion file; none if the field is missing.

    Raises:
        InvalidInput: The field is not a list of entries with identifier, name and weight.
    """
    if value is None:
        return ()
    if not isinstance(value, list):
        raise InvalidInput("LoRAs in der Herkunft des Bildes keine Liste")
    found: list[OriginLora] = []
    for item in value:
        lora_id = item.get("kennung") if isinstance(item, dict) else None
        name = item.get("name") if isinstance(item, dict) else None
        weight = item.get("gewicht") if isinstance(item, dict) else None
        if not (
            isinstance(lora_id, str)
            and isinstance(name, str)
            and isinstance(weight, int | float)
            and not isinstance(weight, bool)
        ):
            raise InvalidInput("LoRA in der Herkunft des Bildes unvollständig")
        found.append(OriginLora(lora_id, name, float(weight)))
    return tuple(found)
