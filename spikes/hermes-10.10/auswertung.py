"""Auswertung 10.10: Kennzahlen aus ``spikes/regel-002/auswertung.py`` plus Schleifen je Vorschlag.

Zusätzlich zu den Kennzahlen aus 5.24 (wörtlich, 6er doppelt, Warte-Enden, Motivfolge, Wörter,
Kosten) wird gezählt, was die Rückmeldung des Eigentümers zu Hermes beschreibt („endlose
Wiederholungen“) – innerhalb eines Vorschlags, nicht zwischen Vorschlägen:

- **Satz doppelt:** Sätze mit mindestens vier Wörtern, die im selben Vorschlag mehr als einmal
  stehen (Summe über die Kette);
- **8er im Vorschlag:** verschiedene 8-Wort-Folgen, die im selben Vorschlag mehr als einmal
  stehen (Summe über die Kette) – fängt auch Schleifen ohne Satzgrenze;
- **längster Vorschlag** in Wörtern;
- **nicht stop:** Vorschläge mit ``finish_reason`` ungleich ``stop`` (z. B. ``length`` nach einer
  Endlosschleife bis zur Grenze von 8.000 Token);
- **Englisch:** Wörter einer kleinen englischen Funktionswortliste in der Kette (Sprachwechsel; ohne „was“, das auch deutsch ist).

Aufruf: uv run python spikes/hermes-10.10/auswertung.py VARIANTE [VARIANTE …]
Schreibt ``ergebnisse/auswertung.md`` mit einer Tabelle je Geschichte (Mittel und Spannweite).
"""

import json
import re
import sys
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT.parent / "regel-002"))

import auswertung as basis  # noqa: E402

SENTENCE = re.compile(r"(?<=[.!?…])\s+|\n+")
ENGLISH = re.compile(r"\b(the|and|of|to|is|he|she|it|that|with|you|but|not)\b", re.I)


def schleifen(path: Path) -> dict[str, float]:
    proposals = [(path / f"{step:02d}.txt").read_text(encoding="utf-8") for step in range(1, 8)]
    metas = [
        json.loads((path / f"{step:02d}.json").read_text(encoding="utf-8")) for step in range(1, 8)
    ]
    doubled_sentences = 0
    doubled_eights = 0
    for proposal in proposals:
        seen: dict[str, int] = {}
        for sentence in SENTENCE.split(proposal):
            key = " ".join(basis.words(sentence))
            if len(key.split()) >= 4:
                seen[key] = seen.get(key, 0) + 1
        doubled_sentences += sum(count - 1 for count in seen.values() if count > 1)
        tokens = basis.words(proposal)
        eights: dict[tuple[str, ...], int] = {}
        for i in range(len(tokens) - 7):
            gram = tuple(tokens[i : i + 8])
            eights[gram] = eights.get(gram, 0) + 1
        doubled_eights += sum(1 for count in eights.values() if count > 1)
    return {
        "Satz doppelt": doubled_sentences,
        "8er im Vorschlag": doubled_eights,
        "längster Vorschlag": max(len(p.split()) for p in proposals),
        "nicht stop": sum(1 for m in metas if m["finish_reason"] != "stop"),
        "Englisch": sum(len(ENGLISH.findall(p)) for p in proposals),
    }


def kennzahlen(path: Path, story: str) -> dict[str, float]:
    return {**basis.chain(path, story), **schleifen(path)}


def main() -> None:
    variants = sys.argv[1:]
    stories = ("salzmark", "glimmergrund")
    lines = ["# Auswertung 10.10", "", "Mittel (Spannweite) über die Ketten je Variante.", ""]
    for story in stories:
        rows: dict[str, list[str]] = {}
        counts = []
        for variant in variants:
            runs = sorted((ROOT / "ergebnisse" / variant / story).glob("lauf-*"))
            values = [kennzahlen(run, story) for run in runs]
            counts.append(f"{variant} {len(values)}")
            for key in values[0]:
                series = [v[key] for v in values]
                cell = f"{mean(series):.2f} ({min(series):.2f}–{max(series):.2f})"
                rows.setdefault(key, []).append(cell)
        lines += [f"## {story} (Ketten: {', '.join(counts)})", ""]
        lines.append("| Kennzahl | " + " | ".join(variants) + " |")
        lines.append("|---|" + "---|" * len(variants))
        lines += [f"| {key} | " + " | ".join(cells) + " |" for key, cells in rows.items()]
        lines.append("")
    text = "\n".join(lines)
    (ROOT / "ergebnisse" / "auswertung.md").write_text(text.rstrip() + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
