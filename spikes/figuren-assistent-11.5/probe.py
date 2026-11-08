"""Kurze Probe der Textmodelle für den Figuren-Assistenten (Schritt 11.5, V.58).

Vor der Vorlage: Liefern grok-4.6, grok-4.7 und qwen3.8-max aus geführten Antworten zum Aussehen
einer Figur (und dem vorhandenen Kanon-Eintrag) zuverlässig zwei Teile, ohne zu sperren?

1. ``## Aussehen`` – deutsche Zeilen ``- **Merkmal:** …`` (Mittelweg der Grundsatzfrage, V.58 (5));
2. ``## Bildbeschreibung`` – englischer Bild-Prompt nach dem Muster der Bildtests vom 2026-11-07
   (``docs/research/bildanbieter.md``: Alter vorn, „adult“, Merkmale als kurze Wendungen).

Geprüft wird je Antwort mechanisch: Sperre (Fehler, ``content_filter``, Ablehnungsformel oder
fehlende Teile), alle Merkmale als Zeile vorhanden, Bildbeschreibung beginnt mit
„a <Zahl>-year-old adult“, Wortzahl, Name nicht im Bild-Prompt, keine Handlung oder Fesselung im
Bild-Prompt (gehört ins Rezept, V.57). Die Brauchbarkeit liest der Mensch bzw. die KI von Hand.

Aufruf:
    uv run python spikes/figuren-assistent-11.5/probe.py        (alle Modelle, je 2 Läufe)
    TROCKEN=1 …   (nur die Anfrage ausgeben)    PRUEFEN=1 …   (gespeicherte Antworten prüfen)
Der Schlüssel kommt aus OPENROUTER_API_KEY und wird nur im scharfen Lauf gebraucht.
"""

import asyncio
import json
import os
import re
import time
from pathlib import Path

from skriptorium.ai_gateway import CompletionRequest, Completed, GatewayError, Message
from skriptorium.ai_gateway import OpenRouterProvider

ROOT = Path(__file__).parent
MODELLE = ("x-ai/grok-4.6", "x-ai/grok-4.7", "qwen/qwen3.8-max-0902")
LAEUFE = 2
MERKMALE = (
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
    "Du hilfst einem Autor, das Aussehen einer Figur aus seiner erzählten Welt festzuhalten. "
    "Alle Figuren sind erwachsen. Du bekommst seine Antworten auf feste Fragen und den "
    "bisherigen Kanon-Eintrag der Figur. Übernimm nur, was dort steht; erfinde keine Merkmale "
    "dazu und lass offene Fragen offen.\n\n"
    "Antworte genau in dieser Form und mit nichts davor oder danach:\n\n"
    "## Aussehen\n\n"
    + "\n".join(f"- **{m}:** …" for m in MERKMALE)
    + "\n\n## Bildbeschreibung\n\n"
    "…\n\n"
    "Regeln für „Aussehen“: Deutsch, je Merkmal eine Zeile in kurzen Wendungen, keine ganzen "
    "Absätze; ein Merkmal ohne Angabe bekommt „–“.\n"
    "Regeln für „Bildbeschreibung“: Englisch, ein einziger Absatz für ein Bildmodell, höchstens "
    "70 Wörter. Beginne genau mit „a <Alter>-year-old adult“, gefolgt von Herkunft und "
    "Geschlecht, dann „with mature adult facial features“. Danach Haut, Gesicht, Haar, Augen, "
    "besondere Merkmale, Größe; Körperbau und Proportionen zuletzt in einer eigenen Wendung. "
    "Kurze, sichtbare Wendungen mit Kommas, keine Namen, keine Gefühle, keine Vorgeschichte, "
    "keine Kleidung, keine Pose, keine Umgebung und keine Fesseln – die setzt der Autor "
    "beim Bild selbst dazu."
)

FIGUREN: tuple[tuple[str, str, dict[str, str]], ...] = (
    (
        "liv",
        "# Liv Arnesdatter\n\nLiv ist Fährfrau am Nordsund und kennt jede Strömung. Sie lacht "
        "laut, flucht leiser und trägt bei jedem Wetter dieselbe geflickte Öljacke. Ihr "
        "kupferrotes Haar fällt ihr fast bis zur Taille.",
        {
            "Herkunft": "Skandinavien",
            "Alter": "26",
            "Größe": "172 cm",
            "Körperbau": "kurvig, Sanduhrfigur",
            "Proportionen": "schmale Taille, breite Hüften, volle Oberschenkel, volle Brust",
            "Gesicht": "weich oval, runde Wangen, volle Lippen",
            "Haar": "kupferrot, glatt, bis zur Rückenmitte",
            "Augen": "grün",
            "Haut": "hell, viele Sommersprossen auf Nase und Wangen",
            "Besondere Merkmale": "",
        },
    ),
    (
        "mara",
        "# Mara\n\nMara wurde bei der Belagerung von Tolm gefangen und dient seitdem im Haus "
        "des Fürsten Edrik als Leibeigene. Sie trägt ein schmales Halsband aus Eisen, das sie "
        "als Eigentum des Hauses kennzeichnet; an den Handgelenken sind Narben von den Ketten "
        "der ersten Wochen geblieben. Sie spricht wenig und beobachtet viel.",
        {
            "Herkunft": "Südeuropa, mediterran",
            "Alter": "24",
            "Größe": "klein, etwa 160 cm",
            "Körperbau": "zierlich, aber weiblich",
            "Proportionen": "schmale Schultern, ausgeprägte Hüften, mittlere Brust",
            "Gesicht": "herzförmig, hohe Wangenknochen",
            "Haar": "schwarz, lockig, schulterlang",
            "Augen": "dunkelbraun, mandelförmig",
            "Haut": "olivfarben",
            "Besondere Merkmale": "feine Narben an beiden Handgelenken; schmales Eisenhalsband",
        },
    ),
    (
        "brann",
        "# Brann Holt\n\nSchmied in Kerrow, seit dem Brand der alten Esse halb taub auf dem "
        "linken Ohr. Er redet nicht gern über den Krieg.",
        {
            "Herkunft": "Nordeuropa",
            "Alter": "48",
            "Größe": "groß, etwa 190 cm",
            "Körperbau": "massig, kräftige Arme",
            "Proportionen": "",
            "Gesicht": "kantig, gebrochene Nase",
            "Haar": "Glatze, grauer Vollbart",
            "Augen": "hellgrau",
            "Haut": "wettergegerbt",
            "Besondere Merkmale": "Brandnarben am linken Unterarm und Hals",
        },
    ),
)

