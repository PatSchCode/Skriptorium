# Getrennte Prüfung – Nachtrag Runware im Bedrohungsmodell (11.1)

- **Datum:** 2026-11-08
- **Prüfinstanz:** Unteragent auf Sonnet 5.5 (anderes Modell als die bauende KI, Opus 5.5), ohne Gesprächsverlauf, nur lesend, keine Netzaufrufe.
- **Erhalten:** den Diff des Nachtrags an `docs/architecture.md` (Abschnitte 3, 4, 6, 7) und das Bedrohungsmodell nach dem Nachtrag (Abschnitt 6 „Security“); zum Abgleich nur lesend `ai_gateway/runware.py`, `api/runware_models.py`, `api/image_routes.py`, `api/app.py`, `manuscript/requests.py`, `storage/store.py`, `.env.example`, `docs/onboarding-runbook.md` Abschnitt 7, ADR-114 bis ADR-116.
- **Grundlage des Schritts:** Befund 6 und Stellungnahme 2 in `docs/research/bewertung-phase-10.md`; ADR-117.

## Ergebnis der Prüfinstanz (zusammengefasst)

- **Zu (a), Abgleich mit dem Code:** keine falsche technische Aussage. Bestätigt wurden die Konstanten (`CHECK_CONTENT`, `MAX_PROMPT_CHARS` 4.000, `MAX_ANSWER_BYTES` 56 MB, `MAX_LORAS` 5, Zeitgrenzen 10/150 s), dass `accountManagement` nie aufgerufen wird, `__repr__` ohne Schlüssel, das erneute Auslösen außerhalb des `except` (`runware.py:187–192`), die strenge base64-Dekodierung, Kosten nur endlich und ≥ 0, die Log-Zeile ohne Prompt und Schlüssel, Fehlermeldungen nur mit Fehlercode, die Grenzen der Liste, `PUT` nur auf bekannte Einträge, die Formatprüfung beim Lesen, die Zuordnung am Kennungsformat, „ohne Schlüssel kein Adapter“, `system/` nicht im Index und die Felder der Anfrage-Ablage.
- **Zu (b), Vollständigkeit:** Schlüssel, Prompts ohne Prüfung, Modell-Liste samt Suche, Logs, Fehlermeldungen und die Antwort des Anbieters (Größe, Dateikopf) sind abgedeckt.
- **Zu (c), Reifegrad:** „Bedrohungsmodell Gesamtsystem“ kann `[BELASTBAR]` bleiben – der Nachtrag ergänzt Datenfluss, Schlüssel, Inhaltsvorgabe und Listenpfad ohne falsche Sicherheitsaussage; die neue Bedrohungsklasse (Anbieter ohne Ausgabengrenze, Prompts ohne Prüfung) ist mit ADR-115 samt Restrisiko hinterlegt. Befund 1 sollte vor dem Commit behoben werden.

## Befunde und Behandlung

| Nr. | Schwere | Befund | Behandlung |
|---|---|---|---|
| 1 | mittel | Ablageort des Runware-Schlüssels in der Cloud-Umgebung fehlt (ADR-115: „nur auf dem Server und in der Cloud-Session“; Gate-Punkt 4 verlangt Ablageort und Rotationsweg jedes Secrets). | Behoben: „Secrets im Betrieb“ nennt die Cloud-Umgebung als zweiten Ablageort beider Schlüssel (belegt im Archiv-Logbuch Phase 10, 2026-11-07) und einen Rotationsweg für beide Orte. |
| 2 | niedrig | „Runware kennt keine Ausgabengrenze“ zu gewiss; „Schaden auf das Guthaben begrenzt“ gilt nur, solange das Nachladen aus bleibt. | Behoben: „nicht gefunden (Stand 2026-11-07)“; Annahme „Nachladen aus“ ausdrücklich benannt, vom Code nicht erzwungen. |
| 3 | niedrig | Nicht prüfbare und veraltende Angaben (Guthaben 21,07 $, Durchreichen der `.env`, Archiv-Zitat). | Betrag entfernt, Verweis auf das Kostenregister; Durchreichen und Eintrag mit Quelle (Archiv-Logbuch). |
| 4 | niedrig | Doppelter Rotationssatz in „Secrets im Betrieb“, liest sich wie nur für OpenRouter. | Behoben: ein Satz für beide Schlüssel, Stand der Erprobung je Anbieter. |
| 5 | niedrig | „Sperrt die Bildauswahl nicht mehr“ gilt nur für die Anzeige; Erzeugen, Preis, Hinzufügen, Bearbeiten scheitern mit 422. | Behoben: Wortlaut präzisiert. |
| 6 | niedrig | Nicht erfasste Kosten bei Zeitgrenze, `processing`, zu großer oder unlesbarer Antwort. | Behoben: Satz im Kosten-Punkt; Verbrauch „Kosten nur bei geliefertem Bild“. |
| 7 | niedrig | Offenes Integritätsthema der Anfrage-Ablage nur im Datenmodell, nicht im Bedrohungsmodell. | Behoben: eigener Punkt im Bedrohungsmodell mit Landeplatz 11.3. |

## Hinweise der Prüfinstanz (optional, über ASVS L1)

- Mengen- oder Tagesgrenze für `POST /api/images/generate` (heute ist das Guthaben die einzige Bremse).
- Warnschwelle für das Runware-Guthaben (E-Mail des Anbieters oder Prüfschritt im Runbook).
- `follow_redirects` ist bei httpx standardmäßig aus, der Bearer-Kopf geht nicht an Fremdadressen – als Beleg erwähnbar, nicht nötig.

Nach `CLAUDE.md` Abschnitt 6 („Schutzbedarf ist Obergrenze“) werden diese Hinweise dem Eigentümer als optional vorgelegt, nicht still umgesetzt.

## Grenze der Prüfung

Geprüft wurden Text und Code. Ob die Einstellungen im Runware-Konto (Guthaben, Nachladen aus, Schlüssel in der Cloud-Umgebung) tatsächlich so stehen, ließ sich aus den Dateien nicht prüfen.
