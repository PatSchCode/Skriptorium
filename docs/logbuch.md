# Logbuch – Skriptorium

<!-- Chronologischer Flugschreiber des Projekts. Ereignisbasierte Einträge, neueste oben.
     Zweck:
       1. Nahtlose Fortsetzung in neuer Session: was war zuletzt los, womit ging es zu Ende?
       2. Wiederfindbarkeit kleiner Lösungen: was war das nochmal mit dem Migrations-Bug?
       3. Selbst-Beobachtung des Projekts: was hat länger gedauert, was war überraschend?

     Abgrenzung zu anderen Dokumenten:
       - fahrplan.md: Was tun wir? (Plan)
       - decisions.md: Warum so? (Begründung)
       - architecture.md: Wie ist es gebaut? (Zustand)
       - blockers.md: Was hindert uns aktuell? (offene Probleme)
       - CHANGELOG.md: Was hat sich für Nutzer geändert? (extern, versionsorientiert)
       - logbuch.md: Was ist während der Arbeit passiert? (intern, chronologisch)

     Das Logbuch ist die einzige chronologisch durchlaufende Erzählung.
     Es darf detailreich sein und kleine Reibungen festhalten – das ist sein Wert. -->

<!-- ANCHOR:aktueller-stand -->
## Aktueller Stand

Die letzten Einträge geben den aktuellen Stand wieder. Bei Sessionbeginn liest die KI mindestens den letzten `[SESSIONENDE]`-Eintrag und alle Einträge danach, um den Faden aufzunehmen.

Das Logbuch beginnt mit der ersten regulären Session nach dem Initialisierungs-Commit (Modus 2, abgeschlossen 2026-09-26). Verlauf und Begründungen der Initialisierung stehen in `docs/decisions.md` (ADR-001 bis ADR-009). Phasen 1 bis 10 sind verdichtet; Details in `docs/archiv/logbuch-phase-1.md` bis `docs/archiv/logbuch-phase-10.md`. Die Einträge vom September 2026 (Reflexionen der Phasen 1 bis 3) stehen seit 2026-11-04 in `docs/archiv/logbuch-2026-09.md`, die vom Oktober 2026 seit 2026-11-07 in `docs/archiv/logbuch-2026-10.md`.

---

<!-- ANCHOR:eintraege -->
## Einträge (neueste oben)

### 2026-11-08 – [PHASEN-WECHSEL] Reflexion Phase 10 (UMSETZUNG) → Phase 11 (UMSETZUNG)

- **Gelernt:** Die Probe des Eigentümers am Server findet, was Tests nicht finden: Die Runware-Anbindung lief, aber die Vorbelegung des Bild-Prompts aus „Aussehen“ ist für die Modelle unbrauchbar (→ 11.5). Die getrennte Instanz kam ohne diese Rückmeldung aus dem Code zum selben Ort (`entryPrompt`, Befund 3).
- **Gelernt:** Eine Erkundung ohne Code (Bildmodelle und LoRAs, 2026-11-07) erzeugt viele Wünsche: 12 der 17 offenen V-Posten entstanden in Phase 10, sieben davon aus 10.8 (V.52–V.58).
- **Gelernt:** Arbeitsteilung Cloud/Mac trägt: KI-Läufe und Bau in der Cloud-Session, Einspielen vom Mac (ADR-025); einen neuen Schlüssel trägt der Eigentümer mit unsichtbarer Eingabe ein, die KI prüft nur das Vorhandensein.
- **Kippende Annahmen:** „Zerlegen hält“ – `ImageGenerate.tsx` wuchs nach 10.4 von 458 auf 687 Zeilen (→ 11.2). „Vorbelegung aus ‚Aussehen‘ genügt“ (ADR-084) – nicht für Runware-Modelle. „Bedrohungsmodell bleibt aktuell“ – kennt den zweiten Bildanbieter nicht (→ 11.1).
- **Reifegrad:** unverändert; „Bedrohungsmodell Gesamtsystem“ bekommt in 11.1 einen getrennt geprüften Nachtrag.
- **ADRs der Phase:** ADR-104 bis ADR-116 (13), 0 reaktiv; an der Grenze ADR-117 (Pflichtfrage) und ADR-118 (Planung Phase 11).
- **Neue Erkundungsbedarfe:** Wirkung einer Prompt-Schicht auf die Bildqualität (Probe in 11.5); Größe der Anfrage-Ablage am Server (11.3); Monatszählung für D.26 weiter offen.
- **Methodik-Lehren:** Beim Sessionstart offene Pull Requests prüfen, bevor der Stand aus `main` übernommen wird (zweimal Reibung); Sessiongröße dreimal über 200.000 Token auf „Weiter hier“; vitest läuft aus dem Wurzelordner, nicht aus `ui/`.
- **Details:** [`docs/archiv/logbuch-phase-10.md`](archiv/logbuch-phase-10.md)

### 2026-11-08 – [ADR-ANGELEGT] ADR-117 Pflichtfrage nach Phase 10, ADR-118 Planung Phase 11

