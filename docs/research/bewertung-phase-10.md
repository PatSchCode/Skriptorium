# Bewertung am Ende von Phase 10 (getrennte Instanz)

Pflichtfrage „Weiterbauen, umbauen oder neu aufsetzen?“ (`CLAUDE.md` Abschnitt 12) in Schritt 10.11, 2026-11-08. Bewertet von einem Unteragenten mit Sonnet ohne Gesprächsverlauf, nur lesend (gebaut hat Phase 10 überwiegend Opus). Der Text bis zur Stellungnahme ist die Bewertung unverändert (nur die Einrückung der Übergabe entfernt und hervorgehobene Zwischenzeilen als Unterüberschriften gesetzt, wegen markdownlint MD036); die Stellungnahme der bauenden KI steht getrennt am Ende.

Geprüft auf Branch `docs/10.11-planung`, HEAD `10a1901` (Arbeitsbaum sauber, gleich `main`). Bezugspunkt der Vorbewertung: `942eabf` (2026-11-05, Ende Phase 9; 274 Commits dazwischen). Nur gelesen und gemessen. Im Repo wurde nichts geändert. Hilfsskripte liegen im Scratchpad.

## Tatsächlich gelesen

- **`docs/vision.md`:** ganz.
- **`docs/architecture.md`:** ganz, in zwei Lesegängen (Zeilen 1–170 und 171–412). Die lange Zeile 123 (`ui`) ist enthalten.
- **`docs/research/bewertung-phase-9.md`:** ganz.
- **`docs/decisions.md`:**
  - Teil A: nur Kopf, Zeilen 16–40 und 120–149 (ADR-001 bis 018 und 098 bis 116 sowie Reaktiv-Quote). Die Zeilen dazwischen nicht.
  - Teil C: ganz.
  - Teil B: ADR-104 bis ADR-116 ganz, mit einer Ausnahme: von ADR-110 nur bis zur Zeile „Vision-Frage“ (Konfidenz und Konsequenzen nicht gelesen). Dazu ADR-084 ganz und aus ADR-092 nur die Zeilen zu Kontext und Entscheidung.
  - Die Reaktiv-Quote habe ich gegen die Tags in Teil B nachgezählt.
- **`docs/fahrplan.md`:**
  - „Aktueller Stand“, Übersicht und Kopf von Phase 10.
  - Schritt 10.11 ganz.
  - V.52 bis V.58 ganz.
  - V.44, V.21 und V.40 nur Titel und Statuszeilen.
  - V.45 bis V.49 nur Titel.
  - 10.1 bis 10.10 nicht im Wortlaut, nur Titel und Status aus der Übersicht.
- **Code, ganz gelesen:** `api/context.py`, `manuscript/requests.py`, `ui/src/imagePrompts.ts`, `ui/src/views/useImageModels.ts`.
- **Code, teilweise gelesen:**
  - `ai_gateway/images.py` Zeilen 25–125.
  - `api/image_routes.py`: Kopf, `generate_image`, `_openrouter_order`, `_runware_order`, Weichen per grep.
  - `ui/src/views/ImageGenerate.tsx` Zeilen 45–140 und 257–325, Rest per grep.
  - `storage/store.py` Index-Teile.
  - `storage/origins.py` Kopf.
- **Code, nur per grep oder Strukturmessung:** `EntryImages.tsx`, `WritingRequests.tsx`, `canon/sections.py`, `ui/src/sections.ts`, `runware.py`, `runware_models.py`, `api/flows/writing.py`.
- **Nicht gelesen:** `logbuch.md` (bewusst; nur Zeilenzahl gemessen), `spikes/`-Inhalte, ADR-001 bis 103 (außer den Tabellenzeilen), `requirements.md`.

## Tatsächlich ausgeführt

- **`uv run pytest -q -p no:cacheprovider --cov=skriptorium --cov-report=term`:** 1.293 bestanden in 38,74 s. Abdeckung 99,90 % (6.358 Statements, 0 verfehlt, 1.540 Zweige, 8 teilweise offen). `fail_under = 99` erreicht.
- **`uv run ruff check`:** sauber.
- **`uv run ruff format --check`:** 170 Dateien sauber.
- **`uv run mypy src tests`:** 170 Dateien, keine Meldung.
- **`npx --no-install vitest run --coverage`:** 52 Dateien, 604 Tests grün (Dauer 8,3 s).
  - Statements 98,83 % (3.889/3.935), Zweige 95,30 %, Funktionen 98,39 %, Zeilen 98,96 %.
  - Hinweis: Der Befehl aus dem Auftrag („im Ordner `ui/`“) ergibt dort „No test files found“. Die Konfiguration `vite.config.ts` liegt im Repo-Wurzelordner, dort läuft er. In `ui/` liegen nur Quellen.
