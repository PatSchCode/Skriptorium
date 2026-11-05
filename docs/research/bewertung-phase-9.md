# Bewertung am Ende von Phase 9 (getrennte Instanz)

Pflichtfrage „Weiterbauen, umbauen oder neu aufsetzen?“ (`CLAUDE.md` Abschnitt 12) in Schritt 9.15, 2026-11-05. Bewertet von einem Unteragenten mit Sonnet ohne Gesprächsverlauf, nur lesend. Der Text bis zur Stellungnahme ist die Bewertung unverändert (nur die Einrückung der Übergabe entfernt); die Stellungnahme der bauenden KI steht getrennt am Ende.

Geprüft auf Branch `docs/9.15-planung` (HEAD `942eabf`, Arbeitsbaum sauber). Bezugspunkt der Vorbewertung: Commit `3d71f19` (2026-10-18). Die Instanz hat nur gelesen und gemessen, nichts im Repo geändert. Ihre Hilfsskripte lagen im Scratchpad außerhalb des Repos.

**Tatsächlich gelesen:**

- `docs/vision.md` ganz, `docs/research/bewertung-phase-8.md` ganz.
- `docs/architecture.md` ganz. Die erste Seite hatte 181 Zeilen, den Rest mit `allow_large` nachgeladen.
- `docs/decisions.md`: Teil A (Übersicht, Reaktiv-Quote) als Auszug und Längenmessung. Gelesen: ADR-089 und ADR-090 ganz, ADR-091 ganz, ADR-100 und ADR-103 ganz, Regel-003. Von ADR-092 bis ADR-099, ADR-101 und ADR-102 nur die Kopfzeilen und die Einträge in der Übersicht. Die Reaktiv-Quote nicht gegen die Tags in Teil B nachgezählt.
- `docs/fahrplan.md`: Kopf, Übersicht, Phase 9 (9.1 und 9.2 mit Notizen, 9.14 und 9.15 ganz). 9.3 bis 9.13 nicht im Wortlaut gelesen, nur Titel und Status aus der Übersicht. Außerdem V.35 ganz, V.43, und von V.20 bis V.46 nur Titel und Statuszeile (V.34, V.36 und V.37 gehören dazu).
- Code gezielt gelesen: `api/usage.py` ganz, `context/appearance.py` ganz, `canon/sections.py` (Kopf, `drop_world_sections`, Konstanten), `tests/api/test_ui_contract.py` (Kopf und Testliste), `api/context.py` (`Services`), Routen-Einbindung in `api/app.py`.
- Vermessen per AST, grep und `wc`: `src/`, `ui/src/`, `tests/`, `e2e/`, `git diff --numstat` seit `3d71f19`, Importkanten zwischen den Modulen, Suppressions, Platzhalter.
- Nicht gelesen: `logbuch.md`, `onboarding-runbook.md`, `requirements.md`, `spikes/`-Inhalte, die übrigen ADRs, die Quelltexte der meisten UI-Ansichten (nur Größe und Hook-Zahl gemessen).

**Tatsächlich ausgeführt:**

- `uv run pytest -q -p no:cacheprovider --cov=skriptorium --cov-report=term`: 1.123 bestanden in 32,5 s.
- `uv run ruff check`, `uv run ruff format --check`, `uv run mypy src tests`: alle sauber.
- `npx --no-install vitest run --coverage`: 558 Tests grün in 10,4 s.
- `npx --no-install tsc --noEmit` und `npx --no-install eslint . --max-warnings 0 --report-unused-disable-directives`: ohne Meldung.
- Messung `UsageLog` in einem Temp-Verzeichnis: 400 / 1.100 / 2.000 / 4.000 vorgefüllte Zeilen, dann eine Anfrage und eine Statistik gemessen.
- Nicht ausgeführt: Playwright (die 15 e2e-Tests nur gezählt), bandit, pip-audit, npm audit, prettier, Build. Kein Netz, kein Server.

**Vergleichbarkeit:** Zeilenzahlen nach `wc -l` über `src/**/*.py`, `tests/**/*.py` und `ui/src/**/*.{ts,tsx}`. Die Hook-Zahlen und Komponentenlängen sind grep-Heuristiken. Die Vorbewertung hat teils anders gemessen, deshalb sind diese Werte nur näherungsweise vergleichbar.

## (a) Messwerte

**Umfang** (Ende Phase 8 in Klammern):

- Python `src`: 12.982 Zeilen in 81 Dateien (10.703 in 74; +21 %). Seit `3d71f19` sind 47 Dateien geändert, +2.485/−206 Zeilen.
- Python `tests`: 13.198 Zeilen in 74 Dateien (9.828 in 57; +34 %). Testverhältnis 1,02 (0,92).
- UI `ui/src` ohne Tests: 15.655 Zeilen in 112 Dateien (12.765 in 104; +22,6 %), davon 82 Ansichtsdateien in `views/`. `styles.css` 2.686 Zeilen (2.328; +15 %).
- UI-Tests: 13.742 Zeilen in 46 Dateien (10.611 in 37; +29 %). Testverhältnis 0,88 (0,81).
- e2e: 1.090 Zeilen und 15 Tests (603 und 11).
- Commits: 936 (767), davon 179 seit 2026-10-18. Davon tragen etwa 93 das Präfix `docs`, 14 `ui`, 11 `api`, 7 `spike`.
- ADRs: 103 (88). Phase 9 hat ADR-089 bis ADR-103 erzeugt, also 15.
- `git ls-files`: 2.805 Dateien, davon `spikes/` 2.384 (85 %; vorher 1.957) mit etwa 4,8 MB (3,93 MB).

