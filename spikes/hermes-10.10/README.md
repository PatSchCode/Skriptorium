# Textqualität von Hermes 4 (Schritt 10.10, V.41)

Messung nach Regel-002 (ADR-047): Schreibt Hermes 4 (`nousresearch/hermes-4-405b`) mit anderen Einstellungen besser als heute? Anlass ist die Rückmeldung des Eigentümers (2026-10-22): Hermes sperrt nicht, schreibt aber schwächer – „Stil / Deutsch, endlose Wiederholungen, selten“.

## Stand im Code (2026-11-06)

- Hermes 4 steht nicht in `ai_gateway/models.py`; die Einstellung kommt aus dem Katalog (`CatalogModel.config`): kein Pflicht-Denken, also Denken aus.
- Temperatur fest 0,8 für alle Modelle (`api/flows/writing.py`, `TEMPERATURE`), keine Strafe gegen Wiederholung.
- Katalog von OpenRouter (2026-11-06): 1 $ / 3 $ je 1 Mio. Token Ein-/Ausgabe, Kontext 131.072 Token. Einziger ausführender Anbieter ist Nebius (fp8). Angeboten werden u. a. `reasoning`, `frequency_penalty`, `presence_penalty`, `repetition_penalty`, `temperature`, `top_p`, `top_k`.

## Aufbau

- **Geschichten, Anweisungen, Ablauf:** wie `spikes/regel-002` (Salzmark und Glimmergrund, je sieben Anweisungen, die fünfte leer). Die Kette ist die aus `spikes/regel-002/lauf.py`, unverändert. Länge „mittel“, je Variante 3 Ketten je Geschichte.
- **Stand des Codes:** `main` `478e5fd` für alle Varianten; geändert wird nur, was an OpenRouter geht (`messung.py`).
- **Varianten:**

| Variante | Modell | Denken | Temperatur | Zusatz |
|---|---|---|---|---|
| `grok46` | `x-ai/grok-4.6` (Bezug, Voreinstellung) | „low“ (wie im Produkt) | 0,8 | – |
| `hermes` | Hermes 4 | aus (wie im Produkt) | 0,8 | – |
| `hermes-fp03` | Hermes 4 | aus | 0,8 | `frequency_penalty` 0,3 |
| `hermes-fp03-t06` | Hermes 4 | aus | 0,6 | `frequency_penalty` 0,3 |
| `hermes-rp105` | Hermes 4 | aus | 0,8 | `repetition_penalty` 1,05 |

- **Warum diese Strafen:** `frequency_penalty` wirkt bei den üblichen Inferenz-Servern nur auf schon erzeugte Token, also gegen Schleifen innerhalb der Antwort; `repetition_penalty` wirkt dort auch auf die Token der Anfrage (hier 9.000–29.000 Token), deshalb nur schwach (1,05). Beides ist Herstellerwissen über die Server, für Nebius nicht belegt (Deutung).
- **Denken:** nicht als Kette gemessen – siehe Vorbefund.

```bash
uv run python spikes/hermes-10.10/denken.py
VARIANTE=hermes uv run python spikes/hermes-10.10/messung.py   # je Variante
uv run python spikes/hermes-10.10/auswertung.py grok46 hermes hermes-fp03 hermes-fp03-t06 hermes-rp105
uv run python spikes/hermes-10.10/blind.py <ZIEL> grok46 hermes hermes-fp03 hermes-fp03-t06 hermes-rp105
```

## Vorbefund: Denken ist bei Hermes 4 nicht nutzbar

Mit `reasoning` `{"enabled": true}` (ebenso `effort` „medium“ und `max_tokens` 1.024) liefert Nebius den Denktext **im Antworttext selbst** – ohne `<think>`-Marken, ohne Feld `reasoning`, `reasoning_tokens` 0. Bei kurzer Frage (Vorprobe, 2026-11-06) englisch, an der echten Schreib-Anfrage (`denken.py`, Schritt 1 je Geschichte, `ergebnisse/denken/`) deutsch:

| Geschichte | Wörter gesamt | davon Denktext | Prosa | Kosten $ |
|---|---|---|---|---|
| Salzmark | 498 | 303 (7 Absätze, „Hmm, der Autor will, dass ich …“ bis „So, jetzt schreibe ich den Text.“) | 195 | 0,012 |
| Glimmergrund | 389 | 321 (6 Absätze, „Hmm, der Nutzer möchte, dass ich …“) | 68 | 0,028 |

Im Produkt stünde dieser Text im Vorschlag und würde mit „Übernehmen“ ins Manuskript gehen. Eine verlässliche Trennstelle gibt es nicht (kein Zeichen, keine feste Schlussformel). Die Variante „Hermes mit Denken“ aus V.41 entfällt deshalb; mit Denken aus (wie heute) kommt reine Prosa.

## Ergebnisse (2026-11-06, Cloud-Session)

30 Ketten, 210 Vorschläge, ein Verbindungsfehler (`hermes`, Glimmergrund Lauf 3, Schritt 7, beim zweiten Versuch geschrieben). Kosten laut Anbieter: grok46 1,21 $; hermes 0,38 $; hermes-fp03 0,34 $; hermes-fp03-t06 0,29 $; hermes-rp105 0,33 $; Denk-Probe 0,04 $ – zusammen 2,59 $ (plus Vorproben unter 0,01 $). Tabellen: `ergebnisse/auswertung.md`; Bewertungen: `ergebnisse/bewertung/`.

### Gezählt (`auswertung.py`), Mittel (Spannweite) je Kette

| Kennzahl | grok46 | hermes | fp03 | fp03-t06 | rp105 |
|---|---|---|---|---|---|
| **Salzmark** wörtlich % | 0,61 (0,29–0,86) | 2,53 (2,03–3,47) | 3,01 (1,58–5,42) | 5,05 (3,22–6,20) | 1,33 (0,74–1,64) |
| 6er doppelt | 0 (0–0) | 9,7 (4–16) | 24,0 (8–48) | 23,3 (18–29) | 1,7 (0–3) |
| 8er im Vorschlag | 0 (0–0) | 2,7 (0–8) | 7,3 (0–18) | 0 (0–0) | 1,3 (0–4) |
| Wörter je Vorschlag | 125 (107–135) | 194 (185–202) | 276 (188–405) | 198 (187–212) | 201 (159–252) |
| längster Vorschlag | 200 (184–232) | 364 (272–506) | 680 (345–1.234) | 359 (310–444) | 458 (314–647) |
| Kosten je Kette $ | 0,15 | 0,02 | 0,03 | 0,02 | 0,03 |
| **Glimmergrund** wörtlich % | 0,07 (0,00–0,21) | 3,93 (1,93–7,78) | 2,15 (0,63–4,72) | 1,49 (0,79–2,76) | 1,32 (0,80–2,02) |
| 6er doppelt | 0 (0–0) | 59,7 (0–179) | 15,3 (0–39) | 17,3 (0–50) | 11,0 (3–16) |
| Satz doppelt | 0 (0–0) | 63,7 (0–190) | 0 (0–0) | 0 (0–0) | 0 (0–0) |
| 8er im Vorschlag | 0 (0–0) | 135 (0–386) | 0 (0–0) | 52,7 (0–157) | 0 (0–0) |
| Wörter je Vorschlag | 111 (106–118) | 634 (224–1.126) | 231 (165–278) | 290 (213–378) | 318 (289–347) |
| längster Vorschlag | 220 (211–227) | 2.872 (339–6.438) | 381 (308–451) | 647 (303–1.247) | 528 (440–596) |
| nicht stop | 0 | 0,33 (0–1) | 0 | 0 | 0 |
| Kosten je Kette $ | 0,25 | 0,10 | 0,08 | 0,07 | 0,08 |

Warte-Enden und Englisch: in allen Varianten 0 bis 0,7 bzw. 0 – Hermes wechselt nicht ins Englische (mit Denken aus).

### Von Hand bewertet (verblindet, je Geschichte und Thema eine getrennte Instanz, Sonnet; 15 Ketten in Zufallsfolge, Zuordnung `bewertung/mapping.json`)

Noten 1–5 (5 = gut), Mittel (Spannweite) je Kette. Kanon: Salzmark eindeutige/knappe Widersprüche; Glimmergrund widersprochene der 12 Proben.