- **`npx --no-install tsc --noEmit`:** ohne Meldung.
- **`npx --no-install eslint . --max-warnings 0 --report-unused-disable-directives`:** ohne Meldung.
- **Eigene Messungen (Skripte im Scratchpad, in einem Temp-Verzeichnis):**
  - Importkanten per AST.
  - Funktionslängen per AST.
  - Test der Anfrage-Ablage mit 50 synthetischen Anfragen zu je rund 100 KB.
- **Nicht ausgeführt:** Playwright (nur die Tests in `e2e/` gezählt), bandit, pip-audit, npm audit, Build. Das Verbrauchsspeicher-Experiment aus Phase 9 habe ich nicht wiederholt (`api/usage.py` ist seit `942eabf` unverändert; Echtdaten des Servers habe ich nicht).

## (a) Messwerte (Phase 9 in Klammern)

Messweise wie in der Vorbewertung: `wc -l` über `src/**/*.py`, `tests/**/*.py`, `ui/src/**/*.{ts,tsx}`.

### Umfang

- Python `src`: 15.336 Zeilen in 86 Dateien (12.982 in 81; +18 %).
- Python `tests`: 15.492 Zeilen in 84 Dateien (13.198 in 74; +17 %). Testverhältnis 1,01 (1,02).
- UI ohne Tests: 18.035 Zeilen (15.655; +15 %).
- UI-Tests: 15.613 Zeilen in 52 Dateien (13.742 in 46; +14 %).
- `ui/src/styles.css`: 2.837 Zeilen (2.686).
- e2e: 1.200 Zeilen, 17 Tests nach grep (1.090 und 15).
- Commits: 1.210 (936). ADRs: 116 (103); Phase 10 hat ADR-104 bis ADR-116 erzeugt, also 13.
- `git diff --shortstat 942eabf..HEAD`: `src` 36 Dateien, +2.508/−154. `ui/src` 60 Dateien, +5.090/−688. `tests` 23 Dateien, +2.630/−35.

### Tests

- pytest: 1.293 (1.123). Abdeckung 99,90 % (99,87 %).
- Unter 100 % liegen: `api/flows/summary.py` 97 %, `context/manuscript_hits.py` 98 %, `ai_gateway/openrouter.py`, `api/auth_routes.py` und `api/flows/writing.py` je 99 %.
- vitest: 604 (558). Statements 98,83 % (98,83 %), Zweige 95,30 % (95,41 %), Funktionen 98,39 % (98,24 %), Zeilen 98,96 % (98,99 %).

### Suppressions und Platzhalter

- `noqa`/`type: ignore` in `src`: 12, alle `N818` (wie in Phase 9). In `tests`: 15 (13).
- `TODO`, `FIXME`, `HACK` in `src`, `ui/src`, `tests`, `e2e`: 0.
- `eslint-disable`, `@ts-ignore`, `@ts-expect-error`: 0.

**Modulgrenzen** (alle Kanten stehen in der Karte, `architecture.md` Abschnitt 2)

- `api`→`ai_gateway` 12, `api`→`canon` 8, `api`→`context` 9, `api`→`manuscript` 8, `api`→`storage` 16 (15).
- `canon`→`storage` 11, `context`→`canon` 9, `context`→`manuscript` 6 (5), `manuscript`→`storage` 9 (8).
- Keine Kante `canon`↔`manuscript`. `ai_gateway` und `context` importieren nichts aus `api`, `ui` oder `storage`. Private Importe (`_name`) über Dateigrenzen in `src`: keine.

### Fassaden und Funktionen

- Methoden: `CanonService` 32 (32), `ManuscriptService` 38 (29), `DocumentStore` 18 (18).
- Funktionen gesamt: 806 (695). Funktionen mit 50 Zeilen oder mehr: 7 (3).

