"""Adapter for generating images through Runware (roadmap step 10.8, ADR-114, ADR-115).

``POST https://api.runware.ai/v1`` takes a list of tasks. ``imageInference`` generates an image;
it comes back as base64 (``outputType: base64Data``), so Runware stores no file, and with its
cost (``includeCost``). ``modelSearch`` looks up a model by its identifier (AIR, e.g.
``civitai:277058@1405120``): its kind (base model or LoRA), its architecture and, for a LoRA, its
trigger words and default weight.

The content check is fixed here, not configurable (ADR-115): ``safety.checkContent`` is always
sent as ``false`` - the owner wants content between fictional adults; Runware states no default,
so it is set explicitly. Runware's terms forbid sexual content involving minors regardless.
The adapter never calls ``accountManagement``: its answer lists the keys of the account.
"""

import base64
import binascii
import json
import logging
import math
import os
import re
import time
import uuid
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Final, Literal

import httpx

from skriptorium.ai_gateway.errors import (
    GatewayError,
    InvalidRequest,
    ModelRefused,
    ProviderUnavailable,
    RateLimited,
)
from skriptorium.ai_gateway.images import GeneratedImage, ImageOrder

RUNWARE_KEY_VARIABLE: Final = "RUNWARE_API_KEY"
_URL: Final = "https://api.runware.ai/v1"
_CONNECT_TIMEOUT_SECONDS: Final = 10.0
# A sync request waits up to 120 s at Runware; then the task continues without us.
_READ_TIMEOUT_SECONDS: Final = 150.0
MAX_PROMPT_CHARS: Final = 4000
# The largest answer read: a 40 MB image as base64 (4/3) plus room for the JSON around it.
MAX_ANSWER_BYTES: Final = 56 * 1024 * 1024
MAX_LORAS: Final = 5
# Fixed content check (ADR-115): off, sent explicitly.
CHECK_CONTENT: Final = False
# Pixel sizes per aspect ratio, about one megapixel, multiples of 64 (Runware wants 16).
SIZES: Final[Mapping[str, tuple[int, int]]] = {
    "1:1": (1024, 1024),
    "2:3": (832, 1216),
    "3:2": (1216, 832),
    "3:4": (896, 1152),
    "4:3": (1152, 896),
    "9:16": (768, 1344),
    "16:9": (1344, 768),
}
# An identifier as Runware forms it (AIR): source, model and version.
AIR: Final = re.compile(r"[a-z0-9_-]{1,40}:[A-Za-z0-9._-]{1,80}@[A-Za-z0-9._-]{1,80}")
_TEXT_LIMIT: Final = 200
_WORDS_LIMIT: Final = 500

_log = logging.getLogger("skriptorium.ai_gateway")

Kind = Literal["checkpoint", "lora"]


@dataclass(frozen=True)
class RunwareModelInfo:
    """What Runware reports about a model: kind, name, architecture, trigger words, weight."""

    air: str
    kind: Kind
    name: str
    architecture: str
    trigger: str
    default_weight: float | None


