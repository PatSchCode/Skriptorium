"""Probe der Vorschläge für den Figuren-Assistenten (Schritt 11.5, ADR-124).

Vor dem Bau: Schlagen grok-4.6 und die Ausweichmodelle aus Eintrag und Weltbeschreibung je Frage
drei brauchbare Antworten vor – in der verlangten Form, ohne zu sperren, in Begriffen, die
Bildmodelle kennen, und als Abwandlung, wenn schon eine Angabe steht?

Geprüft wird je Antwort mechanisch: Sperre (Fehler, ``content_filter``, Ablehnungsformel, keine
einzige Zeile in Form), alle zehn Fragen in der Reihenfolge, je Frage genau drei Vorschläge,
Alter ganze Zahlen ab 18, nichts Unerlaubtes (Kleidung, Fesseln, Namen der Figur, Orte der Welt),
Zahl der Vorschläge mit Kennzeichnung „[Eintrag]“. Die Brauchbarkeit liest der Mensch bzw. die KI
von Hand.

Aufruf:
    uv run python spikes/figuren-assistent-11.5/probe_vorschlaege.py   (alle Modelle, je 2 Läufe)
    TROCKEN=1 …   (nur die Anfrage ausgeben)    PRUEFEN=1 …   (gespeicherte Antworten prüfen)
Der Schlüssel kommt aus OPENROUTER_API_KEY und wird nur im scharfen Lauf gebraucht.
"""

import asyncio
import json
import os
import re
import time
from pathlib import Path

from skriptorium.ai_gateway import Completed, CompletionRequest, GatewayError, Message
from skriptorium.ai_gateway import OpenRouterProvider

ROOT = Path(__file__).parent
MODELLE = tuple(
    os.environ.get("MODELLE", "x-ai/grok-4.6,x-ai/grok-4.7,qwen/qwen3.8-max-0902").split(",")
)
LAEUFE = 2
TEMPERATUR = 0.8
MAX_TOKEN = 3000
RUNDE = os.environ.get("RUNDE", "2")
FRAGEN = (
    "Herkunft",
    "Alter",
    "Größe",
    "Körperbau",
    "Proportionen",
    "Gesicht",
    "Haar",
    "Augen",
    "Haut",
    "Besondere Merkmale",
)

RAHMEN = (
    "Du hilfst einem Autor, das Aussehen einer Figur aus seiner erzählten Welt für Bildmodelle "
    "festzulegen. Alle Figuren sind erwachsen. Du bekommst den Kanon-Eintrag der Figur, die "
    "Beschreibung der Welt und die Angaben, die der Autor schon gemacht hat.\n\n"
    "Mache zu jeder der zehn Fragen genau drei Vorschläge, die zur Figur und zur Welt passen und "
    "sich deutlich voneinander unterscheiden. Lies zuerst den Eintrag: Alles, was er über das "
    "Äußere sagt – auch beiläufig, etwa Narben, Haarfarbe oder Wuchs –, ist Kanon. Es steht "
    "als erster Vorschlag bei der passenden Frage, am Ende gekennzeichnet mit „ [Eintrag]“; "
    "die beiden anderen weichen davon ab. Kein Vorschlag darf dem Eintrag widersprechen. Steht "
    "im Eintrag nichts zur Frage, denkst du dir alle drei passend zur Figur und zur Welt aus. "
    "Steht zu einer Frage schon eine Angabe des Autors, sind die drei Vorschläge Abwandlungen "
    "davon.\n\n"
    "„Herkunft“ beschreibt, wie die Figur aussieht („nordeuropäisch wirkend“), und nennt keinen "
    "Namen aus der Welt (kein Volk, Land oder Ort): Bildmodelle kennen die Welt nicht. „Alter“ "
    "sind drei ganze Zahlen ab 18, sonst nichts. „Größe“ nennt ein Wort und die Zentimeter. "
    "Alle anderen Antworten sind kurze, sichtbare Wendungen auf Deutsch, durch Kommas getrennt. "
    "Keine Namen, keine Gefühle, keine Vorgeschichte, keine Kleidung, keine Pose, keine "
    "Umgebung und keine Fesseln, Ketten oder Halsbänder.\n\n"
    "Antworte genau in dieser Form, eine Zeile je Frage, die drei Vorschläge durch „ | “ "
    "getrennt, und mit nichts davor oder danach:\n\n"
    + "\n".join(f"{frage}: … | … | …" for frage in FRAGEN)
)