| Funktion | Zeilen | Vorher |
|---|---|---|
| `create_app` | 90 | 84 |
| `build_worldbuilder` | 78 | 78 |
| `epub_for` | 71 | 51 |
| `prepare_request` (`api/flows/writing.py`) | 71 | neu |
| `stream_events` (`api/flows/writing.py`) | 70 | 48 |
| `_package` (`manuscript/epub.py`) | 52 | – |
| `stream_answer` | 50 | 50 |

### Größte Python-Dateien

- `manuscript/service.py` 591 (470), `api/image_routes.py` 565, `api/manuscript_routes.py` 517 (460), `context/writing.py` 509 (485), `api/flows/writing.py` 473.
- `storage/store.py` 466, `api/writing_routes.py` 464 (451), `openrouter.py` 450, `sillytavern.py` 445, `canon/service.py` 434.
- Neu seit `942eabf`: `ai_gateway/runware.py` 383, `api/runware_models.py` 333, `manuscript/requests.py` 319.

### Größte UI-Dateien

- `ImageGenerate.tsx` **687 (452)**, `Usage.tsx` 419, `EntryImages.tsx` 419 (556), `WritingStyle.tsx` 415, `api/manuscript.ts` 389.
- `timeline.ts` 361, `Shell.tsx` 335, `sections.ts` 330, `ChapterEditor.tsx` 328, `Settings.tsx` 311 (300).
- Neu seit Phase 9: `ImageViewer.tsx` 169, `RunwareSettings.tsx` 227, `WritingRequests.tsx` 230.

### Reaktiv-Quote

- Teil A nennt 0/10 über ADR-107 bis ADR-116. Teil B trägt `[REAKTIV]` nur bei ADR-018, ADR-049 und ADR-082. Die Quote stimmt, im Fenster der letzten 10 ADRs liegt keiner.
- Phase 10 geplant mit 11 Schritten, 10 erledigt, 10.11 offen. Schwelle: mehr als 22.
- Offene V-Posten: 17 (V.21, V.40, V.44 bis V.58), Phase 9 endete mit 14. 12 davon (V.47 bis V.58) sind in Phase 10 entstanden.

### Dokumentation

- `decisions.md`: 2.827 Zeilen und 375 kB (2.520 und 338 kB). Teil A jetzt 19,6 kB, nach der Kürzung der Reaktiv-Zeile (vorher 29,5 kB). Teil C 4,3 kB.
- `fahrplan.md`: 1.904 Zeilen und 194 kB (1.714 und 184 kB). Mindest-Lektüre: Stand plus Übersicht 7,5 kB, Phase 10 25,6 kB. Die 58 V-Schritte liegen außerhalb der Mindest-Lektüre.
- `architecture.md`: 411 Zeilen, 101 kB. `project-context.md`: 351 Zeilen (Budget 600).
- `logbuch.md`: 1.201 Zeilen und 142 kB. Der harte Trigger liegt bei 800 Zeilen (Klasse M). Nicht gelesen, nur gemessen.
- `git ls-files`: 3.940 Dateien (2.805), davon `spikes/` 3.476 (88 %; vorher 85 %) mit 7,6 MB Dateigröße. Auf der Platte belegt `spikes/` 18 MB (Blockgröße).

## (b) Befunde

Kein Befund hat Schwere hoch. Das Fundament trägt.

1. **[mittel] Der zweite Bildanbieter ist in `ai_gateway` sauber, `api` und `ui` kennen aber Anbieter-Einzelheiten.**
   - `ai_gateway`: `ImageProvider` ist ein Protokoll (`images.py:111`). `openrouter_images.py` und `runware.py` sind getrennte Adapter ohne Import nach oben.
   - `api`: `Services` hat `images` und `runware` als getrennte Einzelfelder plus `runware_models` (`api/context.py`, importiert `RunwareImageProvider` direkt). Die Weiche läuft über `is_runware()` am Kennungsformat. Es gibt 4 Aufrufe und 19 Zugriffe auf `found.runware*` in `src`. `image_routes.py` hat zwei Auftragsfunktionen, `_openrouter_order` und `_runware_order`.
   - `api`: Zusatzregeln sind Runware-spezifisch. LoRAs gibt es nur dort, und `_runware_order` lehnt Ausgangsbild, Auflösung und Qualität ab (`image_routes.py:476`).
   - `ui`: `OfferedModel.runware`, `readiness.{openRouter,runware}`, Gruppen im Dialog, `LoraChoices`. Die Antwort `ImageModelList` hat feste Felder `runware`, `loras`, `runware_ready`.
   - **Kosten eines dritten Anbieters** (Schätzung aus den Zeilenzahlen von Anbieter 2: `runware.py` 383, `runware_models.py` 333, `image_routes.py` +316, `RunwareSettings.tsx` 227):
     - Adapter etwa 200–380 Zeilen.
     - Neues Feld in `Services` und `create_app`.
     - Dritter Zweig in `image_routes.py` (Modelle, Preis, Erzeugen, Bereitschaft).
     - Neues Feld im Antwortschema samt Vertragsdatei `tests/shared/api-responses.json`.
     - Dritte Gruppe in `useImageModels`.
     - Zusammen grob 600–900 Zeilen mit Tests über mindestens 6 Dateien. Das ist in Ordnung, wenn es ein dritter Anbieter bleibt. Eine Registry lohnt erst, wenn V.55 (MOSS über fal.ai) gewählt wird.
   - Bild zu Bild (V.57 „Bezug je Figur“, ADR-097) geht damit nur mit OpenRouter-Modellen. Runware lehnt `reference` ab.

