"""Verblindung 10.10: Ketten aller Varianten je Geschichte in zufälliger Folge nach K01 … K15.

Kopiert je Geschichte die Vorschläge ``01.txt`` … ``07.txt`` jeder Kette (ohne Metadaten, ohne
Modellnamen) in ``<ZIEL>/<geschichte>/Knn/`` und ``start.txt`` daneben; die Zuordnung steht in
``ergebnisse/bewertung/mapping.json`` und wird den Bewertern nicht gezeigt.

Aufruf: uv run python spikes/hermes-10.10/blind.py ZIEL VARIANTE [VARIANTE …]
"""

import json
import random
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent


def main() -> None:
    target = Path(sys.argv[1])
    variants = sys.argv[2:]
    rng = random.SystemRandom()
    mapping: dict[str, dict[str, str]] = {}
    for story in ("salzmark", "glimmergrund"):
        chains = [
            run
            for variant in variants
            for run in sorted((ROOT / "ergebnisse" / variant / story).glob("lauf-*"))
        ]
        rng.shuffle(chains)
        mapping[story] = {}
        for number, run in enumerate(chains, start=1):
            key = f"K{number:02d}"
            dest = target / story / key
            dest.mkdir(parents=True, exist_ok=True)
            for step in range(1, 8):
                shutil.copy(run / f"{step:02d}.txt", dest / f"{step:02d}.txt")
            mapping[story][key] = f"{run.parent.parent.name}/{run.name}"
        shutil.copy(chains[0] / "start.txt", target / story / "start.txt")
    out = ROOT / "ergebnisse" / "bewertung"
    out.mkdir(parents=True, exist_ok=True)
    (out / "mapping.json").write_text(
        json.dumps(mapping, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print({story: len(keys) for story, keys in mapping.items()})


if __name__ == "__main__":
    main()
