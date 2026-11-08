# Probe der Textmodelle für den Figuren-Assistenten (Schritt 11.5, V.58)

Datum: 2026-11-08, Cloud-Session, OpenRouter. Skript: `probe.py` (Aufruf im Dateikopf), Antworten und
Prüftabelle in `ergebnisse/` (`pruefung.md`).

## Aufbau

- Auftrag an das Modell: aus den Antworten des Autors auf zehn feste Fragen (Herkunft, Alter, Größe,
  Körperbau, Proportionen, Gesicht, Haar, Augen, Haut, besondere Merkmale) und dem bisherigen
  Kanon-Eintrag zwei Teile schreiben – `## Aussehen` als deutsche Zeilen `- **Merkmal:** …` und
  `## Bildbeschreibung` als englischen Bild-Prompt nach dem Muster der Bildtests vom 2026-11-07
  (`docs/research/bildanbieter.md`: „a `<Alter>`-year-old adult …“, Alter vorn, höchstens 70 Wörter,
  ohne Name, Kleidung, Pose, Umgebung, Fesseln).
- Drei Figuren: Liv (Testavatar 2, 26, kurvig), Mara (24, Leibeigene mit Eisenhalsband und Narben von
  Ketten im Eintrag – prüft Sperren bei Gefangenschaft), Brann (48, Schmied, ein Merkmal ohne Angabe).
- Modelle: `x-ai/grok-4.6`, `x-ai/grok-4.7`, `qwen/qwen3.8-max-0902`, je Figur 2 Läufe (18 Anfragen),
  Temperatur 0,4, geringste Denkstufe wie im Programm.

## Ergebnis

| Modell | Sperren | Form eingehalten | Alter vorn | Wörter Bild-Prompt | Sekunden | Kosten je Anfrage |
|---|---|---|---|---|---|---|
| grok-4.6 | 0 / 6 | 6 / 6 | 6 / 6 | 41–47 | 9,6–17,3 | 0,0062–0,0090 $ |
| grok-4.7 | 0 / 6 | 6 / 6 | 6 / 6 | 45–56 | 10,2–29,7 | 0,0065–0,0137 $ |
| qwen3.8-max | 0 / 6 | 6 / 6 | 6 / 6 | 47–52 | 15,0–26,1 | 0,0060–0,0098 $ |

Gesamtkosten rund 0,15 $.

Von Hand gelesen (alle 18):

- **Nichts erfunden.** Alle Merkmale aus den Antworten sind im Bild-Prompt; das Merkmal ohne Angabe
  (Brann, Proportionen) steht in allen 6 Antworten als „–“ und fehlt im Prompt.
- **Halsband und Narben:** Das Eisenhalsband (in „Besondere Merkmale“ angegeben) haben alle 6
  Mara-Antworten aus dem Bild-Prompt gelassen (Regel „keine Fesseln“), die Narben an den
  Handgelenken behalten. Keine Sperre wegen der Gefangenschaft im Eintrag.
- **Teil „Aussehen“:** in allen 18 Antworten wörtlich die Antworten des Autors – das Modell fügt
  dort nichts hinzu. Den deutschen Teil kann das Programm selbst bauen; das Modell braucht es nur
  für die englische Bildbeschreibung.
- **Größe:** teils als nackte Zahl („172 cm“) ohne „tall“ – im Rahmen künftig „about … cm tall“
  verlangen.
- Unterschiede zwischen den Modellen gering; grok-4.6 am schnellsten und günstigsten, grok-4.7
  etwas länger und mit einem Ausreißer bei der Zeit, qwen3.8-max wortgetreu, etwas langsamer.

## Grenzen

- Drei Figuren, je zwei Läufe; Figuren mit stärker sexualisierten oder fesselungsbezogenen Einträgen
  (Welten des Eigentümers, an denen grok in 4.8 sperrte) sind nicht geprüft. Sperren bleiben deshalb
  möglich; der Assistent braucht die Erkennung mit Angebot eines anderen Modells (V.58 (7)).
- Bildqualität der Prompts hier nicht geprüft; das zeigt die Probe mit echten Entwürfen am Ende von
  11.5.

## Nachprüfung der eingebauten Anfrage (2026-11-08)

Nach ADR-123 verlangt das Programm vom Modell nur noch die englische Bildbeschreibung (die deutschen
Zeilen baut die Oberfläche) und die Größe als „about … cm tall“. Einmal je Figur mit grok-4.6 über
`prepare_figure_looks` (Skript im Scratchpad der Session, nicht abgelegt):

- Liv 50 Wörter, Mara 47, Brann 40; alle beginnen mit „a `<Alter>`-year-old adult“, Größe jeweils
  „about … cm tall“, Halsband bei Mara weggelassen, Narben behalten; nichts erfunden.
- Kosten 0,0044–0,0050 $ je Anfrage (weniger Ausgabe als in der Probe).
