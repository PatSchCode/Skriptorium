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

### 2026-11-08 – [SESSIONENDE] 11.1 bis 11.4 erledigt und eingespielt

- **Dauer:** 2026-11-08, ca. 16:20–20:35 UTC (lokale Mac-Session, mit Pausen des Eigentümers); ersetzt als Wiedereinstieg die beiden Sessionende-Einträge darunter.
- **Bearbeitet:** 11.1 (PR #224), 11.2 (#225), 11.3 (#226, ADR-120), Doku zum Einspielen (#227), 11.4 (#228, ADR-121) – alle gemergt auf Wort des Eigentümers nach grüner CI; eingespielt `d12f46f` und `3c162fa`.
- **Stand:** `main` mit diesem Abschluss (PR folgt); Server `3c162fa`, `healthy`. Phase 11 bei 4 von 16.
- **Offen:** Pull Request zu diesem Abschluss mergen. D.28 Lösung wählen; D.11 Frist überschritten. Rückweg-Image `skriptorium:vorher` steht auf `d12f46f`.
- **Nächster Schritt:** 11.5 Figuren-Assistent für das Aussehen (Vorlage mit Grundsatzfrage, kurze Probe der Textmodelle; Entscheidungs-Klasse). Datiert: D.5 ab 2026-11-12.
- **Sessionende-Prüfungen:** README gegen Fahrplan (4 von 16, Erledigt 11.1–11.4, Als Nächstes 11.5–11.6), Kontext (Status, eingespielt `3c162fa`), CHANGELOG (11.4 unter „Hinzugefügt“), Blocker 0. Drift: ADR-121 → 11.4 vorhanden; Reifegrade unverändert (ADR-120/121 ohne Wirkung); Modul-Liste unverändert; FR-035 (11.4) vorhanden; 0 blockierte Schritte; Reaktiv-Quote 0/10 (ADR-112 bis ADR-121); Phase 11 bei 16 geplanten Schritten. Größen: `docs/project-context.md` 351 Zeilen; Logbuch rund 185 Zeilen. Ablaufdaten-Register: kein neuer Vorlauf.
- **Modell-Bilanz:** durchgehend Opus 5.5 (Entscheidungs-Klasse). Oberhalb der Empfehlung: 1 Schritt (11.2, Routine). Abgegeben: getrennte Prüfung zu 11.1 an Sonnet 5.5.
- **Kontextgröße:** über der Grenze 200.000 seit Beginn (zuletzt gemessen 429.017, seitdem weiter gewachsen); weiter nach dauerhaftem „weiter hier“. Nächste Session neu beginnen.

### 2026-11-08 – [BEOBACHTUNG] 11.4 eingespielt und vom Eigentümer abgenommen

- CI auf `main` für `3c162fa` erst nach rund 2 Minuten Wartezeit angelaufen (gestartet 20:22 UTC), dann alle vier Jobs grün. Einspielen nach Runbook in einem SSH-Aufruf; `/api/health` 200 nach 60 s, Anmeldeseite 200; eine SSH-Prüfung: `healthy`, `REVISION` `3c162fa`.
- Probe des Eigentümers am Server: fester Startwert und gleiche Beschreibung → „Ja, gleiches Bild“ → 11.4 `[ERLEDIGT]`. Welche Modelle er probiert hat, hat er nicht genannt; ob OpenRouter-Modelle den Startwert einhalten, ist damit nicht einzeln belegt.
- Reibung: Der Eigentümer fragte, von welchem PR die Rede sei, als die KI auf die CI von `main` nach dem Merge wartete – künftig „Lauf auf `main` nach dem Merge“ statt „CI“ ohne Bezug sagen.

### 2026-11-08 – [BEOBACHTUNG] 11.4 gebaut, Probe am Server steht aus

- Vorab geprüft im öffentlichen Katalog von OpenRouter: 18 von 63 Bildmodellen nennen `seed` unter `supported_parameters` (Typ „boolean“, kein Wertebereich), keiner der Anbieter als Durchreich-Parameter. Deshalb zieht der Server den Startwert selbst (1 bis 2.147.483.647) und kennt ihn so auch ohne Rückmeldung des Anbieters.
- Server: `ImageOrder.seed`, `ImageModel.seed`; `image_routes` mit `_seed`, 422 für einen festen Startwert bei einem Modell ohne; Herkunft mit `startwert`, `loras`, `angehaengt` (`OriginLora` über `canon`/`manuscript` weitergereicht wie `ImageOrigin`). Tests: 1.327 grün (+25), alle geänderten Dateien 100 %, Gesamt 99,90 %. Im Testkatalog ein eigenes Modell mit Startwert (`flux.2-flex`) statt FLUX.2 Pro, damit die Vertragsdatei keinen Zufallswert aufnimmt; zwei Tests, die die Modelle aufzählen, nachgezogen.
- Oberfläche: `SeedChoice.tsx` (Hook und Zeile), Vorschau mit „Startwert behalten“, Herkunft mit Startwert, LoRAs, Angehängtem; `seedOf` nimmt Startwert und LoRAs nur auf, wenn vorhanden (alter Test unverändert). 610 Tests grün (+6), Abdeckung 98,84 / 95,30 / 98,41 / 98,97 %.
- Im Browser mit frischem Datenverzeichnis und dem echten Katalog geprüft: Zeile bei FLUX.2 Pro und Qwen Image 3, nicht bei GPT Image; ungültiger fester Wert sperrt „Erzeugen“ mit Hinweis. Reibung: ein Klick nach Koordinaten traf daneben, und `form_input` löste bei der Modellwahl kein React-Ereignis aus – über Referenz bzw. Skript nachgeholt. Erzeugt wurde lokal nichts (lokaler Schlüssel ungültig).

### 2026-11-08 – [ADR-ANGELEGT] ADR-121 Fester Startwert und vollständige Herkunft

- Vorlage zu 11.4 mit Mockup `mockup-11.4.html` (drei Ansichten vorher/nachher). Eigentümer: Bedienung „Umschalter + Behalten“, Neu erzeugen „Fest vorbelegt“, Mockup „Ja, so bauen“ – jeweils Empfehlung → ADR-121.

### 2026-11-08 – [SESSIONENDE] 11.1 bis 11.3 gemergt und eingespielt

- **Dauer:** 2026-11-08, ca. 16:20–17:45 UTC (lokale Mac-Session); ersetzt als Wiedereinstieg den Eintrag „11.1 bis 11.3 erledigt“ darunter, der vor den Merges geschrieben war.
- **Stand:** `main` `d12f46f` (PR #224, #225, #226 gemergt – alle auf „mergen“ des Eigentümers, je nach grüner CI); Server `d12f46f`, `healthy`. Phase 11 bei 3 von 16, Umbau aus ADR-117 abgeschlossen.
- **Offen:** Fernzweige `docs/11.1-bedrohungsmodell-runware`, `refactor/11.2-bildformular`, `fix/11.3-ablage-anfragen` auf GitHub löschen (Eigentümer oder KI auf Anweisung); Rückweg-Image `skriptorium:vorher` (Stand `25c9bd6`) bleibt bis zum nächsten Einspielen. D.28 Lösung wählen; D.11 Frist überschritten.
- **Nächster Schritt:** 11.4 Fester Startwert und vollständige Herkunft (Vorlage, Entscheidungs-Klasse). Datiert: D.5 ab 2026-11-12.
- **Sessionende-Prüfungen:** wie im Eintrag darunter; zusätzlich Kontext (eingespielter Stand `d12f46f`), Fahrplan 11.3 (eingespielt), ADR-120 berichtigt. Drift sonst unverändert.
- **Modell-Bilanz:** wie im Eintrag darunter (Opus 5.5; 1 Schritt oberhalb der Empfehlung: 11.2).
- **Kontextgröße:** rund 450.000 Token (Sitzungsabfrage zuletzt 429.017) – über der Grenze seit Beginn, weiter nach dauerhaftem „weiter hier“.

### 2026-11-08 – [GELÖST] Falsche Aussage zur Größe des Index berichtigt

- In ADR-120, im Logbuch und im Text von PR #226 stand, die Index-Datei schrumpfe beim Neuaufbau. Falsch: `rebuild_index` löscht und füllt dieselbe Datei, SQLite verwendet die frei gewordenen Seiten wieder, die Datei wird nicht kleiner (das ginge nur mit `VACUUM` oder einer neu angelegten Datei). Bemerkt beim Blick auf den Server nach dem Einspielen (4,5 MB). ADR-120 berichtigt; kein Handlungsbedarf, weil künftiges Wachstum die freien Seiten zuerst nutzt.

### 2026-11-08 – [BEOBACHTUNG] 11.2 und 11.3 eingespielt (`d12f46f`)

- Auf „Ja, einspielen“ des Eigentümers, nach grüner CI auf `main` für `d12f46f`. Ablauf nach Runbook Abschnitt 7 in einem SSH-Aufruf: `git archive` → `app.neu`, `REVISION`, `skriptorium:vorher` gesetzt (Stand `25c9bd6`), `app.vorher`, `docker compose build`, `up -d`.
- Warten nur über HTTPS: `/api/health` 200 nach 60 s, Anmeldeseite 200. Danach genau eine SSH-Prüfung: Container `healthy`, `REVISION` `d12f46f`, 0 Zeilen mit Pfad `…/anfragen/…` im Index (das Aufräumen beim Öffnen hat gegriffen), `index.sqlite` 4.468.736 Byte.
- Keine Probe des Eigentümers nötig (11.2 ohne sichtbare Änderung, 11.3 betrifft nur seltene Zeilen und den Index); auffällig wäre ein Fehler beim Öffnen des Reiters „Anfragen“ oder des Fensters „Bild erzeugen“.

### 2026-11-08 – [SESSIONENDE] 11.1 bis 11.3 erledigt, Umbau aus der Pflichtfrage abgeschlossen

- **Dauer:** 2026-11-08, ca. 16:20–17:30 UTC (lokale Mac-Session; nach dem ersten Sessionende zu 11.1 auf Wunsch des Eigentümers weiter mit 11.2 und 11.3).
- **Bearbeitet:** 11.1 (PR #224, gemergt `d73d03f` auf „Du mergst“ des Eigentümers); 11.2 (PR #225, CI grün, offen); 11.3 Vorlage, ADR-120, Umsetzung auf `fix/11.3-ablage-anfragen` (aufgesetzt auf 11.2).
- **Stand:** Phase 11 bei 3 von 16; Umbau aus ADR-117 (11.1–11.3) abgeschlossen. Server unverändert `25c9bd6` – 11.2 und 11.3 sind Code und noch nicht eingespielt.
- **Offen:** #225 und der Pull Request zu 11.3 mergen; danach Einspielen vom Mac auf Anweisung (ADR-039), am besten zusammen; optional danach Index einmal neu aufbauen (Runbook Abschnitt 7), damit die Datei schrumpft. Fernzweige `docs/11.1-bedrohungsmodell-runware` und nach dem Merge die übrigen löschen. D.28 Lösung wählen; D.11 Frist überschritten.
- **Nächster Schritt:** 11.4 Fester Startwert und vollständige Herkunft (Vorlage, Entscheidungs-Klasse). Datiert: D.5 ab 2026-11-12.
- **Sessionende-Prüfungen:** README gegen Fahrplan (3 von 16, Erledigt 11.1–11.3, Als Nächstes 11.4–11.5), Kontext (Status ab 11.4, nicht eingespielt), CHANGELOG (11.3 unter „Behoben“), Blocker 0. Drift: ADR-119 → 11.1, ADR-120 → 11.3 vorhanden; Reifegrade unverändert, Kopfzeile Abschnitt 9 nach ADR-119 (ADR-120 ohne Reifegrad-Wirkung); Modul-Liste unverändert; FR-027 (11.3) vorhanden; 0 blockierte Schritte; Reaktiv-Quote 0/10 (ADR-111 bis ADR-120); Phase 11 bei 16 geplanten Schritten. Größen: `docs/project-context.md` 351 Zeilen (Budget 600); Logbuch rund 150 Zeilen. Ablaufdaten-Register: kein neuer Vorlauf.
- **Modell-Bilanz:** durchgehend Opus 5.5 (Entscheidungs-Klasse). Oberhalb der Empfehlung: 11.2 (Routine; Warnung zu Beginn, Abgabe ruht bis D.22) – 1 Schritt. 11.1 und 11.3 auf ihrer Klasse. Abgegeben: getrennte Prüfung zu 11.1 an Sonnet 5.5 (Pflicht der Methodik).
- **Kontextgröße:** 429.017 Token (Sitzungsabfrage) – über der Grenze 200.000 seit Beginn; weiter nach dauerhaftem „weiter hier“ (2026-09-28). Nächste Session neu beginnen.

### 2026-11-08 – [ADR-ANGELEGT] ADR-120 Anfragen nicht im Suchindex, Trennzeilen gekennzeichnet

- Vorlage zu 11.3 mit zwei Fragen. Selbst nachgeprüft vor der Vorlage: `DocumentStore.search(…, "fulltext")` hat im Programm keinen Aufrufer (nur Tests), `canon.find_entries` nutzt `"name"`. Eigentümer: Index „Nur Anfragen raus“ (Empfehlung war, die Volltextsuche ganz zu entfernen – er behält sie), Trennzeilen „Mit \ kennzeichnen“ (Empfehlung) → ADR-120.

### 2026-11-08 – [BEOBACHTUNG] 11.3 umgesetzt

- `storage/store.py`: `_indexed` lässt genau `worlds/<welt>/stories/<geschichte>/anfragen/<datei>` aus (Tests: Welt, Geschichte, Eintrag und Unterordner namens „anfragen“ bleiben indexiert); `_drop_unindexed` entfernt beim Öffnen alte Zeilen solcher Pfade (Test mit von Hand eingefügten Zeilen in allen drei Tabellen). `manuscript/requests.py`: `_escape`/`_unescape` für Zeilen in Nachrichten, die wie Trennzeilen aussehen, auch mit schon vorangestellten `\`.
- Prüfungen: ruff, ruff format, `mypy --strict`, bandit ohne Befund; pytest 1.302 grün (vorher 1.293, +9), Abdeckung 99,90 %, beide Dateien 100 %. Keine Änderung an Oberfläche oder Abhängigkeiten.
- Zweig auf `refactor/11.2-bildformular` aufgesetzt (PR #225 offen, CI grün) – gleicher Grund wie bei 11.2.

### 2026-11-08 – [BEOBACHTUNG] PR #224 gemergt, PR #225 geöffnet

- #224 (11.1): alle vier Pflicht-Checks grün; Eigentümer „Du mergst“ → Merge-Commit `d73d03f`, Fernzweig nicht gelöscht. #225 (11.2) danach gegen das neue `main` geöffnet, zeigt nur seine zwei Commits; CI mit allen vier Checks grün.

### 2026-11-08 – [BEOBACHTUNG] 11.2 Bildformular zerlegt

- Auf „Ja, 11.2 starten“ des Eigentümers in derselben Session; Klasse über der Empfehlung (Opus statt Routine), zu Beginn gesagt; Abgabe an Sonnet ruht bis D.22.
- Zweig `refactor/11.2-bildformular` auf `docs/11.1-bedrohungsmodell-runware` aufgesetzt statt auf `main`: Der Fahrplan auf `main` kennt den Stand von 11.1 noch nicht (PR #224 offen) – sonst Konflikte in benachbarten Zeilen. Reibung: erst von `main` angelegt, die Fahrplan-Änderung schlug fehl; Zweig ohne eigene Commits gelöscht und neu angelegt.
- Zeilen vorher/nachher: `ImageGenerate.tsx` 687 → 281 (Komponente 162); neu `ImageGenerateForm.tsx` 241, `ImageChoices.tsx` 157, `RunwareLoras.tsx` 115, `imageGenerateText.ts` 97. Die Hilfen (`describePrice`, `describeBasisPrice`, `shortLabel`, `nearestFormat`) bleiben über `ImageGenerate.tsx` erreichbar, Tests unverändert.
- Prüfungen: prettier, eslint (`--max-warnings 0`), `tsc --noEmit` grün; vitest 52 Dateien, 604 Tests grün; Abdeckung 98,83 / 95,29 / 98,39 / 98,97 % (vorher 98,83 / 95,30 / 98,39 / 98,96 %; Zweige im üblichen Schwanken, über 94 %). End-to-End-Tests berühren das Bildformular nicht; sie laufen in der CI.

### 2026-11-08 – [SESSIONENDE] 11.1 erledigt, Bedrohungsmodell bleibt belastbar

- **Dauer:** 2026-11-08, ca. 16:20–16:40 UTC (lokale Mac-Session, gestartet aus der Planungssession).
- **Bearbeitet:** 11.1 – Nachtrag Runware in `docs/architecture.md` Abschnitte 3, 4 (Absatz zu 10.8 verlegt), 6, 7, 9; getrennte Prüfung; ADR-119. Branch `docs/11.1-bedrohungsmodell-runware`, Pull Request nach Freigabe des Eigentümers.
- **Stand:** 11.1 `[ERLEDIGT]`; Phase 11 bei 1 von 16. Server unverändert `25c9bd6` (reine Dokumentation, kein Einspielen).
- **Offen:** Pull Request mergen (Eigentümer); D.28 Lösung wählen; D.11 Frist überschritten.
- **Nächster Schritt:** 11.2 Bildformular entlasten (Routine-Klasse), danach 11.3 (Vorlage, Entscheidungs-Klasse). Datiert: D.5 ab 2026-11-12.
- **Sessionende-Prüfungen:** README gegen Fahrplan (1 von 16, Erledigt 11.1, Als Nächstes 11.2–11.3; Architektur-Reife mit Nachtrag), Kontext (Status ab 11.2), Blocker 0. Drift: ADR-119 → 11.1 vorhanden; Reifegrad „Bedrohungsmodell Gesamtsystem“ ↔ ADR-119 passt, Kopfzeile Abschnitt 9 auf ADR-119; Modul-Liste unverändert; FR-035/FR-025 (11.1) vorhanden; 0 blockierte Schritte; Reaktiv-Quote 0/10 (ADR-110 bis ADR-119); Phase 11 bei 16 geplanten Schritten. Größen: `docs/project-context.md` 351 Zeilen (Budget 600); Logbuch rund 125 Zeilen. Ablaufdaten-Register: kein neuer Vorlauf.
- **Modell-Bilanz:** durchgehend Opus 5.5 (Entscheidungs-Klasse, Sitzungsabfrage); 11.1 verlangt sie, 0 Schritte oberhalb der Empfehlung. Logbuch und README (Routine) nicht abgegeben – kleine Teilarbeiten mit geladenem Kontext, Routine-Abgabe ruht bis D.22. Abgegeben: getrennte Prüfung an Sonnet 5.5 – Pflicht der Methodik, keine Klassen-Abgabe.
- **Kontextgröße:** 336.176 Token (Sitzungsabfrage) – über der Grenze 200.000 schon zu Beginn (204.747); weitergearbeitet nach dauerhaftem „weiter hier“ (2026-09-28).

### 2026-11-08 – [ADR-ANGELEGT] ADR-119 Bedrohungsmodell bleibt belastbar

- Vorlage als `ENTSCHEIDUNG ERFORDERLICH` mit Auswahlfragen. Eigentümer: „Bleibt belastbar“, optionale Hinweise (Tagesgrenze für Bilder, Warnschwelle Guthaben) „Nein, nicht nötig“, Pull Request „Ja“ → ADR-119.

### 2026-11-08 – [BEOBACHTUNG] 11.1: Nachtrag Runware und getrennte Prüfung

- Nachtrag nur aus Code (`ai_gateway/runware.py`, `api/runware_models.py`, `api/image_routes.py`, `api/app.py`, `manuscript/requests.py`, `storage/store.py`, `.env.example`), ADR-114 bis ADR-117 und Runbook Abschnitt 7. Nebenbei berichtigt: Grenze gelieferter Bilder im Bedrohungsmodell stand noch auf 25 MB statt 40 MB (ADR-109); Feldaufzählung der Anfrage-Datei (`geschaetzte_token` usw. neben, nicht in `bausteine`), `kosten_usd` `null` statt leer.
- Getrennte Instanz: Unteragent auf Sonnet 5.5, ohne Gesprächsverlauf, nur lesend; erhielt Diff, Bedrohungsmodell und zum Abgleich die genannten Code-Dateien und ADRs. Ergebnis: keine falsche technische Aussage; Befund mittel – zweiter Ablageort des Runware-Schlüssels in der Cloud-Umgebung fehlte (ADR-115, belegt im Archiv-Logbuch Phase 10, 2026-11-07); 6 niedrige (zu gewisse Aussage zur Ausgabengrenze, veraltender Betrag, doppelter Rotationssatz, „sperrt nicht“ nur für die Anzeige, nicht erfasste Kosten bei Zeitgrenze und `processing`, Anfrage-Ablage fehlte im Bedrohungsmodell). Alle 7 im Text behoben; Bericht `docs/research/pruefung-11.1-runware.md`.
- Reibung: Beim Behandeln von Befund 6 schrieb die KI zuerst „der Eigentümer prüft sie beim Aufladen“ – ein nicht belegter Ablauf; vor dem Commit gestrichen. Ebenso eine ungenaue Aussage zur CI ohne Schlüssel.

### 2026-11-08 16:20 – [SESSIONSTART] 11.1 Bedrohungsmodell um Runware

- **Modell:** eingestellt und bedient `claude-opus-5-5` (Sitzungsabfrage `get_session`) → Entscheidungs-Klasse; 11.1 verlangt sie, kein STOPP nötig.
- **Wiedereinstieg:** `git fetch` und `pull --ff-only` gegen `origin/main` – schon aktuell (`a802faa`, PR #223 gemergt); keine offenen Pull Requests. Mindest-Lektüre vollständig; keine aktiven Blocker.
- **Auftrag:** Session aus der Planungssession gestartet: 11.1 nach Fahrplan abarbeiten, Branch `docs/11.1-bedrohungsmodell-runware`.
- **Kontextgröße zu Beginn:** 204.747 Token (Sitzungsabfrage `get_usage`) – über der Grenze 200.000, weil Systemkontext und Werkzeuge rund 100.000 Token belegen; weitergearbeitet nach dauerhaftem „weiter hier“ des Eigentümers (2026-09-28).
- **Kontingent:** 5-Stunden-Fenster 18 %, Woche 3 %.

### 2026-11-08 – [SESSIONENDE] 10.8 und 10.9 abgeschlossen, Phase 10 beendet, Phase 11 geplant

- **Dauer:** 2026-11-08, ca. 14:55–16:10 UTC (lokale Mac-Session; Detail-Einträge dieser Session im Archiv `docs/archiv/logbuch-phase-10.md`).
- **Bearbeitet:** 10.8 und 10.9 eingespielt (`25c9bd6`), Runware-Schlüssel vom Eigentümer eingetragen, beide Proben bestätigt → `[ERLEDIGT]` (PR #222); Befund zur Vorbelegung des Bild-Prompts bei V.58 bzw. 11.5. 10.11: Pflichtfrage mit getrennter Instanz (ADR-117), Vision-Abgleich, Planung Phase 11 (ADR-118), Phase 10 archiviert, Logbuch verdichtet, Onboarding-Pfad validiert.
- **Stand:** Server `25c9bd6` mit beiden Schlüsseln, `healthy`. `main` `10a1901`; Phasenabschluss auf `docs/10.11-planung` (Pull Request folgt).
- **Offen:** Pull Request zu 10.11 mergen (Eigentümer); D.28 Lösung wählen; D.11 Frist überschritten; Fernzweig `docs/10.8-einspielen-vorbereiten` löschen (Eigentümer, GitHub); Rückweg-Image `skriptorium:vorher` auf dem VPS bleibt bis zum nächsten Einspielen.
- **Nächster Schritt:** 11.1 Bedrohungsmodell und Architektur um Runware ergänzen (getrennte Prüfung), dann 11.2 und 11.3. Datiert: D.5 ab 2026-11-12.
- **Sessionende-Prüfungen:** README gegen Fahrplan (Phase 11, 0 von 16, Als Nächstes 11.1–11.3), Kontext (Status Phase 11, Server `25c9bd6`), Blocker 0. Drift: ADR-117/118 → 11.1–11.16 vorhanden; Reifegrade unverändert, Kopfzeile Abschnitt 9 auf ADR-118 gesetzt (inhaltlicher Nachtrag Runware in 11.1, Befund 6); Modul-Liste unverändert; FR-038 → 11.15; 0 blockierte Schritte; Reaktiv-Quote 0/10 (ADR-109 bis ADR-118); Phase 11 bei 16 geplanten Schritten (Schwelle über 32). Größen: `docs/project-context.md` 351 Zeilen (Budget 600); Logbuch nach Verdichtung rund 100 Zeilen. Ablaufdaten-Register: kein neuer Vorlauf.
- **Modell-Bilanz:** Start auf Sonnet 5.5 (Routine; Einspielen 10.8/10.9 unterhalb der Empfehlung, Entscheidungsanteil lag in ADR-114 bis ADR-116); für 10.11 STOPP mit Modellwechsel, ab da Opus 5.5 (Entscheidungs-Klasse, Sitzungsabfrage). Oberhalb der Empfehlung auf Opus: Logbuch, README, Archivierung (Routine), nicht abgegeben – kleine Teilarbeiten mit geladenem Kontext, Routine-Abgabe ruht bis D.22. Abgegeben: Bewertung an eine getrennte Instanz (Sonnet) – als Pflicht der Methodik, nicht als Klassen-Abgabe.
- **Kontextgröße:** 354.881 Token (Sitzungsabfrage) – über der Grenze 200.000 seit dem Einspielen; 10.11 auf ausdrücklichen Wunsch des Eigentümers hier („10.11 machen wir hier“). Nächste Session neu beginnen.

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
