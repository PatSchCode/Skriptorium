# Logbuch – Archiv Oktober 2026

Quelle: `docs/logbuch.md`, ausgelagert am 2026-11-07 (Archivierungs-Trigger > 800 Zeilen, CLAUDE.md Abschnitt 14). Zeitraum: Einträge vom Oktober 2026.

## Einträge

### 2026-10-18 – [PHASEN-WECHSEL] Reflexion Phase 8 (UMSETZUNG) → Phase 9 (UMSETZUNG)

- **Gelernt:** Der Umbau vor neuen Funktionen wirkte messbar: `canon/service.py` 878 → 349 Zeilen, `WorldMaps.tsx` 716 → 86, Abdeckung Python 98,88 → 99,84 %, Oberfläche 94,45 → 98,84 % Zeilen; die Ratsche der Mindestwerte hielt die ganze Phase.
- **Gelernt:** Proben nach Regel-002 mit 3 Läufen je Seite können Streuung als Befund zeigen; erst 6 Läufe klärten 8.11. Ein Ergebnis-Satz („alle Mittelwerte in der Spannweite“) war weiter gefasst als die Tabelle – Ergebnis-Sätze vor dem Vorlegen Zeile für Zeile gegen die Zahlen prüfen.
- **Gelernt:** Am selben Tag liefen eine Cloud-Session und eine Session auf dem Mac; nicht hochgeladene Commits sieht die andere Session nicht. Nach langer Pause vor dem nächsten Schritt `origin/main` prüfen.
- **Kippende Annahmen:** Die Gliederung eines Eintrags („Aussehen“, „Geografie – …“) galt nach 8.4 als gelöst; tatsächlich kennt sie vor allem die Oberfläche, der Server sieht Textblöcke, vier Stellen erkennen Namen je eigener Regel (Bewertung, Befund 1) → 9.1.
- **Reifegrad:** unverändert `[BELASTBAR]`; NFR Kontexttreue `[VORLÄUFIG]` – die Beförderung lag seit 2026-10-11 ohne Schritt (Vision-Abgleich), jetzt 9.14.
- **ADRs der Phase:** 082–090 (082 `api` → `storage` reaktiv, 083 Abschnitte ersetzen, 084 Bildvorlagen, 085 Kurzfassung, 086 Weltenbauer im Wortlaut, 087 Weltenbauer aus dem Manuskript, 088 Verweise, 089 Pflichtfrage, 090 Planung Phase 9); Reaktiv-Quote 1/10.
- **Wucherung:** 13 → 13 Schritte; neue Wünsche als V.33–V.37 mit Landeplatz 8.13.
- **Getrennte Instanz:** für die Pflichtfrage (Sonnet, ohne Gesprächsverlauf, 20 min); bei 8.11 keine vollständige Handbewertung der Widersprüche.
- **Neue Erkundungsbedarfe:** Quellen für Worldbuilding und Namen, eigener Recherche-Baustein (9.12); Kontexttreue (9.14); Speicherlayout der Verbrauchsdateien (9.11).
- **Methodik-Lehren:** Die Drift-Prüfung am Sessionende vergleicht die Reifegrad-Tabelle mit den ADRs, nicht die NFR-Texte (Abschnitt 6) und Modulbeschreibungen (Abschnitt 3) – beide waren veraltet; erst Vision-Abgleich und Bewertung fanden es. Zusammenführen eines Pull Requests braucht eine ausdrückliche Freigabe; ein bloßes „Weiter“ lehnte die Rechteprüfung ab.
- **Details:** [`docs/archiv/logbuch-phase-8.md`](archiv/logbuch-phase-8.md)

### 2026-10-13 – [PHASEN-WECHSEL] Reflexion Phase 7 (UMSETZUNG) → Phase 8 (UMSETZUNG)