**pytest:**

- 1.123 bestanden (805).
- Abdeckung 99,87 % (99,84 %): 5.475 Statements, 0 verfehlt, 1.300 Zweige, 9 teilweise offen. `fail_under = 99` (`pyproject.toml:73`), Puffer 0,87.
- Unter 100 % liegen nur zwei Dateien: `api/flows/summary.py` mit 97 % (Zweige 157→154 und 161→163) und `context/manuscript_hits.py` mit 98 % (Zweige 178→183, 192→exit, 194→192). Die weiteren teilweise offenen Zweige (zusammen 9) nicht einzeln zugeordnet.

**vitest:**

- 46 Dateien, 558 Tests grün (37 / 398).
- Statements 98,83 % (98,65), Zweige 95,41 % (95,07), Funktionen 98,24 % (97,86), Zeilen 98,99 % (98,84).
- Schwellen laut `ui/vite.config.ts:64`: 98 / 98 / 97 / 94 (Lines / Statements / Functions / Branches).
- Schwächste Dateien: `WorldPage.tsx` (Funktionen 76,9 %), `StoryPage.tsx` (Funktionen 85 %), `useChatScroll.ts` (Zweige 85,7 %), `useChapterDraft.ts` (Zweige 50 %), `ThemeChoice.tsx` (Zweige 66,7 %).

**Werkzeuge:** ruff, `ruff format --check` (155 Dateien), mypy (155 Dateien), eslint und tsc sauber.

**Suppressions und Platzhalter:**

- 12 `noqa` in `src` (alle `N818`, begründet), 13 `noqa`/`type: ignore` in `tests`. UI: `eslint-disable`, `@ts-ignore`, `@ts-expect-error` und `any` je 0.
- `TODO(fahrplan-ref`: 0. Unmarkierte TODO, FIXME oder HACK in `src`, `ui/src`, `tests`, `e2e`: 0.

**Modulgrenzen** (AST, Importkanten zwischen den Fachmodulen):

- `api`→`ai_gateway` 12, `api`→`canon` 8, `api`→`context` 9, `api`→`manuscript` 8, `api`→`storage` 15, `canon`→`storage` 11, `context`→`canon` 9, `context`→`manuscript` 5, `manuscript`→`storage` 8.
- Jede Kante steht in der Karte (`architecture.md` Abschnitt 2). Keine Kante `canon`↔`manuscript`, `context` importiert weder `ai_gateway` noch `storage` noch `api`.
- `api`→`storage` nutzt außerhalb von `system/` nur Fehlertypen, Größengrenzen und `inspect_image`. Das deckt ADR-082.
- Private Importe über Dateigrenzen in `src`: nicht gesucht. In `tests`: `_tail` und `_opening` (`tests/context/test_builder.py:330,789`) und 11 Importe aus anderen Testdateien (z. B. `tests/ai_gateway/test_image_basis.py:16`).

**Größte Python-Dateien:** `context/writing.py` 485 (490), `manuscript/service.py` 470 (375), `storage/store.py` 466 (378), `manuscript_routes.py` 460 (374), `writing_routes.py` 451 (366), `openrouter.py` 450 (440), `sillytavern.py` 445 (445), `canon/service.py` 434 (349). Neu: `canon/sections.py` 338.

**Fassaden (Methodenzahl):** `CanonService` 32 (25), `ManuscriptService` 29 (21), `DocumentStore` 18 (15).

**Längste Python-Funktionen:** 695 Funktionen, 3 über 50 Zeilen (vorher 3 von 573):

- `create_app` 84
- `build_worldbuilder` 78
- `epub_for` 51
- knapp darunter `stream_answer` 50, `apply_import` 49, `stream_events` 48

**Größte UI-Dateien:** `EntryImages.tsx` 556 (410), `ImageGenerate.tsx` 452 (323), `Usage.tsx` 419 (neu), `WritingStyle.tsx` 415, `timeline.ts` 361, `Shell.tsx` 335, `sections.ts` 330, `StoryList.tsx` 301, `Settings.tsx` 300 (neu), `ModelManager.tsx` 299.

**Hauptkomponenten** (von der ersten `export function` bis zur nächsten Deklaration, grep-Heuristik):

- `ImageGenerate` etwa 355 Zeilen, 14 `useState`, 11 Hooks (Phase 8: 275 Zeilen, 9 Hooks).
- `EntryImages` etwa 287 Zeilen.
- `ModelManager` etwa 207 Zeilen, 10 Hooks.
- `Usage` etwa 136 Zeilen.
- `InstructionEditor` 14 Hooks, `Shell` 9, `Guests` 8, `StoryList` 8.