- Modellwechsel auf Wunsch der Methodik: Session lief auf Sonnet 5.5 (Routine), 10.11 verlangt die Entscheidungs-Klasse → STOPP mit Modellwechsel; Eigentümer wechselte per `/model` auf `claude-opus-5-5`, von der Sitzungsabfrage bestätigt.
- Getrennte Instanz (Sonnet, ohne Gesprächsverlauf, nur lesend): klein umbauen; Bericht mit Stellungnahme in `docs/research/bewertung-phase-10.md`. Befunde 2, 5, 6 nachgeprüft (`wc`, grep, `storage/store.py`).
- Eigentümer: „Klein umbauen“ → ADR-117 (11.1–11.3). Themen für Phase 11: alle vier gewählt → ADR-118, 16 Schritte; V.21, V.54, V.55 weiter verschoben (→ 11.16).
- Vision-Abgleich gegen `docs/vision.md` und `docs/requirements.md`: keine verwaisten Elemente (alle 19 Muss erledigt, FR-006 verworfen, FR-038 → V.45 → 11.15, Publizieren bis auf V.21 erledigt).
- Phase 10 nach `docs/archiv/fahrplan-phase-10.md` ausgelagert, Detail-Einträge nach `docs/archiv/logbuch-phase-10.md`.

### 2026-11-08 – [ONBOARDING-VALIDATION] Phasengrenze Phase 10 (10.11)

- Frischer Worktree von `main` (`10a1901`) im Scratchpad: Quick Start der README genau wie dokumentiert (`uv python install 3.14.7`, `uv sync --frozen --python 3.14.7`, `npm ci`, `uv run pre-commit install`, `uv run skriptorium-einrichtung`, `npx vite build`, `uvicorn` auf Port 8765) – alle Schritte Exit 0, `/api/health` → `{"status":"ok"}` nach 2 s; `scripts/session-start.sh` Exit 0. Danach Worktree entfernt und `uv run pre-commit install` im Haupt-Checkout (Runbook Abschnitt 8). Keine Befunde.

<!-- ANCHOR:eintragstypen -->
## Eintragstypen (Übersicht)

Verbindliche Typen, andere nur in Ausnahmefällen:

| Typ | Wann | Pflicht? |
|---|---|---|
| `[SESSIONSTART]` | Zu Beginn jeder Session | Ja |
| `[SESSIONENDE]` | Vor Sessionabschluss | Ja |
| `[GELÖST]` (bis Phase 2: `[PROBLEM-GELÖST]`) | Nach Behebung eines Problems, das Reibung war | Empfohlen, alle Mini-Probleme erfassen |
| `[PROBLEM-OFFEN → BLOCKER]` | Wenn ein Problem zum Blocker eskaliert | Ja, mit Verweis auf `blockers.md` |
| `[BLOCKER-AUFGELÖST]` | Wenn ein Blocker gelöst wurde | Ja, mit Verweis auf den ursprünglichen Logbuch- und Blocker-Eintrag |
| `[REIFEGRAD-WECHSEL]` | Bei jeder Reifegrad-Änderung in `architecture.md` | Ja |
| `[ADR-ANGELEGT]` | Bei Anlage eines neuen ADR | Ja |
| `[BEOBACHTUNG]` | Wenn etwas auffällt, das später nützlich sein könnte | Optional, KI proaktiv |

<!-- ANCHOR:hinweise-zur-pflege -->
## Hinweise zur Pflege

- **Neueste Einträge oben.** Lesefluss bei Sessionbeginn ist „von oben nach unten bis zum letzten gelesenen Stand".
- **Zeitstempel ist Pflicht.** Format: `YYYY-MM-DD HH:MM` (24h, lokale Zeitzone). Bei Unsicherheit: das Datum ist Pflicht, die Uhrzeit kann grob sein.
- **Detailtiefe lieber zu hoch als zu niedrig.** Das Logbuch lebt davon, dass auch kleine Reibungen festgehalten werden – sie sind im Moment des Auftretens unscheinbar, aber später Goldwert. Wenn unsicher, ob etwas eingetragen werden soll: eintragen.
- **Verweise sind willkommen.** Wenn ein Logbuch-Eintrag mit einem ADR, einem Blocker oder einem Fahrplan-Schritt zusammenhängt: verweisen, statt zu duplizieren.
- **Keine sensiblen Daten.** Auch im Logbuch keine Secrets, keine echten PII, keine internen URLs aus Produktion. Platzhalter verwenden.

<!-- ANCHOR:archivierung -->
## Archivierung

Wenn das Logbuch unübersichtlich wird (Richtwert: >800 Zeilen, schneller wachsend als andere Dokumente):

- Alte Einträge nach `docs/archiv/logbuch-YYYY-MM.md` auslagern.
- Im aktiven Logbuch bleibt: die letzten 4–8 Wochen, plus alle Einträge, die mit aktuell offenen `blockers.md`-Einträgen verbunden sind.
- Auslagerung ist Sessionende-Aktion, keine freigabepflichtige Entscheidung.