- **Gelernt:** Prüfaufträge quer über alle KI-Bereiche (D.18) finden Mischungen *innerhalb* von Einträgen, die Tests je Funktion nicht sehen (doppelte Abschnitte, Vorlagen aus dem ganzen Text). Die Zählung in den echten Daten danach (0 von 133) trennt Bauart-Risiko von eingetretenem Schaden.
- **Gelernt:** Große Bild-Themen vorab zuschneiden (ADR-072: fünf Teilschritte) hielt jeden Schritt prüfbar; jede Teilvorlage brachte aber neue Schritte (7.14, 7.15) – Phase an der Wucherungs-Schwelle.
- **Gelernt:** Bestätigungen des Eigentümers sammeln sich, wenn mehrere Schritte gleichzeitig „eingespielt, wartet“ sind (zeitweise sieben); vor einem Phasenabschluss gebündelt abfragen.
- **Kippende Annahmen:** Testabdeckung hält sich nicht von selbst – Oberfläche 98,16 → 94,45 %, weil die Schwellen 80/70 weit unter dem Ist lagen (Bewertung, Befund 3).
- **Reifegrad:** unverändert `[BELASTBAR]`; Tabelle in `docs/architecture.md` Abschnitt 9 ist nachzuziehen (8.1).
- **ADRs der Phase:** 069–081 (072 Bilder und Karten, 073 Karten, 074 Bilder beschreiben, 077 Bilder erzeugen, 078 Aussehen, 079 Markierungen, 080 Pflichtfrage, 081 Planung Phase 8); Reaktiv-Quote 0/10.
- **Wucherung:** 8 → 16 Schritte; Schwelle > 16 erreicht, nicht überschritten.
- **Getrennte Instanz:** bei 7.6, 7.10–7.13 (Sicherheit, keine Befunde hoch/mittel) und für die Pflichtfrage (Sonnet).
- **Neue Erkundungsbedarfe:** wandernde Figuren (8.12); Kosten von Regeln im Wortlaut für den Weltenbauer (8.7).
- **Methodik-Lehren:** Die Onboarding-Prüfung im Worktree verbiegt jedes Mal den gemeinsamen Pre-Commit-Hook (dreimal) – jetzt fester Teil des Ablaufs im Runbook (Abschnitt 8). Sessionstart auf dem Mac prüft den Server mit genau einer gebündelten SSH-Abfrage.
- **Details:** [`docs/archiv/logbuch-phase-7.md`](archiv/logbuch-phase-7.md)

### 2026-10-12 – [PHASEN-WECHSEL] Reflexion Phase 6 (UMSETZUNG) → Phase 7 (UMSETZUNG)

- **Gelernt:** Bei Fremdformaten den schreibenden Code des Herstellers lesen, nicht nur die Spezifikation (Hinweis des Eigentümers in 6.8): SillyTavern schreibt `chara` und `ccv3`, Lorebooks mit `comment`/`enabled`.
- **Gelernt:** Kopfzeilen und Sicherheitsregeln immer auch von außen prüfen – der Proxy überschrieb die CSP der App (6.6). Die getrennte Prüfung des Codes allein sah das nicht.
- **Gelernt:** Erst messen, dann entscheiden: der Spike 6.13 belegte den Schaden fehlender Kanon-Einträge (4,0/3,3 statt 0/0,7 Widersprüche je Kette) und machte 6.3 zur klaren Entscheidung; die Technik-Prüfung an der Geschichte des Eigentümers zeigte 0–28 → 34 von 34 Einträgen.
- **Gelernt:** Sichtproben mit Sonderfunktionen (`@`) Zeichen für Zeichen tippen; Einfügen am Stück übersah das fehlende `@`-Menü im Weltenbauer (6.7).
- **Gelernt:** Beim Einspielen nur über HTTPS warten, dann eine SSH-Abfrage – eine SSH-Schleife sperrte den Zugang vorübergehend.
- **Kippende Annahmen:** Websuche „ca. 1 ct“ – tatsächlich 5–7 ct je Antwort, weil Suchergebnisse als Eingabe zählen (6.7). Pauschaler Überschriften-Versatz im Import aus 6.8 hätte Gegenstände beim Rückimport verformt (6.9, angepasst).
- **Reifegrad:** unverändert `[BELASTBAR]`; NFR Kontexttreue beim Referenzumfang mit 6.3 und der Prüfung an der Geschichte des Eigentümers gestützt.
- **ADRs der Phase:** 059–068 (062 Kanon vor den Seiten, 063 Schutz, 064 Weltenbauer, 065/066 SillyTavern, 067 Pflichtfrage, 068 Planung Phase 7); Reaktiv-Quote 0/10.
- **Wucherung:** 12 → 14 Schritte (+6.13 Spike, +6.14 als Ausnahme auf Wunsch des Eigentümers); Schwelle > 15 nicht erreicht.
- **Getrennte Instanz:** fünfmal eingesetzt (Schutz 6.4–6.6, Import 6.8 mit Nachprüfung, Import-Änderung 6.9, Pflichtfrage); fand u. a. ein kubisch langsames Muster im bestehenden Markdown-Import.
- **Neue Erkundungsbedarfe:** Ablage von Bilddateien (7.6), Format für das Publizieren (7.4), V.20 (Figurenkarten im Netz finden).
- **Methodik-Lehren:** Phasenregeln (ADR-060: neue Wünsche → V-Schritte) vor dem ersten Mockup prüfen; Session erneut weit über der Kontextgrenze (dauerhaftes „weiter hier“ des Eigentümers).
- **Details:** [`docs/archiv/logbuch-phase-6.md`](archiv/logbuch-phase-6.md)