**Reaktiv-Quote:**

- 0/10 laut `decisions.md` Teil A, Schwelle 30 %. Seit ADR-089 ist kein ADR als reaktiv geführt.
- Die Zeile „Aktueller Wert“ ist 10.880 Zeichen lang (8.505). Teil A insgesamt hat etwa 29,5 kB, die „Stand“-Zeile 2.333 Zeichen.
- `decisions.md` hat 338 kB und 2.520 Zeilen (266 kB und 2.145). `fahrplan.md` hat 184 kB und 1.714 Zeilen, `architecture.md` Zeile 123 hat 7.326 Zeichen.

**Phasenumfang:** Phase 9 geplant mit 15 Schritten (ADR-090), jetzt 15. Die Schwelle liegt bei mehr als 30 Schritten. 14 von 15 sind erledigt; 9.15 ist offen. In der Phase entstanden 9 neue V-Schritte (V.38 bis V.46). Für 9.15 stehen 14 verschobene Posten an: V.20, V.21, V.23, V.24, V.33 und V.38 bis V.46 (Phase 8: 21 Posten).

**Verbrauchsspeicher** (eigene Messung, 11 Felder je Zeile, libyaml vorhanden: `yaml.__with_libyaml__` = True):

| Zeilen im Monat | `record` (eine Anfrage) | `stats` (alle Monate) | Dateigröße |
|---|---|---|---|
| 400 | 27 ms | 20 ms | 90 kB |
| 1.100 | 88 ms | 54 ms | 248 kB |
| 2.000 | 137 ms | 111 ms | 451 kB |
| 4.000 | 303 ms | 222 ms | 902 kB |

- Die Echtdaten laut `logbuch.md:151` und ADR-100: Oktober 1.094 Anfragen, November bis zum 04. 81. `UsageLog.record` liest und schreibt weiterhin die ganze Monatsdatei je Anfrage (`api/usage.py:~195-215`, Sperre `:~165`).
- `architecture.md:243` und `project-context.md:289` rechnen noch mit „ca. 400 Anfragen im Monat“. Das ist 2,7-fach unter dem gemessenen Wert.

**Vertragsabsicherung:**

- `tests/shared/api-responses.json` hat 87 aufgezeichnete Antworten und Ereignisse. `tests/api/test_ui_contract.py` (589 Zeilen) vergleicht sie mit dem Server und schreibt die Datei bei Abweichung neu und schlägt fehl. `ui/src/api/contract.test.ts` (285 Zeilen) prüft sie mit der TypeScript-Compiler-API gegen die handgeschriebenen Typen.
- Die Datei deckt `usage`, `usageStats`, `worldDeletion`, `storyDeletion` und Modelle ab. Server-Routen insgesamt: etwa 82 Dekoratoren. Nicht geprüft, welche der Routen fehlen.

## (b) Befunde

Kein Befund hat Schwere hoch. Das Fundament trägt, aber die Instanz widerspricht den Dokumenten an den Stellen 1, 3 und 5.

1. **[mittel] Der „Abschnitts-Schicht im Server“ fehlt der produktive Nutzer.**
   - ADR-091, `architecture.md:63`, Regel-003 und die Planung der Phase 8 (Option (i), Bewertung Phase 8) sagen, `render`, Import und Aussehen nutzten die Abschnittsregel des Servers.
   - Im Code gilt das nur für `drop_empty_sections`, `drop_world_sections`, `nest_headings`, `template_for` und `is_section_name` (je 2 bis 3 Aufrufstellen außerhalb von `sections.py`).
   - `read_section`, `read_part`, `put_section`, `append_section` und `read_labelled` haben null Aufrufer in `src` (grep ohne `canon/sections.py` und `canon/__init__.py`). Sie werden nur exportiert und in `tests/canon/test_sections.py` mit den gemeinsamen Testvektoren geprüft.
   - `context/appearance.py:36-37` übergibt den ganzen `entry.body` an die KI und liest den Abschnitt „Aussehen“ nicht. Das Akzeptanzkriterium von 9.1 („‚Aussehen‘ wird an allen Stellen gleich gefunden“) stimmt für den Server nur mit dem Vermerk, dass der Server den Abschnitt nirgends sucht. Gefunden und ersetzt wird er nur in der Oberfläche (`ui/src/sections.ts`, `imagePrompts.ts`, `relations.ts`).
   - Das Risiko ist klein, der Zweck (eine Regel, geprüft an Testvektoren) ist erfüllt. Aber etwa 100 Zeilen Servercode haben keinen Laufzeitnutzer und tragen den Anschein einer Absicherung, die es so nicht gibt.
   - Bei V.38 oder V.39 (Server liest „Wesen“, Aussehen herauslösen für Orte) wird sich zeigen, ob die Funktionen taugen.