| Kennzahl | grok46 | hermes | fp03 | fp03-t06 | rp105 |
|---|---|---|---|---|---|
| **Salzmark** Deutsch | 3,67 (3–4) | 3,00 (3–3) | 2,67 (1–4) | 4,00 (4–4) | 3,33 (3–4) |
| Stil | 3,67 (3–4) | 3,00 (3–3) | 2,33 (1–4) | 3,33 (3–4) | 3,33 (2–4) |
| Gesamt | 3,33 (3–4) | 2,67 (2–3) | 2,00 (1–3) | 3,33 (3–4) | 3,00 (2–4) |
| Widersprüche eindeutig | 0,00 (0–0) | 0,67 (0–1) | 1,67 (0–3) | 0,00 (0–0) | 0,67 (0–1) |
| Widersprüche knapp | 0,33 (0–1) | 1,00 (0–2) | 0,67 (0–2) | 1,33 (0–2) | 1,67 (0–3) |
| **Glimmergrund** Deutsch | 4,00 (4–4) | 2,33 (2–3) | 4,00 (4–4) | 3,00 (2–4) | 3,00 (3–3) |
| Stil | 4,00 (4–4) | 2,00 (2–2) | 3,00 (3–3) | 3,00 (2–4) | 3,00 (3–3) |
| Gesamt | 4,00 (4–4) | 1,33 (1–2) | 3,00 (3–3) | 2,67 (1–4) | 2,67 (2–3) |
| Proben widersprochen (von 12) | 0,33 (0–1) | 2,00 (1–4) | 2,33 (0–4) | 2,67 (2–4) | 2,67 (2–3) |

Stichprobe der bauenden KI gegen die Texte (3 von 3 bestätigt): Pell hält einen Zettel „in ungelenker Schrift“ (hermes, Salzmark Lauf 2, Schritt 5; Kanon: kann nicht schreiben); Tomas sagt „Ilka…“ (fp03, Salzmark Lauf 3, Schritt 7; Kanon: nie „Ilka“); Anfragetext „# Kapitel 3 – Die Einfahrt / Das Manuskript endet mit: …“ im Vorschlag (fp03-t06, Glimmergrund Lauf 2, Schritt 7).

### Befunde

1. **Die Schleifen des Eigentümers sind nachgestellt.** Hermes wie heute: in Glimmergrund 2 von 3 Ketten mit Endlosschleife – Lauf 2, Schritt 5: 1.839 Wörter, dieselbe Szene („Ich weiß es nicht … Aber ich weiß, wer es empfangen hat. Wendt nickte.“) mit wechselnden Figuren; Lauf 3, Schritt 6: 6.438 Wörter bis zur Grenze von 8.000 Token („und weil ich nicht weiß, was ich sonst sagen soll, …“). Salzmark ohne solche Schleife.
2. **Keine Einstellung beseitigt die Entgleisungen.** `frequency_penalty` 0,3 tauscht die Schleife gegen Wortsalat (Salzmark Lauf 2, Schritt 4: 1.234 Wörter, „verknotet verheddert verstrickt verwoben …“); mit Temperatur 0,6 dazu ein Satz über 1.247 Wörter ohne Satzzeichen samt Anfragetext (Glimmergrund Lauf 2, Schritt 7); `repetition_penalty` 1,05 ohne Totalausfall, aber Vorschläge bis 647 Wörter bei Länge „mittel“.
3. **Nach Regel-002 (Bezug `hermes`, Wirkung nur in beiden Geschichten außerhalb der Spannweite):** `fp03-t06` hebt die Gesamtnote in beiden Geschichten (Salzmark 3,33 gegen höchstens 3; Glimmergrund 2,67 gegen höchstens 2) – eine Wirkung, aber mit „wörtlich %“ in der Salzmark gegenläufig schlechter (5,05 gegen höchstens 3,47). `rp105` senkt „wörtlich %“ in beiden Geschichten (1,33 gegen mindestens 2,03; 1,32 gegen mindestens 1,93); die Noten nur in Glimmergrund besser. `fp03` gegenläufig (Glimmergrund besser, Salzmark schlechter). Kanon-Widersprüche: keine Variante in beiden Geschichten außerhalb der Spannweite von `hermes` (`fp03` in der Salzmark schlechter: 1,67 eindeutige gegen höchstens 1).
4. **Abstand zu grok-4.6 bleibt.** grok-4.6 hat in keiner Kette eine Schleife, die wenigsten Kanon-Verstöße (Glimmergrund 0,33 gegen 2,0–2,67 Proben) und in Glimmergrund die beste Gesamtnote (4,00 gegen höchstens 3,00 bei Hermes). In der Salzmark liegt `fp03-t06` gleichauf (3,33). grok-4.6 schreibt kürzer, als „mittel“ verlangt (111–125 Wörter, Band 150–300); Hermes trifft das Band im Mittel besser, streut aber stark.
5. **Kosten:** Hermes kostet je Kette ein Sechstel (Salzmark) bis ein Drittel (Glimmergrund) von grok-4.6.