### 2026-10-11 – [PHASEN-WECHSEL] Reflexion Phase 5 (UMSETZUNG) → Phase 6 (UMSETZUNG)

- **Gelernt:** Die größten Verbesserungen kamen aus den Befunden des Eigentümers bei echter Nutzung (Einleitungs- und Schlusssätze, Scrollen, Chat-Aufbau, Smartphone), nicht aus Tests; Befunde sofort mit Code-Stelle festhalten und einordnen, dann bauen.
- **Gelernt:** Wirkung von Anweisungen nur mit festem Prüfverfahren belegen: Probeschreiben nach Regel-002 mit mehreren Läufen und verblindeter Bewertung (ADR-047); einzelne Läufe belegen nichts.
- **Gelernt:** Bei einem Wunsch nach „Skript“ erst die Form klären (einmaliger Befehl oder gepflegtes Werkzeug); der Schlüsseltausch wurde am Ende ein einzelner Terminalbefehl, das fertige Skript wurde verworfen. Bei Abfragen mit Inhalt der Geschichte des Eigentümers nur Art und Größe ausgeben, keine Titel.
- **Kippende Annahmen:** grok-4.7 als Modell für den Alltag – Sperren bei echten Genres und 44–157 s bis zum ersten Textstück (ADR-044, ADR-052); grok-4.6 wurde Voreinstellung, grok-4.7 bleibt wählbar. Der Referenzumfang (D.4) ließ sich nur hochrechnen; dabei blieb eine Kanon-Lücke offen (ADR-057).
- **Reifegrad:** NFR Reaktionszeit `[BELASTBAR]` → `[VORLÄUFIG]` → `[BELASTBAR]` (ADR-051, ADR-052); NFR Kontexttreue Referenzumfang `OFFEN` → `[VORLÄUFIG]` (Beförderung nach 6.3); Secrets im Betrieb bleibt `[VORLÄUFIG]` bis D.11.
- **ADRs der Phase:** 044–060 (u. a. 047 Probeschreiben, 048 Service Worker, 053 Schreibweise, 055 Modell-Katalog, 056 Verlauf der Anweisungen, 057 Nachweis D.4, 058 v1.0.0 mit Verzicht auf den menschlichen Blick, 059 Planung Phase 6, 060 Pflichtfrage); Reaktiv-Quote 0/10.
- **Wucherung:** 13 → 26 Schritte durch Befunde des Eigentümers im Alltag; Schwelle erreicht, nicht überschritten; 24 erledigt, 2 verschoben (5.4 → V.16, 5.25 → V.13 → 6.4).
- **Neue Erkundungsbedarfe:** Kanon-Lücke aus D.4 (6.3), 6.11 und 6.12 aus der Pflichtfrage (ADR-060, weiterbauen mit Umbau), freiwillige Maßnahmen V.18 und V.19, Wortanzeige im Manuskript (V.17).
- **Methodik-Lehren:** Sessions erneut weit über der Kontextgrenze auf Anweisung; 5.26 wurde doppelt begonnen, weil die Arbeit einer anderen Session übersehen wurde – vor Beginn eines Schritts Stand von `origin/main` prüfen.
- **Details:** [`docs/archiv/logbuch-phase-5.md`](archiv/logbuch-phase-5.md)