2. **[mittel] `drop_world_sections` entfernt Abschnitte nach Teilstring.**
   - `canon/sections.py:118-148` entfernt jeden Abschnitt samt Unterabschnitten, dessen Überschrift mit „In “ oder „Im “ beginnt und den Weltnamen irgendwo enthält (`name in text`, `:~142`).
   - Eine Überschrift wie „In der Stadt am Eisenmeer“ wird laut Docstring bewusst mitentfernt. Eine Welt mit kurzem Namen oder einem Namen, der in einem Satz vorkommt, entfernt aber auch ungewollt Inhalt aus der Anfrage. Gespeichert wird nichts verändert.
   - Das Entfernen geschieht still. Es gibt weder ein Protokoll noch einen Hinweis in der Oberfläche, nur die Prüfung in den Tests (nicht gelesen).
   - Die Abschnittsregel aus ADR-102 hängt zudem an einer Namenskonvention („In ‹Welt›“), nicht an einer Liste in `SECTIONS`.

3. **[mittel] ADR-103 stuft die Kontexttreue auf `[BELASTBAR]` und rechnet bis 30 Kapitel hoch. Gemessen sind 9.**
   - Gemessen wurde die Zusammensetzung einer Anfrage ohne KI (Zahlen aus der Anfrage, keine Bewertung eines KI-Textes): 29.793 von 30.000 Token, Handlungsstand, 8 Kurzfassungen, 20 von 20 Kanon-Einträgen. Das sagt, dass nichts abgeschnitten wurde, nicht, dass der Text widerspruchsfrei ist.
   - Die Grenze „etwa 30 Kapitel“ ist eine Hochrechnung bei gleichem Kanon und gleicher Kapitelgröße. Die Konfidenz nennt der ADR selbst „mittel“. `architecture.md:245` stuft trotzdem `[BELASTBAR]` ein.
   - Die Regel des Projekts verlangt für `[BELASTBAR]` eine funktionierende Umsetzung oder einen ADR. Das ist formal erfüllt. D.25 ist als Nachmessung vorgesehen, sobald eine Geschichte 25 Kapitel erreicht. Trotzdem ist die Einstufung großzügiger als der Beleg.
   - Dass die Kurzfassungen wegen `CANON_SHARE` nur 3.121 von 29.793 Token ausmachen, ist ein Nebenbefund: Das Kernversprechen der Vision („kein Kontextverlust“) hängt an der Qualität dieser 8 Texte, nicht an ihrer Länge. Diese Qualität misst 9.14 nicht.

4. **[mittel] Verwaiste Kennungen nach dem Löschen eines Kanon-Eintrags (V.43) sind bekannt, aber offen.**
   - Nach V.43 entfernt `CanonService.delete_entry` Bilder und Markierungen, lässt aber Fakten, geführte Figuren und Gast-Verbindungen stehen. Ein `@`-Verweis auf einen gelöschten Gast scheitert mit „Unbekannter Kanon-Eintrag“.
   - Kennungen entstehen aus dem Namen (`architecture.md:160`). Wird später ein Eintrag mit demselben Namen angelegt, hängen die alten Verweise unbemerkt an einem neuen Eintrag. Nicht im Code nachgestellt, folgt aus der Beschreibung.
   - Das Löschen von Welt, Geschichte und Kapitel ist dagegen mit Kaskade, Vorschau und Namensabfrage umgesetzt (ADR-098).

5. **[mittel] Die Hauptkomponente `ImageGenerate` wächst in dem Muster, das in Phase 8 `WorldMaps` hatte.**
   - Eine einzige Funktion mit etwa 355 Zeilen, 14 `useState` und 11 Hooks (`ui/src/views/ImageGenerate.tsx:30-385`). In Phase 8 war es ein Wachstumspunkt bei 275 Zeilen.
   - `EntryImages` (556 Zeilen, Hauptfunktion etwa 287 Zeilen, `ImageViewer` etwa 170) ist ebenfalls gewachsen. `styles.css` ist um 360 Zeilen in dieser Phase gewachsen.
   - V.23 (Bilder im Manuskript), V.24 (weitere Anbieter) und V.33 (Bilder beim Schreiben) greifen genau in diese Bildbereiche ein.
   - Es gibt weiter keine Größen- oder Komplexitätsgrenze in `pyproject.toml:46` (`select = ["E","W","F","I","B","UP","S","N","SIM","RUF"]`) und keine in `eslint`.

6. **[mittel] Der Verbrauchsspeicher ist besser, aber nicht umgebaut.**
   - ADR-100 hat die Messung ernst genommen und libyaml eingeführt (370 ms auf 88 ms bei 1.100 Zeilen). Das trägt die heutige Nutzung (1.094 Anfragen im Oktober).
   - Es bleibt ein Lesen und Schreiben der ganzen Datei je Anfrage unter einer Sperre. Mit V.42 (vollständige Anfrage festhalten) oder weiteren Feldern wächst die Zeile. Bei 4.000 Zeilen sind es etwa 300 ms je Anfrage.
   - `record` wird synchron aufgerufen (`api/flows/writing.py:240`, `worldbuilder.py:150`, `summary.py:137`). Ob es die Ereignisschleife blockiert, nicht gemessen.
   - Die Kostenschätzung im Dokument (400 Anfragen) ist veraltet (siehe Befund 8).