2. **[mittel] `ImageGenerate.tsx` wächst wieder, im Muster von Phase 8 und 9.**
   - Zeilen: 452 (Phase 9), 458 nach 10.4 (`d469dfa`), 571 nach 10.5 (`753eb84`), 687 nach 10.8 (`ade0df6`). Das sind +50 % in zwei Schritten nach dem Zerlegen.
   - Die Hauptfunktion hat 212 Zeilen (Zeilen 45–256) und 12 Props. `ImageGenerateForm` hat 144 Zeilen und 13 Props. Die Datei enthält 11 Funktionen oder Komponenten, darunter `LoraChoices` und das Gewichtsfeld.
   - Das Ziel aus Phase 9 war „Hauptkomponente unter 200 Zeilen“. Es wird knapp verfehlt: 212 Zeilen bei 6 Hook-Aufrufen im Rumpf.
   - `EntryImages.tsx` blieb dank 10.4 klein: 556 auf 419, dazu `ImageViewer.tsx` 169 und `LooksHint.tsx` 67.
   - Die nächsten Bildfunktionen (V.52 Schlagwort-Knopf, V.53 Seed, V.57 Rezeptwahl, V.56 Gewichts- und Negativ-Prompt-Regeln) greifen alle in dieses Formular.

3. **[mittel] Vorbelegung des Bild-Prompts bei Figuren: Das Datenmodell trägt, es fehlt eine Schicht.**
   - **Ort der Prompt-Bildung:** `entryPrompt` (`ui/src/imagePrompts.ts`) liefert bei Figuren „Name: Aussehen“. Dafür werden Überschriften und Listenzeichen entfernt, die Zeilen mit Leerzeichen verbunden und bei 700 Zeichen gekürzt (`plainText`, `cut`). Der Prompt ist reiner Fließtext aus dem Kanon, ohne Wissen über die Modellfamilie.
   - **Verteilung:** Der Prompt-Aufbau liegt an drei Stellen: in der UI (`entryPrompt`), im Server (`_runware_order` hängt Zusatz und Auslösewörter an) und künftig bei einer KI (V.52). Die Familie des Modells (`_FAMILIES`, Architektur) kennt nur `api/runware_models.py`.
   - **Server-Zugriff:** Der Server liest „Aussehen“ nirgends. `read_section`, `read_part`, `put_section`, `append_section` und `read_labelled` haben null Aufrufer in `src` (belegt in Regel-003). Produktive Nutzer sind nur `take_section` für „Wesen“ und „Lage“ (ADR-107, ADR-108).
   - **Mittelweg für V.58 (Zeilen `- **Herkunft:** …`):** Die Abschnittsregel trägt ihn. `read_labelled` und `read_part` existieren in beiden Implementierungen und sind an gemeinsamen Testvektoren gekoppelt. `plainText` macht daraus aber „Herkunft: …“-Bruchstücke, die Vorbelegung bliebe ohne neuen Baustein unbrauchbar.
   - **Herkunft eines Bildes:** `ImageOrigin` (`storage/origins.py:19`) hält Modell, Prompt, Seitenverhältnis, Kosten, Datum, Grundlage, Auflösung und Qualität. Nicht gehalten werden Seed, LoRAs mit Gewicht und Zusatz. `ImageGenerate` hat Props für `initialModel` und `initialLevels`, aber keine für LoRAs. Ein „Neu erzeugen“ eines Runware-Bildes verliert damit die LoRA-Wahl.
   - **Fehlende Ablagen:**
     - Rezepte (V.57) haben keinen Ort. `system/` ist das vorhandene Muster (`modelle.md`, `runware-modelle.md`).
     - Ein Bezug je Figur (Seed oder Bezugsbild) hat im Eintragskopf kein Feld. Dort stehen `name`, `aliasse`, `kategorie`, `status`, `bilder`.
   - **Fachlogik im falschen Modul:** `api/runware_models.py` (333 Zeilen) enthält Fachlogik wie Familien und Passung, obwohl `api` laut `architecture.md` „keine Fachlogik über das Zusammenschalten hinaus“ hat. Rezepte und Prompt-Bau würden dort weiterwachsen. Die Frage, wohin die Bild-Fachlogik gehört, ist ein Thema der Vorlage zu V.57 (Kategorie 1 und 2).
   - **Fazit:** Ein Datenmodell-Umbau ist vorher nicht nötig, alle Erweiterungen sind additiv (Muster ADR-109, ADR-115). Nötig ist vor V.57 und V.58 die Grundsatzfrage zur Form von „Aussehen“, eine Prompt-Baustein-Schicht und die Erweiterung der Herkunft.
   - **Nicht geprüft:** Wie viele Figuren des Eigentümers Zeilen- oder Fließform haben. Das ist Sache der Probe in V.58.

