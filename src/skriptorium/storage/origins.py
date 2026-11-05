"""Origin of a generated image, kept in a companion file next to it (steps 9.6, 9.8, 10.5,
ADR-095, ADR-097, ADR-109).

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
class ImageOrigin:
    """How an image was generated: model, prompt, aspect ratio, reported cost, date taken over,
    if it was made from another image a short description of that basis, and the resolution and
    quality chosen (ADR-109; ``None`` when the model offers none or for older origins)."""

    model: str
    prompt: str
    aspect_ratio: str
    cost_usd: float | None
    date: str
    basis: str | None = None
    resolution: str | None = None
    quality: str | None = None


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
    return ImageOrigin(
        model,
        prompt,
        aspect_ratio,
        None if cost is None else float(cost),
        date,
        basis,
        resolution if isinstance(resolution, str) else None,
        quality if isinstance(quality, str) else None,
    )
