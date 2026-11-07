"""The owner's image models and LoRAs at Runware (roadmap step 10.8, ADR-115).

``system/runware-modelle.md`` holds two header fields: ``grundmodelle``, the base models in the
chosen order (identifier, name, architecture, addition to the prompt), and ``loras``, the
additions (identifier, name, architecture, trigger words, weight). Without the file the start
list applies. Every entry was looked up at Runware before it was added; the list never takes an
identifier Runware does not list.
"""

import math
import re
import threading
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Final

from skriptorium.storage import DocumentStore, InvalidInput, NotFound

PATH: Final = "system/runware-modelle.md"
MAX_MODELS: Final = 50
MAX_LORAS: Final = 100
MAX_TEXT: Final = 200
MAX_WORDS: Final = 500
MIN_WEIGHT: Final = -2.0
MAX_WEIGHT: Final = 2.0

# An identifier as Runware forms it (the same pattern as in ``ai_gateway``).
_AIR: Final = re.compile(r"[a-z0-9_-]{1,40}:[A-Za-z0-9._-]{1,80}@[A-Za-z0-9._-]{1,80}")
# A Civitai link with a version: civitai.com or civitai.red, ``/models/<id>...?modelVersionId=<v>``.
_CIVITAI: Final = re.compile(
    r"https?://(?:www\.)?civitai\.(?:com|red)/models/(\d{1,12})(?:/[^?#\s]*)?"
    r"\?(?:[^#\s]*&)?modelVersionId=(\d{1,12})(?:[&#][^\s]*)?"
)
_CIVITAI_ANY: Final = re.compile(r"https?://(?:www\.)?civitai\.(?:com|red)/", re.IGNORECASE)

# Architectures that share their weights: a LoRA fits a base model of the same family.
_FAMILIES: Final[Mapping[str, str]] = {
    "sdxl": "sdxl",
    "sdxllightning": "sdxl",
    "sdxlturbo": "sdxl",
    "sdxlhyper": "sdxl",
    "pony": "sdxl",
    "illustrious": "sdxl",
    "noobai": "sdxl",
    "sd1x": "sd1",
    "sd1xlcm": "sd1",
    "flux1d": "flux1",
    "flux1s": "flux1",
}


@dataclass(frozen=True)
class RunwareModel:
    """A base model at Runware; ``addition`` is appended to every prompt (e.g. quality tags)."""

    id: str
    name: str
    architecture: str
    addition: str = ""


@dataclass(frozen=True)
class Lora:
    """An addition to base models of the same family, with its trigger words and weight."""

    id: str
    name: str
    architecture: str
    trigger: str
    weight: float


START: Final[tuple[RunwareModel, ...]] = (
    RunwareModel("runware:400@1", "FLUX.2 [dev]", "flux_2_dev"),
    RunwareModel("runware:z-image@turbo", "Z-Image-Turbo", "z_image_turbo"),
    RunwareModel("runware:97@2", "HiDream-I1 Dev", "hidreamdev"),
    RunwareModel("civitai:277058@1405120", "epiCRealism XL VXIV", "sdxl"),
)


def family(architecture: str) -> str:
    """The family of an architecture; an unknown one is a family of its own."""
    return _FAMILIES.get(architecture, architecture)


def fits(lora: Lora, model: RunwareModel) -> bool:
    """Whether ``lora`` works with ``model``: same family, known architecture."""
    return bool(lora.architecture) and family(lora.architecture) == family(model.architecture)


def identifier(reference: str) -> str:
    """The Runware identifier of ``reference``: an identifier or a Civitai link with a version.

    Raises:
        InvalidInput: Neither, or a Civitai link without ``modelVersionId``.
    """
    given = reference.strip()
    if _AIR.fullmatch(given):
        return given
    link = _CIVITAI.fullmatch(given)
    if link is not None:
        return f"civitai:{link.group(1)}@{link.group(2)}"
    if _CIVITAI_ANY.match(given):
        raise InvalidInput(
            "Im Civitai-Link fehlt die Version (modelVersionId) - bitte den Link einer "
            "bestimmten Version einfügen"
        )
    raise InvalidInput("Keine Kennung (z. B. civitai:277058@1405120) und kein Civitai-Link")


