"""Messung 10.10 (V.41): Textqualität von Hermes 4 mit Einstellungen je Variante, nach Regel-002.

Nutzt die Kette aus ``spikes/regel-002/lauf.py`` unverändert (``prepare_request`` wie die
Oberfläche, sieben Anweisungen, jeder Vorschlag wird übernommen) und ändert je Variante nur, was
an OpenRouter geht: Modell, Denken, Temperatur und Strafen gegen Wiederholung. Der Code des
Produkts bleibt unberührt; die Zusätze werden nur in diesem Prozess in den Anfragekörper gelegt.

Varianten (``VARIANTEN`` unten):

- ``grok46``: Bezug, ``x-ai/grok-4.6`` wie im Produkt (Denken „low“, Temperatur 0,8);
- ``hermes``: ``nousresearch/hermes-4-405b`` wie heute (Denken aus, Temperatur 0,8);
- ``hermes-fp03``: dazu ``frequency_penalty`` 0,3 (nur auf erzeugte Token);
- ``hermes-fp03-t06``: dazu Temperatur 0,6;
- ``hermes-rp105``: ``repetition_penalty`` 1,05 statt ``frequency_penalty``.

Aufruf:
    VARIANTE=NAME [LAENGE=mittel] [LAEUFE=3] [GESCHICHTEN=salzmark,glimmergrund]
    uv run python spikes/hermes-10.10/messung.py
Ergebnisse unter ``ergebnisse/<VARIANTE>/<geschichte>/lauf-<n>/`` wie in ``spikes/regel-002``;
dazu ``einstellungen.json`` je Variante. Schlüssel aus ``OPENROUTER_API_KEY``.

Denken bei Hermes: ``denken.py`` (eine Anfrage je Geschichte, keine Kette).
"""

import asyncio
import dataclasses
import functools
import json
import os
import sys
import tempfile
from collections.abc import AsyncIterator, Mapping
from pathlib import Path
from types import MappingProxyType
from typing import Any

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT.parent / "regel-002"))

import lauf as regel002  # noqa: E402
from geschichten import GESCHICHTEN  # noqa: E402

from skriptorium.ai_gateway import OpenRouterProvider  # noqa: E402
from skriptorium.ai_gateway import openrouter  # noqa: E402
from skriptorium.ai_gateway.models import DEFAULT_MODELS, ModelConfig  # noqa: E402
from skriptorium.ai_gateway.provider import CompletionRequest, StreamEvent  # noqa: E402

HERMES = "nousresearch/hermes-4-405b"
GROK = "x-ai/grok-4.6"


@dataclasses.dataclass(frozen=True)
class Variante:
    model: str
    temperature: float | None = None  # None: wie im Produkt (0,8)
    extra: Mapping[str, Any] = dataclasses.field(default_factory=dict)  # zusätzlich im Körper
    reasoning: Mapping[str, Any] | None = None  # None: wie im Produkt


VARIANTEN: dict[str, Variante] = {
    "grok46": Variante(GROK),
    "hermes": Variante(HERMES),
    "hermes-fp03": Variante(HERMES, extra={"frequency_penalty": 0.3}),
    "hermes-fp03-t06": Variante(HERMES, temperature=0.6, extra={"frequency_penalty": 0.3}),
    "hermes-rp105": Variante(HERMES, extra={"repetition_penalty": 1.05}),
}


class Eingestellt:
    """Anbieter, der vor dem Senden Temperatur und Zusätze der Variante setzt."""

    def __init__(self, inner: OpenRouterProvider, variante: Variante) -> None:
        self._inner = inner
        self._variante = variante

    async def stream(self, request: CompletionRequest) -> AsyncIterator[StreamEvent]:
        if self._variante.temperature is not None:
            request = dataclasses.replace(request, temperature=self._variante.temperature)
        async for event in self._inner.stream(request):
            yield event

    async def aclose(self) -> None:
        await self._inner.aclose()


def zusaetze_einbauen(extra: Mapping[str, Any]) -> None:
    """Legt ``extra`` in jeden Anfragekörper (nur in diesem Prozess)."""
    original = openrouter._payload

    def payload(request: CompletionRequest, config: ModelConfig) -> dict[str, object]:
        body = original(request, config)
        body.update(extra)
        return body

    openrouter._payload = payload  # type: ignore[assignment]


async def main() -> None:
    name = os.environ["VARIANTE"]
    variante = VARIANTEN[name]
    runs = int(os.environ.get("LAEUFE", "3"))
    stories = os.environ.get("GESCHICHTEN", "salzmark,glimmergrund").split(",")
    length = os.environ.get("LAENGE", "mittel")
    zusaetze_einbauen(variante.extra)
    models = dict(DEFAULT_MODELS)
    if variante.reasoning is not None:
        models[variante.model] = ModelConfig(reasoning=MappingProxyType(dict(variante.reasoning)))
    # prepare_request prüft das Modell gegen die Liste; im Produkt kommt Hermes aus dem Katalog
    # mit derselben Einstellung (Denken aus, ``catalog.CatalogModel.config``).
    models.setdefault(HERMES, ModelConfig())
    regel002.prepare_request = functools.partial(regel002.prepare_request, models=models)
    inner = OpenRouterProvider(os.environ["OPENROUTER_API_KEY"], models=models)
    provider = Eingestellt(inner, variante)
    out_base = ROOT / "ergebnisse" / name
    out_base.mkdir(parents=True, exist_ok=True)
    settings = {
        "modell": variante.model,
        "temperatur": variante.temperature if variante.temperature is not None else 0.8,
        "zusaetze": dict(variante.extra),
        "denken": dict(variante.reasoning)
        if variante.reasoning is not None
        else dict(models.get(variante.model, ModelConfig()).reasoning),
        "laenge": length,
    }
    (out_base / "einstellungen.json").write_text(
        json.dumps(settings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    total = 0.0
    try:
        for story in stories:
            for run in range(1, runs + 1):
                with tempfile.TemporaryDirectory() as tmp:
                    g = GESCHICHTEN[story](Path(tmp))
                    out = out_base / story / f"lauf-{run}"
                    total += await regel002.chain(
                        g, provider, variante.model, {"length": length}, out  # type: ignore[arg-type]
                    )
    finally:
        await provider.aclose()
    print(f"Kosten gesamt {name}: {total:.3f} $", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
