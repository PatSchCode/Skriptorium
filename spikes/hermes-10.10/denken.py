"""Messung 10.10: Was liefert Hermes 4 mit eingeschaltetem Denken an einer echten Schreib-Anfrage?

Vorprobe (2026-11-06, kurze Frage „Schreibe einen Satz über das Meer.“): Beim einzigen
ausführenden Anbieter (Nebius, fp8) steht der Denktext mit ``reasoning`` ``enabled``, ``effort``
oder ``max_tokens`` im Antworttext selbst – ohne ``<think>``-Marken, ohne Feld ``reasoning``,
``reasoning_tokens`` 0. Hier dasselbe an der echten Anfrage: Schritt 1 jeder Testgeschichte
über ``prepare_request`` wie die Oberfläche, einmal je Geschichte, nur mit ``reasoning``
``{"enabled": true}``. Gespeichert werden Rohtext und Kennzahlen unter
``ergebnisse/denken/<geschichte>.txt`` und ``.json``.

Aufruf: uv run python spikes/hermes-10.10/denken.py
"""

import asyncio
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from types import MappingProxyType

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT.parent / "regel-002"))

from geschichten import GESCHICHTEN  # noqa: E402

from skriptorium.ai_gateway import Completed, OpenRouterProvider  # noqa: E402
from skriptorium.ai_gateway.models import DEFAULT_MODELS, ModelConfig  # noqa: E402
from skriptorium.api.flows.writing import WriteOrder, prepare_request  # noqa: E402

HERMES = "nousresearch/hermes-4-405b"
ENGLISH = re.compile(r"\b(the|and|user|wants|let|me|think|should|maybe|okay|i|is)\b", re.I)


def english_share(text: str) -> float:
    words = re.findall(r"\w+", text)
    return len(ENGLISH.findall(text)) / len(words) if words else 0.0


async def main() -> None:
    models = dict(DEFAULT_MODELS)
    models[HERMES] = ModelConfig(reasoning=MappingProxyType({"enabled": True}))
    provider = OpenRouterProvider(os.environ["OPENROUTER_API_KEY"], models=models)
    out = ROOT / "ergebnisse" / "denken"
    out.mkdir(parents=True, exist_ok=True)
    try:
        for name in ("salzmark", "glimmergrund"):
            with tempfile.TemporaryDirectory() as tmp:
                g = GESCHICHTEN[name](Path(tmp))
                order = WriteOrder(
                    g.world, g.story, g.chapter, instruction=g.instructions[0], model=HERMES,
                    length="mittel",
                )
                prepared = prepare_request(g.canon, g.manuscripts, g.builder, order, models)
                text, usage, finish = "", None, None
                async for event in provider.stream(prepared.completion):
                    if isinstance(event, Completed):
                        usage, finish = event.usage, event.finish_reason
                    else:
                        text += event.text
            (out / f"{name}.txt").write_text(text, encoding="utf-8")
            paragraphs = [p for p in text.split("\n") if p.strip()]
            meta = {
                "geschichte": name,
                "woerter": len(text.split()),
                "absaetze": len(paragraphs),
                "englisch_anteil_erster_absatz": round(english_share(paragraphs[0]), 3)
                if paragraphs
                else None,
                "englisch_anteil_gesamt": round(english_share(text), 3),
                "think_marke": "<think>" in text or "</think>" in text,
                "token_aus": usage.output_tokens if usage else None,
                "kosten_usd": usage.cost_usd if usage else None,
                "finish_reason": finish,
            }
            (out / f"{name}.json").write_text(
                json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
            print(meta, flush=True)
    finally:
        await provider.aclose()


if __name__ == "__main__":
    asyncio.run(main())