7. **[niedrig] Die Fassaden `CanonService` und `ManuscriptService` wachsen wieder.**
   - `canon/service.py` 349 → 434, `manuscript/service.py` 375 → 470, Methodenzahl 25 → 32 und 21 → 29. Das ist das Muster, das in Phase 7 `canon/service.py` auf 878 Zeilen brachte.
   - Noch ist es dünn delegierend, keine Funktion über 50 Zeilen. Die Wachstumsrate liegt bei etwa +25 % je Phase.
   - `storage/store.py` wuchs auf 466 Zeilen (378): `delete_tree`, Herkunft, libyaml.

8. **[niedrig] Dokumentations-Drift.**
   - `architecture.md:364` trägt „Stand vom 2026-10-19, nach ADR-093“. Die Tabelle nennt für `api`, `ai_gateway` und `storage` keine Phase-9-Änderungen (Archiv/Löschen, Bild zu Bild, `origins`, libyaml). Abschnitte 3 und 4 sind dagegen gepflegt.
   - `architecture.md:243` und `project-context.md:289` rechnen mit etwa 400 Anfragen im Monat. Gemessen sind 1.094.
   - V.34, V.36 und V.37 stehen noch als `⏸️ VERSCHOBEN → 9.x`, obwohl 9.10, 9.11 und 9.13 erledigt sind. Der Landeplatz ist gültig, der Status ist missverständlich.
   - Das Logbuch hat 828 Zeilen und liegt über dem harten Trigger von 800 (Klasse M). Es wird beim Phasenwechsel verdichtet; das ist zu erledigen, nicht ein Befund gegen den Code.

9. **[niedrig] Die Pflichtlektüre wächst.** Teil A von `decisions.md` hat etwa 29,5 kB. Die „Reaktiv-Quote“-Zeile (10.880 Zeichen) und die „Stand“-Zeile (2.333 Zeichen) führen jede frühere Begründung seit ADR-018 mit. Gebraucht wird nur der aktuelle Wert. Das kostet bei jedem Sessionstart Kontext, ohne zu informieren. Von den 179 Commits seit 2026-10-18 tragen etwa 93 das Präfix `docs`.

10. **[niedrig] Unverändert aus Phase 8:**
    - Der Volltextindex (`storage/store.py` `fulltext`) hat keinen Aufrufer in der Oberfläche (`ui/src/api/` enthält kein `/search`).
    - `sillytavern.py` 445 Zeilen.
    - Fünf ähnlich gebaute Streaming-Abläufe: `stream_answer` 50, `stream_events` 48 Zeilen, `summarize_chapter` 47.
    - `Services.images` ist weiter ein einzelner Slot (`api/context.py:47`), V.24 braucht mehr als einen Adapter.
    - Test-zu-Test-Importe (11).
    - `spikes/` wächst weiter im Index (2.384 Dateien).

11. **[niedrig] Zwei Rechenwege für dieselbe Namensregel in UI und Server.** `ui/src/sections.ts` (330 Zeilen) und `canon/sections.py` (338 Zeilen) sind zwei Implementierungen derselben Regel, gekoppelt über `tests/shared/sections.json` und `names.json` (ADR-091 bewusst so gewählt). `ui/src/timeline.ts` (361 Zeilen) hat eine eigene Zeitangabe-Erkennung, ohne eigenen Server-Gegenpart. Das ist akzeptiert, aber jede Regeländerung ist ein Doppelcommit.

## (c) Vergleich mit der Bewertung nach Phase 8

| Nr. (Phase 8) | Befund Phase 8 | Stand jetzt | Beleg |
|---|---|---|---|
| 1 | Abschnitts-Konvention nur in der UI | teilweise behoben | `canon/sections.py` und `canon/names.py` mit gemeinsamen Testvektoren; Namenserkennung an vier Stellen auf `name_pattern` gebracht (`context/writing.py:61`, `manuscript_hits.py:152`). Aber `read_section`/`put_section` ohne produktiven Aufrufer (Befund 1) |
| 2 | Verbrauchsspeicher skaliert nicht | gemildert | libyaml, 370 → 88 ms bei 1.100 Zeilen (ADR-100). Layout unverändert (Befund 6) |
| 3 | Kein Vertragstest, e2e gewachsen 0 | behoben | e2e 11 → 15, 87 aufgezeichnete Antworten mit Compiler-Prüfung, CI-Schrittnamen berichtigt (`ci.yml:65,96`) |
| 4 | Rückstau 21 Posten | teilweise | Phase 9 hat 15 von 15 geplanten Schritten genommen, 14 neue Posten liegen vor. Phase 9 blieb bei Faktor 1,0. 9 davon sind neue Wünsche |
| 5 | Architektur-Drift | erneut aufgelaufen | Abschnitt 9 trägt „nach ADR-093“ (Befund 8) |
| 6 | `api`→`storage` ohne Gate | unverändert, durch ADR-082 gedeckt | 15 Importstellen, alle auf der Karte |
| 7 | Namenserkennung mehrfach | behoben | eine Regel `name_pattern` (ADR-091) |
| 8 | Wachstumspunkte ohne Gate (`writing.py`, `build_worldbuilder`, `ImageGenerate`) | besteht und verschärft | `context/writing.py` 490 → 485, `build_worldbuilder` 78 unverändert; `ImageGenerate` 275 → etwa 355 Zeilen; keine Grenze in `pyproject.toml` oder CI |
| 9 | Volltextindex ohne Nutzer | besteht | |
| 10 | Kein Migrationsmechanismus | besteht | Phase 9 war durchgängig additiv (`origins`, `archiviert`, `welt`/`geschichte`, `weltbezug`). Die erste nicht additive Änderung war das Nachrücken der Kapitelnummern (ADR-098) |
| 11 | Offene Belege (Probe 8.11, Kontexttreue VORLÄUFIG) | behoben | ADR-103 (aber siehe Befund 3) |
| 12 | `sillytavern.py`, Streaming-Flows, `spikes/`, Test-Importe | besteht | |