_ABLEHNUNG = re.compile(
    r"\b(I can(?:'|no)t|I won't|I'm sorry|kann ich nicht|nicht helfen|nicht erstellen)\b", re.I
)
_VERBOTEN_IM_PROMPT = re.compile(
    r"\b(collar|shackle|chain|bound|tied|wearing|dress|jacket|standing|sitting|captive|slave)\b",
    re.I,
)


def anfrage(modell: str, figur: tuple[str, str, dict[str, str]]) -> CompletionRequest:
    _, eintrag, antworten = figur
    zeilen = "\n".join(f"- {m}: {antworten[m] or '(keine Angabe)'}" for m in MERKMALE)
    nutzer = f"Antworten des Autors:\n\n{zeilen}\n\nBisheriger Kanon-Eintrag:\n\n{eintrag}"
    return CompletionRequest(
        modell,
        (Message("system", RAHMEN), Message("user", nutzer)),
        max_tokens=1500,
        temperature=0.4,
    )


def teil(antwort: str, titel: str) -> str | None:
    treffer = re.search(rf"^##\s*{titel}\s*$(.*?)(?=^##\s|\Z)", antwort, re.M | re.S)
    return None if treffer is None else treffer.group(1).strip()


def pruefe(antwort: str, meta: dict[str, object], name: str) -> dict[str, object]:
    aussehen, bild = teil(antwort, "Aussehen"), teil(antwort, "Bildbeschreibung")
    gesperrt = (
        bool(meta.get("fehler"))
        or meta.get("finish_reason") == "content_filter"
        or (aussehen is None and bild is None)
        or bool(_ABLEHNUNG.search(antwort[:300]))
    )
    zeilen = [] if aussehen is None else re.findall(r"^- \*\*(.+?):\*\*", aussehen, re.M)
    vorname = name.split()[0]
    return {
        "gesperrt": gesperrt,
        "form": aussehen is not None and bild is not None,
        "merkmale_vollstaendig": list(MERKMALE) == zeilen,
        "alter_vorn": bild is not None
        and re.match(r"an? \d{2}-year-old adult\b", bild, re.I) is not None,
        "woerter_bild": None if bild is None else len(bild.split()),
        "name_im_bild": bild is not None and vorname.lower() in bild.lower(),
        "verbotenes_im_bild": [] if bild is None else sorted(
            {w.lower() for w in _VERBOTEN_IM_PROMPT.findall(bild)}
        ),
        "nur_die_teile": antwort.strip().startswith("## Aussehen"),
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
        "| Lauf | gesperrt | Form | Merkmale | Alter vorn | Wörter | Name | Unerlaubt | Kosten $ |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for datei in sorted(ausgabe.glob("*.json")):
        meta = json.loads(datei.read_text(encoding="utf-8"))
        antwort = datei.with_suffix(".txt").read_text(encoding="utf-8")
        p = pruefe(antwort, meta, namen[meta["figur"]])
        verboten = p["verbotenes_im_bild"]
        assert isinstance(verboten, list)
        zeilen.append(
            f"| {datei.stem} | {p['gesperrt']} | {p['form']} | {p['merkmale_vollstaendig']} | "
            f"{p['alter_vorn']} | {p['woerter_bild']} | {p['name_im_bild']} | "
            f"{', '.join(verboten) or '–'} | {meta.get('kosten_usd')} |"
        )
    text = "# Prüfung der Probe 11.5\n\n" + "\n".join(zeilen) + "\n"
    (ausgabe / "pruefung.md").write_text(text, encoding="utf-8")
    return text


def main() -> None:
    ausgabe = ROOT / "ergebnisse"
    ausgabe.mkdir(exist_ok=True)
    if os.environ.get("TROCKEN"):
        print(anfrage(MODELLE[0], FIGUREN[1]).messages[0].content)
        print(anfrage(MODELLE[0], FIGUREN[1]).messages[1].content)
        return
    if not os.environ.get("PRUEFEN"):
        asyncio.run(lauf(ausgabe))
    print(bericht(ausgabe))


if __name__ == "__main__":
    main()
