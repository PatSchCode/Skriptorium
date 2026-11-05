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

Das Logbuch beginnt mit der ersten regulären Session nach dem Initialisierungs-Commit (Modus 2, abgeschlossen 2026-09-26). Verlauf und Begründungen der Initialisierung stehen in `docs/decisions.md` (ADR-001 bis ADR-009). Phasen 1 bis 8 sind verdichtet; Details in `docs/archiv/logbuch-phase-1.md` bis `docs/archiv/logbuch-phase-8.md`. Die Einträge vom September 2026 (Reflexionen der Phasen 1 bis 3) stehen seit 2026-11-04 in `docs/archiv/logbuch-2026-09.md`.

---

<!-- ANCHOR:eintraege -->
## Einträge (neueste oben)

### 2026-11-05 – [BEOBACHTUNG] Deployment `e809696` (9.13)

- Auf Anweisung des Eigentümers („Erstmal einspielen“). Baum von `main` gleich dem in PR #202 geprüften Baum (`391420f`). Runbook Abschnitt 7: `REVISION` `e809696`, Rückweg `skriptorium:vorher` = `7319b26`. `/api/health` 200 nach ca. 55 s (nur über HTTPS abgefragt), Anmeldeseite 200; eine SSH-Prüfung: `(healthy)`, `REVISION` `e809696`, 0 Fehlerzeilen in den ersten Minuten.
- Mini-Reibung: erster Aufruf brach lokal vor jedem Server-Zugriff ab (`git rev-parse --short` mit zwei Namen) – nichts auf dem Server verändert, zweiter Aufruf korrekt.

### 2026-11-05 – [REIFEGRAD-WECHSEL] NFR Kontexttreue Referenzumfang → `[BELASTBAR]` (ADR-103, 9.14)

- Messung auf dem Server (eine SSH-Prüfung; Skript im Container, ohne KI, nur Zahlen ausgegeben, keine Titel, Namen oder Texte): 11 Geschichten; größte 94.682 Wörter in 9 Kapiteln (zweitgrößte 73.090 in 8). Anfrage für Kapitel 9 der größten: geschätzt 29.793 von 30.000 Token; Handlungsstand (560 Wörter) und Kurzfassungen 1–8 (alle geprüft) vollständig; alle 20 Kanon-Einträge (6 Regeln, 14 Auffüllung, 5.701 Token); letzte Seiten 14.944 Token. Mit 5 Figuren per `@` ebenfalls 20 von 20, gleiche Größe. Damit ist auch die Technik-Prüfung aus ADR-062 erbracht.
- Hochrechnung: ca. 390 Token Kurzfassung je Kapitel; unter 5.000 Token Seiten ab ca. 34 Kapiteln, Ablehnung ab ca. 60. Eigentümer: „Belastbar bis ~30 Kapitel“ → ADR-103, neuer Querschnitt-Schritt D.25 (nachmessen ab 25 Kapiteln).
- 9.13 ist zu dem Zeitpunkt nicht eingespielt; die Messung betrifft eine Geschichte ohne Gäste, der Stand auf dem Server (`7319b26`) baut die Anfrage dafür gleich.

### 2026-11-05 – [BEOBACHTUNG] PR #202 zusammengeführt (9.13), Einspielen später

- Eigentümer gab die Bildschirmfotos frei („Ja, PR und Merge“); PR #202 angelegt, CI 4 von 4 grün, Protokoll ohne neue Warnung (nur die von Tests ausgelösten Zugangs- und Schlüsselwarnungen). Als Merge-Commit zusammengeführt (`e809696`). Einspielen: Eigentümer „Später“.

### 2026-11-05 – [BEOBACHTUNG] 9.13 umgesetzt (lokal), Bildschirmfotos zur Abnahme

- Umsetzung nach ADR-102 auf `feat/9.13-gaeste`; Einzelheiten und Zahlen im Fahrplan bei 9.13. Python 1123 bestanden (100 % Zeilen), Oberfläche 558, E2E 15; ruff, ruff format, `mypy --strict`, bandit, ESLint, Prettier, tsc grün.
- Abweichung vom Mockup: Überschrift des Feldes „In dieser Welt („Die Salzmark“)“ statt „In der Salzmark“ (der Artikel lässt sich aus dem Weltnamen nicht sicher bilden); keine Kostenschätzung am Knopf, die tatsächlichen Kosten stehen nach dem Vorschlag; der Vorschlag ist nur der übernehmbare Text, ohne erklärenden Absatz davor.
- Mini-Reibung: `vite build` im Ordner `ui` baute nach `ui/dist` statt nach `dist/ui` (Wurzel steht in der `vite.config.ts` des Projekts) – der erste E2E-Lauf prüfte deshalb den alten Build. Ordner entfernt, Build vom Projektordner, E2E erneut 15 grün. Merke: `npx vite build` nur vom Projektordner.
- Mini-Reibung: `pytest --cov=<einzelnes Modul>` lässt unter Python 3.14 den libyaml-Schreiber in `storage` scheitern (`EmitterError`), auch in `tests/storage/test_frontmatter.py`; ohne Abdeckung und mit `--cov=skriptorium` (wie in der CI) alles grün. Messartefakt, kein Fehler im Produkt; Abdeckung nur über das ganze Paket messen.

### 2026-11-05 – [ADR-ANGELEGT] ADR-102 Weltbezug je Gast und Einpassen (9.13)

- Eigentümer per Auswahlfragen zum Mockup: Bedienung so, Weltbezug je Geschichte, Heimatwelt-Abschnitt weglassen, wenn ein Weltbezug da ist. Kategorien 4, 1, 5, additiv, nicht reaktiv.

### 2026-11-05 – [BEOBACHTUNG] 9.13 begonnen: Bestandsaufnahme und Mockup

- Probe des Eigentümers (2026-10-21): „Gastfiguren funktionieren auch“ – kein benannter Mangel. Server (eine SSH-Prüfung, nur Anzahlen): 5 Welten, 11 Geschichten, 0 Gast-Verbindungen, 0 Fakten „nur diese Geschichte“.
- Rückfrage mit Empfehlung „auf später (nach 9.15)“, weil kein Mangel und keine Nutzung belegt sind; Eigentümer: „A wie geplant“.
- Bestand im Code: `GuestLink(world, entry)` im Kopf der Geschichte (`gast_verbindungen`), Fakten je Geschichte in `facts.md`; die Anfrage zeigt einen Gast mit „Gast aus der Welt …“ in der Überschrift und den ganzen Eintrag (`context/parts.py::render`). Bedienung: `ui/src/views/Guests.tsx` in der Seitenleiste der Geschichte.
- Mockup `mockup-9.13.html` (lokal, ausgeschlossen): Feld „In ‹Welt›“ je Gast, „✨ Einpassen vorschlagen“, Anfrage vorher/nachher, Smartphone.

### 2026-11-05 – [BEOBACHTUNG] 9.12 erledigt; V.44–V.46 und FR-038 angelegt

- Akzeptanzkriterien erfüllt: Erkenntnisdokument mit Optionen und Kosten, Vorlage an den Eigentümer, Umsetzung als eigene Schritte V.44 (Recherche), V.45 (Namen), V.46 (Fragenliste) mit Landeplatz 9.15. FR-038 Namenshilfe (Kann, von mir vorgeschlagen) angelegt.
- Drift behoben: Kennzahl „Muss / Soll / Kann“ in `docs/requirements.md` stand seit 2026-11-04 auf 19 / 10 / 6, tatsächlich 19 / 11 / 6 (FR-036 ist Soll) – jetzt mit FR-038 19 / 11 / 7.
- Reaktiv-Quote 0 / 10 über ADR-092 bis ADR-101; Phase 9 weiter 15 von 15 Schritten (V-Schritte zählen nicht zur Phase).

### 2026-11-05 – [ADR-ANGELEGT] ADR-101 Recherche, Namen, Fragenliste (9.12)

- Eigentümer per Auswahlfragen; zwei Rückfragen („Baustein Wikipedia?“, „Gibts keine Datenbanken oder spezielle RPG-Hintergrundseiten?“) – daraufhin Open5e, Fandom, World Anvil, TV Tropes und Wikidata nachgeprüft (Nachtrag 5a im Erkenntnisdokument). Entscheidung: Wikipedia und offenes D&D-Regelwerk (SRD 5.1 über Open5e) als eigene Quellen plus Websuche mit Exa und 3 Treffern; offene Namenslisten (GeoNames, Wikidata); Fragenliste je Art. Kategorien 3 und 8, nicht reaktiv.

### 2026-11-05 – [BEOBACHTUNG] Erkenntnisdokument 9.12 geschrieben, Vorlage folgt

- `docs/research/quellen-und-recherche.md`: V1 (Optionen A Plugin einstellen, B eigener Wikipedia-Baustein, C eigene Such-API, D nichts), H1 Namen (N1–N4) und Anleitungen; Preise aus OpenRouter-, Exa-, Wikimedia-, GeoNames- und Behind-the-Name-Seiten vom 2026-11-05.
- Server gelesen (eine SSH-Prüfung, nur Zahlen): 141 Weltenbauer-Anfragen im Oktober und November; ca. 26 mit sprunghaft großer Eingabe (15.000–83.000 Token, fast alle Grok, 2026-10-12 bis 10-20), zusammen ca. 1,90 $ – höchstwahrscheinlich Websuchen, die Verbrauchsdatei hat dafür kein Merkmal. Seit 2026-10-21 keine mehr.
- Befund: Die Suchgebühr (Exa 0,7 ct) ist klein; teuer ist der Suchtext im Modell, besonders bei der eigenen Suche von Grok, die OpenRouter ohne Angabe der Suchmaschine wählt.
- Mini-Reibung: fantasynamegenerators.com lehnt automatische Abrufe ab (HTTP 403); Lizenzhinweis nur über eine Kopie gefunden. Brave-Preisseite nicht direkt abrufbar – Preise aus Übersichten, im Dokument als „vor Umsetzung prüfen“ markiert.

### 2026-11-05 – [SESSIONSTART] 9.12 Quellen und Recherche (Erkundung)