Die Umbauteile (i) bis (iii) der Vorbewertung sind erledigt: (i) mit der Einschränkung aus Befund 1, (ii) 9.2 (+4 e2e, +87 Antworten), (iii) in 8.13. Die Reaktiv-Quote ist von 1/10 auf 0/10 gesunken. Die Vorhersage der Vorbewertung, dass Phase 9 bei 21 Posten nahe der Wucherungsgrenze liegt, hat sich nicht bestätigt: Phase 9 blieb bei 15 Schritten.

## (d) Die drei Optionen

**1. Weiterbauen wie bisher.**

- Kosten: kein Vorlauf.
- Risiko: mittel.
  - Die nächsten Wünsche (V.23, V.24, V.33) greifen in `ImageGenerate` und `EntryImages` (Befund 5). Dort würde die Hauptfunktion bei etwa 400 Zeilen und mehr als 15 Hooks landen. In `WorldMaps` führte dasselbe Muster zum Umbau.
  - V.38/V.39 würden zum ersten Mal die toten Server-Abschnittsfunktionen benutzen und dabei auf Fehler stoßen (Befund 1).
  - V.43 bleibt ein Risiko für stille Falschverweise (Befund 4).
  - Die Dokumentationslast wächst weiter (Befund 9).
- Dafür: alle Gates grün (1.123 und 558 Tests), 0 Platzhalter, 0 reaktive ADRs, keine Importverstöße, Phase 9 ohne Wucherung.

**2. Gezielt umbauen** (innerhalb der Module, Schnittstellen höchstens additiv).

- (i) **Bildansichten zerlegen:** `ImageGenerate` (Zustand und Preisabfrage in Hooks, Formular, Vorschau) und `EntryImages` (`ImageViewer` in eigene Datei). Verhalten unverändert, vorhandene Tests (etwa `ImageBasis.test.tsx` 384 Zeilen, `ImageOriginPanel.test.tsx`) bleiben die Absicherung. Umfang: etwa 900 Zeilen in zwei Dateien, Aufwand wie 8.2.
- (ii) **Server-Abschnittsfunktionen:** entweder einen echten Nutzer geben (z. B. `build_appearance` oder V.38) oder auf das beschränken, was gebraucht wird, und Regel-003 und `architecture.md:63` entsprechend berichtigen. Zusätzlich `drop_world_sections` auf eine feste Form binden (Überschrift beginnt mit „In ‹Welt›“ statt Teilstring) oder das Entfernen sichtbar machen. Umfang: etwa 100 Zeilen Produktivcode und Tests in `tests/canon/test_sections.py`.
- (iii) **V.43 vorziehen:** Löschkaskade für Kanon-Einträge wie in ADR-098 (Kategorie 4, destruktiv, braucht eine Vorlage). Umfang: `canon`, `manuscript`, `api/flows/removal.py` (133 Zeilen vorhanden).
- (iv) **Dokumentation:** `architecture.md` Abschnitt 9 und die 400-Anfragen-Schätzung nachziehen; die „Reaktiv-Quote“-Zeile auf den aktuellen Wert kürzen und den Verlauf archivieren; V.34, V.36, V.37 auf den tatsächlichen Stand bringen; Logbuch beim Phasenwechsel verdichten. Das ist Pflege, kein Umbau.
- (v) Optional: Größengrenze für Komponenten (Kategorie 7, braucht Freigabe); Verbrauchsspeicher als Anhängen statt Neuschreiben, erst wenn ein Monat 3.000 Zeilen erreicht (Auslöser statt Schritt).
- Kosten (Schätzung): 3 Schritte ((i), (ii), (iii)), etwa 2 bis 3 Sessions. Risiko: gering. Gefahr ist Wucherung durch Umbau ohne Ende, deshalb höchstens 3 Schritte mit eigener ID.

**3. Neu aufsetzen.**

- Kosten: etwa 41.800 Zeilen Code (Python 12.982, UI 15.655, Tests 13.198 ohne UI-Tests, dazu UI-Tests 13.742 und e2e 1.090, zusammen etwa 56.700), 936 Commits, 103 ADRs und der Betrieb mit den Daten des Eigentümers (laut ADR-100 1.175 Verbrauchszeilen auf dem Server).
- Risiko: hoch, nichts im Code spricht dafür. Keine fachlichen Zyklen, alle Importe auf der Karte, 0 Platzhalter, 0 reaktive ADRs, ruff, mypy, eslint und tsc sauber, Abdeckung 99,87 % und 98,83 %.