4. **[mittel] Funktionen des Schreib-Ablaufs wachsen.**
   - `stream_events` 48 auf 70 Zeilen, `prepare_request` 71 (neu), `epub_for` 51 auf 71. Funktionen mit 50 Zeilen oder mehr: 3 auf 7.
   - Ursache sind 10.7 (Bilder) und 10.9 (Anfrage festhalten). Die Datei `api/flows/writing.py` hat 473 Zeilen.
   - V.51 (Längengrenze) und V.40 greifen in denselben Ablauf. In `pyproject.toml` und der CI gibt es weiter keine Größengrenze.

5. **[niedrig bis mittel] Ablage der Schreib-Anfragen (10.9, ADR-116).**
   - **Trennung über Kommentarzeilen, gemessen:**
     - `_body` schreibt `<!-- nachricht: <rolle> -->` ohne Maskierung. Enthält eine Nachricht eine solche Zeile, wird sie beim Lesen aufgeteilt. Geschrieben 2 Nachrichten, gelesen 3 (`['system','user','system']`).
     - Die Antwort bleibt heil, weil sie bis zum Dateiende läuft. Eine Antwort mit der Zeile `<!-- antwort der ki -->` wurde unverändert zurückgelesen.
     - Betroffen ist nur die Anzeige. Nachrichten enthalten Kanon- und Manuskript-Text des Autors oder importiertes Material, das solche Zeilen theoretisch enthalten kann.
   - **Größe, gemessen mit 50 Dateien zu je rund 100 KB:**
     - Dateien 4,94 MB. `list_requests` 28 ms (liest und parst alle Dateien). Speichern mit Kürzen auf 50: 6 ms.
     - Hochgerechnet auf 11 Geschichten wären das etwa 55 MB (Rechnung, am Server nicht gemessen).
   - **Suchindex:**
     - Alle `anfragen/*.md` unter `worlds/<welt>/` landen in `documents` und in der FTS-Tabelle (`storage/store.py` `_index_document`; nur Pfade außerhalb von Welten werden ausgenommen). `index.sqlite` hatte 6,3 MB bei 5 MB Anfragen.
     - Die Volltextsuche hat keinen Aufrufer: `canon.find_entries` nutzt die Namenssuche mit `is_entry_path`. Der Index trägt Ballast, der nie gelesen wird.
     - `rebuild_index` liest alle Dokumente vorab in eine Liste (kein Produktionsaufrufer, nur Wiederherstellung nach Runbook).
     - Den Index auszunehmen ist eine Änderung der Indexstrategie, also Kategorie 4 und freigabepflichtig.
   - **Dokumentation:** `architecture.md` Zeile 327 und der Ablagebaum nennen `anfragen/<kennung>.md`, ADR-116 nennt `<zeit>.md`. Das ist ein Wortlaut-Unterschied.
   - **Gute Seiten:** `RequestStore` ist ein eigenes Untermodul (319 Zeilen), die Fassade delegiert nur. Fehler beim Speichern brechen den Stream nicht ab.