**Grenzen:** 3 Ketten je Variante und Geschichte; seltene Ereignisse wie Endlosschleifen (Eigentümer: „selten“) streuen stark. Je Thema ein Bewerter mit ganzzahligen Noten; bei 8.11 und 9.3 verschwanden Wirkungen aus 3 Ketten im Nachlauf. Die Bewertung der Sprache ist ein neues Werkzeug ohne Vergleich zu früheren Messungen.

## Nachlauf (2026-11-06, Wahl des Eigentümers „Nachlauf zuerst“)

Je 3 weitere Ketten `hermes` und `hermes-fp03-t06` im gleichen Aufbau (`ergebnisse/hermes-2/`, `…/hermes-fp03-t06-2/`; 0,32 $ + 0,29 $). Ausgewertet über 6 Ketten je Seite (`ergebnisse/sechs-*/` als zusammengeführte Kopien, `ergebnisse/auswertung-nachlauf.md`); **neue** verblindete Bewertung aller 12 Ketten je Geschichte durch vier neue Instanzen (Sonnet), neue Zufallsfolge (`ergebnisse/bewertung-2/`).

| Kennzahl, Mittel (Spannweite) | Salzmark heute | Salzmark fp03-t06 | Glimmergrund heute | Glimmergrund fp03-t06 |
|---|---|---|---|---|
| wörtlich % | 3,13 (0,63–8,09) | 5,27 (3,22–6,20) | 3,83 (0,90–7,78) | 2,31 (0,79–7,14) |
| Satz doppelt | 0,17 (0–1) | 0,33 (0–1) | 32,2 (0–190) | 0 (0–0) |
| 8er im Vorschlag | 1,7 (0–8) | 0 (0–0) | 77,3 (0–386) | 26,8 (0–157) |
| längster Vorschlag | 331 (272–506) | 336 (272–444) | 1.910 (339–6.438) | 520 (303–1.247) |
| Deutsch (Note) | 3,50 (3–4) | 3,50 (3–4) | 3,17 (2–4) | 3,83 (2–5) |
| Stil (Note) | 3,33 (3–4) | 3,33 (3–4) | 2,67 (2–4) | 3,33 (2–4) |
| Gesamt (Note) | 3,00 (2–4) | 2,67 (2–4) | 2,00 (1–3) | 3,17 (1–4) |
| Widersprüche eindeutig (Salzmark) / Proben widersprochen (Glimmergrund) | 0,33 (0–1) | 0,67 (0–2) | 1,83 (1–4) | 3,00 (2–5) |

**Ergebnis nach Regel-002:** Die Wirkung auf die Gesamtnote aus den ersten 3 Ketten hält nicht – in der Salzmark liegt `fp03-t06` jetzt sogar unter `heute` (2,67 gegen 3,00), nur in Glimmergrund darüber. Keine Kennzahl liegt in beiden Geschichten außerhalb der Spannweite von `heute`; „wörtlich %“ in der Salzmark und die Kanon-Proben in Glimmergrund sind mit der Einstellung im Mittel schlechter (innerhalb der Spannweite). **Keine Wirkung der Einstellung.** Einzig belastbar ist der Unterschied bei den groben Schleifen in Glimmergrund (längster Vorschlag 1.247 gegen 6.438 Wörter, 0 gegen 190 doppelte Sätze) – auch mit der Einstellung bleibt dort aber eine Entgleisung über 1.247 Wörter mit Anfragetext.