**Tragen Datenmodell und Schnittstellen die auf 9.15 verschobenen Posten ohne Neuaufbau?** Ja, alle, mit Vorbehalten:

| Posten | Trägt es? | Beleg / Vorbehalt |
|---|---|---|
| V.20 Figurenkarten im Netz | ja | Recherche-Baustein aus 9.12 (ADR-101) und SillyTavern-Import vorhanden. Neuer Dienst wäre Kategorie 3 |
| V.21 Veröffentlichung | ja, aber sicherheitskritisch | Jeder Router hängt hinter `Depends(current_session)` (`canon_routes.py:27`, `manuscript_routes.py:28` usw.); ein öffentlicher Lese-Router bricht die Annahme in `architecture.md:183`. Kategorie 6, Bedrohungsmodell, getrennte Prüfung |
| V.23 Bilder im Manuskript | ja | Bildablage und Prüfung vorhanden. `epub.py` (`epub_for` 51 Zeilen, `_package` 47) kennt nur Absätze und Überschriften. Fällt mit Befund 5 zusammen |
| V.24 weiterer Bildanbieter | ja, mehr als ein Adapter | `Services.images` ist ein einzelner Slot (`api/context.py:47`); Zuordnung Modell → Anbieter fehlt |
| V.33 Bilder beim Schreiben | ja | `Message.images` und `reads_images` existieren. Die Token-Schätzung zählt nur Text |
| V.38/V.39 Abschnitte im Server lesen | ja | genau der Fall von Befund 1 |
| V.40, V.41, V.42 | ja | V.42 vergrößert die Verbrauchszeile oder braucht ein eigenes Ziel (Befund 6) |
| V.43 verwaiste Kennungen | ja | Befund 4 |
| V.44 bis V.46 | ja | Folgen aus ADR-101, Kategorie 3 und 8 sind in ADR-101 geklärt |

## (e) Empfehlung

**Gezielt umbauen, klein, danach weiterbauen. Konfidenz: mittel** (gegen Neuaufbau hoch). Es liegt nahe an „weiterbauen“. Der Unterschied ist die Reihenfolge: drei kleine Schritte vor den Bildthemen, dazu die Pflege der Dokumente.

Begründung:

- Die Grundlage ist gesund. Alle Gates grün (1.123 pytest, 558 vitest), Abdeckung 99,87 % und 98,83 %, 0 Platzhalter, 0 reaktive ADRs, alle Modulkanten auf der Karte, kein Befund hoch. Phase 9 hat 15 von 15 Schritten erledigt, ohne die Grenze zu berühren. Das spricht klar gegen einen Neuaufbau.
- Die drei Befunde mit Folgekosten sind klein und liegen vor den nächsten Wünschen: `ImageGenerate` (Befund 5) vor V.23/V.24/V.33, die Abschnittsfunktionen (Befund 1 und 2) vor V.38/V.39, und die Löschkaskade (Befund 4) vor der nächsten Verwaltungsarbeit.
- Der Verbrauchsspeicher braucht keinen Schritt, solange ein Monat unter etwa 3.000 Zeilen bleibt.

Konkrete Umbau-Schritte (höchstens 3, jeder mit eigener Schritt-ID zu Beginn der nächsten Phase, Reihenfolge wie gelistet):

1. **U.1 Bildansichten zerlegen.** `ImageGenerate.tsx` (Zustand, Preis, Vorschau, Basisbild) und `EntryImages.tsx` (`ImageViewer`, Herkunftspanel) in kleinere Dateien und Hooks, ohne Änderung des Verhaltens und der Tests. Ziel: keine Hauptkomponente über 200 Zeilen, höchstens 8 Hooks je Komponente. Umfang: etwa 900 Zeilen in 2 Dateien, Aufwand wie 8.2. Klasse: Routine (Umbau innerhalb eines Moduls). Eine Größengrenze in der CI ist Kategorie 7 und braucht eine eigene Freigabe.
2. **U.2 Abschnittsfunktionen und Weltabschnitte klären.** `read_section`/`put_section`/`read_part` entweder durch einen echten Nutzer rechtfertigen (zuerst V.38 oder die Aussehen-Anfrage) oder aus der öffentlichen Schnittstelle und aus Regel-003 und `architecture.md:63` zurücknehmen, mit den Testvektoren als Referenz in `tests/shared/`. `drop_world_sections` auf die Form „Überschrift beginnt mit In/Im ‹Weltname›“ einengen oder das Entfernen im Protokoll der Anfrage sichtbar machen. Umfang: etwa 100 Zeilen und deren Tests. Klasse: Entscheidung (berührt Regel-003 und ADR-102).
3. **U.3 Löschkaskade für Kanon-Einträge (V.43).** Mit Vorlage und ADR (Kategorie 4, destruktiv). Gegebenenfalls Kennungen gelöschter Einträge nicht wiederverwenden oder die Kaskade wie in ADR-098 mit Vorschau. Klasse: Entscheidung.