WELT = (
    "# Welt: Kerrow und die Küstenlande\n\nRauer Norden am Nordmeer: Eisenminen, Schmieden, "
    "kleine Handelshäfen und Fährleute. Die Menschen der Küstenlande stammen aus vielen Ländern, "
    "weil das Meer sie zusammengespült hat. Kriege um die Minen sind erst wenige Jahre vorbei."
)

# (Kennung, Eintrag, bisherige Angaben)
FIGUREN: tuple[tuple[str, str, dict[str, str]], ...] = (
    (
        "brann",
        "# Brann Holt\n\nSchmied in Kerrow, seit dem Brand der alten Esse halb taub auf dem "
        "linken Ohr. Er redet nicht gern über den Krieg.",
        {},
    ),
    (
        "liv",
        "# Liv Arnesdatter\n\nLiv ist Fährfrau am Nordsund und kennt jede Strömung. Sie lacht "
        "laut, flucht leiser und trägt bei jedem Wetter dieselbe geflickte Öljacke. Ihr "
        "kupferrotes Haar fällt ihr fast bis zur Taille.",
        {"Alter": "26", "Haar": "kupferrot, glatt"},
    ),
    (
        "mara",
        "# Mara\n\nMara wurde bei der Belagerung von Tolm gefangen und dient seitdem im Haus "
        "des Fürsten Edrik als Leibeigene. Sie trägt ein schmales Halsband aus Eisen, das sie "
        "als Eigentum des Hauses kennzeichnet; an den Handgelenken sind Narben von den Ketten "
        "der ersten Wochen geblieben. Sie spricht wenig und beobachtet viel.",
        {},
    ),
)

_ABLEHNUNG = re.compile(
    r"\b(I can(?:'|no)t|I won't|I'm sorry|kann ich nicht|nicht helfen|nicht erstellen)\b", re.I
)
_UNERLAUBT = re.compile(
    r"\b(Halsband|Kette|Ketten|Fessel|Fesseln|Kleid|Jacke|Rüstung|trägt|sitzt|steht|lächelt|"
    r"Kerrow|Tolm|Küstenländ\w*|Küstenlande|Nordmeer)\b",
    re.I,
)
_ZEILE = re.compile(r"^([^:\n]+):\s*(.+)$", re.M)


def anfrage(modell: str, figur: tuple[str, str, dict[str, str]]) -> CompletionRequest:
    _, eintrag, bisher = figur
    angaben = "\n".join(f"- {f}: {bisher.get(f) or '(noch keine Angabe)'}" for f in FRAGEN)
    nutzer = (
        f"{WELT}\n\nKanon-Eintrag der Figur:\n\n{eintrag}\n\nAngaben des Autors bisher:\n\n{angaben}"
    )
    return CompletionRequest(
        modell,
        (Message("system", RAHMEN), Message("user", nutzer)),
        max_tokens=MAX_TOKEN,
        temperature=TEMPERATUR,
    )


def zerlege(antwort: str) -> dict[str, list[str]]:
    """Die Zeilen ``Frage: a | b | c`` als Frage → Vorschläge."""
    ergebnis: dict[str, list[str]] = {}
    for frage, rest in _ZEILE.findall(antwort):
        if frage.strip() in FRAGEN and frage.strip() not in ergebnis:
            ergebnis[frage.strip()] = [teil.strip() for teil in rest.split("|")]
    return ergebnis