6. **[mittel] Dokumentations-Drift zu Phase 10.**
   - `architecture.md` Abschnitt 9 trägt „Stand vom 2026-11-05, nach ADR-105“. ADR-106 bis ADR-116 sind in der Kopfzeile nicht abgebildet. Die Zeilen zu `ai_gateway` und `api` nennen Runware.
   - Abschnitt 3, Modul `ai_gateway` (Zeilen 90–97): „Abhängigkeiten (extern): httpx; OpenRouter-API“, Runware fehlt. Der Absatz zu 10.8 steht unter den Schnittstellen von `ManuscriptService` (Zeile 178).
   - Abschnitt 6 (Bedrohungsmodell, Sensitive Datenflüsse, Secrets im Betrieb) kennt Runware nicht. Das ist ein Sicherheitsthema (ADR-115: Prüfung aus, neuer Schlüssel, Prompt-Fluss an einen zweiten Anbieter). `grep` findet in der Datei insgesamt nur 8 Treffer für „Runware“, keinen in Abschnitt 6.
   - Abschnitt 7: In der Ablage fehlt `system/runware-modelle.md`, in den Kopffeldern der Eintrag dazu (nur `anfragen/` ist nachgezogen).
   - `logbuch.md` mit 1.201 Zeilen über dem Trigger 800. Die Verdichtung zum Phasenwechsel steht an.

7. **[niedrig] Prompt-Länge bei Runware.** `runware.py:247` kürzt den zusammengesetzten Prompt hart auf 4.000 Zeichen (`MAX_PROMPT_CHARS`). Zusatz und Auslösewörter stehen am Ende und fielen bei einem langen eigenen Prompt still weg. Die Eingabe in der UI ist ebenfalls auf 4.000 begrenzt. Nur gelesen, nicht ausgeführt.

8. **[niedrig] Wachstum ohne Gate, unverändert aus Phase 9.**
   - `ManuscriptService` 29 auf 38 Methoden und `manuscript/service.py` 470 auf 591 Zeilen (+26 %); die Fassade delegiert noch dünn.
   - `Services` hat 16 Felder und wächst mit jedem Anbieter.
   - Der Volltextindex hat weiter keinen Aufrufer; `sillytavern.py` hat 445 Zeilen.
   - Vom Verbrauchsspeicher gilt weiter D.26 (Auslöser 3.000 Anfragen im Monat); der Monatswert des Servers wurde nicht gemessen.
   - `spikes/` macht 88 % der Dateien im Index aus. Das behindert Tests und CI nicht, nur Repo-Größe und unqualifiziertes `git grep`.

9. **[niedrig, geprüft] Zwei niedrige Befunde der getrennten Prüfung zu Runware (ADR-115) sind im Code behoben:**
   - Größengrenze der Antwort vor dem Dekodieren: `MAX_ANSWER_BYTES` 56 MB (`runware.py:46`, `:232–238`).
   - Eine beschädigte Listendatei sperrt die Modell-Liste nicht mehr: `_runware_lists` zeigt die Startliste mit Warnung (`image_routes.py:346`).

   Die Runware-Antworten zum Hinzufügen und Speichern der Liste (`POST` und `PUT /api/images/runware`) habe ich in `tests/shared/api-responses.json` nicht als eigene Einträge gefunden (92 Einträge insgesamt, `imageModels` enthält `runware`).

## (c) Optionen

### 1. Weiterbauen wie bisher

- Kosten: kein Vorlauf.
- Risiko: mittel.
  - V.52, V.53, V.57 und V.56 wachsen in ein Formular, das nach 10.4 schon wieder um 50 % gewachsen ist (Befund 2).
  - V.57 und V.58 würden die Prompt-Bildung (UI-Funktion `entryPrompt`) ein weiteres Mal erweitern und die Bild-Fachlogik in `api` verdichten (Befund 3).
  - Der Suchindex wächst mit jeder Schreib-Anfrage um ungenutzte Volltexte (Befund 5).
- Dafür: alle Gates grün (1.293 pytest, 604 vitest, 99,90 % und 98,83 %), 0 Platzhalter, 0 reaktive ADRs, alle Modulkanten auf der Karte, kein Befund hoch.

**2. Gezielt umbauen** (innerhalb der Module, Schnittstellen höchstens additiv)