- **Modell (Quelle: Systemkontext):** Opus 5.5 → Entscheidungs-Klasse; passt zur Empfehlung von 9.12 (bereitet eine Abhängigkeits- und Kostenentscheidung vor).
- **Wiedereinstieg:** `main` auf `7508191` (PR #200), Arbeitszweig `docs/9.12-quellen-recherche`. Mindest-Lektüre aus der vorigen Session im Kontext; seitdem nur die eigenen Doku-Commits. Kein aktiver Blocker.
- **Ausgangslage 9.12:** Websuche im Weltenbauer über das OpenRouter-Plugin `web` (ADR-064, max. 5 Treffer); gemessen in 6.7: 5,9–7,0 ct je Antwort, weil 17.000–22.000 Token Suchergebnisse als Eingabe des Sprachmodells zählen – die Suchgebühr selbst ist der kleinere Teil.
- **Datiert ab heute:** D.1 (Node 26 LTS frühestens 2026-11-05); D.5 Nachprüfung mypy 2 am 2026-11-06.
- **Kontextgröße:** nicht feststellbar; fortgesetzte, einmal verdichtete Session (dauerhaftes „weiter hier“ des Eigentümers).

### 2026-11-04 23:00 – [SESSIONENDE] 9.9, 9.10 und 9.11 eingespielt, gemessen und abgeschlossen

- **Dauer:** ca. 20:10–23:00 (fortgesetzte Session, einmal verdichtet).
- **Bearbeitet:** Einspielen von 9.9 und 9.10 (`e52d69a`); 9.11 von der Vorlage über Mockup, ADR-100, Umsetzung, PR #199 bis zum Einspielen (`7319b26`); Messung 9.10 (4) an Testanfragen des Eigentümers; Abschluss von 9.9, 9.10, 9.11 nach Bestätigung des Eigentümers (FR-036, FR-037 erledigt).
- **Stand:** Kein Schritt in Arbeit. Doku-PR #200 angelegt; Zusammenführen nach grüner CI freigegeben („Ja, nach grüner CI“). Kein Einspielen nötig (nur Dokumentation).
- **Offen:** nichts aus dieser Session. Lokaler Zweig `feat/9.9-loeschen-archivieren` ist überholt (zusammengeführt mit #195); Löschen nur auf Wort des Eigentümers.
- **Nächster Schritt:** 9.12 Quellen und Recherche (Erkundung). Datiert: D.1 frühestens 2026-11-05, Nachprüfung mypy 2 (D.5) am 2026-11-06.
- **Sessionende-Prüfungen:** README gegen Fahrplan, Kontext, Architektur und Blocker abgeglichen (9.9–9.11 ✅, aktive Blocker 0). Drift zwischen Pflicht-Dokumenten: ADR-098/099/100 verweisen auf bestehende Schritte; Reifegrade unverändert; Modul-Liste unverändert; FR-036/037 mit Schritt und Status; keine `[BLOCKIERT]`-Schritte; Reaktiv-Quote unverändert 0/10; Phase 9 bei 15 von 15 geplanten Schritten. `docs/project-context.md` 349 Zeilen (Budget 600). Logbuch über 800 Zeilen → September-Scheibe nach `docs/archiv/logbuch-2026-09.md` ausgelagert (830 → 756 Zeilen). Ablaufdaten-Register: D.1 und D.5 haben Schritte, kein neuer Vorlauf erreicht.
- **Modell-Bilanz:** aktiv Opus 5.5 (Entscheidungs-Klasse, Quelle: Systemkontext). Oberhalb der Empfehlung liefen das Einspielen und die Messung 9.10 (Routine) sowie die Status-Nachträge in Fahrplan, README und Logbuch; keine Abgabe an Unteragenten – kleine Teilarbeiten mit bereits geladenem Kontext, Abgabe hätte nicht gespart.
- **Kontextgröße:** nicht feststellbar (keine Abfrage in der Laufzeitumgebung genutzt); Session einmal verdichtet.

### 2026-11-04 22:50 – [BEOBACHTUNG] 9.9 erledigt

- Eigentümer prüfte Archivieren, Zurückholen, endgültiges Löschen und Kapitel löschen mit einer Wegwerf-Welt und bestätigte („9.9 passt“). Fahrplan (Schritt und Übersicht ✅), FR-036 `ERLEDIGT`, README; CHANGELOG-Eintrag 9.9 nachgetragen (fehlte). Damit ist der Block Verwaltung 9.9–9.11 abgeschlossen; nächster Schritt 9.12 (Erkundung). Keine Phasengrenze – 9.12 bis 9.15 offen.

### 2026-11-04 22:40 – [BEOBACHTUNG] 9.11 erledigt

- Eigentümer prüfte die Seite „Verbrauch“ mit den Testanfragen von 9.10 und bestätigte („9.11 passt“). Fahrplan (Schritt und Übersicht ✅, aktiver Schritt jetzt 9.9), FR-037 `ERLEDIGT`, README angepasst; CHANGELOG-Eintrag bestand schon. Priorität „Kann“ von FR-037 bleibt mein Vorschlag, vom Eigentümer nicht eigens bestätigt.

### 2026-11-04 22:30 – [BEOBACHTUNG] 9.10 erledigt

- Eigentümer bestätigte die Messung („Ja, 9.10 erledigt“). Fahrplan (Schritt und Übersicht ✅), README und CHANGELOG (Eintrag 9.10 nachgetragen) angepasst. Eingangskriterium von 9.11 („9.10 erledigt“) ist damit auch formal erfüllt.

### 2026-11-04 22:20 – [BEOBACHTUNG] Messung 9.10 (4): Zwischenspeicher greift bei Schreiben, Weltenbauer und Kurzfassung

- Testanfragen des Eigentümers 22:07–22:14 UTC in einer seiner Welten, je Ablauf zwei (Weltenbauer drei) gleiche Anfragen kurz hintereinander. Gelesen in einer SSH-Prüfung: Protokollzeilen `ki_anfrage` der letzten zwei Stunden und die November-Verbrauchsdatei (jetzt 90 Einträge, 9 neue, alle mit `welt`, Schreiben und Kurzfassungen auch mit `geschichte`). Modell `qwen/qwen3.8-max-0902`, ausführender Anbieter jedes Mal Alibaba.
- Schreiben: 1. Anfrage 23.247 Token ein, 0 aus dem Zwischenspeicher, 0,0546 $; 2. Anfrage (2,5 min später) 23.247 ein, **23.168 gelesen (99,7 %)**, 0,0155 $ (−72 %, bei mehr Ausgabe).
- Weltenbauer: 12.765 ein, 0 gelesen, 0,0269 $; dann 12.910 ein, **12.672 gelesen (98,2 %)**, 0,0134 $; dann 13.494 ein, 12.672 gelesen (93,9 %), 0,0092 $. Die Aufträge waren nicht ganz gleich; der gleichbleibende Anfang (Regeln und Kanon) wurde trotzdem gelesen.
- Kurzfassung: 23.646 ein, 0 gelesen, 0,0533 $; 1 min später 23.646 ein, **23.552 gelesen (99,6 %)**, 0,0114 $ (−79 %). Die jeweils folgende Gesamtzusammenfassung (ca. 1.550 Token ein) hatte beide Male 0 gelesen; Ursache nicht untersucht (kurze Eingabe, Anfang ändert sich mit der neuen Kurzfassung).
- `cache_geschrieben` war bei Alibaba immer 0 – der Anbieter meldet das Schreiben in den Zwischenspeicher nicht, nur das Lesen.
- Aus den Kosten errechnet: Eingabe 2 $ je Million Token, Ausgabe 6 $, gelesene Eingabe 0,25 $ – ein Achtel des Eingabepreises. Nebenbefund aus `docs/research/modell-eignungstest.md` damit für qwen3.8-max belegt; Ergänzung dort.
- Schon vor dem Einspielen von 9.10 kosteten einzelne Schreib-Anfragen am selben Tag nur ca. 0,014 $ statt 0,037 $ (18:51 und 18:57 UTC) – der Zwischenspeicher wirkte also schon vorher; 9.10 macht ihn sichtbar.
- Akzeptanzkriterien 9.10 damit erfüllt bis auf die Bestätigung des Eigentümers.

### 2026-11-04 21:45 – [BEOBACHTUNG] PR #199 zusammengeführt und eingespielt (9.11, `7319b26`)

- Eigentümer gab die Bildschirmfotos frei („Ja, push und PR“), PR #199 angelegt; CI 4 von 4 grün, Protokoll ohne neue Warnung, keine Bündelgrößen-Warnung (416,65 kB). Auf Anweisung („Merge?“) als Merge-Commit zusammengeführt (`7319b26`); #198 ist damit ebenfalls zusammengeführt (sein Commit war enthalten).
- Vor dem Einspielen geprüft: Baum von `main` gleich dem Baum des geprüften PR-Zweigs (`fed074d`) – der grüne Lauf gilt für `main`, ohne auf den Lauf auf `main` zu warten.
- Eingespielt nach Runbook Abschnitt 7; `/api/health` 200 nach ca. 60 s (nur HTTPS abgefragt), Anmeldeseite 200; eine SSH-Prüfung: `healthy`, `REVISION` `7319b26`, im Container `yaml.__with_libyaml__` wahr und `FAST` aktiv. November-Datei weiter 81 Zeilen, keine mit `welt` – seit dem ersten Einspielen heute keine KI-Anfrage (auch die Testanfragen zu 9.10 stehen aus).
- Doku-Stand dazu lokal auf `docs/9.11-eingespielt`, nicht gepusht (Regel „PR erst nach Freigabe“: gebündelt mit Messung 9.10 und den Bestätigungen).

### 2026-11-04 21:20 – [BEOBACHTUNG] 9.11 umgesetzt (lokal), Bildschirmfotos zur Freigabe

- Commits `50c57d8` (api), `31e0742` (storage), `a3d27d4` (ui); Prüfzahlen im Fahrplan 9.11. pytest 1094, Abdeckung 99,86 %; vitest 551; Playwright 15/15; Linter, Formatter, Typprüfer grün. Quick-Start nicht berührt (keine neue Abhängigkeit: libyaml steckt im PyYAML-Rad); Kategorie 6 nicht berührt (nur Kennungen in den Verbrauchsdateien, ADR-021).
- Reibungen: (1) Pre-Commit prüft mit mypy den ganzen Baum samt noch nicht hinzugefügter Dateien – der erste Commit nur mit `storage` scheiterte an den neuen, ungestagten `api`-Dateien; Reihenfolge gedreht (erst `api`, dann `storage`). (2) `ruff format` im Hook formatierte `usage_routes.py` nach einer `sed`-Änderung neu – erneut gestaged. (3) Der erste Playwright-Lauf lief gegen die alte gebaute Oberfläche (`dist/` vor der Änderung); nach `npx vite build` erneut 15/15. (4) Drei Konto-Tests in `ModelChoice.test.tsx` brauchten einen Router, weil das Konto jetzt einen Verweis enthält. (5) Smartphone-Bildschirmfoto zeigte fleckigen Hintergrund der Unterzeilen und fehlende Trenner – CSS nachgebessert, neu fotografiert.
- Größtes Bündel 416,6 kB (vorher 409 kB), keine Bündelgrößen-Warnung.
- Nach Regel „PR erst nach Freigabe“: lokal committet, nicht gepusht – Bildschirmfotos der echten Seite an den Eigentümer.

### 2026-11-04 20:40 – [ADR-ANGELEGT] ADR-100 Verbrauch je Welt und Geschichte (9.11)

- Bestandsaufnahme: alle Abläufe kennen ihre Welt; Geschichte kennen Schreiben, Kurzfassung, Gesamtzusammenfassung; Bild erzeugen kennt kein Ziel (die Oberfläche schon). Messung auf dem Mac (Skript im Scratchpad, 1.100 Zeilen im neuen Format): Schreiben der Monatsdatei 370 ms, Lesen 240 ms; libyaml 30 + 34 ms statt 140 + 226 ms für Ausgabe und Einlesen; JSON-Zeilen ca. 3 ms. Bei 2.000 Zeilen 674 / 432 ms.
- Mockup `mockup-9.11.html` (lokal, vorher/nachher, Desktop und Smartphone, Testwelten Salzmark und Glimmergrund, Beispielzahlen). Eigentümer per Auswahlfragen: Ort A, Speicher 1, Zuordnung nach Vorschlag – jeweils die Empfehlung → ADR-100, FR-037 (Priorität „Kann“ von der KI gesetzt nach dem Wortlaut von V.37 – Wunsch, keine Pflicht; Bestätigung offen). Reaktiv-Quote 0 / 10 (ADR-091–100).
- 9.10 Messung: Testanfragen des Eigentümers noch nicht gemacht („nein noch nicht“). 9.11 beginnt trotzdem – der Code von 9.10 liegt vor, nur die Messung fehlt; damit drei Schritte `[IN ARBEIT]` (9.9 wartet auf Prüfung, 9.10 auf Messung) – Abweichung von `CLAUDE.md` Abschnitt 7 mit Zustimmung des Eigentümers („dann 9.11“).

### 2026-11-04 20:12 – [BEOBACHTUNG] 9.9 und 9.10 eingespielt (`e52d69a`); Anfragen je Monat gezählt

- Eingespielt nach Runbook Abschnitt 7: `git archive` von `origin/main` (`e52d69a`, CI grün), `REVISION` geschrieben, altes Image als `skriptorium:vorher`, `app.vorher` liegt bereit; Build und Start ohne Fehler. `/api/health` 200 nach ca. 65 s (Warten nur per HTTPS), Anmeldeseite 200; eine SSH-Prüfung: Container `healthy`, `REVISION` `e52d69a`.
- Zählung für 9.11 (nur Anzahl, lesend, `data/system/verbrauch/`): 2026-10 1.094 Anfragen (176 kB), 2026-11 bis heute 81 (13 kB). Je Art über beide Monate: schreiben 915, weltenbau 138, bilderzeugung 62, kurzfassung 26, gesamtzusammenfassung 25, aussehen 9.
- Offen: Prüfung 9.9 und Messung 9.10 (4) mit echten Anfragen des Eigentümers – je Ablauf zwei gleiche Anfragen hintereinander.

### 2026-11-04 20:10 – [SESSIONSTART] Einspielen, 9.10 messen, dann 9.11

- **Modell:** Opus 5.5 (`claude-opus-5-5`, laut `get_session` und Systemkontext), Entscheidungs-Klasse – passend zu 9.11 (Empfehlung Entscheidung); Einspielen und Messung wären Routine (keine Abgabe, D.22 offen).
- **Umgebung:** Mac-Session (SSH zum VPS, ADR-025). `git fetch`: `main` auf `e52d69a` (9.9 PR #195, 9.10 PR #197), Doku-PR #198 offen. Arbeitszweig `feat/9.11-verbrauchsstatistik` auf dem Stand von #198 (`origin/scp/youthful-hawking-eb5ybn`), damit dessen Doku-Stand nicht verloren geht.
- **Beobachtung:** Der lokale Zweig `feat/9.9-loeschen-archivieren` (9 Commits, nie gepusht) ist eine ältere, parallele Umsetzung von 9.9; die gültige kam aus der Cloud-Session (PR #195). Nicht gelöscht – Entscheidung beim Eigentümer.
- **Wiedereinstieg:** Mindest-Lektüre vollständig (Projektkontext; Logbuch ab dem letzten `[SESSIONENDE]`; Fahrplan „Aktueller Stand“ und Phase 9; Architektur 1, 2, 9; Entscheidungen Teil A und C; aktive Blocker: keine). Keine offenen STOPP-Situationen.
- **Kontextgröße:** `get_session` meldet keine Kontextgröße – Regel zur Sessiongröße entfällt für diese Session.

### 2026-11-04 – [BEOBACHTUNG] 9.11 auf die Mac-Session verlegt

- Eigentümer: „weiter mit 9.11“. Rückfrage, weil das Eingangskriterium (9.10 erledigt) fehlt, die Vorlage die Zahl der Anfragen je Monat vom Server braucht (nur per SSH, ADR-025) und die Session über der Größengrenze liegt. Eigentümer per Auswahlfrage: „Neue Mac-Session“ (Empfehlung) – dort zuerst 9.9 und 9.10 einspielen, 9.10 messen, dann 9.11 mit Bestandsaufnahme, Serverzählung, Mockup und Vorlage (Entscheidungs-Klasse). Doku-PR #198 angelegt.

### 2026-11-04 – [BEOBACHTUNG] PR #197 zusammengeführt (9.10), Einspielen offen

- Entwurf #196 auf Anweisung des Eigentümers mit Verweis auf #197 geschlossen. CI zu #197 auf `1fb6b68` grün (4 von 4); Protokoll des TypeScript-Jobs ohne Bündelgrößen-Warnung, größtes Bündel 409 kB (unverändert). Kein Review, keine Konflikte. Auf Anweisung des Eigentümers („merge“) als Merge-Commit zusammengeführt (`e52d69a`). Beobachtung beendet, ausstehender Check-in gelöscht.
- 9.9 und 9.10 bleiben `[IN ARBEIT]` bis Einspielen (nur aus der Mac-Session, ADR-025); danach Prüfung 9.9 durch den Eigentümer und Messung 9.10 (4). Dieser Doku-Stand liegt auf dem neu auf `main` aufgesetzten Session-Branch und braucht einen eigenen kleinen PR.

### 2026-11-04 – [SESSIONENDE] 9.10 entschieden (ADR-099) und umgesetzt

- **Bearbeitet:** Entwurfs-PR #196 aufgegriffen; 9.10 erklärt, Wahl C → ADR-099, Umsetzung (1)–(3).
- **Stand:** Phase 9, 8 von 15; 9.9 und 9.10 `[IN ARBEIT]` (beide warten auf Einspielen; 9.9 auf die Prüfung des Eigentümers, 9.10 auf die Messung (4)). Keine aktiven Blocker, keine offenen STOPP-Situationen.
- **Nächster Schritt:** Branch `scp/youthful-hawking-eb5ybn` als Pull Request (ersetzt den Entwurf #196, dessen Branch diese Session nicht beschreiben darf), CI, Merge auf Anweisung; dann 9.9 und 9.10 aus der Mac-Session einspielen (ADR-025) und je Ablauf (Schreiben, Weltenbauer, Kurzfassung) zwei gleiche Anfragen hintereinander: `cache_gelesen` in der Protokollzeile bzw. Verbrauchsdatei festhalten.
- **Offen:** D.11 (Frist 2026-10-31 überschritten, Eigentümer); D.1 ab 2026-11-05; mypy-2-Nachprüfung 2026-11-06 (D.5); D.22 Probelauf Sonnet 5.5.
- **Modell-Bilanz:** Start Sonnet 5.5 (Routine) für Wiedereinstieg und Erklärung; nach Wechsel durch den Eigentümer Opus 5.5 (Entscheidung) für ADR und Datenmodell – passend zur Empfehlung von 9.10 bei Erweiterung der Verbrauchsdateien, 0 Schritte oberhalb der Empfehlung; keine Abgabe an Unteragenten (D.22 offen).
- **Kontextgröße:** `get_session` meldet unverändert 211.975 Token seit dem Modellwechsel – Wert wird offenbar nicht laufend aktualisiert (wie am 2026-10-25 und heute Vormittag). Über der Grenze → kein weiterer Schritt in dieser Session.
- **Sessionende-Prüfungen:** README nachgezogen (9.9 zusammengeführt, 9.10 umgesetzt). Drift: ADR-099 → 9.10 vorhanden, 9.10 nennt ADR-099; Reaktiv-Quote 0 / 10 (ADR-090–099) stimmt mit Teil B; Modul-Liste unverändert (ai_gateway, api); keine `[BLOCKIERT]`-Schritte; Phase 9 weiter 15 Schritte. Ablaufdaten-Register: D.1 erreicht morgen sein Datum, Schritt vorhanden. Archiv: Logbuch unter 800 Zeilen. Projektkontext unter Budget. Quick-Start nicht berührt; Kategorie 6 nicht berührt.

### 2026-11-04 – [BEOBACHTUNG] 9.10 umgesetzt (C, ADR-099), Messung offen

- Commits `8c31f17` (ai_gateway) und `b2faeca` (api): Cache-Token aus `usage.prompt_tokens_details` in `Usage`, Protokollzeile und Verbrauchszeile; Monatssumme und `/api/usage` unverändert. Prüfzahlen im Fahrplan 9.10.
- pytest 1046 grün, diesmal auch die 7 Fälle mit Pwned Passwords – der Dienst ist aus dieser Cloud-Session erreichbar (am Vormittag nicht). Abdeckung 99,86 %.
- Reibungen: Pre-Commit-Hook markdownlint scheiterte wieder an `nodeenv` (Vorabversion „0-alpha“) – neue Cloud-Umgebung, `~/.nodeenvrc` mit `node = 24.21.0` erneut angelegt, danach alle Hooks grün, nichts übersprungen. Ruff RUF002 (Gedankenstrich im Docstring) und ein mypy-Fund im neuen Test (Listenelemente als beliebige Kopfwerte) behoben.
- README-Drift behoben: 9.9 stand noch als „Umsetzung offen“.
- Kategorie 6 nicht berührt (nur Token-Zahlen, ADR-021); Quick-Start nicht berührt. Messung (4) braucht echte Anfragen – nach dem Einspielen aus der Mac-Session.

### 2026-11-04 – [ADR-ANGELEGT] ADR-099 Cache-Token in der Verbrauchsdatei (9.10)

- Eigentümer per Auswahlfrage nach Erklärung des Schritts: „C, dann Opus für den ADR“ → ADR-099 (Datenmodell, Kategorie 4, additiv; `/api/usage` unverändert), Reaktiv-Quote 0 / 10 (ADR-090–099). 9.10 von `[WARTET-AUF-FREIGABE]` auf `[IN ARBEIT]`.
- Feldnamen gegen die OpenRouter-Dokumentation „Prompt Caching“ geprüft (2026-11-04): beide Zahlen unter `usage.prompt_tokens_details` (`cached_tokens`, `cache_write_tokens`) – nicht auf oberster Ebene von `usage`, wie der Logbuch-Eintrag vom 2026-10-18 offen ließ.

### 2026-11-04 – [SESSIONSTART] Entwurfs-PR #196 aufgreifen, 9.10 fortsetzen

- **Modell:** Start Sonnet 5.5 (`claude-sonnet-5-5`, eingestellt und bedient laut `get_session`), Routine-Klasse – Erklärung von 9.10 und Rückfrage A/B/C. Danach Wechsel durch den Eigentümer auf Opus 5.5 (`get_session`: `user_switched_model` `claude-opus-5-5`) → Entscheidungs-Klasse für ADR und Datenmodell, passend zur Empfehlung von 9.10 bei Erweiterung der Verbrauchsdateien.
- **Umgebung:** Cloud-Session, Branch `scp/youthful-hawking-eb5ybn`, per Fast-Forward auf den Stand des Entwurfs-PR #196 (`39bd714`, Branch `claude/festive-cori-lrt580`) gezogen; auf den alten Branch darf diese Session nicht pushen.
- **Wiedereinstieg:** Mindest-Lektüre (Projektkontext, Fahrplan „Aktueller Stand“ und Phase 9, Architektur 1/2/9, Entscheidungen Teil A und C, aktive Blocker). Logbuch: Einträge bis zurück zum 2026-10-25 gelesen, die älteren bis zum `[SESSIONENDE]` vom 2026-10-18 nicht vollständig – Abweichung von der Mindest-Lektüre, die Einträge seit dem 2026-10-25 enthalten den vollständigen Stand von 9.9 und 9.10. Keine aktiven Blocker, keine offenen STOPP-Situationen.
- **Kontextgröße:** zu Beginn nicht feststellbar (`used_tokens` 0); nach dem Modellwechsel 211.975 Token (Grenze 200.000). 9.10 ist kein neuer Schritt (begonnen 2026-11-04, wartete nur auf die Freigabe) – Fortsetzung eines laufenden Schritts, keine Ausnahme „weiter hier“ nötig. Nach 9.10 kein weiterer Schritt in dieser Session.

### 2026-11-04 – [BEOBACHTUNG] Vorlage 9.10 vorgelegt, Zwischenstand als Entwurfs-PR

- Vorlage zu V.36 Punkt (3) (Kategorien 4 und 5, additiv): A nur Protokollzeile / B Verbrauchsdatei und Anzeige / C Verbrauchsdatei jetzt, Anzeige mit 9.11 (Empfehlung). Eigentümer hat nicht gewählt, sondern „Zwischenstand als PR-Entwurf festhalten“ → 9.10 auf `[WARTET-AUF-FREIGABE]`, Vorlage im Fahrplan-Schritt; kein Code begonnen.

### 2026-11-04 – [BEOBACHTUNG] 9.10 begonnen – erneut „weiter hier“, parallel zu 9.9

- `get_session`: 368.414 Token (Grenze 200.000). Eigentümer per Auswahlfrage für 9.10 erneut „Weiter hier“ → zweite Ausnahme dieser Session. 9.9 bleibt `[IN ARBEIT]` (wartet auf Einspielen und Prüfung); 9.10 hängt nicht davon ab und beginnt parallel – Abweichung von „höchstens ein `[IN ARBEIT]` je Session“ (`CLAUDE.md` Abschnitt 7) mit Zustimmung des Eigentümers.
- Modell Opus 5.5 (Entscheidung); 9.10 empfiehlt Routine, bei Erweiterung der Verbrauchsdateien Entscheidung – die Vorlage zu Punkt (3) ist Entscheidungs-Arbeit, die Umsetzung des Adapters wäre Routine (Abgabe an Sonnet 5.5 erst nach Probelauf D.22).

### 2026-11-04 – [BEOBACHTUNG] PR #195 zusammengeführt (9.9), Einspielen offen

- CI auf `005ea21` grün (4 von 4), Protokoll des TypeScript-Jobs ohne Bündelgrößen-Warnung (größtes Bündel 409 kB, +7 kB). Auf Anweisung des Eigentümers („merge“) als Merge-Commit zusammengeführt (`949b73e`). Beobachtung beendet, ausstehender Check-in gelöscht.
- 9.9 bleibt `[IN ARBEIT]` bis Einspielen (nur aus der Mac-Session, ADR-025) und Prüfung durch den Eigentümer im Betrieb.

### 2026-11-04 – [BEOBACHTUNG] Kurzfassungs-Zustand `veraltet` entschieden und umgesetzt; 9.9 lokal fertig

- Eigentümer per Auswahlfragen: neuer Zustand `veraltet` (Option A, Empfehlung) und Bestätigung der sieben Festlegungen der Umsetzung → als „Präzisiert in der Umsetzung“ in ADR-098 aufgenommen.
- Umsetzung durch einen zweiten Unteragenten (Opus, frischer Kontext) in 4 Commits `483af5d`…`aba1161`: `SummaryStatus` um `veraltet` erweitert; `ChapterStore._move_up` setzt `erzeugt`/`geprüft` → `veraltet`, `fehlt` bleibt; Kontext nutzt nur den Text (Test belegt: `veraltet` wie `erzeugt`); Oberfläche zeigt „veraltet – nach dem Löschen eines Kapitels neu erzeugen“, Rückfrage beim Kapitel-Löschen nennt die Markierung; „Als geprüft markieren“ auch für `veraltet` (Festlegung des Unteragenten, gleiche Logik wie bei `erzeugt`). `TODO(fahrplan-ref: 9.9)` entfernt.
- Gegenprüfung hier: pytest 1030 grün (rot nur die 7 bekannten Fälle ohne Passwortprüfung), vitest 545 grün, Abdeckung 98,84 / 95,7 / 98,23 / 99,01 %; laut Unteragent Python 99,67 %, alle Hooks grün. Hinweis: `483af5d` allein bricht den Vertragstest, erst mit `804cb71` grün – im PR unerheblich.

### 2026-11-04 – [BEOBACHTUNG] 9.9 umgesetzt (Unteragent), geprüft, ein Punkt offen

- Umsetzung durch einen Unteragenten (Opus, frischer Kontext) in 7 Commits `e91a1b1`…`ec42fff` (storage, canon, manuscript, api ×2, ui, docs); Einzelheiten im Fahrplan 9.9 und in `docs/architecture.md` Abschnitt 4 und 7. 9 neue Routen (71 → 80), alle ohne Sitzung abgewiesen.
- Gegenprüfung hier: ruff, ruff format, `mypy --strict` (147 Dateien) grün; pytest 1028 grün, rot nur die bekannten 7 Fälle ohne erreichbare Passwortprüfung; eslint, prettier, tsc grün, vitest 544 grün, Abdeckung 98,84 / 95,69 / 98,23 / 99,01 %. Laut Unteragent Python 99,67 %, Playwright 15/15 (Chromium über `PLAYWRIGHT_CHROMIUM_EXECUTABLE`). Durchgesehen: `DocumentStore.delete_tree` – Pfad nur über `_checked`, Aufruf nur nach „archiviert und Name stimmt“, Ordner erst per `os.replace` beiseite, dann Index und Dateien.
- Offen: Kurzfassungen nachrückender Kapitel als veraltet markieren – es gibt nur `fehlt`, `erzeugt`, `geprüft`; kein Wert erfunden, `TODO(fahrplan-ref: 9.9)` in `manuscript/chapters.py`. Rückfrage an den Eigentümer, ebenso die Festlegungen des Unteragenten über ADR-098 hinaus (u. a. Umnummerierung nicht atomar über mehrere Dateien).
- Kategorie 6 nicht berührt (keine Anmeldung, Secrets, personenbezogenen Daten); Quick-Start nicht berührt.

### 2026-11-04 – [BEOBACHTUNG] Sessiongröße überschritten – „weiter hier“ für die Umsetzung von 9.9

- `get_session` meldet 310.133 Token (Grenze 200.000, Projektkontext Abschnitt 6). Nach `CLAUDE.md` Abschnitt 0 kein neuer Schritt; Eigentümer per Auswahlfrage ausdrücklich „Weiter hier“ → Ausnahme, Umsetzung von 9.9 in dieser Session. Modell weiter Opus 5.5 (Entscheidungs-Klasse).
- Vorgehen: Die Umsetzung läuft in einem Unteragenten derselben Klasse mit frischem Kontext (Auftrag aus ADR-098 und Fahrplan 9.9) – spart gegenüber dem Weiterarbeiten im 310.000-Token-Kontext; Prüfung des Ergebnisses, Commit-Kontrolle und Push hier.

### 2026-11-04 – [BEOBACHTUNG] PR #194 zusammengeführt; D.24 erledigt

- Zweiter Lauf nach D.24 (`1c29c8b`) grün, 4 von 4 Pflicht-Checks; Protokoll des TypeScript-Jobs ohne Bündelgrößen-Warnung (die übrigen Protokolle nicht gelesen – `gh` liest Job-Protokolle durch den Proxy nicht). Ein Sicherheits-Check-in um 15:44 UTC ohne Neues. Auf Anweisung des Eigentümers („merge“) als Merge-Commit zusammengeführt (`7643a53`) → D.24 `[ERLEDIGT]`. Beobachtung beendet, ausstehender Check-in gelöscht. Kein Einspielen: nur Doku und ein Entwicklungswerkzeug.
- 9.9 bleibt `[IN ARBEIT]` (Entscheidung ADR-098 auf `main`, Umsetzung in neuer Session). Dieser Doku-Stand liegt auf dem neu auf `main` aufgesetzten Session-Branch und braucht einen eigenen kleinen PR.

### 2026-11-04 – [GELÖST] Roter Audit-Job im PR #194 durch neuen Sicherheitsfund (D.24)

- Check-in zu PR #194 (Doku 9.9): Pre-Commit, TypeScript und End-to-End grün, „Python“ rot im Dependency-Audit – `pip-audit` meldet CVE-2026-114613 in msgpack 1.2.2 (Korrektur 1.2.3). Nicht vom PR verursacht (nur Doku), blockiert jeden PR; lokal reproduziert. msgpack nur über pip-audit → cachecontrol (Entwicklungsgruppe).
- Behoben als D.24 im selben PR: `uv lock --upgrade-package msgpack` → 1.2.4 (neueste der Linie, Regel-001); `pip-audit` ohne Befund. pytest lokal: 992 grün, 7 rot (4 failed, 3 errors) – alle im Testaufbau „ohne Anbieter“, der ein Passwort über Pwned Passwords anlegt; die Prüfung ist aus der Cloud-Session nicht erreichbar („Passwortprüfung nicht erreichbar“, Folgefehler 401). Gleiches Ergebnis ohne die Änderung (gegengeprüft per `git stash`); die CI erreicht den Dienst.
- Reibung: Die Claude-GitHub-App ist auf dem Repository nicht installiert – PR-Ereignisse kommen nicht von selbst, Prüfung per geplantem Check-in. GitHub nennt das Repository in Antworten `PatSchCode/Skriptorium` (Umleitung von `Paddel87/Skriptorium`, Ursache nicht geprüft).
- Pre-Commit-Hook markdownlint wieder lauffähig: Ursache war, dass nodeenv ohne Vorgabe die neueste Node-Version aus dem Index nimmt und an einer Vorabversion („…0-alpha“) scheitert. Behoben ohne Repo-Änderung mit `~/.nodeenvrc` (`node = 24.21.0`, die Projektversion) in der Cloud-Session; danach liefen alle Hooks ohne Überspringen. Für künftige Cloud-Sessions wäre das ein Fall für `scripts/session-start.sh` (Kategorie 7, freigabepflichtig) – dem Eigentümer vorgelegt.

### 2026-11-04 – [SESSIONENDE] 9.9 entschieden, Umsetzung in neuer Session

- **Bearbeitet:** Auskunft offene Schritte/TypingMind (siehe Einträge unten); 9.9 Bestandsaufnahme, Mockup, Vorlage → ADR-098, FR-036, V.43 (Landeplatz 9.15).
- **Stand:** Phase 9, 8 von 15; 9.9 `[IN ARBEIT]` – Entscheidung liegt vor, Code noch nicht begonnen. Keine aktiven Blocker, keine offenen STOPP-Situationen.
- **Nächster Schritt:** 9.9 umsetzen nach ADR-098 und der Liste „Zu tun“ im Fahrplan (Reihenfolge `storage` → `canon`/`manuscript` → `api` → `ui`), Entscheidungs-Klasse empfohlen wegen des destruktiven Ablaufs. Mockup liegt nur im Scratchpad dieser Session – Inhalt steht vollständig im ADR.
- **Offen:** D.11 (Frist 2026-10-31 überschritten, Eigentümer); D.1 ab 2026-11-05; mypy-2-Nachprüfung 2026-11-06 (D.5). Eigentümer gibt per Auswahlfrage frei, den markdownlint-Hook für diesen Commit zu überspringen (`SKIP=markdownlint-cli2`, nur dieser Hook; Ursache `nodeenv` in der Cloud-Umgebung); markdownlint-cli2 0.23.3 von Hand: 0 Funde in 196 Dateien, übrige Hooks grün. Damit sind auch die beiden Einträge der Auskunft unten committet.
- **Modell-Bilanz:** Start Sonnet 5.5 (Routine) für die Auskunft; nach Wechsel durch den Eigentümer Opus 5.5 (Entscheidung) für 9.9 – 0 Schritte oberhalb der Empfehlung; Bestandsaufnahme an einen Suchagenten abgegeben (Lesearbeit, hält Dateiinhalte aus dem Hauptkontext; kein Kostenvorteil beim Cache-Lesen).
- **Kontextgröße:** `get_session` meldet 191.033 Token, unverändert seit dem Modellwechsel – Wert wird offenbar nicht laufend aktualisiert (wie am 2026-10-25); tatsächliche Größe vermutlich über 200.000. Kein weiterer Schritt in dieser Session.
- **Sessionende-Prüfungen:** README nachgezogen (9.9 🟠, entschieden); Drift: ADR-098 → 9.9 vorhanden, FR-036 → 9.9 und 9.9 → FR-036, V.43 → 9.15 in Übersicht und Schritt; Modul-Liste unverändert; Reaktiv-Quote 0 / 10 (ADR-089–098); keine `[BLOCKIERT]`-Schritte; Phase 9 weiter 15 Schritte. Ablaufdaten-Register: D.1 erreicht morgen sein Datum, Schritt vorhanden. Archiv: Logbuch ca. 700 Zeilen – kein Trigger. Quick-Start nicht berührt; Kategorie 6 nicht berührt.

### 2026-11-04 – [ADR-ANGELEGT] ADR-098 Archivieren und Löschen (9.9)

- Bestandsaufnahme per Suchagent (Opus-Session, nur Lesen): Löschen nur für Kanon-Einträge, Bilder, Karten, Titelbild, Gäste, Fakten; kein Archiv, kein Papierkorb, kein Ordner-Löschen in `storage`; Kapitelnummer muss `Anzahl + 1` sein, Verlauf hängt an der Nummer. Heuristiken Teil 1–4 geladen, verworfene Alternativen geprüft (nichts zum Löschen).
- Mockup `mockup-9.9.html` (Scratchpad der Session, nicht im Repo) und Vorlage vorgelegt. Eigentümer per Auswahlfragen: A Archiv + endgültig, Gäste mit entfernen, archivierte Welt nur ausgeblendet (je Empfehlung); Kapitel jedes mit Umnummerierung (gegen die Empfehlung „nur das letzte“) → ADR-098, FR-036, Reaktiv-Quote 0 / 10 (ADR-089–098).
- Reibung: Das erste Einfügen von ADR-098 scheiterte am nicht eindeutigen Anker „Abgeleitete Regel: keine“ (71 Treffer) – mit dem Schluss von ADR-097 als Anker wiederholt.
- Nebenbefund ohne Änderung: Gelöschte Kanon-Einträge lassen Fakten und geführte Figuren mit ihrer Kennung stehen – als V.43 mit Landeplatz 9.15 angelegt.

### 2026-11-04 – [BEOBACHTUNG] Modellwechsel auf die Entscheidungs-Klasse; 9.9 begonnen

- **Modell:** Eigentümer wechselt auf `claude-opus-5-5`; `get_session` meldet eingestellt `claude-opus-5-5` (`user_switched_model`) → Entscheidungs-Klasse, passend zur Empfehlung von 9.9. Die Session wird damit nach dem `[SESSIONENDE]` von heute fortgesetzt („weiter mit 9.9“).
- **Kontextgröße:** jetzt feststellbar, 191.033 Token (Grenze 200.000). 9.9 beginnt knapp unter der Grenze; Haltepunkt nach der Vorlage, Umsetzung in neuer Session.
- **9.9:** auf `[IN ARBEIT]`; Bestandsaufnahme der vorhandenen Lösch-Abläufe per Suchagent (nur Lesen). Die Antwort auf die Rückfrage zum Überspringen des markdownlint-Hooks steht aus – Logbuch-Einträge weiter uncommitted.

### 2026-11-04 – [SESSIONENDE] Auskunft: offene Schritte und TypingMind-Import

- **Bearbeitet:** keine Fahrplan-Schritte; Auskunft über offene Schritte (Phase 9 ab 9.9, Querschnitt D.x) und Stand von V.4 (TypingMind-Import: verworfen, ADR-059, 2026-10-11).
- **Stand:** unverändert – Phase 9, 8 von 15; kein aktiver Schritt, keine aktiven Blocker, keine offenen STOPP-Situationen. Nächster Schritt weiter 9.9 (Vorlage mit Mockup, Entscheidungs-Klasse).
- **Offen:** D.11 (Frist 2026-10-31) ist überschritten – Rückfrage an den Eigentümer gestellt; D.1 ab 2026-11-05, mypy-2-Nachprüfung 2026-11-06 (D.5). Ob der TypingMind-Import wieder aufgenommen wird, entscheidet der Eigentümer (Kategorie 4, Entscheidungs-Klasse).
- **Uncommitted:** Diese beiden Einträge sind nicht committet – der Pre-Commit-Hook bricht in der Cloud-Umgebung beim Einrichten der Umgebung für markdownlint ab (`nodeenv`: `ValueError … '0-alpha'` beim Auswerten der Node-Version). Kein `--no-verify` (`CLAUDE.md` Abschnitt 15). Ursache liegt in der Umgebung, nicht im Eintrag; Behebung wäre ein eigener Schritt.
- **Modell-Bilanz:** Sonnet 5.5 (Routine), 0 Schritte oberhalb der Empfehlung, keine Abgabe an Unteragenten.
- **Kontextgröße:** nicht feststellbar (`used_tokens` 0).
- **Sessionende-Prüfungen:** nur dieser Eintrag geändert; README und Pflicht-Dokumente inhaltlich nicht berührt, daher keine neue Drift; Archiv-Trigger nicht erreicht (Logbuch unter 800 Zeilen); Quick-Start nicht berührt.

### 2026-11-04 – [SESSIONSTART] Auskunft: offene Schritte und TypingMind-Import

- **Modell:** Sonnet 5.5 (`claude-sonnet-5-5`, eingestellt und bedient laut `get_session`), Routine-Klasse. Aufgabe ist reine Auskunft, kein Fahrplan-Schritt, kein Eskalations-Auslöser – kein Schritt oberhalb der Empfehlung.
- **Umgebung:** Cloud-Session, Branch `claude/festive-cori-lrt580`, `main` auf `d0fb6ef` (letzter Logbuch-Eintrag 2026-10-26).
- **Wiedereinstieg:** Mindest-Lektüre vollständig (Projektkontext, Logbuch ab letztem `[SESSIONENDE]` 2026-10-25 19:01, Fahrplan „Aktueller Stand“ und Phase 9, Architektur 1/2/9, Entscheidungen Teil A und C, aktive Blocker). Keine aktiven Blocker, keine offenen STOPP-Situationen. Phase 9: 8 von 15 erledigt.
- **Kontextgröße:** `get_session` meldet `used_tokens` 0 – nicht feststellbar, Regel zur Sessiongröße entfällt.
- **Vorhaben:** keine Änderung an Code oder Planung. Eine Wiederaufnahme von V.4 (TypingMind-Import, verworfen mit ADR-059) wäre freigabepflichtig (Kategorie 4) und liefe auf der Entscheidungs-Klasse.

### 2026-10-26 – [BEOBACHTUNG] 9.8 vom Eigentümer bestätigt

- Eigentümer im Chat: „Funktioniert“ – Prüfung im Betrieb, zugleich die erste echte Probe mit einem Bild (lokal nicht möglich, Schlüssel 401). Eingespielt war `48b8f8f`. 9.8 → `[ERLEDIGT]`; Phase 9: 8 von 15. Nächster Schritt: 9.9 Löschen oder Archivieren (Vorlage mit Mockup, Entscheidungs-Klasse).

### 2026-10-26 – [BEOBACHTUNG] Deployment `48b8f8f` (9.8)

- Auf Anweisung des Eigentümers („Doch einspielen“). Runbook Abschnitt 7 (ADR-039): `REVISION` `48b8f8f`, Rückweg `skriptorium:vorher` (Abbild `23cdc23faf30`, zuvor `7bc5333`).
- Prüfung: Warten nur per HTTPS – `/api/health` nach rund 55 s 200 `{"status":"ok"}`, Anmeldeseite 200. Eine SSH-Prüfung: `skriptorium` `(healthy)`, `app/REVISION` `48b8f8f`.
- Offen: erste echte Probe mit einem Bild und Prüfung von 9.8 durch den Eigentümer.

### 2026-10-26 – [BEOBACHTUNG] PR #192 zusammengeführt, Einspielen zurückgestellt

- Auf Anweisung des Eigentümers („merge“) nach grüner CI (4 von 4, keine neue Warnung im Protokoll) als Merge-Commit zusammengeführt (`48b8f8f`). Einspielen auf Rückfrage zurückgestellt („Noch nicht einspielen.“) – auf nodica1 läuft weiter `7bc5333`. Dieser Doku-Stand liegt lokal auf `docs/9.8-zusammengefuehrt` und wird mit dem Einspielen gebündelt.

### 2026-10-26 – [BEOBACHTUNG] 9.8 umgesetzt, getrennt geprüft, Prüfung offen

- Umgesetzt nach ADR-097 (Einzelheiten und Prüfzahlen im Fahrplan 9.8). Nebenbefund behoben: `_price` nahm die erste Preiszeile ohne Variante – bei FLUX.2 Flex ist das der Preis des Eingabebildes (zufällig gleich hoch, daher bisher unbemerkt); jetzt nur Zeilen `output_image` bzw. ohne `billable`.
- Getrennte Prüfung (Kategorie 6, CLAUDE.md Abschnitt 9 und 12): Unteragent mit Sonnet 5.5, ohne Gesprächsverlauf, Auftrag nur Diff `cb3b608..301bd67` und Bedrohungsmodell. Ergebnis: keine Befunde hoch/mittel; Pfadüberschreitung ausgeschlossen (Kennungen über `checked_identifier`, Dateinamen nur aus den Listen in den Dateiköpfen, `store._checked`), Logs nur Metadaten, `ImageReference.__repr__` ohne Bilddaten, alle Routen hinter der Sitzung. Befund 1 (niedrig): Bezeichnung „Bild N von (Name)“ kann bei langem Eintragsnamen über 200 Zeichen gehen → Übernehmen 422 nach bezahltem Bild – behoben (Kürzung im Browser, Test). Optional (über ASVS 1 hinaus, dem Eigentümer vorgelegt): Bezeichnung trimmen und Steuerzeichen ablehnen; Bezeichnung gegen die Grundlage prüfen; Obergrenze der Anfrage an den Anbieter; Anbieterpreise auf Endlichkeit prüfen – Eigentümer: „Die optionalen Härtungen lassen wir weg.“ Nicht prüfbar: Aufbewahrung beim Anbieter (Dokumentation nennt nichts, in Architektur Abschnitt 6 vermerkt), echter Lauf.
- Reibungen: Der lokale Schlüssel wird weiter abgelehnt (HTTP 401, nur Statusabfrage) – die echte Probe läuft mit der Prüfung des Eigentümers nach dem Einspielen. `Object.defineProperty` auf `naturalWidth` im Test brauchte `configurable: true`, weil der Test die Größe zweimal setzt.
- Quick-Start nicht berührt (keine Skripte, Abhängigkeiten, `.env`).

### 2026-10-26 – [ADR-ANGELEGT] ADR-097 Bild zu Bild (9.8)

- Recherche: `GET /api/v1/images/models` (61 Modelle; 57 mit `input_references` ≥ 1, FLUX.2 Pro 8) und die Anbieterpreise je Modell; Format aus der Dokumentation von OpenRouter („Image Generation“): `input_references` mit `image_url` (Base64 erlaubt) im selben Aufruf. Preis des Ausgangsbildes uneinheitlich (FLUX.2 Flex 0,06 $/MP, Seedream und Qwen 0 $, FLUX.2 Pro ohne Angabe).
- Mockup `mockup-9.8.html` (lokal) und Vorlage vorgelegt; Eigentümer per Auswahlfragen jeweils die Empfehlung: genau ein Ausgangsbild, nur gespeicherte Bilder, „Ja, umbauen“ → ADR-097. Kategorie 6 berührt (Bild an den Bildanbieter) → getrennte Prüfung vor dem Abschluss.

### 2026-10-26 – [BEOBACHTUNG] 9.7 vom Eigentümer bestätigt

- Eigentümer im Chat: „Funktioniert alles.“ Eingespielt war `7bc5333`. 9.7 → `[ERLEDIGT]` (Fahrplan, Schrittliste, Stand, README). Phase 9: 7 von 15 – die Zählung in der Fahrplan-Übersicht stand noch auf 5 (seit 9.6 nicht nachgezogen), mit korrigiert. Nächster Schritt: 9.8 Bild zu Bild (Vorlage, Entscheidungs-Klasse).

### 2026-10-26 – [BEOBACHTUNG] Deployment `7bc5333` (9.7)

- Auf Anweisung des Eigentümers („merge PR #190 und spiele main auf nodica1 ein“): PR #190 nach grüner CI (4 von 4) als Merge-Commit zusammengeführt, CI auf `main` grün. Runbook Abschnitt 7 (ADR-039): `REVISION` `7bc5333`, Rückweg `skriptorium:vorher` (Abbild `4e35b8e16068`, zuvor `adda4b9`).
- Prüfung: Warten nur per HTTPS – `/api/health` nach rund 55 s 200 `{"status":"ok"}`, Anmeldeseite 200, `PUT /api/models/aufgaben` ohne Sitzung abgewiesen (403). Eine SSH-Prüfung: `skriptorium` `(healthy)`, `app/REVISION` `7bc5333`.
- Offen: Prüfung von 9.7 durch den Eigentümer (Seite „Einstellungen“, Vorbelegung in den Aufgaben, Kurzfassungen mit eigenem Modell).

### 2026-10-26 – [BEOBACHTUNG] 9.7 umgesetzt, Prüfung offen

- Umgesetzt nach ADR-096 in `api` und `ui` (Commits `9a7e5aa`, `6252f35`); Einzelheiten und Prüfzahlen im Fahrplan 9.7. Nebenbefund aus der Bestandsaufnahme behoben: `Favorites.set` hätte das neue Feld `aufgaben` überschrieben – beide Schreibwege ersetzen jetzt nur ihr eigenes Feld (Test `test_favorites_and_task_models_keep_each_other`).
- Kurzfassungen nahmen bisher nur Modelle der festen Liste (`summarize_chapter` ohne Katalog) – mit der Einstellung wäre ein Katalogmodell sonst mit „Unbekanntes Modell“ gescheitert; die Route gibt jetzt den Katalog mit.
- Reibungen: Der Vertragstest Server ↔ Oberfläche schrieb `tests/shared/api-responses.json` erwartungsgemäß neu (neues Feld `tasks`, neuer Endpunkt aufgenommen); der Routenzähler in `test_security.py` stieg auf 71/68. Im lokalen Bildschirmstand lieferte `/einstellungen` 404 – die Oberfläche nutzt Adressen mit `#/` (`/#/einstellungen`), kein Fehler. Die Seite zeigte während des Ladens des Katalogs (ca. 5 s) eine leere Karte → Hinweis „Modelle laden …“ ergänzt. Beschriftung der Voreinstellung bei „Bild beschreiben“ und „Bilder erzeugen“ nach dem echten Katalog genauer gemacht (nennt das Modell, das die Aufgabe ohne Wahl nimmt).
- README-Drift gefunden und behoben: 9.6 stand dort noch als „Prüfung offen“, Fortschritt 5 statt 6 von 15.
- Lokaler Bildschirmstand mit leerem Test-Datenverzeichnis im Scratchpad und echtem Katalog: Auswahl gespeichert (`system/modelle.md` nur mit `aufgaben`), nach Neuladen erhalten, `GET /api/images/models` meldet das gewählte Bildmodell; Smartphone-Breite stapelt Beschriftung und Auswahl. Quick-Start nicht berührt (keine Skripte, Abhängigkeiten, `.env`); Kategorie 6 nicht berührt.

### 2026-10-25 – [ADR-ANGELEGT] ADR-096 Modell je Aufgabe, eigene Seite „Einstellungen“ (9.7)

- Bestandsaufnahme: Jede Aufgabe nimmt ihr Modell anders; Kapitel-Kurzfassung und Gesamtzusammenfassung laufen fest mit grok-4.6 und nehmen nur Modelle der festen Liste (`summarize_chapter` ohne Katalog), Bilder erzeugen jedes Mal FLUX.2 Pro. Nebenbefund: `Favorites.set` schreibt den Kopf von `system/modelle.md` neu – ein zweites Feld ginge dabei verloren; die Umsetzung muss beide Felder erhalten.
- Mockup `mockup-9.7.html` (lokal, nicht im Repo) und Vorlage vorgelegt; Eigentümer per Auswahlfragen jeweils die Empfehlung: eigene Seite, Wahl in der Aufgabe nur für dieses Mal, „Ja, umbauen“ → ADR-096.

### 2026-10-25 23:39 MEZ – [SESSIONSTART] 9.7 Einstellungsseite – Modell je Aufgabe

- **Modell:** Opus 5.5 (`claude-opus-5-5`, eingestellt und bedient laut `get_session`), Entscheidungs-Klasse. 9.7 empfiehlt Entscheidung – kein Schritt oberhalb der Empfehlung.
- **Umgebung:** Mac-Session („Deploy“), `main` auf `aad29d2`, eingespielt `adda4b9`. Diese Session begann auf Sonnet 5.5 (Routine) mit dem Einspielen von `adda4b9` und dem PR #189 ohne eigenen `[SESSIONSTART]` – Einspielen ist kein Fahrplan-Schritt; beim Anstoß von 9.7 Stopp nach `CLAUDE.md` Abschnitt 0 (Auslöser 1), danach Wechsel durch den Eigentümer.
- **Wiedereinstieg:** Mindest-Lektüre vollständig (Projektkontext, Logbuch ab `[SESSIONENDE]` 2026-10-25 19:01, Fahrplan „Aktueller Stand“ und Phase 9, Architektur 1/2/9, Entscheidungen Teil A und C, aktive Blocker). Keine aktiven Blocker, keine offenen STOPP-Situationen, Reaktiv-Quote 0 / 10. Phase 9: 6 von 15 erledigt.
- **Kontextgröße:** `get_session` meldet keinen Wert – Regel zur Sessiongröße entfällt für diese Session (`CLAUDE.md` Abschnitt 0).
- **Vorhaben:** 9.7 beginnt mit Bestandsaufnahme, Mockup vorher/nachher und Vorlage (Kategorien 4 und 5); Branch `feat/9.7-modell-je-aufgabe`.

### 2026-10-25 – [BEOBACHTUNG] Deployment `adda4b9` (9.6, D.21, D.23)

- Auf Anweisung des Eigentümers („deploy“); vorher `git fetch`/Merge gegen `origin/main` (Konflikte in Fahrplan, Logbuch, Projektkontext aufgelöst, Merge `6487d76` lokal). CI auf `main` grün. Runbook Abschnitt 7 (ADR-039): `REVISION` `adda4b9`, Rückweg `skriptorium:vorher` (Abbild `19f6f3791ef6`, zuvor `e886916`).
- Reibung: Der Berechtigungsprüfer lehnte den Server-Befehl (Tausch, Build, Neustart) beim ersten Mal ohne Begründung ab; nach ausdrücklicher Bestätigung des Eigentümers lief er durch. Der Upload war schon vorher erfolgt, es blieb nichts halb getauscht.
- Prüfung: Warten nur per HTTPS – `/api/health` lieferte während des Starts 404 (Proxy), nach rund 55 s 200 `{"status":"ok"}`; Anmeldeseite 200. Eine SSH-Prüfung: `skriptorium` `(healthy)`, `app/REVISION` `adda4b9`.
- Offen: Prüfung von 9.6 durch den Eigentümer.

### 2026-10-25 – [BEOBACHTUNG] 9.6 vom Eigentümer bestätigt

- Eigentümer im Chat: „9.6 hat erfolgreich funktioniert.“ Eingespielt war `adda4b9`. 9.6 → `[ERLEDIGT]` (Fahrplan, Schrittliste, Stand). Nächster Schritt: 9.7 Einstellungsseite – Modell je Aufgabe (Mockup und Vorlage zuerst).

### 2026-10-25 – [BEOBACHTUNG] PR #187 zusammengeführt; D.23 erledigt

- Zweiter Lauf nach D.23 (`cfd86c6`) grün, 4 von 4 Pflicht-Checks; ein Kommentar im PR erklärt den ersten roten Lauf. Auf Anweisung des Eigentümers („merge“) zusammengeführt als Merge-Commit (`b66196e`) → D.23 `[ERLEDIGT]`. 9.6 bleibt `[IN ARBEIT]` bis Einspielen und Bestätigung. Beobachtung des PR beendet. Dieser Doku-Stand liegt auf dem Branch der Session, neu auf `main` aufgesetzt; er braucht einen eigenen kleinen PR.

### 2026-10-25 – [GELÖST] Rote Audit-Jobs im PR #187 durch neue Sicherheitsfunde (D.23)

- PR #187 (9.6) lief rot in „Python“ und „TypeScript“, jeweils im Dependency-Audit: `pip-audit` meldet drei CVEs in filelock 4.0.4, `npm audit` (Schwelle high) Funde in undici 7.30.0 und zod 4.6.5. Nicht vom PR verursacht, blockiert jeden PR – lokal reproduziert. Pre-Commit und End-to-End waren grün.
- Behoben als D.23 im selben PR: `uv lock --upgrade-package filelock` → 4.2.4; `npm audit fix` (ohne `--force`) → undici 7.30.1, zod 4.6.7. Beide Audits ohne Befund über der Schwelle, vitest 506 und Pre-Commit grün. Alles nur Entwicklungswerkzeuge – kein Einspielen. Drei mittlere vitest-Funde bleiben unter der Schwelle (Landeplatz D.2).

### 2026-10-25 19:01 MEZ – [SESSIONENDE] 9.5 erledigt, 9.6 entschieden und umgesetzt

- **Dauer:** 18:34 bis 19:01 MEZ (Cloud-Session, Branch `claude/festive-hawking-shngn2`).
- **Bearbeitet:** 9.5 `[ERLEDIGT]` (Bestätigung des Eigentümers); 9.6 Vorlage → ADR-095, V.42 (Landeplatz 9.15); 9.6 umgesetzt in `storage`, `canon`, `manuscript`, `api`, `ui` (Commits `1272662`, `0ec0b8f`, `0eb1767`).
- **Stand:** Phase 9, 5 von 15; 9.6 `[IN ARBEIT]` – lokal fertig: pytest 956, vitest 506, Playwright 15/15, ruff, mypy --strict, bandit, eslint, prettier, tsc grün. Keine aktiven Blocker, keine offenen STOPP-Situationen.
- **Offen:** Pull Request zu 9.6 (CI) nach Freigabe des Eigentümers; Einspielen von 9.5 und 9.6 auf dem VPS (nur vom Mac aus, ADR-025); Prüfung von 9.6 durch den Eigentümer. Probelauf der Routine-Klasse mit Sonnet 5.5 (Wechsel gegenüber Sonnet 5, `CLAUDE.md` Abschnitt 0) – auf Wahl des Eigentümers als D.22 angelegt; Abgabe an die Routine-Klasse bis dahin ausgesetzt (Projektkontext Abschnitt 6). D.11 bis 2026-10-31, D.19 bis 2026-11-02.
- **Nächster Schritt:** Pull Request 9.6, nach Einspielen Prüfung durch den Eigentümer; dann 9.7 (Vorlage, Entscheidungs-Klasse).
- **Modell-Bilanz:** Start auf Routine-Klasse (Sonnet 5.5) – nur Sessionstart, kein Schritt; nach Wechsel durch den Eigentümer Entscheidungs-Klasse (Opus 5.5, eingestellt und bedient laut `get_session`). 9.6 empfiehlt Entscheidung → 0 Schritte oberhalb der Empfehlung. Statuspflege von 9.5 und Doku nicht abgegeben: kleiner Umfang, Kontext geladen; Abgabe an Sonnet 5.5 ohne eigenen Probelauf ohnehin nicht gedeckt.
- **Kontextgröße:** `get_session` meldete einmal 174.394 Token (nach dem Modellwechsel) und danach unverändert denselben Wert – der Wert wird offenbar nicht laufend aktualisiert; tatsächliche Größe zum Sessionende vermutlich über der Grenze von 200.000. Kein neuer Schritt begonnen; 9.6 wurde als laufender Schritt zu Ende gebaut.
- **Sessionende-Prüfungen:** README synchron (5 von 15, 9.5 ✅, 9.6 🟠, 0 Blocker). Drift: ADR-095 → 9.6 vorhanden; V.42 → 9.15 in Übersicht und „Zu tun“; Modul-Liste unverändert; Reaktiv-Quote 0 / 10 (ADR-086–095); keine `[BLOCKIERT]`-Schritte; Phase 9 weiter 15 Schritte; Schnittstellen in `docs/architecture.md` Abschnitt 4 nachgetragen, Ablage in Abschnitt 7, Verworfenes in 8. Projektkontext-Status auf „ab 9.6“. Ablaufdaten-Register: D.19 läuft; D.1 ab 2026-11-05 noch nicht im Vorlauf. Archiv: Logbuch ca. 560 Zeilen, project-context 349 – kein Trigger. Quick-Start nicht berührt (keine Skripte, Abhängigkeiten, `.env`). Kategorie 6 nicht berührt (keine Anmeldung, Secrets oder personenbezogenen Daten; Logs nennen weiter keine Anweisung).

### 2026-10-25 – [BEOBACHTUNG] Umsetzung 9.6: Tests prüfen die genaue Folge der Anfragen

- Sieben bestehende Komponenten-Tests schlugen fehl, weil die große Ansicht jetzt die Herkunft lädt (zusätzliche `GET …/origin`) und `calls.at(-1)` bzw. `calls` gleich `[]` prüften; ein Test fand „kein Fake“ doppelt (Fehlertext der Herkunft). Gelöst mit `withoutOrigins(calls)` in `ui/fake-api.ts` und genauerem Muster; außerdem schickt das Hochladen `herkunft` nur mit, wenn es eine gibt – der Körper beim reinen Hochladen bleibt wie bisher.
- `test_security.py` zählt die Routen fest (67 → 70, geschützt 64 → 67) – gewollt, prüft, dass jede neue Route ohne Sitzung abgewiesen wird.
- Ein bestehender Speicher-Test (Löschen schlägt fehl) traf nach der Änderung zuerst die Begleitdatei; der Fehlerweg des Bildes selbst blieb ungetestet (Abdeckung 99 % statt 100 % in `store.py`) – eigener Test ergänzt.

### 2026-10-25 – [ADR-ANGELEGT] ADR-095 Herkunft erzeugter Bilder in einer Begleitdatei (9.6)

- Vorlage mit drei Optionen (Kopf / Begleitdatei / zentrales Verzeichnis), Heuristiken Teil 1–3 geladen. Eigentümer per Auswahlfragen jeweils die Empfehlung: B Begleitdatei, aufklappbar mit „Mit dieser Anweisung neu erzeugen“, Kosten mit festhalten, Nebenfrage KI-Text „Später planen“ → V.42 (Landeplatz 9.15).
- Feststellung bei der Vorlage: Der Suchindex liest jede `.md`-Datei unter dem Datenverzeichnis (`storage/store.py`, `rglob("*.md")`) – deshalb Endung `.herkunft.yml`.
- Reaktiv-Quote 0 / 10 (ADR-086–095).

### 2026-10-25 – [BEOBACHTUNG] Modellwechsel auf die Entscheidungs-Klasse; 9.5 erledigt; 9.6 begonnen

- **Modell:** Eigentümer wechselt per `/model` auf `claude-opus-5-5`; `get_session` bestätigt eingestellt und bedient `claude-opus-5-5` → Entscheidungs-Klasse. Kontextgröße jetzt feststellbar: 174.394 Token (Grenze 200.000).
- **9.5:** Eigentümer im Chat: „9.5 ist bestätigt“. Code lag bereits auf `main` (PR #184, `e886916`) → `[ERLEDIGT]`, Phase 9: 5 von 15. Ob 9.5 auf dem VPS eingespielt ist, ist hier nicht belegt (zuletzt eingespielt laut Projektkontext `2586ef8`).
- **9.6:** auf `[IN ARBEIT]`. Befund für die Vorlage: Erzeugen speichert nichts (ADR-077), die Übernahme läuft wie ein Hochladen (Browser verkleinert, Server prüft und legt ab) – der Server sieht beim Ablegen weder Modell noch Anweisung; Herkunft muss die Oberfläche mitschicken. Drei Ablageorte mit verschiedenen Kopffeldern: `bilder` (Liste von Dateinamen, Eintrag), `karten` (Liste von Abbildungen mit `name`, `datei`, `marken`, Welt), `titelbild` (ein Dateiname, Geschichte).

### 2026-10-25 18:34 MEZ – [SESSIONSTART] Neue Cloud-Session ohne Auftrag

- **Modell (Quelle: `get_session`):** eingestellt `claude-sonnet-5-5`, bedient `claude-sonnet-5-5` → Routine-Klasse. Hinweis: `docs/project-context.md` Abschnitt 6 nennt „Claude Sonnet 5“ mit bestandenem Probelauf (2026-09-28); Sonnet 5.5 ist ein Modellwechsel innerhalb der Klasse, der Probelauf ist nach `CLAUDE.md` Abschnitt 0 zu wiederholen (offen, kein Fahrplan-Schritt angelegt – dem Eigentümer vorzulegen).
- **Kontextgröße:** nicht feststellbar – `get_session` meldet `used_tokens` 0 (`max_tokens` 1.000.000); Regel zur Sessiongröße entfällt.
- **Wiedereinstieg:** Mindest-Lektüre vollständig (Projektkontext, Logbuch ab `[SESSIONENDE]` 2026-10-22, Fahrplan „Aktueller Stand“ und Phase 9, Architektur 1/2/9, Entscheidungen Teil A und C, aktive Blocker). Keine aktiven Blocker, keine offenen STOPP-Situationen, `main` = Stand dieses Branchs (`8a6b4d4`, PR #186). Phase 9: 4 von 15 erledigt; 9.5 umgesetzt, Prüfung durch den Eigentümer offen; 9.6 ist der nächste Schritt (Empfehlung Entscheidung, Datenmodell – würde in dieser Klasse einen Stopp nach Abschnitt 0 auslösen).
- **Auftrag:** keiner genannt („neue session“); es wurde nichts am Code geändert.

### 2026-10-22 – [BEOBACHTUNG] Textqualität von Hermes 4 → V.41; D.21 erledigt

- PR #185 nach grüner CI zusammengeführt (`214b8c7`) → D.21 `[ERLEDIGT]`.
- Frage des Eigentümers: Wie lässt sich die Textqualität von Hermes verbessern? Hermes 4 wurde im Projekt nie gemessen. Befund im Code: Reasoning für nicht gelistete Modelle aus (Hermes 4 405B bietet es laut OpenRouter-Katalog an), Temperatur fest 0,8, keine Strafe gegen Wiederholungen. Schwächen laut Eigentümer: Stil/Deutsch, selten endlose Wiederholungen. Auf seine Wahl V.41 angelegt (Messung nach Regel-002, Landeplatz 9.15).

### 2026-10-22 – [GELÖST] Roter Audit-Job durch Sicherheitsfunde in virtualenv (D.21)

- Doku-PR #185 lief rot in „Python“, Schritt Dependency-Audit: `pip-audit` meldet fünf CVEs in virtualenv 21.13.0 (Korrekturen bis 21.14.9). Nicht vom PR verursacht, blockiert jeden PR – lokal reproduziert.
- Behoben als D.21 im selben PR (nur dieser Branch ist für die Cloud-Session beschreibbar): `uv lock --upgrade-package virtualenv` → 21.14.12; Audit ohne Befund, Pre-Commit grün. virtualenv kommt nur über pre-commit, nicht im Betrieb – kein Einspielen.

### 2026-10-22 – [SESSIONENDE] Cloud-Session zu 9.4 und Rückmeldung zu Sperren

- **Dauer:** 2026-10-19 22:28 MESZ bis 23:16 MESZ (9.4), fortgesetzt 2026-10-22 (Rückmeldung zu Sperren).
- **Bearbeitet:** 9.4 (ADR-093, PR #181, später von der Mac-Session eingespielt und abgenommen); Nachtrag D.19; D.13 erste Beispiele ohne Wortlaut, Wortlaut wechselt mit der Eingabe; V.40 angelegt (Landeplatz 9.15).
- **Stand:** Phase 9, 4 von 15; 9.5 in Arbeit (Mac-Session, Prüfung des Eigentümers offen). Keine aktiven Blocker, keine offenen STOPP-Situationen.
- **Offen:** Wortlaut einiger Sperren und Weigerungen von Figuren für D.13 (Eigentümer); D.19 bis 2026-11-02.
- **Nächster Schritt:** Prüfung von 9.5 durch den Eigentümer, dann 9.6.
- **Modell-Bilanz:** Entscheidungs-Klasse (Opus 5.5, eingestellt und bedient laut `get_session` 2026-10-19). 9.4 empfiehlt Entscheidung; die Doku-Arbeit zu D.13/V.40 ist Routine – wegen kleinen Umfangs und geladenen Kontexts nicht abgegeben. 0 Schritte oberhalb der Empfehlung, keine Abgabe.
- **Kontextgröße:** nicht feststellbar – `get_session` meldet `used_tokens` 0; Regel zur Sessiongröße entfällt (vermerkt).
- **Sessionende-Prüfungen:** README synchron (4 von 15, 0 Blocker; V.40 nicht nutzerrelevant). Drift: ADR-093 → 9.4 vorhanden; V.40 → 9.15 in Übersicht und „Zu tun“ von 9.15 nachgetragen; D.13-Zeile der Übersicht nachgezogen; keine `[BLOCKIERT]`-Schritte; keine neuen ADRs seit ADR-094. Ablaufdaten-Register: D.19 läuft; D.1 ab 2026-11-05 noch nicht im Vorlauf. Archiv: Logbuch ca. 520 Zeilen, project-context 349 – kein Trigger. Quick-Start nicht berührt.

### 2026-10-22 – [BEOBACHTUNG] Nachtrag aus der Cloud-Session zu 9.4; Rückmeldung zu Sperren (D.13)

- **Nachtrag 9.4 (2026-10-19):** Die Cloud-Session hat nach dem Merge von PR #181 (`67fc36e`, CI 4 von 4 grün 21:12–21:15 UTC) einen Doku-Commit (`b8a9aa8`) nur auf ihren Branch gepusht und keinen `[SESSIONENDE]` geschrieben – Versäumnis, nicht nachholbar. Inhalt übertragen, soweit nicht überholt: D.19 – Python-Job lief auf `ubuntu-24.04` (Abbild 20261018.339.1), ohne Warnung; nur dieser Job gelesen. Bei den Proben zu 9.4 lief Playwright lokal erst mit `PLAYWRIGHT_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium` und nach `npm run build` (vorher 404 auf `/`).
- **Rückmeldung des Eigentümers:** „Blockade der KI“ – per Auswahlfrage: die KI im Skriptorium sperrt. Gehört zu D.13 (Eingangskriterium: Beispiele echter Sperren). Angaben (Ablauf, Modell, Wortlaut, Form, Wiederholung) erfragt. Antwort: Sperren im Weltenbauer, im Kanon, bei Kurzfassung und „Bild beschreiben“; grok-4.5 (seltener) und grok-4.6, qwen3.8 ebenso, Hermes 4 bisher nicht; teils bei CNC-Szenarien; sah aus wie eine Antwort; „jedes Modell blockt, wenn im Verlauf zuvor ein anderes geblockt hatte – nur im Kanon“.
- **Ursache im Code (Hypothese, nicht mit echter KI geprüft):** `ui/src/views/useWorldbuilder.ts` schickt das ganze Gespräch mit; eine als Antwort gelieferte Sperre bleibt als Antwort der KI im Verlauf und geht an jedes folgende Modell. Kurzfassung und „Bild beschreiben“ haben keinen Verlauf. Abhilfe bis dahin: Seite neu laden (Gespräch wird nicht gespeichert), Auftrag mit anderem Modell neu stellen.
- **Landeplatz:** Eigentümer per Auswahlfrage: neuer Schritt mit Planung 9.15 „plus die Möglichkeit, die letzte Eingabe wiederholt zu senden“ → V.40 (Antwort aus dem Gespräch nehmen, letzte Eingabe erneut senden). Beispiele bei D.13 vermerkt, ohne Wortlaut.
- **Nachtrag:** Eigentümer: Der Wortlaut der Sperren ist dynamisch, abhängig von der Eingabe. Bei D.13 vermerkt mit vier zu vergleichenden Wegen (Kennung im Rahmen, äußere Merkmale, zweites Modell, Entscheidung des Autors über V.40).

### 2026-10-21 – [BEOBACHTUNG] Deployment `e886916` (9.5); D.19 erledigt

- Auf Anweisung des Eigentümers („Pushen, mergen, einspielen“): #184 nach grüner CI gemergt, CI auf `main` grün. Runbook Abschnitt 7 (ADR-039): `REVISION` `e886916`, Rückweg `skriptorium:vorher` = `2586ef8`; `/api/health` 200 nach ca. 63 s (über HTTPS), `/` 200, `/api/worlds` 401, `/sw.js` 200; einmal per SSH `(healthy)`, 0 Fehlerzeilen.
- D.19: Im Lauf zu #184 liefen alle vier Jobs auf `ubuntu-26.04` (Abbild 20261012.163.1), alle grün, keine Warnung im Protokoll → `[ERLEDIGT]`, Register-Zeile nachgezogen.
- Offen: Prüfung von 9.5 durch den Eigentümer an seinen Welten.

### 2026-10-21 – [BEOBACHTUNG] 9.5 umgesetzt, Prüfung offen

- Mockup vorher/nachher (echte Bildschirmfotos auf einem lokalen Server mit der Testwelt Salzmark, Nachher in die echte Seite eingesetzt) freigegeben: „Passt, umbauen“, Orte vorab „Alle angekreuzt“.
- Umgesetzt nur in `ui` (siehe Fahrplan 9.5). Bei der Durchsicht der echten Bildschirmfotos nachgebessert: Der Hinweis beim Gegenstand nannte „ersten Satz aus ‚Zweck‘“ auch ohne Abschnitt „Zweck“ – jetzt „ersten Satz des Textes“. Ein eigener Test wartete zuerst auf „Abbrechen“ des Herauslösens; der Knopf heißt dort „Verwerfen“, „Abbrechen“ gehört zum Bildfenster – Tests auf die richtigen Knöpfe umgestellt.
- Prüfungen: vitest 498 (gesamt 98,7 % Zeilen, 95,4 % Zweige), tsc/eslint/prettier sauber, Build, Playwright 15, pytest 932. Commits lokal; Push nach Freigabe des Eigentümers.

### 2026-10-21 – [ADR-ANGELEGT] ADR-094 Bilder vom Bedarf her (9.5)

- Zählung im Betrieb (nur Zahlen, keine Namen): Figuren 12/27 mit „Aussehen“, Gegenstände 3/43 (38 mit Zweck/Verwendung/Auswirkung), Orte 0/19 gegliedert, Kultur 10 ungegliedert, 0/5 Welten mit „Geografie – …“.
- Vorlage mit Tabelle je Bildart; Eigentümer per Auswahlfragen jeweils die Empfehlung: 1B Orte ankreuzen, 2A Hinweis mit Knopf, 3A Name + erster Satz „Zweck“. Danach richtiggestellt: Herauslösen gibt es nur für Figuren (ADR-083) – Eigentümer: „Nur Figuren jetzt“, Gegenstände und Orte → V.39 (Landeplatz 9.15). Reaktiv-Quote 0 / 10 (ADR-085–094). 9.5 auf `[IN ARBEIT]`, als Nächstes Mockup.

### 2026-10-21 – [SESSIONSTART] 9.5 Bilder vom Bedarf her; Karte aus den Orten

- **Modell:** Opus 5.5 (`claude-opus-5-5`, laut `get_session`), Entscheidungs-Klasse. 9.5 empfiehlt Entscheidung – kein Schritt oberhalb der Empfehlung.
- **Umgebung:** Mac-Session (fortgesetzt seit 2026-10-11, „LocalDev (fork)“), `main` auf `2586ef8`, eingespielt `2586ef8`.
- **Wiedereinstieg:** Mindest-Lektüre nachgeholt (Projektkontext ganz, Logbuch ab `[SESSIONENDE]` 2026-10-19 02:00, Fahrplan „Aktueller Stand“ und Phase 9, Architektur 1/2/9, Entscheidungen Teil A und C, aktive Blocker): kein aktiver Schritt, keine aktiven Blocker, keine offenen STOPP-Situationen, Reaktiv-Quote 0 / 10. Die Cloud-Session zu 9.4 hat keinen `[SESSIONENDE]` geschrieben.
- **Kontextgröße:** über der Grenze von 200.000 Token (fortgesetzte Session); Weiterarbeit nach dauerhaftem „weiter hier“ des Eigentümers (Gedächtnis, 2026-09-28) – vermerkt nach `CLAUDE.md` Abschnitt 0.
- **Vorhaben:** 9.5 beginnt mit einer Vorlage (ändert die Vorbelegung aus ADR-084).

### 2026-10-21 – [BEOBACHTUNG] Deployment `2586ef8` (D.20 erledigt)

- Auf Anweisung des Eigentümers („einspielen“); vorher #183 (D.20) und #182 gemergt, CI auf `main` grün. Runbook Abschnitt 7 (ADR-039): `REVISION` `2586ef8`, Rückweg `skriptorium:vorher` = `67fc36e`; `/api/health` 200 nach ca. 63 s (über HTTPS), `/` 200, `/api/worlds` 401, `/sw.js` 200; einmal per SSH `(healthy)`, 0 Fehlerzeilen, im Container certifi 2026.10.19 → D.20 `[ERLEDIGT]`.

### 2026-10-21 – [ERLEDIGT] Abnahme 9.4

- Eigentümer zusätzlich: „Gastfiguren funktionieren auch“ – Eingangskriterium von 9.13 (Probe mit einer Gast-Figur) erfüllt.

- Eigentümer fand die Funktion zunächst nicht (der Block „Verweise hierher“ erscheint nur, wenn ein anderer Eintrag verweist); nach Anleitung: „9.4 funktioniert, der Block erscheint“ → 9.4 `[ERLEDIGT]`. Phase 9: 4 von 15. Nächster Schritt 9.5 mit Vorlage.
- Erklärt auf Nachfrage (ohne Änderung): D.1, D.5 (httpx2 auf PyPI nachgesehen: Fortführung von httpx durch das Pydantic-Team, 2.0 am 2026-05-12, heute 2.15.1 – keine neuen Funktionen fürs Skriptorium, Gewinn ist Pflege und Sicherheitsupdates), D.15.

### 2026-10-20 – [BEOBACHTUNG] Deployment `67fc36e` (8.9–9.4)

- In der fortgesetzten Mac-Session (`claude-opus-5-5`) auf Anweisung des Eigentümers („einspielen“), vorher „Pull from Main und prüfe offene PRs“: keine offenen PRs, `main` auf `67fc36e` (#181), CI grün. Auf dem Server lief `19a5e48`; seitdem 15 PRs (#165–#181). Geprüft vor dem Einspielen: keine Änderung an Dockerfile, Compose, `pyproject.toml` oder `package.json`; laut ADR-091 bis ADR-093 keine Umwandlung bestehender Dateien.
- Ablauf nach Runbook Abschnitt 7 (ADR-039): `REVISION` `67fc36e`, Rückweg `skriptorium:vorher` = `19a5e48`; `/api/health` 200 nach ca. 63 s (über HTTPS), `/` 200, `/api/worlds` 401, `/sw.js` 200; danach einmal per SSH `(healthy)`, 0 Fehlerzeilen in den letzten 3 Minuten.
- Offen: Bestätigung des Eigentümers zu 9.4 (Beziehungen mit Art und „Verweise hierher“). Diese Session hat keine Mindest-Lektüre und keinen `[SESSIONSTART]` neu angelegt – sie setzt die Session vom 2026-10-11 fort und hat nur eingespielt.

### 2026-10-21 – [GELÖST] Rote Audit-Jobs durch neue Sicherheitsfunde (D.20)

- Doku-PR #182 lief rot in „Python“ und „TypeScript“, beide im Schritt Dependency-Audit: `pip-audit` meldet PYSEC-2026-4320 für certifi 2026.7.22 (Korrektur 2026.10.19 vom 2026-10-20), `npm audit` drei Hinweise hoher Stufe zu launch-editor über vite 8.3.0–8.3.2. Nicht vom PR verursacht – blockiert jeden PR.
- Behoben als neuer Querschnitt-Schritt D.20 (Routine, Updates innerhalb der Linie): certifi über `uv lock --upgrade-package certifi`, vite auf 8.3.4 nach Regel-001 (npm schlug 8.3.5 vom selben Tag vor). Beide Audits ohne Befund; pytest 932, vitest 492, Playwright 15, Build grün.
- certifi läuft im Betrieb mit (Zertifikate für TLS zu OpenRouter und Pwned Passwords) → nach dem Merge einspielen. vite betrifft nur Bau und Entwicklung.

### 2026-10-19 22:45 MESZ – [ADR-ANGELEGT] ADR-093 Beziehungen mit Art und Rückverweis (9.4)

- Vorlage mit vier Fragen vorgelegt (Schreibweise, Gegenseite, Weltenbauer, Auffüllung), Eigentümer wählte per Auswahlfragen jeweils die Empfehlung: Zeile `- verheiratet mit @Kael` im Abschnitt „Beziehungen“; Block „Verweise hierher“ berechnet in der Oberfläche; Weltenbauer schreibt beide Seiten; Anfrage beim Schreiben unverändert (keine Probe nach Regel-002). Reaktiv-Quote 0 / 10 (ADR-084–093). 9.4 auf `[IN ARBEIT]`.

### 2026-10-19 22:28 MESZ – [SESSIONSTART] 9.4 Beziehungen mit Art und Rückverweis

- **Modell:** Opus 5.5 (`claude-opus-5-5`, eingestellt und bedient laut `get_session`), Entscheidungs-Klasse. 9.4 empfiehlt Entscheidung – kein Schritt oberhalb der Empfehlung.
- **Umgebung:** Cloud-Session (Umgebung `env_01E4xYkAExv13rZdZH7cdo1B`), Branch des Werkzeugs `claude/new-session-7c9ptj` auf `416f706` (= `origin/main`, PR #180).
- **Wiedereinstieg:** letzter `[SESSIONENDE]` 2026-10-19 02:00 – 9.3 erledigt, kein aktiver Schritt, keine aktiven Blocker, keine offenen STOPP-Situationen. Die dort als offen genannten Branches (`feat/9.3-gegliederte-eintraege`, `scp/affectionate-pare-f0afee`, `spike/9.3-proben-ki`, `scp/wizardly-ride-p7n55n`) bestehen auf `origin` nicht mehr – nur `main` und der Branch dieser Session.
- **Kontextgröße:** `get_session` meldet `used_tokens` 0 (Wert beim Start noch nicht gefüllt); Prüfung nach jedem Schritt erneut.
- **Vorhaben:** 9.4 beginnt mit einer Vorlage (Datenmodell-Konvention, Kategorie 4; ggf. Kategorie 1). D.19 am ersten CI-Lauf dieser Session prüfen (erster Lauf ab 2026-10-19 UTC).

### 2026-10-19 02:00 MESZ – [SESSIONENDE] 9.3 erledigt, 9.4 in neuer Session

- **Dauer:** ca. 01:50 bis 02:00 MESZ (Fortsetzung der Cloud-Session des zweiten Versuchs mit der Übergabe aus dem dritten).
- **Bearbeitet:** 9.3 abgeschlossen – Pflichtlektüre (Änderungen seit `1371264`), Titel und Beschreibung von PR #179 berichtigt („spike(9.3): Proben mit echter KI – Regel-002 und Weltenbauer“, Deutsch, „-2“ als Nachlauf erklärt), CI-Protokolle von #179 gelesen, #179 auf Anweisung zusammengeführt (`273813d`), 9.3 auf `[ERLEDIGT]` (Fahrplan-Schritt, Übersicht, „Aktueller Stand“), README „3 von 15“, FR-002 und FR-029 nachgetragen; Beobachtung bei D.19. Abschluss-PR von `scp/wizardly-ride-p7n55n`; der Eigentümer hat das Zusammenführen nach grüner CI vorab freigegeben.
- **Stand:** Phase 9, 3 von 15; kein aktiver Schritt. Keine offenen STOPP-Situationen, keine aktiven Blocker.
- **Offen:** Branches `feat/9.3-gegliederte-eintraege`, `scp/affectionate-pare-f0afee`, `spike/9.3-proben-ki`, `scp/wizardly-ride-p7n55n` – Löschen erfragt, keine Auswahl getroffen, daher nicht gelöscht. D.19 offen (siehe dort).
- **Nächster Schritt:** 9.4 Beziehungen mit Art und Rückverweis in einer neuen Session – zu Beginn Vorlage (Entscheidungs-Klasse); dabei D.19 am ersten CI-Lauf ab dem 2026-10-19 (UTC) prüfen.
- **Modell-Bilanz:** Entscheidungs-Klasse (Opus 5.5, eingestellt und bedient laut `get_session` um 01:49 und 01:55). 9.3 empfiehlt Entscheidung – 0 Schritte oberhalb der Empfehlung; die Abschlussarbeit selbst (Status, Logbuch, README) ist Routine-Arbeit, wegen kleinen Umfangs und geladenen Kontexts nicht abgegeben.
- **Kontextgröße:** mindestens 348.610 Token (`get_session`, Wert seit 01:49 unverändert gemeldet) – über der Grenze von 200.000; deshalb kein neuer Schritt in dieser Session (Abschnitt 0, „Sessiongröße“).
- **Sessionende-Prüfungen:** README synchron (3 von 15, 9.3 ✅, 0 Blocker, „Nächste Schritte“ ab 9.4). Drift: Übersicht im Fahrplan nannte „1 von 15“ (seit 9.2 veraltet) – auf „3 von 15“ berichtigt; ADR-092 → 9.3, 9.4, 9.5 vorhanden; Modulnamen unverändert; FR-002 und FR-029 erledigt mit Verweis auf 9.3; keine `[BLOCKIERT]`-Schritte, keine aktiven Blocker; Reaktiv-Quote 0 / 10 (ADR-083–092, keine neuen ADRs); Phase 9 mit 15 Schritten (Schwelle 30). Ablaufdaten-Register: Ubuntu 26 ab 2026-10-19 hat seinen Schritt (D.19); sonst kein Vorlauf erreicht (D.1 ab 2026-11-05, mypy 2 am 2026-11-06). Archiv: Logbuch ca. 445 Zeilen, project-context 349 Zeilen – kein Trigger. Keine Phasengrenze. Quick-Start nicht berührt.

### 2026-10-19 01:58 MESZ – [ERLEDIGT] 9.3 Gegliederte Einträge je Art

- **Definition of Done:** Code und Tests in PR #177 (CI grün, 4 von 4 Pflicht-Checks; zusammengeführt `5878215`; lokal pytest 931 mit 99,85 %, vitest 485, Playwright 15/15); Proben mit echter KI in PR #179 (CI grün, 4 von 4: pytest 931 / 99,85 %, vitest 485 / 98,67 – 95,24 – 97,88 – 98,86 %, Playwright 15/15, Pre-Commit alle Hooks; keine Warnung über dem Bestand, kein Hinweis der Plattform, keine Bündelgrößen-Warnung; auf Anweisung zusammengeführt `273813d`); CHANGELOG-Eintrag vorhanden; Bestätigung des Eigentümers 2026-10-19.
- **Ergebnisse der Proben:** Regel-002 über je 6 Ketten ohne Wirkung und ohne Verschlechterung; Weltenbauer gliedert in allen vier Arten, Import ganz, zwei knappe Kanon-Abweichungen ohne Bezug zur Gliederung; Kosten 5,88 $ (Einzelheiten in den READMEs unter `spikes/regel-002/` und `spikes/weltenbauer-9.3/`).
- **Nachgezogen:** Fahrplan (Schritt, Übersicht, „Aktueller Stand“), README „3 von 15“, FR-002 und FR-029 in `docs/requirements.md`. Reifegrad-Wirkung keine.
- **D.19 (Beobachtung):** alle vier Jobs zu #179 noch auf `ubuntu-24.04` (24.04.5, Abbild 20261012.334.1) – der Lauf war um 23:44 UTC am 2026-10-18, vor dem Beginn der Umstellung.

### 2026-10-19 01:50 MESZ – [SESSIONSTART] Abschluss von 9.3 nach den Proben

- **Modell:** Opus 5.5 (`claude-opus-5-5`, eingestellt und bedient laut `get_session`), Entscheidungs-Klasse. 9.3 empfiehlt Entscheidung – kein Schritt oberhalb der Empfehlung.
- **Umgebung:** dieselbe Cloud-Session wie der zweite Versuch (Umgebung „Flight_Research“, Branch des Werkzeugs `scp/wizardly-ride-p7n55n`), fortgesetzt mit der Übergabe aus der Session „Proben 9.3 (3. Versuch)“. Branch per Fast-Forward auf `spike/9.3-proben-ki` (`a1d5b6b`) gebracht, keine Historie umgeschrieben.
- **Wiedereinstieg:** PR #177 in `main` zusammengeführt (`5878215`); PR #179 (`spike/9.3-proben-ki` → `main`, nur `spikes/` und Doku) offen, alle vier Pflicht-Checks grün (23:44–23:45 UTC); 9.3 vom Eigentümer bestätigt. PR #178 auf Anweisung geschlossen (Commits in #179 enthalten). `project-context`, `architecture`, `decisions`, `blockers` unverändert gegenüber `1371264`. Keine aktiven Blocker, keine offenen STOPP-Situationen.
- **Kontextgröße:** 348.610 Token (`get_session`) – über der Grenze von 200.000. Nach `CLAUDE.md` Abschnitt 0 („Sessiongröße“) beginnt diese Session keinen neuen Schritt: Sie schließt nur den laufenden Schritt 9.3 ab (PR #179, `[ERLEDIGT]`, Branches nach Rückfrage); D.19 hier nur als Beobachtung aus der CI von #179; 9.4 in einer neuen Session, außer der Eigentümer sagt ausdrücklich „weiter hier“.
- **Berichtigung der Zeiten des zweiten Versuchs:** Laut `get_session` begann diese Session um 00:06 MESZ, die Session des dritten Versuchs um 00:19 MESZ. Die Uhrzeiten 00:12 und 00:30 in den Einträgen des zweiten Versuchs waren geschätzt und zu spät; der zweite Versuch endete gegen 00:18 MESZ. Das erklärt die Abweichung, die der dritte Versuch in seinem `[SESSIONSTART]` vermerkt hat.

### 2026-10-19 – [BEOBACHTUNG] Eigentümer bestätigt 9.3

- Im Chat: „9.3 bestätigt“ – nach Weltenbauer-Probe und Probe nach Regel-002 mit Nachlauf (keine Verschlechterung). Akzeptanzkriterium „Eigentümer bestätigt“ erfüllt. 9.3 bleibt `[IN ARBEIT]`, bis die lokale Session `spike/9.3-proben-ki` übernommen, PR #177 mit grüner CI zusammengeführt und den Schritt auf `[ERLEDIGT]` gesetzt hat.

### 2026-10-19 01:15 MESZ – [SESSIONENDE] Nachlauf zu 9.3: Befund war Streuung

- **Dauer:** Fortsetzung nach dem `[SESSIONENDE]` von 00:45 MESZ, ca. 00:50 bis 01:15 MESZ (nach Neustart des Arbeitsprozesses; Schlüssel, Branch und Worktree erneut geprüft).
- **Bearbeitet:** 9.3 – Eigentümer wählte per Auswahlfrage „3 weitere Läufe je Seite (Empfohlen)“; Nachlauf (`76d0ea2`), zweite verblindete Bewertung, Auswertung über je 6 Ketten; Spike-README, Fahrplan, README nachgezogen.
- **Stand:** Phase 9, 2 von 15; 9.3 🟠 – beide Proben abgeschlossen, keine Verschlechterung; offen nur die Bestätigung des Eigentümers, danach Zusammenführen durch die lokale Session (Branch `spike/9.3-proben-ki`, PR #177). Keine aktiven Blocker, keine offenen STOPP-Situationen.
- **Kosten bei OpenRouter (Session gesamt):** 2,98 $ + 2,91 $ (Nachlauf: 1,472 $ + 1,433 $) = 5,88 $.
- **Modell-Bilanz:** Entscheidungs-Klasse (Opus 5.5), 0 Schritte oberhalb der Empfehlung; abgegeben an Unteragenten der Routine-Klasse (Sonnet): vier verblindete Bewertungen (je ca. 2–3 min), Funde nachgeprüft.
- **Kontextgröße:** nicht feststellbar; Regel entfiel.
- **Sessionende-Prüfungen:** README-Zeile 9.3 nachgezogen; sonst wie im Eintrag 00:45 (keine neuen ADRs, Schritt-IDs, Module, Blocker; kein Vorlauf im Ablaufdaten-Register erreicht; Logbuch unter 420 Zeilen).

### 2026-10-19 01:10 MESZ – [BEOBACHTUNG] Nachlauf nach Regel-002 zu 9.3: keine Wirkung über je 6 Ketten

- **Aufbau:** wie der erste Lauf, je 3 weitere Ketten (`vorher-9.3-2`, `nachher-9.3-2`), 84 Vorschläge, alle `stop`.
- **Ergebnis über je 6 Ketten:** keine Kennzahl nachher in beiden Geschichten außerhalb der Vorher-Spannweite – auch nicht die von Hand bewerteten Widersprüche: Salzmark vorher 0 / nachher 1, Glimmergrund vorher 1 (`vorher-9.3-2/lauf-3`: „Dreizehn“ statt zwölf geborgener Toter) / nachher 1. Nur in einer Geschichte außerhalb: Salzmark ein echtes Warte-Ende (`nachher-9.3-2/lauf-2`, Schritt 6) und der Widerspruch, Glimmergrund 6er doppelt 0,50 (innerhalb 5.24). Der Befund aus drei Läufen war Streuung – wie bei 8.11.

### 2026-10-19 00:45 MESZ – [SESSIONENDE] Proben zu 9.3 gelaufen und ausgewertet

- **Dauer:** ca. 00:20 bis 00:45 MESZ (Cloud-Session, dritter Versuch).
- **Bearbeitet:** 9.3 – Schlüssel geprüft (gesetzt), Ausgangs-Commit `40a02eb`; Weltenbauer-Probe (4 Aufträge) und Probe nach Regel-002 (12 Ketten, vorher im Worktree `2ac204b`) gelaufen, ausgewertet, verblindete Widerspruchs-Bewertung durch zwei getrennte Instanzen; README beider Spikes, Fahrplan-Notiz bei 9.3, „Aktueller Stand“, README-Zeile 9.3.
- **Stand:** Phase 9, 2 von 15; 9.3 🟠 – Proben gelaufen; offen: Entscheidung des Eigentümers zum Befund der Regel-002-Probe (Widersprüche nachher 1 von 3 Ketten je Geschichte, vorher 0) und seine Bestätigung; Zusammenführen durch die lokale Session. Keine aktiven Blocker, keine offenen STOPP-Situationen.
- **Nächster Schritt:** Eigentümer entscheidet über weitere Läufe; lokale Session übernimmt `spike/9.3-proben-ki`, dann PR #177 nach Bestätigung; danach 9.4.
- **Kosten bei OpenRouter:** 0,045 $ (Weltenbauer) + 1,500 $ (vorher) + 1,438 $ (nachher) = 2,98 $.
- **Modell-Bilanz:** Entscheidungs-Klasse (Opus 5.5 laut `get_session`, 00:20). 9.3 empfiehlt Entscheidung – 0 Schritte oberhalb der Empfehlung. Abgegeben an zwei Unteragenten der Routine-Klasse (Sonnet): verblindete Widerspruchs-Bewertung je Geschichte (je ca. 2–3 min); Ergebnisse an Text und Kanon nachgeprüft.
- **Kontextgröße:** nicht feststellbar (`used_tokens` 0); Regel entfiel.
- **Sessionende-Prüfungen:** README: Zeile 9.3 nachgezogen, Fortschritt 2 von 15 und 0 Blocker unverändert. Drift: keine neuen ADRs, Schritt-IDs oder Module; Reaktiv-Quote unverändert; keine `[BLOCKIERT]`-Schritte; Phase 9 mit 15 Schritten. Ablaufdaten-Register: kein Vorlauf erreicht, keine CI gelaufen. Archiv: Logbuch unter 400 Zeilen. Quick-Start nicht berührt. Worktree `../vorher` liegt außerhalb des Klons und verfällt mit dem Container.

### 2026-10-19 00:40 MESZ – [BEOBACHTUNG] Probe nach Regel-002 zu 9.3: gezählt keine Wirkung, ein Befund bei den Widersprüchen

- **Aufbau:** grok-4.6, mittel, je 3 Ketten an Salzmark und Glimmergrund; vorher `2ac204b` (Worktree, eigener Code geprüft: `skriptorium.__file__` im Worktree), nachher `40a02eb`; 84 Vorschläge, alle `stop`, keine Fehler; Ergebnisse `spikes/regel-002/ergebnisse/vorher-9.3/`, `nachher-9.3/`, Bewertung `9.3-bewertung/`.
- **Gezählt:** einzig „wörtlich %“ in beiden Geschichten außerhalb der Vorher-Spannweite, gegenläufig (Salzmark 0,40 gegen 0,44–0,76; Glimmergrund 0,71 gegen 0,00–0,39) – keine Wirkung. Glimmergrund 0,71 ist der höchste bisher gemessene Mittelwert dieser Geschichte.
- **Widersprüche (verblindet, Sonnet):** nachher je ein eindeutiger (Salzmark `lauf-2` Schritt 5: „Heddas Kind“ am Abend; Glimmergrund `lauf-3` Schritt 6: „mein Teuerster“ zu Wendt), vorher keiner; 12 Kanon-Proben in Glimmergrund überall ohne Widerspruch. Nach dem Wortlaut von Regel-002 ein Befund; Rate wie grok-4.6 in 5.26; beide Einzelheiten stehen in beiden Ständen im Wortlaut in der Anfrage (ohne KI nachgebaut).

### 2026-10-19 00:30 MESZ – [GELÖST] markdownlint prüft Rohantworten unter `spikes/`

- **Problem:** Der Commit des Logbuchs scheiterte am Pre-Commit: `markdownlint-cli2` meldete 8 Fehler in `spikes/weltenbauer-9.3/ergebnisse/*.md` (MD041, MD047). Der erste Commit mit den Antworten (`3970465`) war durchgegangen, weil Pre-Commit `spikes/` per `exclude` auslässt – markdownlint selbst sucht aber mit `**/*.md` im ganzen Repo, sobald irgendeine `.md`-Datei geändert ist.
- **Lösung:** Rohantworten als `.txt` abgelegt (wie die Texte unter `spikes/regel-002/ergebnisse/`), `probe.py` und README nachgezogen (`8f64fc9`); `PRUEFEN=1` liefert dieselbe Tabelle.

### 2026-10-19 00:27 MESZ – [BEOBACHTUNG] Weltenbauer-Probe zu 9.3 mit echter KI

- **Ergebnis:** vier Aufträge (Figur, Ort, Gegenstand, Kultur), grok-4.6, alle `stop`, 0,045 $. (a), (b), (d) maschinell in allen vier erfüllt: Abschnitte der Art vollständig in Reihenfolge auf Ebene 3, kein Füllwerk, Import ganz, keine Ebenen-Korrektur nötig.
- **(c) von Hand:** Ort erkennt die Falle im Auftrag (Rehl ist ehemaliger Zöllner); knapp: Haken für den Siegelring im Zollhaus (Drach trägt ihn stets – Text des Rings nicht in der Anfrage); Figur „meidet den Südhafen“, obwohl der Nordkai dazugehört. Gegenstand und Kultur ohne Widerspruch. Einzelheiten `spikes/weltenbauer-9.3/README.md`.

### 2026-10-19 00:20 MESZ – [SESSIONSTART] Proben zu 9.3 (dritter Versuch): Regel-002 und Weltenbauer

- **Modell:** Opus 5.5 (`claude-opus-5-5`, eingestellt und bedient laut `get_session`), Entscheidungs-Klasse. 9.3 empfiehlt Entscheidung – kein Schritt oberhalb der Empfehlung.
- **Umgebung:** Cloud-Session in der Umgebung „OPENROUTER_API_KEY“; `OPENROUTER_API_KEY` **gesetzt** (nur Vorhandensein geprüft). Ausgangs-Commit `40a02eb` (Branch `scp/wizardly-ride-p7n55n`); `git diff --stat 1371264 HEAD -- src ui tests` leer, `canon/sections.py` enthält „Fähigkeiten“. Das Werkzeug hat der Session `scp/wizardly-ride-p7n55n` zugewiesen, auf den nicht gepusht werden soll – deshalb eigener Branch `spike/9.3-proben-ki` (Konvention aus `docs/project-context.md` Abschnitt 10).
- **Zeit:** Die Uhr der Session zeigt 00:20 MESZ; die Einträge der Vorsession tragen 00:07–00:30 MESZ desselben Tages – deren Zeitangaben stimmen offenbar nicht mit dieser Uhr überein (Reihenfolge der Einträge gilt).
- **Wiedereinstieg:** Phase 9, 2 von 15; 9.3 🟠 umgesetzt (PR #177), offen: Probe nach Regel-002 und Weltenbauer-Probe in der Salzmark, beide vom Eigentümer freigegeben. Keine aktiven Blocker, keine offenen STOPP-Situationen.
- **Kontextgröße:** `get_session` meldet `used_tokens` 0 – nicht verlässlich feststellbar, Regel „Sessiongröße“ entfällt.

### 2026-10-19 00:30 MESZ – [SESSIONENDE] Proben zu 9.3 nicht gelaufen (kein Schlüssel), Weltenbauer-Probe vorbereitet

- **Dauer:** ca. 00:07 bis 00:30 MESZ (Cloud-Session).
- **Bearbeitet:** 9.3 – Stand geprüft (Start auf `1371264`, „Fähigkeiten“ in `canon/sections.py`), Schlüssel fehlt (Eintrag 00:12). Ohne KI vorbereitet: `spikes/weltenbauer-9.3/probe.py` und README (vier Aufträge mit `@`-Verweisen, maschinelle Prüfung (a), (b), (d), Trockenlauf, Selbsttest der Prüflogik mit sechs konstruierten Antworten im Scratchpad); Vorher-Worktree auf `2ac204b` geprüft (eigener Code, Anfrage ändert sich wie erwartet: Salzmark 38 → 9 Überschriften der Ebene 1, Glimmergrund 36 → 13). Notiz bei 9.3 und „Aktueller Stand“ im Fahrplan.
- **Stand:** Phase 9, 2 von 15; 9.3 🟠 umgesetzt, PR #177 offen; beide Proben weiterhin offen, Bestätigung des Eigentümers offen. Keine offenen STOPP-Situationen, keine aktiven Blocker (fehlender Schlüssel ist eine Frage der gewählten Umgebung, kein Blocker nach Abschnitt 10).
- **Nächster Schritt:** Cloud-Session in der Umgebung „OPENROUTER_API_KEY“ vom Branch `scp/wizardly-ride-p7n55n`; zuerst Schlüssel prüfen, dann Regel-002 (vorher `2ac204b` im Worktree, nachher Stand des Branches – `src/` gleich `1371264`) und `uv run python spikes/weltenbauer-9.3/probe.py`, auswerten (c von Hand), festhalten.
- **Modell-Bilanz:** Entscheidungs-Klasse (Opus 5.5, eingestellt und bedient laut `get_session` um 00:07 und 00:29). 9.3 empfiehlt Entscheidung – 0 Schritte oberhalb der Empfehlung; nichts an Unteragenten abgegeben (Werkzeug klein, Kontext schon geladen).
- **Kontextgröße:** nicht feststellbar – `get_session` meldet `used_tokens` 0; Regel „Sessiongröße“ entfiel (vermerkt im `[SESSIONSTART]`).
- **Sessionende-Prüfungen:** README synchron (2 von 15, 9.3 „Proben mit echter KI offen“, 0 Blocker) – keine Änderung. Drift: keine neuen ADRs, Schritt-IDs oder Module; Reaktiv-Quote unverändert 0 / 10; keine `[BLOCKIERT]`-Schritte; Phase 9 mit 15 Schritten. Ablaufdaten-Register: kein Vorlauf erreicht (D.19 greift ab dem ersten CI-Lauf nach dem 2026-10-19 – in dieser Session lief keine CI). Archiv: Logbuch ca. 370 Zeilen, kein Trigger. Quick-Start nicht berührt.

### 2026-10-19 00:12 MESZ – [BEOBACHTUNG] Zweiter Versuch der Proben zu 9.3: Cloud-Session in der falschen Umgebung, kein Schlüssel

- **Befund:** `OPENROUTER_API_KEY` ist in dieser Cloud-Session nicht gesetzt (nur Vorhandensein geprüft). Auch keine andere Variable mit „openrouter“ im Namen, keine Datei im Home-Verzeichnis; `https://openrouter.ai/api/v1/key` antwortet ohne Schlüssel mit 401, der Proxy fügt also nichts ein.
- **Ursache:** Die Session läuft laut `get_session` in der Cloud-Umgebung „Flight_Research“ (dort ist nur ein Zugang für einen fremden Dienst hinterlegt). Laut `list_environments` gibt es eine eigene Umgebung „OPENROUTER_API_KEY“ – vermutlich die mit dem Schlüssel. Der erste Versuch scheiterte am fehlenden Branch auf GitHub, dieser an der Umgebung.
- **Folge:** Keine der beiden Proben ist gelaufen; keine Kosten bei OpenRouter. Stand unverändert: Branch `scp/affectionate-pare-f0afee` = `1371264` ist korrekt, `canon/sections.py` enthält „Fähigkeiten“, `2ac204b` (Vorher-Stand) ist im Klon vorhanden.
- **Für den nächsten Versuch:** Cloud-Session in der Umgebung „OPENROUTER_API_KEY“ starten und zuerst prüfen, ob `OPENROUTER_API_KEY` gesetzt ist (nur gesetzt/nicht gesetzt), bevor irgendetwas anderes läuft.

### 2026-10-19 00:07 MESZ – [SESSIONSTART] Proben zu 9.3 (zweiter Versuch): Regel-002 und Weltenbauer

- **Modell:** Opus 5.5 (`claude-opus-5-5`, eingestellt und bedient laut `get_session`), Entscheidungs-Klasse; Aufwand „xhigh“. 9.3 empfiehlt Entscheidung – kein Schritt oberhalb der Empfehlung.
- **Umgebung:** Cloud-Session (Linux), gestartet vom Branch `scp/affectionate-pare-f0afee` (`1371264`, gleich `feat/9.3-gegliederte-eintraege`, PR #177 offen); eigener Branch des Werkzeugs `scp/wizardly-ride-p7n55n`, zweigt von `1371264` ab. Pre-Commit-Hook über den SessionStart-Hook eingerichtet.
- **Wiedereinstieg:** Phase 9, 2 von 15; 9.3 🟠 umgesetzt, offen: Probe nach Regel-002 (vorher `2ac204b`, nachher `1371264`, je 3 Läufe an Salzmark und Glimmergrund, grok-4.6, mittel) und Weltenbauer-Probe in der Salzmark (Figur, Ort, Gegenstand, Kultur); Eigentümer hat beide freigegeben. Keine aktiven Blocker, keine offenen STOPP-Situationen, Reaktiv-Quote 0 / 10.
- **Kontextgröße:** `get_session` meldet `context_usage.used_tokens` 0 (vermutlich noch nicht aktualisiert); Größe damit nicht verlässlich feststellbar, Regel „Sessiongröße“ entfällt für diese Session.
- **Auftrag:** beide Proben ausführen, auswerten und festhalten; Commits nur auf `scp/wizardly-ride-p7n55n`, kein Pull Request, nichts zusammenführen.

### 2026-10-18 23:40 MESZ – [SESSIONENDE] 9.3 entschieden und lokal umgesetzt, Proben offen

- **Dauer:** Fortsetzung nach dem `[SESSIONENDE]` von 22:10 MESZ: 9.2 zusammengeführt (PR #175, #176), dann auf „weiter“ 9.3 bis 23:40 MESZ.
- **Bearbeitet:** 9.2 abgeschlossen (CI grün, `65a0f13`, Abschluss `2ac204b`). 9.3: Mockup vorher/nachher, Entscheidung per Auswahlfragen → ADR-092, Umsetzung (Unteragent, geprüft und nachgebessert), V.38 angelegt. Commits lokal auf `feat/9.3-gegliederte-eintraege` (`1529ac3` … `a409878`), nicht hochgeladen.
- **Stand:** Phase 9, 2 von 15 erledigt; 9.3 🟠 umgesetzt, offen: Probe nach Regel-002 und Probe des Weltenbauers mit echter KI (Cloud-Session; Plan in den Notizen von 9.3), Bestätigung des Eigentümers. Keine offenen STOPP-Situationen, keine aktiven Blocker.
- **Nächster Schritt:** Branch hochladen und Pull Request nach Freigabe; die Proben in einer Cloud-Session vom Branch; danach Bestätigung und Zusammenführen. Dann 9.4 (Beziehungen, baut auf dem Abschnitt „Beziehungen“).
- **Modell-Bilanz:** Entscheidungs-Klasse (Opus 5.5, laut `get_session`; Abfrage um 22:09, seither kein Modellwechsel gemeldet). 9.3 empfiehlt Entscheidung – 0 Schritte oberhalb der Empfehlung in diesem Teil. Abgegeben an Unteragenten der Routine-Klasse (Sonnet): Mockup (ca. 5 min, 37 Aufrufe) und Umsetzung (ca. 14 min, 72 Aufrufe); Vorlage, ADR, Prüfung, Nachbesserung des Imports, Doku und Commits hier.
- **Kontextgröße:** 509.699 Token (`get_usage`), über der Grenze von 200.000; weitergearbeitet nach dem dauerhaften „weiter hier“ des Eigentümers (Abweichung nach `CLAUDE.md` Abschnitt 0, „Sessiongröße“).
- **Sessionende-Prüfungen:** README synchron (Fortschritt 2 von 15; „Nächste Schritte“ 9.3 umgesetzt, Proben offen). Drift: ADR-092 verweist auf 9.3, 9.4, 9.5 – vorhanden; V.38 mit Landeplatz 9.15, in 9.15 und der Übersicht genannt; `docs/architecture.md` Abschnitte 7–9 auf Stand ADR-092; Modulnamen unverändert; FR-002, FR-029 unverändert erledigt (9.3 noch offen); keine aktiven Blocker und keine `[BLOCKIERT]`-Schritte; Reaktiv-Quote 0/10 (ADR-083–092); Phase 9 mit 15 Schritten (Schwelle 30). Ablaufdaten-Register: kein Vorlauf erreicht (D.1 ab 2026-11-05, mypy 2 am 2026-11-06; D.19 ab dem ersten CI-Lauf nach dem 2026-10-19). Archiv: Logbuch ca. 340 Zeilen, project-context 349 Zeilen – kein Trigger. Keine Phasengrenze. Quick-Start nicht berührt.

### 2026-10-18 – [BEOBACHTUNG] 9.3 lokal umgesetzt; Messung der Anfrage an den Testwelten

- Umsetzung von ADR-092 durch einen Unteragenten der Routine-Klasse (Sonnet, ca. 14 min, 72 Werkzeugaufrufe), geprüft von der bauenden KI. Lokal grün: pytest 931 (99,85 %; canon 100 %, context 99 %), vitest 485 (98,67 / 95,29 / 97,88 / 98,86 %), Playwright 15/15, ruff, mypy, bandit, eslint, prettier, tsc. Bildschirmfotos des echten Formulars (Desktop, Smartphone; Figur und Wechsel auf Ort) entsprechen dem Mockup.
- Messung `render` alt gegen neu an den 52 Einträgen von Salzmark und Glimmergrund: alle 52 ändern sich, weil ihr Text mit `# Name` beginnt (wird `### Name`); +104 Zeichen gesamt; keine leeren Abschnitte, nichts erreicht Ebene 6. Die Anfrage beim Schreiben ändert sich also in beiden Testgeschichten – die Probe nach Regel-002 misst genau das.
- Vertragsdatei: Gegenstand und Kultur bekommen die neue Vorlage; geschätzte Token beim Schreiben 1.477 → 1.450 (leere Abschnitte fallen weg), beim Weltenbauer 816 → 994 (längerer Rahmen, ca. +180 Token je Antwort).
- Befund SillyTavern-Export: trennt „Wesen“ an der wörtlichen Zeile `### Wesen` (Abweichung von Regel-003); mit der neuen Vorlage (`## Wesen`) bleibt `personality` leer → V.38, Landeplatz 9.15.

### 2026-10-18 – [GELÖST] Import zerlegte eine Figur mit eigenem Zusatz-Abschnitt

- Bericht des Unteragenten: Eine Überschrift ohne eigenen Text galt nur dann als Eintrag, wenn alle Unterüberschriften feste Abschnitte waren; eine Figur des Weltenbauers mit „Aussehen“, „Wesen“ und einem eigenen „Herkunft“ wäre in der Import-Vorschau in mehrere Einträge zerfallen – mit 9.3 wahrscheinlicher. Nachgebessert von der bauenden KI: Bei bekannter Art reicht ein fester Abschnitt dieser Art (`_holds_item_sections`); bei unbekannter Art bleibt die strenge Regel. Zwei Tests ergänzt.

### 2026-10-18 – [ADR-ANGELEGT] ADR-092 Feste Abschnitte je Art (9.3)

- Mockup vorher/nachher (Formular „Neuer Eintrag“, Figur Anselm Drach, Ort Aschturm; Testwelt Salzmark, Desktop und Smartphone, vom Unteragenten gebaut) und vier Auswahlfragen. Eigentümer: A (Vorlage im Formular, Weltenbauer, Import; Bestand bleibt), Figur mit „Fähigkeiten“ (Aussehen · Wesen · Fähigkeiten · Geschichte · Beziehungen), übrige Arten wie vorgeschlagen, Abschnitte in der KI-Anfrage unter dem Namen mit Probe nach Regel-002. `[OPERATIV]`, in 9.3 als Vorlage vorgesehen – nicht reaktiv; Reaktiv-Quote 0/10 (ADR-083–092). Auf der Entscheidungs-Klasse vorgelegt (Opus 5.5).
- Befund beim Lesen: In der Anfrage an die KI steht ein von Hand angelegtes `## Aussehen` auf derselben Ebene wie `## Kael (Figur)`; aus dem Weltenbauer übernommene Einträge haben `### Aussehen`. Mit mehr Abschnitten je Eintrag wäre die Zuordnung für die KI unsicher – deshalb Teil von ADR-092.

### 2026-10-18 – [BEOBACHTUNG] 9.3 in derselben Session begonnen

- Auf „weiter“ des Eigentümers nach dem Abschluss von 9.2 beginnt 9.3 in dieser Session, obwohl die Kontextgröße über 200.000 Token liegt (Abweichung von `CLAUDE.md` Abschnitt 0, „Sessiongröße“, nach dem dauerhaften „weiter hier“ des Eigentümers). Modell weiter Opus 5.5, Entscheidungs-Klasse – 9.3 empfiehlt Entscheidung, keine Arbeit oberhalb der Empfehlung. Branch `feat/9.3-gegliederte-eintraege` von `main` `2ac204b`. Zuerst Vorlage mit Mockup (Kategorien 1 und 4); das Mockup baut ein Unteragent der Routine-Klasse.

### 2026-10-18 – [ERLEDIGT] 9.2 End-to-End-Tests für die Abläufe der Phasen 6–8

- PR #175, CI grün (4 von 4; End-to-End 1 min 18 s), auf Anweisung des Eigentümers („merge“) zusammengeführt (`65a0f13`). Im CI-Protokoll nur der bekannte Hinweis „ubuntu-latest → Ubuntu 26 ab 2026-10-19“ (D.19, Lauf noch vor dem Stichtag), keine Bündelgrößen-Warnung. Auto-fix für #175 auf Wunsch des Eigentümers eingeschaltet, nicht gebraucht. Lokal zuvor: Playwright 15/15, pytest 887 (99,85 %), vitest 467 (98,66 / 95,3 / 97,87 / 98,85 %). Phase 9: 2 von 15 erledigt; nächster Schritt 9.3 (Vorlage mit Mockup, Entscheidungs-Klasse) – in einer neuen Session.
- `gh pr merge --delete-branch` brach beim Wechsel auf das lokale `main` ab (im Haupt-Checkout belegt); der entfernte Branch blieb stehen und wurde von Hand gelöscht. Merken: aus einem Worktree heraus den entfernten Branch nach dem Merge prüfen.

### 2026-10-18 22:10 MESZ – [SESSIONENDE] 9.2 lokal fertig, Pull Request nach Freigabe

- **Dauer:** 2026-10-18 21:48 bis 22:10 MESZ; Neben-Session, gestartet aus der Session des Eigentümers mit dem Auftrag 9.2.
- **Bearbeitet:** 9.2 – vier Playwright-Tests, Vertragstest Server ↔ Oberfläche, Typ `DescribeEvent` berichtigt, CI-Schrittnamen auf die geltenden Schwellen (ADR-090). Commits lokal auf `feat/9.2-e2e-ablaeufe`, nicht hochgeladen.
- **Stand:** Phase 9, 1 von 15 erledigt; 9.2 🟠 lokal fertig, offen ist nur das Akzeptanzkriterium „grün in der CI“. Keine offenen STOPP-Situationen, keine aktiven Blocker.
- **Nächster Schritt:** Pull Request für `feat/9.2-e2e-ablaeufe` nach Freigabe des Eigentümers, CI grün → 9.2 erledigt, README-Fortschritt 2 von 15; fällt der Lauf auf oder nach den 2026-10-19, gleich D.19 mit prüfen. Danach 9.3 (Vorlage mit Mockup, Entscheidungs-Klasse).
- **Modell-Bilanz:** Entscheidungs-Klasse (Opus 5.5, `get_session` um 22:09 erneut abgefragt). 1 Schritt oberhalb der Empfehlung (9.2 empfiehlt Routine; Warnung zu Beginn ausgesprochen). Abgegeben an zwei Unteragenten der Routine-Klasse (Sonnet): Playwright-Tests (ca. 10 min, 51 Werkzeugaufrufe) und Vertragstest (ca. 12 min, 63 Werkzeugaufrufe); Prüfung, Typ-Berichtigung, Fake-Modellliste typisiert, Prüfkette, Doku und Commits hier.
- **Kontextgröße:** 315.539 Token (`get_usage`), über der Grenze von 200.000 – in dieser Session beginnt kein neuer Schritt.
- **Sessionende-Prüfungen:** README synchron („Nächste Schritte“: 9.2 lokal fertig; Fortschritt bleibt 1 von 15 bis zur grünen CI). Drift: kein neuer ADR; FR-029 und FR-035 nur Test-Spalte ergänzt, Status unverändert; Modulnamen unverändert; keine aktiven Blocker, keine `[BLOCKIERT]`-Schritte; Reaktiv-Quote 1/10 unverändert; Phase 9 mit 15 Schritten (Schwelle 30). Ablaufdaten-Register: kein Vorlauf erreicht; Zusatz an D.2 (Compiler-API in `ui/src/api/contract.test.ts`); D.19 ohne CI-Lauf in dieser Session. Archiv: Logbuch unter 300 Zeilen, project-context 349 Zeilen – kein Trigger. Keine Phasengrenze. Nicht Quick-Start-relevant (keine der Dateien aus `CLAUDE.md` Abschnitt 17); kein CHANGELOG-Eintrag (nur Tests und CI-Namen).

### 2026-10-18 – [BEOBACHTUNG] Vertragstest fand `web_search` im Start der Beschreibungen

- `tests/api/test_ui_contract.py` zeichnet 73 echte Antworten und Strom-Ereignisse auf; `ui/src/api/contract.test.ts` prüft sie mit der Compiler-API von `typescript` gegen die Typen in `ui/src/api/` (Gegenprobe: umbenanntes, zusätzliches, fehlendes Feld, Wert außerhalb einer Literal-Union, falscher Typ – jeweils genau die beschädigte Antwort gemeldet). Einziger Befund: Das `start`-Ereignis von „Bild/Karte beschreiben“ und „Aussehen herauslösen“ trägt `web_search`, weil der Server dafür `stream_answer` des Weltenbauers nutzt (`api/flows/worldbuilder.py`); `DescribeEvent` war der Start des Schreib-Stroms ohne das Feld. Zur Laufzeit harmlos. Berichtigt auf der Typseite (`DescribeEvent` aus `WorldbuilderEvent`) – den Server zu ändern wäre eine nicht-additive API-Änderung (Kategorie 5) gewesen.
- Merken: Ein Vertragstest mit aufgezeichneten Antworten prüft nur die Fälle, die die Daten zeigen; Varianten (null/gesetzt, Fehlerarten) sind deshalb einzeln aufgenommen.

### 2026-10-18 – [GELÖST] Reibungen beim Schreiben der Tests (9.2)

- Playwright: `getByLabel("Kategorie", { exact: true })` fand das Auswahlfeld nicht (30 s Wartezeit), weil der Beschriftungstext die Optionen mitzählt → `getByRole("combobox", { name: /^Kategorie/ })`. „Beschreiben lassen“ traf auch „✨ Von der KI beschreiben lassen“ → `exact: true`.
- Playwright: „Bild beschreiben“ braucht ein Modell, das Bilder liest; die Liste kommt sonst live von OpenRouter → in zwei Tests durch eine an `ModelList` typisierte Liste ersetzt, damit der Lauf nicht am Netz hängt.
- Playwright: Alle Tests eines Laufs teilen ein Datenverzeichnis; feste Weltnamen vertragen kein `--repeat-each` – Wiederholung als getrennte Läufe.
- Vertragstest: `ui/test-setup.ts` braucht jsdom (`Range`), also kein `@vitest-environment node`; Zufalls-Dateinamen standen auch in der Route und mussten dort ebenfalls ersetzt werden; eine Gast-Verbindung auf eine Figur der eigenen Welt gibt 422.
- Eigene Reibung: Ein Python-Heredoc mit Umlauten im Terminal brach mit „Non-UTF-8 code“ ab; Skripte für Doku-Ersetzungen mit vielen Umlauten als Datei im Scratchpad ablegen.

### 2026-10-18 21:48 MESZ – [SESSIONSTART] 9.2 End-to-End-Tests

- **Modell:** Opus 5.5 (`claude-opus-5-5`, laut `get_session`), Entscheidungs-Klasse; Aufwand „xhigh“. 9.2 empfiehlt Routine – Schritt läuft oberhalb der Empfehlung; das Schreiben der Tests (ausgabelastig) geht an einen Unteragenten der Routine-Klasse (Sonnet), Prüfung und Commit hier.
- **Umgebung:** Mac des Eigentümers (macOS arm64); Neben-Session, gestartet aus der Session des Eigentümers, eigener Worktree (`.claude/worktrees/affectionate-pare-f0afee`), Branch `feat/9.2-e2e-ablaeufe`; Pre-Commit-Hook über den SessionStart-Hook eingerichtet.
- **Stand:** vor der Mindest-Lektüre `git fetch` – `main` `993863d` gleich `origin/main`, kein Fast-Forward nötig.
- **Wiedereinstieg:** Phase 9, 1 von 15; nächster Schritt 9.2. Keine aktiven Blocker, keine offenen STOPP-Situationen, Reaktiv-Quote 1 / 10. Querschnitt: D.19 (Ubuntu 26 ab 2026-10-19), D.11 bis 2026-10-31 (Eigentümer).
- **Kontextgröße:** über `get_usage` feststellbar (189.298 Token nach der Mindest-Lektüre).
- **Auftrag:** 9.2 umsetzen – mindestens drei neue Playwright-Tests (Weltenbauer mit Übernahme-Fenster, „Abschnitt ersetzen“, Karte oder Bild), Antwortformen gegen `ui/src/api/` ohne neues Werkzeug, CI-Schrittnamen auf die geltenden Schwellen (ADR-090); lokal committen, Pull Request erst nach Freigabe.

### 2026-10-18 20:31 MESZ – [SESSIONENDE] 9.1 erledigt

- **Dauer:** 2026-10-18 17:58 bis 20:31 MESZ; Neben-Session, gestartet aus der Session des Eigentümers mit dem Auftrag „Vorlage α/β“, auf seine Frage „Können wir weitermachen?“ bis zum Abschluss von 9.1 fortgesetzt.
- **Bearbeitet:** 9.1 – Vorlage α/β, Entscheidung α (ADR-091, Regel-003), Umsetzung, PR #173 mit grüner CI, auf Anweisung des Eigentümers („merge“) zusammengeführt (`f479509`). Neu D.19 (Ubuntu 26 auf den CI-Runnern).
- **Stand:** Phase 9, 1 von 15 erledigt. Keine offenen STOPP-Situationen, keine aktiven Blocker.
- **Nächster Schritt:** 9.2 (End-to-End-Tests, Routine) und 9.3 (gegliederte Einträge je Art, Vorlage mit Mockup, Entscheidungs-Klasse); D.19 ab dem ersten CI-Lauf nach dem 2026-10-19. Beim Eigentümer: Probe mit einer Gast-Figur (9.13), D.11 bis 2026-10-31.
- **Modell-Bilanz:** Entscheidungs-Klasse (Opus 5.5, `get_session` um 20:31 erneut abgefragt). 0 Schritte oberhalb der Empfehlung (9.1 empfiehlt Entscheidung). Keine Teilarbeit abgegeben – Logbuch, Fahrplan und README im geladenen Kontext erledigt.
- **Kontextgröße:** 458.017 Token (`get_usage`), über der Grenze von 200.000; weitergearbeitet nach dem dauerhaften „weiter hier“ des Eigentümers (Abweichung nach `CLAUDE.md` Abschnitt 0, „Sessiongröße“).
- **Sessionende-Prüfungen:** README synchron (Phase 9, 1 von 15; „Nächste Schritte“ 9.1 erledigt). Drift: ADR-091 verweist auf 9.1, 9.3 – vorhanden; `docs/architecture.md` Abschnitt 9 auf Stand ADR-091 (Modul canon ergänzt, Reifegrad unverändert `[BELASTBAR]`); Modulnamen unverändert; FR-002, FR-003 unverändert erledigt; keine aktiven Blocker und keine `[BLOCKIERT]`-Schritte; Reaktiv-Quote 1/10 (ADR-082–091, nur ADR-082); Phase 9 mit 15 Schritten (Schwelle 30). Ablaufdaten-Register: neu Ubuntu 26 → D.19; sonst kein Vorlauf erreicht (D.1 ab 2026-11-05, mypy 2 am 2026-11-06). Archiv: Logbuch 260 Zeilen, project-context 349 Zeilen – kein Trigger. Keine Phasengrenze, kein Vision-Abgleich fällig.
- **Arbeitskopie:** eigener Worktree im Scratchpad (`docs/9.1-abschluss`); der gemeinsame Checkout des Eigentümers steht sauber auf `main`.

### 2026-10-18 – [ERLEDIGT] 9.1 Gliederung im Server verlässlich

- PR #173, CI grün (4 von 4), zusammengeführt `f479509`. `canon/sections.py` und `canon/names.py` mit gemeinsamen Testfällen (47 und 27) für Server und Oberfläche; Import erkennt „Wesen und Geschichte“; Namenserkennung an vier Stellen eine Regel. Lokal pytest 886 (99,85 %), vitest 459, Playwright 11. Anfrage beim Schreiben unverändert (274 Kombinationen, 0 Unterschiede). CI-Hinweis „ubuntu-latest → Ubuntu 26 ab 2026-10-19“ → D.19 mit Frist 2026-11-02; keine Bündelgrößen-Warnung.

### 2026-10-18 – [GELÖST] `ruff format` machte aus Escape-Folgen echte Sonderzeichen

- Die Leerzeichen-Konstante in `canon/sections.py` stand als zwei verkettete Zeilen mit `\u00a0` usw.; `ruff format` fügte sie zu einer zusammen und schrieb dabei die Zeichen selbst hinein, `ruff check` meldete sie danach als mehrdeutig (RUF001). Lösung: Konstante aus `chr(...)` zusammengesetzt. Merken: unsichtbare Zeichen im Code nie als Escape-Folgen in verketteten Literalen.

### 2026-10-18 – [GELÖST] Genitiv mit großem „S“: Server und Oberfläche waren verschieden

- Beim Angleichen der Namenserkennung schlug `ui/src/references.test.ts` („@KaelS“ zählt nicht, Schritt 5.23) fehl, weil zuerst die Oberfläche an den Server angepasst war (dort zählte `@KAELS` wegen `IGNORECASE`). Gelöst in Richtung der bestätigten Regel aus 5.23: Genitiv nur mit kleinem „s“, im Server mit `(?-i:s)`. Bestehende Erwartungen unverändert.

### 2026-10-18 – [BEOBACHTUNG] Figur in Vorlage-Form zerfiel beim Import

- Probe vor 9.1: `# Figuren / ## Kael / ### Aussehen / ### Wesen und Geschichte` ergab die Einträge „Aussehen“ und „Wesen und Geschichte“, nicht „Kael“ – der Import kannte „Wesen und Geschichte“ nicht. Behoben mit der Namensliste aus `canon/sections.py` (Test `test_a_figure_in_the_form_of_its_template_stays_one_entry`).

### 2026-10-18 – [ADR-ANGELEGT] ADR-091 Gliederung bleibt Markdown (α), Regel-003

- Eigentümer per Auswahlfrage: „A – Text mit Überschriften (Empfohlen)“. β (Felder im Dateikopf) verworfen, in `docs/architecture.md` Abschnitt 8. Regel-003: Teile eines Eintrags nur über die gemeinsame Abschnittsregel. `[OPERATIV]`, in 9.1 als Vorlage vorgesehen – nicht reaktiv; Reaktiv-Quote 1/10 (ADR-082–091). Auf der Entscheidungs-Klasse vorgelegt (Opus 5.5).
- Arbeitsweise: Neben-Session im gemeinsamen Checkout des Eigentümers; damit dort kein Branch gewechselt wird, läuft 9.1 in einem eigenen Worktree im Scratchpad (Branch `feat/9.1-gliederung-server`), die Doku-Änderungen vom Sessionstart sind dorthin umgezogen.

### 2026-10-18 17:58 MESZ – [SESSIONSTART] Vorlage α/β zu 9.1

- **Modell:** Opus 5.5 (`claude-opus-5-5`, laut `get_session`), Entscheidungs-Klasse; Aufwand „xhigh“. 9.1 empfiehlt Entscheidung – keine Arbeit oberhalb der Empfehlung.
- **Umgebung:** Mac des Eigentümers (macOS arm64); Neben-Session, gestartet aus der Session des Eigentümers; Pre-Commit-Hook über den SessionStart-Hook eingerichtet.
- **Stand:** vor der Mindest-Lektüre `git fetch` – `main` `fb705d8` gleich `origin/main`, kein Fast-Forward nötig.
- **Wiedereinstieg:** Phase 9, 0 von 15; nächster Schritt 9.1 mit Vorlage α (Abschnitte in Markdown) gegen β (Felder im Dateikopf). Keine aktiven Blocker, keine offenen STOPP-Situationen, Reaktiv-Quote 1 / 10. Querschnitt: D.11 bis 2026-10-31 (Eigentümer).
- **Kontextgröße:** über `get_usage` feststellbar (181.169 Token nach der Mindest-Lektüre).
- **Auftrag:** Vorlage α gegen β als `ENTSCHEIDUNG ERFORDERLICH` (Kategorie 4) vorlegen; nichts bauen vor der Entscheidung.

### 2026-10-18 17:32 MESZ – [SESSIONENDE] Phase 8 abgeschlossen, Phase 9 geplant

- **Dauer:** Fortsetzung derselben Session nach dem `[SESSIONENDE]` von 15:51 MESZ (jetzt in `docs/archiv/logbuch-phase-8.md`), ca. 15:55 bis 17:32 MESZ; Session insgesamt 2026-10-18 00:48 bis 17:32 MESZ mit langen Pausen.
- **Bearbeitet:** kein Produktcode. 8.9 und 8.11 bestätigt und abgeschlossen (PR #171, gemergt `ad05dce`). 8.13 erledigt: Vision-Abgleich mit Drift-Korrekturen, Onboarding-Pfad auf frischem Worktree, V.35 mit dem Eigentümer durchgegangen, Pflichtfrage mit getrennter Instanz (ADR-089), Planung von Phase 9 (ADR-090). Phase 8 abgeschlossen und archiviert, Logbuch verdichtet.
- **Nächster Schritt:** 9.1 Gliederung im Server verlässlich – zu Beginn Vorlage α (Abschnitte in Markdown) gegen β (Felder im Dateikopf), Entscheidungs-Klasse; 9.2 (End-to-End-Tests, Routine) kann daneben laufen. Beim Eigentümer: Probe mit einer Gast-Figur (Eingangskriterium 9.13), D.11 bis 2026-10-31.
- **Offen:** Pull Request für den Phasenabschluss (Branch `docs/8.13-phasenabschluss`) nach grüner CI zusammenführen; NFR Kontexttreue bleibt bis 9.14 `[VORLÄUFIG]`.
- **Modell-Bilanz:** Entscheidungs-Klasse (Opus 5.5, `get_session` um 17:32 erneut abgefragt). 0 Schritte oberhalb der Empfehlung (8.13 empfiehlt Entscheidung). Die getrennte Bewertung lief als Unteragent mit Sonnet (Methodik, nicht Kostenabgabe; ca. 20 min, 100 Werkzeugaufrufe). Routine-Teilarbeiten (Archivierung, Logbuch-Verdichtung, README, Fahrplan-Status) per Skript im geladenen Kontext, nicht abgegeben.
- **Kontextgröße:** über die Sitzungsabfrage nicht feststellbar; Regel „Sessiongröße“ entfiel.
- **Sessionende-Prüfungen:** README synchron (Phase 9, 0 von 15, „Nächste Schritte“). Drift: ADR-089 und ADR-090 verweisen auf vorhandene Schritte 9.1–9.15; Modulnamen und FR-IDs der Phase 9 vorhanden; Reifegrade unverändert, `docs/architecture.md` Abschnitt 9 auf Stand ADR-088; Reaktiv-Quote 1/10 (ADR-081–090, nur ADR-082); keine aktiven Blocker; Phase 9 mit 15 Schritten (Schwelle 30). Ablaufdaten-Register: kein Vorlauf erreicht (D.1 ab 2026-11-05, mypy 2 am 2026-11-06). Archiv: Phase 8 → `docs/archiv/fahrplan-phase-8.md`; Logbuch 223 Zeilen, project-context 348 Zeilen – kein Trigger. Vision-Abgleich an der Phasengrenze in 8.13 erledigt.
- **Abweichungen:** Das Zusammenführen von #171 auf ein bloßes „Weiter“ lehnte die Rechteprüfung ab; danach per Auswahlfrage ausdrücklich freigegeben. Erste Antwort der Session auf Englisch (Erinnerung „Antworten auf Deutsch“ angelegt).

### 2026-10-18 – [ADR-ANGELEGT] ADR-089 Pflichtfrage nach Phase 8, ADR-090 Planung Phase 9

- ADR-089: gezielt umbauen (9.1 Gliederung im Server verlässlich mit Vorlage α/β, 9.2 End-to-End-Tests), Bewertung der getrennten Instanz unverändert in `docs/research/bewertung-phase-8.md`, Stellungnahme daneben. ADR-090: Phase 9 mit 15 Schritten in der Reihenfolge des Eigentümers (Fundament, Kanon, Bilder, Verwaltung, Erkundung, Gäste, Kontexttreue); V.34–V.37 übernommen, V.20, V.21, V.23, V.24, V.33 → 9.15. Kontexttreue auf Wunsch des Eigentümers nicht jetzt befördert, sondern in 9.14 neu gemessen. Beide `[STRATEGISCH]`, auf der Entscheidungs-Klasse vorgelegt (Opus 5.5); Reaktiv-Quote 1/10.

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