def pruefe(antwort: str, meta: dict[str, object], name: str) -> dict[str, object]:
    zeilen = zerlege(antwort)
    gesperrt = (
        bool(meta.get("fehler"))
        or meta.get("finish_reason") == "content_filter"
        or not zeilen
        or bool(_ABLEHNUNG.search(antwort[:300]))
    )
    alle = [v for vorschlaege in zeilen.values() for v in vorschlaege]
    alter = zeilen.get("Alter", [])
    vorname = name.split()[0]
    return {
        "gesperrt": gesperrt,
        "reihenfolge": list(zeilen) == list(FRAGEN),
        "je_drei": all(len(v) == 3 for v in zeilen.values()) and bool(zeilen),
        "alter_ok": len(alter) == 3 and all(re.fullmatch(r"\d{1,3}", a) and int(a) >= 18 for a in alter),
        "aus_eintrag": sum("[Eintrag]" in v for v in alle),
        "unterscheidbar": all(len({v.lower() for v in vs}) == len(vs) for vs in zeilen.values()),
        "name": any(vorname.lower() in v.lower() for v in alle),
        "unerlaubt": sorted({w.lower() for v in alle for w in _UNERLAUBT.findall(v)}),
    }


async def lauf(ausgabe: Path) -> None:
    provider = OpenRouterProvider(os.environ["OPENROUTER_API_KEY"])
    try:
        for modell in MODELLE:
            for figur in FIGUREN:
                for nummer in range(1, LAEUFE + 1):
                    kurz = f"{modell.split('/')[1]}-{figur[0]}-{nummer}"
                    start = time.monotonic()
                    antwort, meta = "", {"modell": modell, "figur": figur[0], "lauf": nummer}
                    try:
                        async for event in provider.stream(anfrage(modell, figur)):
                            if isinstance(event, Completed):
                                meta["finish_reason"] = event.finish_reason
                                meta["kosten_usd"] = event.usage.cost_usd
                                meta["token_aus"] = event.usage.output_tokens
                            else:
                                antwort += event.text
                    except GatewayError as error:
                        meta["fehler"] = str(error)
                    meta["sekunden"] = round(time.monotonic() - start, 1)
                    (ausgabe / f"{kurz}.txt").write_text(antwort, encoding="utf-8")
                    (ausgabe / f"{kurz}.json").write_text(
                        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
                    )
                    print(kurz, meta.get("sekunden"), "s", meta.get("kosten_usd"), flush=True)
    finally:
        await provider.aclose()


def bericht(ausgabe: Path) -> str:
    namen = {f[0]: f[1].splitlines()[0].lstrip("# ") for f in FIGUREN}
    zeilen = [
        "| Lauf | gesperrt | Reihenfolge | je drei | Alter | aus Eintrag | verschieden | Name | "
        "Unerlaubt | Sek. | Kosten $ |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for datei in sorted(ausgabe.glob("*.json")):
        meta = json.loads(datei.read_text(encoding="utf-8"))
        antwort = datei.with_suffix(".txt").read_text(encoding="utf-8")
        p = pruefe(antwort, meta, namen[meta["figur"]])
        unerlaubt = p["unerlaubt"]
        assert isinstance(unerlaubt, list)
        zeilen.append(
            f"| {datei.stem} | {p['gesperrt']} | {p['reihenfolge']} | {p['je_drei']} | "
            f"{p['alter_ok']} | {p['aus_eintrag']} | {p['unterscheidbar']} | {p['name']} | "
            f"{', '.join(unerlaubt) or '–'} | {meta.get('sekunden')} | {meta.get('kosten_usd')} |"
        )
    text = "# Prüfung der Probe der Vorschläge (11.5, ADR-124)\n\n" + "\n".join(zeilen) + "\n"
    (ausgabe / "pruefung.md").write_text(text, encoding="utf-8")
    return text


def main() -> None:
    ausgabe = ROOT / f"ergebnisse-vorschlaege-{RUNDE}"
    ausgabe.mkdir(exist_ok=True)
    if os.environ.get("TROCKEN"):
        print(anfrage(MODELLE[0], FIGUREN[1]).messages[0].content)
        print("\n---\n")
        print(anfrage(MODELLE[0], FIGUREN[1]).messages[1].content)
        return
    if not os.environ.get("PRUEFEN"):
        asyncio.run(lauf(ausgabe))
    print(bericht(ausgabe))


if __name__ == "__main__":
    main()