- **U.1 Bildformular entlasten** (`ui`). Runware-Teile (`LoraChoices`, Gewichtsfeld, Modellgruppen, Zusatz und Auslösewörter) in eigene Dateien oder einen Hook, `ImageGenerateForm` in Teilformulare. Verhalten und Tests unverändert. Umfang etwa 300–400 Zeilen verschoben. Aufwand wie 10.4. Klasse: Routine.
- **U.2 Anfrage-Ablage härten** (Kategorie 4). `anfragen/` vom Volltextindex ausnehmen (Pfadfilter in `store.py`, Größenordnung 10–20 Zeilen plus Test) und die Marker-Zeilen maskieren oder eindeutig machen (etwa 20–30 Zeilen plus Test). Kein Wechsel der Dateiform. Klasse: Entscheidung, weil die Indexstrategie berührt ist.
- **U.3 Dokumentation nachziehen:** Abschnitte 3, 6, 7 und 9 von `architecture.md` für ADR-106 bis ADR-116, einschließlich Bedrohungsmodell für Runware. Dazu die Logbuch-Verdichtung beim Phasenwechsel. Das ist Pflege, kein Umbau.
- **Nicht als Umbau vorab, sondern in die Vorlagen von V.57 und V.58:** Grundsatzfrage zur Form von „Aussehen“, Prompt-Baustein-Schicht (Ort: UI, Server oder neues Modul), Erweiterung von `ImageOrigin` um Seed, LoRAs mit Gewicht und Zusatz (additiv, Muster ADR-109), Ablage der Rezepte unter `system/`.
- **Nicht jetzt:** Anbieter-Registry in `api` (erst bei einer Entscheidung für V.55) und ein Neubau des Verbrauchsspeichers (Auslöser D.26).
- Kosten: etwa 2 Schritte mit eigener ID plus Pflege, rund 2 Sessions. Risiko: gering. Gefahr bleibt, dass der Umbau ohne Ende wuchert; deshalb höchstens U.1 und U.2 mit eigener Schritt-ID.

### 3. Neu aufsetzen

- Kosten: rund 33.400 Zeilen Code ohne Tests (Python 15.336, UI 18.035), dazu 31.100 Zeilen Tests (Python 15.492, UI 15.613) und e2e 1.200 Zeilen, 1.210 Commits, 116 ADRs und der Betrieb mit den Daten des Eigentümers.
- Risiko: hoch, nichts im Code spricht dafür. Keine Zyklen, alle Kanten auf der Karte, `ai_gateway` ohne Fachbegriffe, 0 Platzhalter, Abdeckung 99,90 % und 98,83 %.
- Auch die Figuren-Richtung (Befund 3) verlangt keinen Neuaufbau: Es fehlt eine Schicht, nicht ein Fundament.

## (d) Empfehlung

**Gezielt umbauen, klein, danach weiterbauen.** Konfidenz: mittel (hoch gegen einen Neuaufbau). Umkehrbarkeit: billig. Die Umbauten betreffen Oberfläche, Index und Dokumente, keine Entscheidung ist unumkehrbar.

### Begründung

- Die Grundlage ist gesund und die Zusage aus Phase 9 eingehalten: Der Anbieter-Zugang zu Runware ist in `ai_gateway` sauber gekapselt, 10.4 hat `EntryImages.tsx` deutlich verkleinert (556 auf 419).
- Die Stelle mit echter Folgekost ist das Bildformular, das nach dem Zerlegen schon wieder um 50 % gewachsen ist. Die nächsten Figuren- und Bildfunktionen greifen genau dort ein.
- Für die Figuren-Richtung (V.52 bis V.58) trägt das Datenmodell: Abschnittsregel, `context` und `system/` genügen für additive Erweiterungen. Offen ist keine Migration, sondern drei Entscheidungen, die in die Vorlagen von V.58 und V.57 gehören: Form von „Aussehen“, Ort der Prompt-Bildung, Ablage von Rezept und Bezug.
- Konfidenz „mittel“, weil ich die tatsächliche Form der Figuren-Einträge des Eigentümers nicht gesehen habe und weil die Wirkung der Prompt-Schicht auf die Bildqualität erst eine Probe zeigt.

**Konkrete Schritte** (für den Fahrplan, höchstens zwei mit eigener ID)