def is_runware(model: str) -> bool:
    """Whether ``model`` is a Runware identifier (OpenRouter's have the form ``a/b``)."""
    return _AIR.fullmatch(model) is not None


class RunwareModels:
    """Reads and writes the list of base models and LoRAs."""

    def __init__(self, store: DocumentStore) -> None:
        """Use ``store`` for ``system/runware-modelle.md``."""
        self._store = store
        self._lock = threading.Lock()

    def models(self) -> list[RunwareModel]:
        """The base models; the start list if none were saved.

        Raises:
            InvalidInput: The file is broken.
        """
        header = self._header()
        if "grundmodelle" not in header:
            return list(START)
        return [_base_model(item) for item in _items(header["grundmodelle"], "grundmodelle")]

    def loras(self) -> list[Lora]:
        """The LoRAs; none if none were saved.

        Raises:
            InvalidInput: The file is broken.
        """
        return [_lora(item) for item in _items(self._header().get("loras", []), "loras")]

    def model(self, model_id: str) -> RunwareModel | None:
        """The base model with this identifier; ``None`` if it is not in the list."""
        return next((m for m in self.models() if m.id == model_id), None)

    def lora(self, lora_id: str) -> Lora | None:
        """The LoRA with this identifier; ``None`` if it is not in the list."""
        return next((lora for lora in self.loras() if lora.id == lora_id), None)

    def add_model(self, model: RunwareModel) -> None:
        """Append ``model``; an entry with the same identifier is replaced in place.

        Raises:
            InvalidInput: The list is full or a field is out of bounds.
        """
        checked = _check_model(model)
        with self._lock:
            current = self.models()
            replaced = [checked if m.id == checked.id else m for m in current]
            if not any(m.id == checked.id for m in current):
                if len(current) >= MAX_MODELS:
                    raise InvalidInput(f"Höchstens {MAX_MODELS} Grundmodelle")
                replaced.append(checked)
            self._write(replaced, self.loras())

    def add_lora(self, lora: Lora) -> None:
        """Append ``lora``; an entry with the same identifier is replaced in place.

        Raises:
            InvalidInput: The list is full or a field is out of bounds.
        """
        checked = _check_lora(lora)
        with self._lock:
            current = self.loras()
            replaced = [checked if x.id == checked.id else x for x in current]
            if not any(x.id == checked.id for x in current):
                if len(current) >= MAX_LORAS:
                    raise InvalidInput(f"Höchstens {MAX_LORAS} LoRAs")
                replaced.append(checked)
            self._write(self.models(), replaced)

    def replace(self, models: Sequence[RunwareModel], loras: Sequence[Lora]) -> None:
        """Save the lists as edited: order, names, additions, trigger words and weights.

        Only entries already in the list are taken; their architecture stays as looked up.
        Leaving an entry out removes it.

        Raises:
            InvalidInput: An unknown or repeated identifier, or a field out of bounds.
        """
        with self._lock:
            known_models = {m.id: m for m in self.models()}
            known_loras = {x.id: x for x in self.loras()}
            _unique([m.id for m in models])
            _unique([x.id for x in loras])
            new_models = []
            for model in models:
                old = known_models.get(model.id)
                if old is None:
                    raise InvalidInput(f"Grundmodell nicht in der Liste: {model.id}")
                new_models.append(
                    _check_model(RunwareModel(old.id, model.name, old.architecture, model.addition))
                )
            new_loras = []
            for lora in loras:
                found = known_loras.get(lora.id)
                if found is None:
                    raise InvalidInput(f"LoRA nicht in der Liste: {lora.id}")
                new_loras.append(
                    _check_lora(
                        Lora(found.id, lora.name, found.architecture, lora.trigger, lora.weight)
                    )
                )
            self._write(new_models, new_loras)

    def _header(self) -> dict[str, Any]:
        try:
            return dict(self._store.read(PATH).header)
        except NotFound:
            return {}

    def _write(self, models: Sequence[RunwareModel], loras: Sequence[Lora]) -> None:
        self._store.write(
            PATH,
            {
                "grundmodelle": [
                    {
                        "kennung": m.id,
                        "name": m.name,
                        "architektur": m.architecture,
                        "zusatz": m.addition,
                    }
                    for m in models
                ],
                "loras": [
                    {
                        "kennung": x.id,
                        "name": x.name,
                        "architektur": x.architecture,
                        "ausloesewort": x.trigger,
                        "gewicht": x.weight,
                    }
                    for x in loras
                ],
            },
            "",
        )


