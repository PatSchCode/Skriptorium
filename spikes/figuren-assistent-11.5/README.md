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

## Probe der Vorschläge (2026-11-09, ADR-124)

Datum: 2026-11-09, Cloud-Session, OpenRouter. Skript: `probe_vorschlaege.py` (Aufruf im Dateikopf), Antworten und Prüftabelle je Runde in `ergebnisse-vorschlaege-1` bis `-3` (`pruefung.md`).

### Aufbau

- Auftrag an das Modell: aus Weltbeschreibung, Kanon-Eintrag und den bisherigen Angaben des Autors zu jeder der zehn Fragen drei Vorschläge als eine Zeile `Frage: a | b | c`; ein Vorschlag, den der Eintrag hergibt, endet auf „ [Eintrag]“. Dieselben drei Figuren wie oben, mit einer erfundenen Welt „Kerrow und die Küstenlande“: Brann (Eintrag ohne Aussehen, keine Angaben), Liv (Alter und Haar vorgegeben, Haarfarbe im Eintrag), Mara (Narben an den Handgelenken und Halsband im Eintrag). Temperatur 0,8.
- Runde 1: erster Entwurf, 1.200 Ausgabe-Token, drei Modelle × drei Figuren × zwei Läufe (18 Anfragen). Runde 2: Auftrag geschärft („Eintrag zuerst, erster Vorschlag daraus, in der Herkunft kein Name aus der Welt, durch Kommas getrennt“), 3.000 Token, wieder 18. Runde 3: nur grok-4.6, Satz zum Eintrag noch einmal geschärft („Alles, was er über das Äußere sagt – auch beiläufig –, ist Kanon … Kein Vorschlag darf dem Eintrag widersprechen“), 6 Anfragen.

### Ergebnis

| Runde | Modell | Sperren | Form (10 Zeilen, je 3, Alter ab 18) | Eintrag eingehalten (Mara: Narben an den Handgelenken) |
|---|---|---|---|---|
| 1 | grok-4.6 | 0 / 6 | 6 / 6 | 1 / 2 |
| 1 | grok-4.7 | 0 / 6 | 6 / 6 | 2 / 2 (in einem Lauf drei Abwandlungen derselben Narbe) |
| 1 | qwen3.8-max | 0 / 6 | 2 / 6 – vier Antworten abgeschnitten (`finish_reason` `length`, Denk-Token) | nicht auswertbar (beide Mara-Läufe abgeschnitten) |
| 2 | grok-4.6 | 0 / 6 | 6 / 6 | 0 / 2 |
| 2 | grok-4.7 | 0 / 6 | 6 / 6 | 2 / 2 |
| 2 | qwen3.8-max | 0 / 6 | 6 / 6 | 2 / 2 |
| 3 | grok-4.6 | 0 / 6 | 6 / 6 | 2 / 2 |

Kosten 0,004–0,015 $ je Anfrage, zusammen 0,39 $ für 42 Anfragen; Dauer grok-4.6 14–31 s, grok-4.7 18–50 s, qwen3.8-max 28–48 s. Rund 20 der 42 Antworten von Hand gelesen, die übrigen mechanisch geprüft (Reihenfolge, je drei, Alter, Namen, Kleidung, Fesseln, Namen der Welt).

Von Hand gelesen:

- **Keine Sperre**, auch nicht bei Maras Eintrag mit Halsband und Ketten; die Antworten lassen Halsband und Ketten wie verlangt weg und schlagen Narben vor.
- **Herkunft** durchgehend als sichtbares Aussehen („nordeuropäisch wirkend“, „mediterran wirkend“). In Runde 1 erfand grok-4.6 einmal „gemischtküstenländisch“ (Name der Welt); Runde 2 und 3 ohne solche Fälle.
- **Alter** als drei Zahlen, bei vorgegebenem Alter 26 als 24 | 26 | 28 (Abwandlung).
- **Haar bei vorgegebenem „kupferrot, glatt“** (Liv): Abwandlungen, der Eintrag („fast bis zur Taille“) kommt als erster Vorschlag mit „[Eintrag]“.
- **grok-4.6 überging den Eintrag** häufig (Mara: Runde 1 in 1 von 2 Läufen, Runde 2 in 0 von 2 Läufen die Narben an den Handgelenken, sonst andere Narben); mit dem geschärften Satz aus Runde 3 hält es ihn ein (2 von 2). grok-4.7 und qwen3.8-max hielten ihn in Runde 2 ein (je 2 von 2). Gezählt mechanisch: „Handgelenk“ in der Zeile „Besondere Merkmale“.
- Kleine Schwächen, die bleiben: doppelte Merkmale über Fragen hinweg (Sommersprossen bei Haut und bei besonderen Merkmalen); „aus Eintrag“ wird nicht immer gesetzt, wenn der Eintrag das Merkmal nur beiläufig nennt (Brann: „halb taub auf dem linken Ohr“ → „Brandnarbe am linken Ohr“ ohne Kennzeichnung).

### Folgerung für den Bau

- Voreinstellung bleibt grok-4.6 (ADR-123); der geschärfte Satz zum Eintrag gehört in den Auftrag. Ausweichmodelle brauchen Raum für Denk-Token: Ausgabegrenze 4.000 statt 1.200.
- Ob eine Antwort brauchbar ist, entscheidet die Oberfläche am Format: Ohne eine einzige erkennbare Zeile meldet sie „keine Vorschläge in der erwarteten Form“, und das Fenster bietet ein anderes Modell an.

### Grenzen

- Drei Figuren, je zwei Läufe; Einträge mit stark sexualisiertem oder fesselungsbezogenem Inhalt (Welten des Eigentümers, an denen grok in 4.8 sperrte) nicht geprüft. Sperren bleiben möglich.
- Ob die Vorschläge bildtauglich sind, zeigt erst die Abnahme am Server mit einer echten Figur.

### Nachprüfung der eingebauten Anfrage (2026-11-09)

Einmal je Figur mit grok-4.6 über `prepare_looks_suggestions` (Skript im Scratchpad der Session, nicht abgelegt), Welt und Einträge in einem leeren Datenverzeichnis: 3 von 3 mit zehn Zeilen zu je drei Vorschlägen und Alter ab 18, Maras Narben an den Handgelenken und Livs Haar mit „[Eintrag]“ als erstem Vorschlag, keine Namen der Welt, keine Kleidung oder Fesseln; 0,0077–0,0097 $ je Anfrage.
