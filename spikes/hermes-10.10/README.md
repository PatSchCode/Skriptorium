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

## Ergebnisse

(folgt)