- **U.1** Bildformular entlasten, wie oben. Vor dem ersten Bildschritt der nächsten Phase (V.52, V.53 oder V.57).
- **U.2** Anfrage-Ablage härten (Index-Ausnahme, Maskierung der Marker), mit Freigabe, weil die Indexstrategie berührt ist. Zeitpunkt unkritisch, vor dem Anwachsen der Ablage auf dem Server.
- **Pflege:** Dokumente nachziehen (Befund 6) im Phasenabschluss.
- **Hinweis zur Reihenfolge der Planung von 10.11:** V.58 und V.57 zuerst als Vorlagen mit den drei offenen Entscheidungen; V.53 (Seed) bringt die Erweiterung der Herkunft mit und sollte vor V.57 stehen; V.55 (dritter Anbieter) erst danach und nur mit einer Registry, falls gewählt.
- **Nicht geprüft und daher offen:** Playwright-Läufe, bandit, pip-audit, npm audit, Build, Wirkung der Prompt-Schicht auf Bildqualität, Monatszählung der Anfragen am Server (D.26), Größe der Anfrage-Ablage am Server.

---

## Stellungnahme der bauenden KI (Opus 5.5, 2026-11-08)

Die Bewertung oben ist unverändert. Hier ergänze ich sie oder widerspreche ihr, jeweils mit Beleg.

### Selbst nachgeprüft und bestätigt

- **Befund 2:** `ImageGenerate.tsx` hat 687 Zeilen, bei `942eabf` waren es 452 (`wc -l`).
- **Befund 5:** Die Volltextsuche hat keinen Aufrufer. Der einzige Aufruf von `DocumentStore.search` steht in `canon/entries.py:124`, mit Modus `"name"`. `_index_document` nimmt nur Pfade außerhalb einer Welt aus.
- **Befund 6:** Abschnitt 6 von `docs/architecture.md` (zwischen den Ankern `nicht-funktionale-anforderungen` und `datenmodell`) hat 0 Treffer für „Runware“.

### Ergänzungen

1. **Befund 3 trifft die Rückmeldung des Eigentümers aus der Probe von 10.8 am selben Tag.** Er meldete zuerst, die Kanon-Beschreibung reiche für vernünftiges Prompten nicht. Auf Nachfrage präzisierte er: Es fehlen keine Körper- oder Gesichtsangaben, unbrauchbar ist die Vorbelegung. Die Instanz kannte diese Rückmeldung nicht und kam aus dem Code zum selben Ort (`entryPrompt`). Das stützt die Empfehlung, V.58 und V.57 als erste Vorlagen der nächsten Phase zu führen.
2. **Befund 6 ist mehr als Pflege.** Mit Runware kam ein zweiter Empfänger von Prompts hinzu, ohne Inhaltsprüfung (ADR-115), mit eigenem Schlüssel. Das Bedrohungsmodell ist `[BELASTBAR]` (4.5), kennt diesen Datenfluss aber nicht. Der Code von 10.8 wurde getrennt geprüft (Logbuch 2026-11-07). Fehlend ist der Nachtrag im Dokument. Dafür setze ich einen eigenen Schritt mit ID an, nicht nur „Pflege im Phasenabschluss“. Er gehört an den Anfang der nächsten Phase, weil er den Reifegrad „Bedrohungsmodell Gesamtsystem“ betrifft. Abschnitt 6 von `CLAUDE.md` verlangt, dass ein Bestandteil nicht still `[BELASTBAR]` bleibt, wenn er nicht mehr stimmt.
3. **Zu U.2:** Ich stimme zu. Zusätzlich frage ich in der Vorlage, ob der Volltextindex ganz entfallen soll. Er hat keinen Aufrufer (Befund 5 und 8) und wächst sonst weiter mit jeder Geschichte. Das ist eine Frage der Indexstrategie (Kategorie 4) und gehört deshalb in dieselbe Vorlage, nicht in einen neuen Schritt.
4. **Die Hinweise zur Reihenfolge übernehme ich:** V.53 (Seed, mit der Erweiterung der Herkunft) vor V.57, V.55 erst danach. Bei Befund 3 ergänze ich: Die Herkunft eines Runware-Bildes verliert heute die LoRA-Wahl. Das ist für „Neu erzeugen“ ein echter Mangel und gehört deshalb in denselben Schritt wie der Seed.

**Kein Widerspruch** zur Empfehlung „gezielt umbauen, klein, danach weiterbauen“. Der Hinweis zum vitest-Aufruf (im Wurzelordner, nicht in `ui/`) betrifft nur den Prüfauftrag und hat keine Folge im Code.