Dazu Pflege, kein Schritt mit ID:

- `architecture.md` Abschnitt 9 nachziehen und die „ca. 400 Anfragen“-Schätzung auf den gemessenen Wert bringen.
- Die „Reaktiv-Quote“- und „Stand“-Zeilen in `decisions.md` Teil A auf den aktuellen Wert kürzen, den Verlauf nach `docs/archiv/` verlegen.
- V.34/V.36/V.37 im Status auf „übernommen in 9.13/9.10/9.11“ setzen.
- Das Logbuch beim Phasenwechsel verdichten (828 Zeilen > 800).

Hinweise zur Planung von Phase 10 (9.15):

- Die 14 verschobenen Posten nicht alle in eine Phase nehmen. Sinnvoll: U.1 bis U.3 vorn, dann V.38/V.39/V.43 mit dem Nutzer für die Abschnittsfunktionen, dann die Bildthemen (V.23, V.24, V.33), V.21 als eigene Vorlage mit Prüfung durch eine getrennte Instanz.
- Die Einstufung von ADR-103 nicht als Beleg für Qualität lesen; D.25 bleibt der nächste echte Test, und eine KI-gestützte Bewertung des Textes an der größten Geschichte fehlt weiterhin.
- Messung des Verbrauchsspeichers bei Gelegenheit wiederholen (Auslöser: 3.000 Zeilen in einem Monat).

Nicht geprüft und daher offen: Playwright-Läufe, bandit, pip-audit, npm audit, Build, die Umsetzung von 9.3 bis 9.13 im Einzelnen, die Reaktiv-Quote gegen die Tags in Teil B.

## Stellungnahme der bauenden KI (2026-11-05)

Die Bewertung oben bleibt unverändert; hier ergänze ich und widerspreche, jeweils mit Beleg.

- **Empfehlung:** Zustimmung zu „gezielt umbauen, klein, danach weiterbauen“ und gegen einen Neuaufbau.
- **Befund 1 bestätigt:** `grep -rn "<name>(" src` ohne `canon/sections.py` ergibt für `read_section`, `read_part`, `put_section`, `append_section` und `read_labelled` je 0 Aufrufer. Ergänzung: Die Funktionen sind nicht wertlos, weil sie die Regel gegen `tests/shared/sections.json` festhalten, die die Oberfläche tatsächlich benutzt. Ich empfehle deshalb für U.2 den ersten Weg: einen echten Nutzer geben. V.38 (SillyTavern-Export liest „Wesen“) und V.39 (Aussehen für Orte und Gegenstände) brauchen genau `read_section`; U.2 sollte mit V.38 zusammenfallen, statt die Funktionen erst zurückzunehmen und dann wieder einzuführen.
- **Befund 2 teilweise bestätigt:** Der Teilstring-Vergleich war Absicht (Docstring, Test `in der Stadt am eisenmeer`), das Risiko bei kurzen Weltnamen ist aber real: Für eine Welt „Ys“ würde „In Ysas Haus“ wegfallen. Ein Vergleich auf Wortgrenze behält „Im Eisenmeer“ und „In der Stadt am Eisenmeer“ und schließt das aus; Aufwand wenige Zeilen. Derzeit betrifft es niemanden (keine Gast-Verbindung auf dem Server, Zählung 2026-11-05).
- **Befund 3:** Einverstanden, dass ADR-103 die Vollständigkeit der Anfrage belegt, nicht die Textqualität. Die Textqualität deckt der getrennte Bestandteil „Kanon-Treue“ (`[BELASTBAR]` seit 4.8) und das Urteil des Eigentümers im Alltag. Ich stufe nicht zurück, präzisiere aber den Text in `docs/architecture.md` Abschnitt 6: „belegt ist die vollständige Anfrage, nicht die Qualität des Textes“.
- **Befund 5 und U.1:** Der Umbau hängt an den Bildthemen. Er sollte unmittelbar vor dem ersten Bildschritt (V.23, V.24 oder V.33) liegen, nicht unabhängig davon am Anfang einer Phase ohne Bildthemen. Wählt der Eigentümer die Bildthemen für Phase 10, kommt U.1 an deren Anfang; sonst zieht U.1 mit ihnen in die Planung der Phase danach.
- **Befund 8 und 9:** bestätigt (`docs/project-context.md:289`, `docs/architecture.md:243`; V.34, V.36 und V.37 mit Status `⏸️ VERSCHOBEN → 9.x`). Ich behebe das im Phasenabschluss. Die Zeilen „Aktueller Wert“ und „Stand“ in `decisions.md` Teil A kürze ich auf den aktuellen Stand und lege den Verlauf im Archiv ab; das ist Pflege, keine Methodik-Änderung.
- **Befund 6:** Einverstanden, dass kein Schritt nötig ist. Den Auslöser „3.000 Zeilen in einem Monat“ lege ich als Querschnitt-Schritt mit ID an, damit er einen Landeplatz hat (`CLAUDE.md` Abschnitt 6, „Keine Verschiebung ohne Landeplatz“).