class RunwareImageProvider:
    """Generates images and looks up models at Runware; one client, reused."""

    name: str = "runware"

    def __init__(self, api_key: str, *, transport: httpx.AsyncBaseTransport | None = None) -> None:
        """Create the adapter; ``transport`` replaces the network in tests."""
        if not api_key:
            raise ProviderUnavailable(f"{RUNWARE_KEY_VARIABLE} ist nicht gesetzt")
        self._headers = {"Authorization": f"Bearer {api_key}"}
        self._client = httpx.AsyncClient(
            transport=transport,
            timeout=httpx.Timeout(
                connect=_CONNECT_TIMEOUT_SECONDS,
                read=_READ_TIMEOUT_SECONDS,
                write=_CONNECT_TIMEOUT_SECONDS,
                pool=_CONNECT_TIMEOUT_SECONDS,
            ),
        )

    @classmethod
    def from_environment(
        cls,
        environ: Mapping[str, str] = os.environ,
        *,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> RunwareImageProvider:
        """Create the adapter with the key from ``RUNWARE_API_KEY``.

        Raises:
            ProviderUnavailable: The variable is missing or empty.
        """
        return cls(environ.get(RUNWARE_KEY_VARIABLE, ""), transport=transport)

    def __repr__(self) -> str:
        """Representation without the key."""
        return "RunwareImageProvider()"

    async def aclose(self) -> None:
        """Close the reused client."""
        await self._client.aclose()

    async def generate(self, order: ImageOrder) -> GeneratedImage:
        """Generate one image; see :class:`~skriptorium.ai_gateway.ImageProvider`."""
        start = time.monotonic()
        result = "erfolg"
        cost: float | None = None
        try:
            task = _inference(order)
            row = await self._task(task)
            image = _image(row)
            cost = image.cost_usd
            return image
        except Exception as error:
            result = type(error).__name__
            raise
        finally:
            _log.info(
                "bild_anfrage anbieter=runware modell=%s loras=%d ergebnis=%s kosten_usd=%s "
                "dauer_ms=%d",
                _safe(order.model),
                len(order.loras),
                result,
                "-" if cost is None else cost,
                int((time.monotonic() - start) * 1000),
            )

    async def lookup(self, air: str) -> RunwareModelInfo | None:
        """The model with exactly this identifier; ``None`` if Runware does not list it.

        Runware refuses identifiers its search does not list (probe 2026-11-07), so this is the
        check before a model goes into the list.

        Raises:
            InvalidRequest: ``air`` is not an identifier.
            GatewayError: The search failed.
        """
        if not AIR.fullmatch(air):
            raise InvalidRequest("Keine gültige Kennung")
        row = await self._task({"taskType": "modelSearch", "search": air, "limit": 10})
        results = row.get("results")
        if not isinstance(results, list):
            raise ProviderUnavailable("Antwort der Modellsuche nicht lesbar")
        found = next(
            (r for r in results if isinstance(r, dict) and r.get("air") == air),
            None,
        )
        return None if found is None else _info(air, found)

    async def _task(self, task: dict[str, object]) -> dict[str, object]:
        """Send one task and return its row of the answer.

        Raises:
            GatewayError: Network, status or an error the answer names.
        """
        task_id = str(uuid.uuid4())
        failure: str | None = None
        status = 0
        content = b""
        try:
            async with self._client.stream(
                "POST", _URL, json=[{**task, "taskUUID": task_id}], headers=self._headers
            ) as response:
                status = response.status_code
                content = await _bounded(response)
        except httpx.HTTPError as exc:
            failure = type(exc).__name__
        if failure is not None:
            # Raised outside the except clause: the httpx error carries the request with its
            # authorization header and must not stay reachable via __context__.
            raise ProviderUnavailable(f"Verbindung fehlgeschlagen ({failure})")
        try:
            body = json.loads(content)
        except ValueError:
            body = None
        errors = body.get("errors") if isinstance(body, dict) else None
        if isinstance(errors, list) and errors:
            raise _error(status, errors[0])
        _check_status(status)
        data = body.get("data") if isinstance(body, dict) else None
        row = next(
            (
                r
                for r in (data if isinstance(data, list) else [])
                if isinstance(r, dict) and r.get("taskUUID") == task_id
            ),
            None,
        )
        if row is None:
            raise ProviderUnavailable("Antwort des Anbieters nicht lesbar")
        if row.get("status") == "processing":
            raise ProviderUnavailable("Das Bild war nach zwei Minuten noch nicht fertig")
        return row


class _TooLarge(httpx.HTTPError):
    """The answer is larger than :data:`MAX_ANSWER_BYTES`; reported like a broken connection."""


async def _bounded(response: httpx.Response) -> bytes:
    """The body of ``response``, read in pieces and refused once it grows too large.

    A base64 image up to the size the server takes (40 MB, ``image_routes``) plus the JSON around
    it fits; a larger answer is cut off before it fills the memory (finding 1 of the separate
    review of 10.8).

    Raises:
        httpx.HTTPError: The answer exceeds the bound, or the connection broke.
    """
    declared = response.headers.get("content-length", "")
    if declared.isdigit() and int(declared) > MAX_ANSWER_BYTES:
        raise _TooLarge("Antwort zu groß")
    chunks: list[bytes] = []
    size = 0
    async for chunk in response.aiter_bytes():
        size += len(chunk)
        if size > MAX_ANSWER_BYTES:
            raise _TooLarge("Antwort zu groß")
        chunks.append(chunk)
    return b"".join(chunks)


def full_prompt(prompt: str, *additions: str) -> str:
    """``prompt`` with the non-empty ``additions`` appended, separated by commas, bounded."""
    parts = [prompt.strip(), *(a.strip() for a in additions if a.strip())]
    return ", ".join(p for p in parts if p)[:MAX_PROMPT_CHARS]


def _inference(order: ImageOrder) -> dict[str, object]:
    """The ``imageInference`` task of ``order``.

    Raises:
        InvalidRequest: An aspect ratio without a size, a basis image, levels or too many LoRAs.
    """
    size = SIZES.get(order.aspect_ratio)
    if size is None:
        raise InvalidRequest("Dieses Format kennt der Anbieter nicht")
    if order.reference is not None or order.resolution is not None or order.quality is not None:
        raise InvalidRequest("Ausgangsbild, Auflösung und Qualität gibt es hier nicht")
    if len(order.loras) > MAX_LORAS:
        raise InvalidRequest(f"Höchstens {MAX_LORAS} Zusätze")
    task: dict[str, object] = {
        "taskType": "imageInference",
        "model": order.model,
        "positivePrompt": order.prompt[:MAX_PROMPT_CHARS],
        "width": size[0],
        "height": size[1],
        "numberResults": 1,
        "outputType": "base64Data",
        "outputFormat": "PNG",
        "includeCost": True,
        "safety": {"checkContent": CHECK_CONTENT},
    }
    if order.loras:
        task["lora"] = [{"model": lora.model, "weight": lora.weight} for lora in order.loras]
    return task


def _image(row: Mapping[str, object]) -> GeneratedImage:
    """The image of the answer row.

    Raises:
        ProviderUnavailable: The row holds no readable image.
    """
    encoded = row.get("imageBase64Data")
    if not isinstance(encoded, str):
        raise ProviderUnavailable("Der Anbieter hat kein Bild geliefert")
    try:
        data = base64.b64decode(encoded, validate=True)
    except binascii.Error, ValueError:
        raise ProviderUnavailable("Bild des Anbieters nicht lesbar") from None
    cost = row.get("cost")
    return GeneratedImage(
        data=data,
        # The server reads the type from the first bytes (``inspect_image``).
        media_type="",
        cost_usd=(
            float(cost)
            if isinstance(cost, int | float)
            and not isinstance(cost, bool)
            and math.isfinite(cost)
            and cost >= 0
            else None
        ),
    )


def _info(air: str, found: Mapping[str, object]) -> RunwareModelInfo | None:
    """The reported model; ``None`` for anything but a base model or a LoRA."""
    category = found.get("category")
    if category not in ("checkpoint", "lora"):
        return None
    kind: Kind = "checkpoint" if category == "checkpoint" else "lora"
    name = _text(found.get("name")) or air
    version = _text(found.get("version"))
    if version and version not in name:
        name = f"{name} {version}"
    weight = found.get("defaultWeight")
    return RunwareModelInfo(
        air=air,
        kind=kind,
        name=name[:_TEXT_LIMIT],
        architecture=_text(found.get("architecture")).lower(),
        trigger=_words(found.get("positiveTriggerWords")),
        default_weight=(
            float(weight)
            if isinstance(weight, int | float)
            and not isinstance(weight, bool)
            and math.isfinite(weight)
            else None
        ),
    )


def _text(value: object) -> str:
    """A short single-line text; empty for anything else."""
    if not isinstance(value, str):
        return ""
    return " ".join(value.split())[:_TEXT_LIMIT]


def _words(value: object) -> str:
    """Trigger words as one line; Runware sends them as text or as a list."""
    if isinstance(value, list):
        value = ", ".join(v for v in value if isinstance(v, str))
    if not isinstance(value, str):
        return ""
    return " ".join(value.split()).strip(" ,")[:_WORDS_LIMIT]


def _safe(model: str) -> str:
    """The identifier for the log line, without anything that could break it."""
    return "".join(c if c.isalnum() or c in "._:@-" else "_" for c in model)[:_TEXT_LIMIT]


# Error codes that mean the request itself was wrong (Runware's error list).
_INVALID_PREFIX: Final = ("invalid", "missing", "unsupported")


def _error(status: int, error: object) -> GatewayError:
    """The error kind of the first error in the answer; its text names no prompt or key."""
    code = error.get("code") if isinstance(error, dict) else None
    code = code if isinstance(code, str) and re.fullmatch(r"[A-Za-z]{1,60}", code) else ""
    if status == httpx.codes.TOO_MANY_REQUESTS:
        return RateLimited("Zu viele Anfragen beim Anbieter")
    lowered = code.lower()
    if "nsfw" in lowered or "content" in lowered or "safety" in lowered:
        return ModelRefused("Der Anbieter hat das Bild abgelehnt")
    if status in (httpx.codes.UNAUTHORIZED, httpx.codes.PAYMENT_REQUIRED, httpx.codes.FORBIDDEN):
        return ProviderUnavailable(f"Schlüssel abgelehnt oder Guthaben erschöpft (HTTP {status})")
    if lowered.startswith(_INVALID_PREFIX):
        return InvalidRequest(f"Der Anbieter hat die Anfrage zurückgewiesen ({code})")
    return ProviderUnavailable(f"Der Anbieter meldet einen Fehler ({code or status})")


def _check_status(status: int) -> None:
    """An HTTP status without an error list."""
    if status == httpx.codes.OK:
        return
    if status == httpx.codes.TOO_MANY_REQUESTS:
        raise RateLimited("Zu viele Anfragen beim Anbieter")
    raise ProviderUnavailable(f"Der Anbieter ist nicht erreichbar (HTTP {status})")