def _unique(ids: Sequence[str]) -> None:
    if len(set(ids)) != len(ids):
        raise InvalidInput("Eine Kennung steht doppelt in der Liste")


def _items(value: object, field: str) -> list[Mapping[str, object]]:
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise InvalidInput(f"{PATH}: Feld '{field}' muss eine Liste von Einträgen sein")
    return [item for item in value if isinstance(item, dict)]


def _field(item: Mapping[str, object], name: str) -> str:
    value = item.get(name, "")
    if not isinstance(value, str):
        raise InvalidInput(f"{PATH}: Feld '{name}' muss Text sein")
    return value


def _base_model(item: Mapping[str, object]) -> RunwareModel:
    model = RunwareModel(
        _field(item, "kennung"),
        _field(item, "name"),
        _field(item, "architektur"),
        _field(item, "zusatz"),
    )
    if not _AIR.fullmatch(model.id):
        raise InvalidInput(f"{PATH}: ungültige Kennung")
    return model


def _lora(item: Mapping[str, object]) -> Lora:
    weight = item.get("gewicht", 1.0)
    if not isinstance(weight, int | float) or isinstance(weight, bool):
        raise InvalidInput(f"{PATH}: Feld 'gewicht' muss eine Zahl sein")
    lora = Lora(
        _field(item, "kennung"),
        _field(item, "name"),
        _field(item, "architektur"),
        _field(item, "ausloesewort"),
        float(weight),
    )
    if not _AIR.fullmatch(lora.id):
        raise InvalidInput(f"{PATH}: ungültige Kennung")
    return lora


def _line(text: str, limit: int, what: str) -> str:
    """One line of at most ``limit`` characters."""
    cleaned = " ".join(text.split())
    if len(cleaned) > limit:
        raise InvalidInput(f"{what}: höchstens {limit} Zeichen")
    return cleaned


def _check_model(model: RunwareModel) -> RunwareModel:
    if not _AIR.fullmatch(model.id):
        raise InvalidInput("Ungültige Kennung")
    name = _line(model.name, MAX_TEXT, "Name") or model.id
    return RunwareModel(
        model.id,
        name,
        _line(model.architecture, MAX_TEXT, "Architektur").lower(),
        _line(model.addition, MAX_WORDS, "Zusatz"),
    )


def _check_lora(lora: Lora) -> Lora:
    if not _AIR.fullmatch(lora.id):
        raise InvalidInput("Ungültige Kennung")
    if not math.isfinite(lora.weight) or not MIN_WEIGHT <= lora.weight <= MAX_WEIGHT:
        raise InvalidInput(f"Gewicht zwischen {MIN_WEIGHT} und {MAX_WEIGHT}")
    name = _line(lora.name, MAX_TEXT, "Name") or lora.id
    return Lora(
        lora.id,
        name,
        _line(lora.architecture, MAX_TEXT, "Architektur").lower(),
        _line(lora.trigger, MAX_WORDS, "Auslösewort"),
        round(lora.weight, 2),
    )