### 2026-10-08 13:15 UTC – [PHASEN-WECHSEL] Reflexion Phase 4 (STABILISIERUNG) → Phase 5 (UMSETZUNG)

- **Gelernt:** Das Gate vor dem ersten öffentlichen Deployment hat getragen: Host, Netz, Sicherung mit echter Wiederherstellung und Notfall-Handbuch lagen vor dem 30.09.; kein Sicherheitsvorfall.
- **Gelernt:** Erst die echte Nutzung zeigte die wichtigsten Mängel: Modell-Sperren bei echten Genres, Einleitungs- und Schlusssätze, Scrollen, unübersichtliche Oberfläche. Tests und Probeschreiben mit Testwelten fanden sie nicht.
- **Gelernt:** Befunde vom Eigentümer sofort mit Code-Stelle festhalten und einordnen, ohne gleich zu bauen; Entscheidungen über das Frage-System gehen auch vom Handy.
- **Kippende Annahmen:** Startmodell grok-4.7 ungeeignet für die echten Inhalte (Kanon-Treue gemessen mit qwen3.8-max); 1-Mio.-Kontextfenster sind wegen des Budgets von 30.000 Token nicht nötig; ein „Guthaben“ des Coding-Agents war irrelevant.
- **Reifegrad:** Host, Netz, Backups, Bedrohungsmodell `[BELASTBAR]`; NFR Kanon-Treue `[BELASTBAR]`; Secrets im Betrieb `[VORLÄUFIG]` bis D.11.
- **ADRs der Phase:** 025–043; reaktiv 0; Quote 0/10.
- **Wucherung:** 8 → 16 Schritte (Infrastruktur-Befunde und Funktionstest); STOPP beim 17., Neuplanung mit getrennter Instanz (ADR-042).
- **Neue Erkundungsbedarfe:** D.13 (Sperren im Text erkennen), D.4 (Referenzumfang) bleibt; grok-4.5 über 5.12 prüfen.
- **Methodik-Lehren:** Sessions erneut weit über der Kontextgrenze auf Anweisung; `pkill -f`/`pgrep -f` treffen die eigene Shell, wenn das Muster im Befehl steht (Muster mit `[u]vicorn` schreiben); Markdown-Linter verlangt echte Überschriften statt fetter Zeilen.
- **Details:** [`docs/archiv/logbuch-phase-4.md`](archiv/logbuch-phase-4.md)

### 2026-10-08 13:05 UTC – [ONBOARDING-VALIDATION] Phasenabschluss 4 und Versionsänderung (Trigger 3, DoD)

- **Form (Klasse M):** frischer Worktree von `fb912f4` im Scratchpad, eigenes Datenverzeichnis; README-Quick-Start wie dokumentiert: `uv python install 3.14.7`, `uv sync --frozen --python 3.14.7`, `npm ci` (0 Schwachstellen), `uv run pre-commit install`, `uv run skriptorium-einrichtung` (Exit 0; Ausgabe mit dem Einrichtungscode nicht angezeigt), `npx vite build`, uvicorn.
- **Ergebnis:** `/api/health` → `{"status":"ok"}`; `/` → 200; `/api/worlds` ohne Sitzung → 401; Server-Log nur eine erwartete Warnung „ki-anbieter nicht eingerichtet“ (kein Schlüssel, README: Tests ohne Schlüssel). `pytest --cov`: 410 bestanden, 99,79 %; `vitest --coverage`: 102 bestanden, 98,67 % Zeilen, 96,53 % Zweige. `scripts/session-start.sh` im Worktree: Exit 0. Pre-Commit-Hook danach im Haupt-Checkout neu installiert.
- **Befund:** keiner im Onboarding-Pfad. End-to-End-Tests laufen im CI-Job.

### 2026-10-08 13:00 UTC – [ADR-ANGELEGT] ADR-043 v0.1.0 als Vorabversion

- Vision-Checkpoint vor Go-Live: offene Elemente D.4 (FR-010 teilweise), 5.1, 5.2, 5.3; V.1/V.2 laut Vision nicht in der ersten Version; kein externer Blick. Vorgelegt als `ENTSCHEIDUNG ERFORDERLICH`; Eigentümer: „A: Vorabversion“ (Frage-System). Go-Live vor v1.0.0 in 5.14.
