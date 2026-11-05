# Archiv – Fahrplan Phase 9

<!-- Quelle: docs/fahrplan.md, Abschnitt „Aktuelle Phasen". Ausgelagert am 2026-11-05 (CLAUDE.md Abschnitt 14:
     Phase vollständig erledigt). Abgedeckter Zeitraum: 2026-10-18 bis 2026-11-05. -->

## Aktuelle Phasen

### Phase 9: Verlässlicher Kanon, Bilder und Verwaltung – Typ: UMSETZUNG – ABGESCHLOSSEN (2026-11-05)

**Ziel:** Die Gliederung der Kanon-Einträge verlässlich machen (Pflichtfrage, ADR-089) und darauf die Befunde des Eigentümers umsetzen: gegliederte Einträge und Beziehungen, Bilder vom Bedarf her mit Herkunft und festem Modell, Löschen oder Archivieren, Verbrauch je Welt und Geschichte; dazu eine Erkundung zu Quellen und Recherche, der Ausbau der Gast-Figuren und eine erneute Prüfung der Kontexttreue.

**Abschlusskriterium:** Schritte 9.1–9.15 `[ERLEDIGT]`, `[VERWORFEN]` mit ADR oder `[VERSCHOBEN]` mit Ziel-Schritt.

**Reifegrad-Erwartung am Phasenende:** unverändert `[BELASTBAR]`; Datenmodell- und Ablauf-Entscheidungen (9.1, 9.3, 9.4, 9.6–9.9, 9.11, 9.13) werden per ADR entschieden, bevor gebaut wird; NFR Kontexttreue nach 9.14 `[BELASTBAR]` oder begründet `[VORLÄUFIG]`.

**Ursprünglicher Schrittplan:** 15 Schritte, festgehalten am 2026-10-18 (ADR-089, ADR-090). Wucherungs-Schwelle: Default aus `docs/project-context.md` Abschnitt 6 (Faktor 2 und mindestens 5 zusätzliche Schritte, also mehr als 30); neue Wünsche während der Phase werden V-Schritte mit Landeplatz 9.15.

**Reihenfolge (Eigentümer, 2026-10-18; ADR-090):** Fundament 9.1–9.2, Kanon 9.3–9.4, Bilder 9.5–9.8, Verwaltung 9.9–9.11, Erkundung 9.12, Gäste 9.13 (nach der Probe des Eigentümers), Kontexttreue 9.14; zuletzt 9.15.

**Pflichtfrage am Phasenende:** ADR-104 – weiterbauen mit drei kleinen Umbauten (Bewertung `docs/research/bewertung-phase-9.md`)

#### 9.1: Gliederung im Server verlässlich – Abschnitte und Namenserkennung

- **Status:** ✅ ERLEDIGT (2026-10-18) – Vorlage α/β vorgelegt (Empfehlung α, Konfidenz hoch); Eigentümer per Auswahlfrage: „A – Text mit Überschriften (Empfohlen)“ → ADR-091, Regel-003. PR #173: CI grün (4 von 4 Pflicht-Checks), auf Anweisung des Eigentümers zusammengeführt (`f479509`)
- **Phasentyp-Kontext:** UMSETZUNG (mit Vorlage zu Beginn)
- **Abhängigkeiten:** keine
- **Freigabepflichtig:** ja – zu Beginn Vorlage α (Abschnitte bleiben in Markdown, der Server kennt sie je Kategorie) gegen β (Felder im Dateikopf): Datenmodell (Kategorie 4). Der Umbau selbst bleibt innerhalb der Module, Schnittstellen höchstens additiv (ADR-089)
- **Empfohlene Klasse:** Entscheidung – Datenmodell-Weiche für V.35 G1/G2 (Eskalations-Auslöser 1).
- **Eingangskriterien:** alle berührten Bestandteile `[BELASTBAR]`
- **Anforderungen (ab Klasse M):** FR-002, FR-003
- **Zu tun:** Befunde 1 und 7 der Bewertung (`docs/research/bewertung-phase-8.md`). (1) Eine Regel für Abschnitte im Server (`canon`): Lesen, Ersetzen und Ergänzen nach der Regel aus `ui/src/sections.ts`; `render` (`context/parts.py`), Markdown-Import (`canon/importers/markdown.py`) und Aussehen (`context/appearance.py`) nutzen sie; gemeinsame Testfälle für Server und Oberfläche. (2) Namenserkennung (`ui/src/references.ts`, `context/writing.py`, `context/manuscript_hits.py`, `ui/src/canonFact.ts`) auf eine Regel bringen, Genitiv einheitlich. (3) Vorlage α/β mit der Sicht des Eigentümers („Verlässlichkeit“, V.35) und Vision 7 (lesbare Dateien, FR-020).
- **Akzeptanzkriterien:** Vorlage und ADR; dieselben Testfälle grün in Server und Oberfläche; „Aussehen“ wird an allen Stellen gleich gefunden – auch leer, doppelt, unterteilt; übriges Verhalten unverändert (Tests ohne geänderte Erwartungen); Anfrage beim Schreiben byte-gleich, sonst Probe nach Regel-002.
- **Betroffene Module:** canon, context, ui
- **Reifegrad-Wirkung:** keine (Datenmodell bleibt `[BELASTBAR]` nach ADR)
- **Artefakte:** Code, Tests, ADR
- **Notizen:** Aus ADR-089. Trägt 9.3–9.5 und 9.13. Umsetzung (ADR-091): `canon/sections.py`, `canon/names.py`, gemeinsame Testfälle `tests/shared/sections.json` (47 Fälle) und `tests/shared/names.json` (27 Fälle) in Server und Oberfläche; Vorlage und Import nehmen die Abschnittsnamen aus `SECTIONS` (Import erkennt jetzt „Wesen und Geschichte“); Namenserkennung an vier Stellen auf eine Regel. Lokal: pytest 886 grün, Abdeckung 99,85 % (`canon/sections.py` und `canon/names.py` je 100 %); vitest 459 grün, 98,66 / 95,35 / 97,87 / 98,85 % (Anweisungen / Zweige / Funktionen / Zeilen); Playwright 11 grün; ruff, mypy, bandit, eslint, prettier, tsc, Pre-Commit grün; bestehende Tests ohne geänderte Erwartungen (die Fälle aus `ui/src/sections.test.ts` liegen unverändert in der gemeinsamen Datei). Anfrage beim Schreiben unverändert: `find_references` alt und neu an 274 Kombinationen, 0 Unterschiede.

#### 9.2: End-to-End-Tests für die Abläufe der Phasen 6–8

- **Status:** ✅ ERLEDIGT (2026-10-18) – PR #175: CI grün (4 von 4 Pflicht-Checks; im Protokoll nur der bekannte Hinweis zu Ubuntu 26 → D.19, keine Bündelgrößen-Warnung), auf Anweisung des Eigentümers zusammengeführt (`65a0f13`)
- **Phasentyp-Kontext:** UMSETZUNG
- **Abhängigkeiten:** keine
- **Freigabepflichtig:** nein für die Tests; ja für das Umbenennen der CI-Schritte (Kategorie 7) – freigegeben mit ADR-090
- **Empfohlene Klasse:** Routine – Test-Erstellung und Testwartung.
- **Eingangskriterien:** keine
- **Anforderungen (ab Klasse M):** FR-029, FR-035
- **Zu tun:** Befund 3 der Bewertung: Playwright-Pfade für den Weltenbauer mit Übernahme-Fenster (8.8), „Abschnitt ersetzen“ (8.4) sowie Karte oder Bild (7.6, 7.10); Antwortformen des Servers gegen die Typen in `ui/src/api/` prüfen, soweit es ohne neues Werkzeug geht (ein Generator nur mit Vorlage, Kategorie 3). CI-Schrittnamen auf die geltenden Schwellen berichtigen (`.github/workflows/ci.yml` Zeilen 65 und 96).
- **Akzeptanzkriterien:** mindestens drei neue End-to-End-Tests grün in der CI; Schrittnamen nennen dieselben Schwellen wie `pyproject.toml` und `vite.config.ts`.
- **Betroffene Module:** ui, api (nur Tests)
- **Reifegrad-Wirkung:** keine
- **Artefakte:** Tests, CI-Konfiguration
- **Notizen:** Aus ADR-089. Umsetzung (Tests von Unteragenten der Routine-Klasse geschrieben, von der bauenden KI geprüft): vier neue Playwright-Tests in `e2e/skriptorium.spec.ts` gegen den echten Server, KI-Ströme im Browser ersetzt – Weltenbauer mit Übernahme-Fenster, Gespräch bleibt, zweite Fassung überschreibt (8.8); Bild hochladen, beschreiben lassen, „Aussehen“ ersetzen (7.6, 7.13, 8.4); Karte hochladen und markieren, Punkt führt zum Eintrag (7.10, 7.14); Karte beschreiben, Rückfrage abbrechen und „Darunter ergänzen“ (7.13, 8.4). Die Modellliste von OpenRouter ist in zwei Tests durch eine an `ModelList` typisierte Liste ersetzt (sonst hinge der Lauf am Netz). Antwortformen: `tests/api/test_ui_contract.py` zeichnet 73 echte Antworten und Strom-Ereignisse auf (`tests/shared/api-responses.json`), `ui/src/api/contract.test.ts` prüft sie mit der Compiler-API des vorhandenen `typescript` gegen die Typen in `ui/src/api/` – überzählige, fehlende und falsch getypte Felder, Werte außerhalb von Literal-Unionen; Gegenprobe mit fünf absichtlich beschädigten Antworten im selben Test. Kein neues Werkzeug. Gefunden: Das `start`-Ereignis von „Bild/Karte beschreiben“ und „Aussehen herauslösen“ trägt `web_search` (der Server nutzt den Strom des Weltenbauers), `DescribeEvent` kannte das Feld nicht – Typ auf den Weltenbauer-Strom umgestellt (nur Typ, keine Laufzeitwirkung, Server unverändert). CI-Schrittnamen: Python „global 99 %“, TypeScript „98 % Lines und Statements, 97 % Functions, 94 % Branches“ (ADR-090). Lokal: Playwright 15/15 (25,6 s; Unteragent drei Läufe je 15/15), pytest 887 (99,85 %; canon 100 %, context 99 %), vitest 467 (98,66 / 95,3 / 97,87 / 98,85 % Anweisungen / Zweige / Funktionen / Zeilen), ruff, mypy, bandit, pip-audit, eslint, prettier, tsc, npm audit grün.

#### 9.3: Gegliederte Einträge je Art (V.35 B2, G1/G2)

- **Status:** ✅ ERLEDIGT (2026-10-19) – entschieden mit Mockup (ADR-092); Code PR #177: CI grün (4 von 4 Pflicht-Checks), zusammengeführt (`5878215`); Proben mit echter KI (Regel-002 mit Nachlauf, Weltenbauer; Notiz unten) PR #179: CI grün (4 von 4), auf Anweisung des Eigentümers zusammengeführt (`273813d`); keine Verschlechterung; vom Eigentümer bestätigt (2026-10-19, im Chat: „9.3 bestätigt“)
- **Phasentyp-Kontext:** UMSETZUNG (mit Vorlage und Mockup zu Beginn)
- **Abhängigkeiten:** 9.1
- **Freigabepflichtig:** ja – Gliederung je Kategorie ist Datenmodell-Konvention (Kategorie 4); Anfrage des Weltenbauers (Kategorie 1)
- **Empfohlene Klasse:** Entscheidung – Datenmodell-Konvention (Eskalations-Auslöser 1).
- **Eingangskriterien:** 9.1 erledigt
- **Anforderungen (ab Klasse M):** FR-002, FR-029
- **Zu tun:** Für jede Kategorie eine feste Gliederung (z. B. Figur: Aussehen, Wesen, Geschichte, Beziehungen; eigene für Ort, Gegenstand, Regel, Kultur, Zeitlinie) – beim Anlegen von Hand (Vorlage, ADR-083) und durch den Weltenbauer (`context/worldbuilder.py`); der Import erkennt die Abschnitte (Fallstrick aus V.35: ein unbekannter Abschnitt auf Namensebene wird ein eigener Eintrag); Bestand bleibt lesbar.
- **Akzeptanzkriterien:** Vorlage mit Mockup und ADR; Tests je Kategorie; der Weltenbauer liefert gegliederte Einträge (Probe mit echter KI-Antwort); Eigentümer bestätigt.
- **Betroffene Module:** canon, context, ui
- **Reifegrad-Wirkung:** keine
- **Artefakte:** Code, Tests, ADR, Mockup
- **Notizen:** Aus V.35 (ADR-090). Entschieden 2026-10-18 mit Mockup vorher/nachher (Formular, Figur Anselm Drach, Ort Aschturm; Testwelt Salzmark) → ADR-092. Umsetzung (Unteragent der Routine-Klasse, geprüft und nachgebessert von der bauenden KI): `canon/sections.py` – `SECTIONS` je Art, frühere Namen (`FORMER_SECTIONS`: „Wesen und Geschichte“), `is_section_name` je Art, `drop_empty_sections`, `nest_headings`; gemeinsame Liste und Vorlagen-Fälle in `tests/shared/sections.json`, Spiegel und `templateFor` in `ui/src/sections.ts`; Import erkennt die Namen nur in Einträgen der passenden Art (Gruppe oder `Kategorie:`-Zeile), bei bekannter Art reicht ein fester Abschnitt, damit eine Überschrift ohne Text ein Eintrag bleibt (eigener Abschnitt wie „Herkunft“ zerfällt nicht – Nachbesserung der bauenden KI); Formular mit Vorlage, Wechsel der Art, Hinweis, 12 Zeilen; Weltenbauer-Rahmen aus `SECTIONS`; `render` rückt die Überschriften eines Eintrags unter den Namen (Ebene 3) und lässt leere Abschnitte weg. Messung an den Testwelten: alle 52 Einträge ändern sich in der Anfrage (ihr Text beginnt mit `# Name`, wird `### Name`), +104 Zeichen gesamt, keine leeren Abschnitte. Lokal: pytest 931 (99,85 %; canon 100 %, context 99 %), vitest 485 (98,67 / 95,29 / 97,88 / 98,86 %), Playwright 15/15, ruff, mypy, bandit, eslint, prettier, tsc grün; Bildschirmfotos des echten Formulars (Desktop, Smartphone) entsprechen dem Mockup. Befund SillyTavern-Export → V.38.
  - **Offene Proben (Cloud-Session, Branch `feat/9.3-gegliederte-eintraege`):** (1) Regel-002 mit `spikes/regel-002/lauf.py`: `VARIANTE=vorher` auf `main`, `VARIANTE=nachher` auf dem Branch, je 3 Läufe an Salzmark und Glimmergrund, Modell grok-4.6, Länge mittel; Auswertung mit `auswertung.py` – Wirkung nur, was in beiden Geschichten außerhalb der Vorher-Spannweite liegt; erwartet: keine Verschlechterung. (2) Weltenbauer mit echter Antwort in der Salzmark: je eine neue Figur, ein Ort, ein Gegenstand, eine Kultur; geprüft wird, dass die Abschnitte der Art in der Reihenfolge stehen, leere fehlen, nichts erfunden ist und die Import-Vorschau jeden Eintrag ganz lässt.
  - **Zweiter Versuch (2026-10-19, Cloud-Session):** nicht gelaufen – die Session lief in der Umgebung „Flight_Research“, `OPENROUTER_API_KEY` nicht gesetzt (Logbuch); keine Kosten. Vorbereitet ohne KI: `spikes/weltenbauer-9.3/probe.py` mit README (Aufträge mit `@Kerrow`, `@Tomas Rehl`, `@Totensitte`, damit Texte vorhandener Einträge mitgehen und Widersprüche prüfbar sind; Prüfung (a), (b), (d) maschinell, Trockenlauf und Selbsttest der Prüflogik grün). Vorher-Stand geprüft: ein Worktree auf `2ac204b` nutzt seinen eigenen Code; die erste Anfrage der Kette ändert sich wie erwartet (Salzmark 38 → 9 Überschriften der Ebene 1, +61 Zeichen; Glimmergrund 36 → 13, +46 Zeichen).
  - **Dritter Versuch (2026-10-19, Cloud-Session in der Umgebung „OPENROUTER_API_KEY“, Branch `spike/9.3-proben-ki`):** beide Proben gelaufen, Kosten zusammen ca. 2,99 $. (1) Regel-002 (vorher `2ac204b`, nachher `40a02eb` = `src/` von `1371264`, 12 Ketten, 84 Vorschläge, alle `stop`): gezählt keine Wirkung – einzig „wörtlich %“ liegt in beiden Geschichten außerhalb der Vorher-Spannweite, aber gegenläufig (Salzmark 0,40 gegen 0,44–0,76; Glimmergrund 0,71 gegen 0,00–0,39). Widersprüche zum Kanon (verblindet, getrennte Instanz): nachher je Geschichte 1 eindeutiger in 3 Ketten (Salzmark: Totenname am Abend; Glimmergrund: „mein Teuerster“ zu Wendt), vorher 0 – nach dem Wortlaut von Regel-002 ein Befund; die Rate entspricht der von grok-4.6 aus 5.26, beide Einzelheiten stehen in beiden Ständen im Wortlaut in der Anfrage (Deutung: Streuung; klären nur weitere Läufe). Einzelheiten `spikes/regel-002/README.md`. (2) Weltenbauer: alle vier Aufträge gegliedert je Art in Reihenfolge, Ebene 3, kein Füllwerk, Import ganz; zwei knappe Abweichungen vom Kanon (Siegelring am Haken im Zollhaus – Text des Rings war nicht in der Anfrage; Fischerin „meidet den Südhafen“, obwohl der Nordkai dazugehört); `spikes/weltenbauer-9.3/README.md`. Nachlauf auf Wahl des Eigentümers („3 weitere Läufe je Seite“, 2,90 $): über je 6 Ketten liegt keine Kennzahl – gezählt oder von Hand – nachher in beiden Geschichten außerhalb der Vorher-Spannweite; eindeutige Widersprüche vorher 1, nachher 2 in je 12 Ketten (Glimmergrund vorher jetzt ebenfalls 1) – der Befund war Streuung, nach Regel-002 keine Wirkung und keine Verschlechterung. Gesamtkosten der Proben 5,88 $. Eigentümer bestätigt 9.3 am 2026-10-19.

#### 9.4: Beziehungen mit Art und Rückverweis (V.35 B3)

- **Status:** ✅ ERLEDIGT (2026-10-21) – eingespielt (`67fc36e`), vom Eigentümer bestätigt („9.4 funktioniert, der Block erscheint“). Verlauf: 🟠 IN ARBEIT (seit 2026-10-19) – Vorlage vorgelegt, Eigentümer per Auswahlfragen: 1A, 2A, Weltenbauer beide Seiten, 4A → ADR-093
- **Phasentyp-Kontext:** UMSETZUNG (mit Vorlage zu Beginn)
- **Abhängigkeiten:** 9.1, 9.3
- **Freigabepflichtig:** ja – Datenmodell-Konvention (Kategorie 4), ggf. Anfrage-Zusammenstellung (Kategorie 1); ADR-088 hatte ein Feld „Verbunden mit“ verworfen
- **Empfohlene Klasse:** Entscheidung – Datenmodell und Kontext-Zusammenstellung (Eskalations-Auslöser 1).
- **Eingangskriterien:** 9.3 erledigt
- **Anforderungen (ab Klasse M):** FR-002, FR-013
- **Zu tun:** Beziehungen zwischen Figuren sichtbar und gegliedert festhalten (z. B. Abschnitt „Beziehungen“ mit Art: „verheiratet mit @Kael“), auch wenn der Weltenbauer mehrere Figuren in einem Auftrag anlegt; anzeigen, wer auf einen Eintrag verweist; Wirkung auf die Auffüllung nach ADR-088 prüfen.
- **Akzeptanzkriterien:** Vorlage und ADR; Tests; Probe nach Regel-002, falls die Anfrage beim Schreiben betroffen ist; Eigentümer bestätigt.
- **Betroffene Module:** canon, context, ui
- **Reifegrad-Wirkung:** keine
- **Artefakte:** Code, Tests, ADR
- **Notizen:** Aus V.35 (ADR-090). Entschieden 2026-10-19 → ADR-093. Umsetzung (Cloud-Session 2026-10-19): `RELATIONS` in `canon/sections.py` und gespiegelt in `ui/src/sections.ts` (Regel-003); `ui/src/relations.ts` (`relationsOf`, `incomingOf`) nach Abschnitts- und Namensregel; Block „Verweise hierher“ (`ui/src/views/IncomingLinks.tsx`) unter jedem Eintrag der eigenen Welt; Rahmen des Weltenbauers (`context/worldbuilder.py`) mit Zeile je Beziehung, beiden Seiten und vorhandener Figur nur mit Text in der Anfrage. Anfrage beim Schreiben unverändert; die des Weltenbauers +163 geschätzte Token (`tests/shared/api-responses.json` 994 → 1.157). Probe mit echter KI (`spikes/weltenbauer-9.4/README.md`, grok-4.6, 0,037 $): drei von drei Aufträgen mit Beziehung je Zeile, beiden Seiten und ganzem Import; Tomas Rehl überarbeitet ohne Verlust, Ilka Varn (ohne `@`) nicht angefasst, Gegenseite im Gespräch genannt. Lokal: pytest 932 (99 %; `canon/sections.py`, `context/worldbuilder.py` je 100 %), vitest 492 (98,68 / 95,36 / 97,9 / 98,88 % Anweisungen / Zweige / Funktionen / Zeilen; `relations.ts`, `IncomingLinks.tsx` 100 %), Playwright 15/15, ruff, mypy, bandit, eslint, prettier, tsc grün. Offen: CI, Bestätigung des Eigentümers.

#### 9.5: Bilder vom Bedarf her; Karte aus den Orten (V.35 G4, B4)

- **Status:** ✅ ERLEDIGT (2026-10-25) – PR #184 mit grüner CI zusammengeführt (`e886916`), vom Eigentümer bestätigt (2026-10-25, im Chat: „9.5 ist bestätigt“). Verlauf: 🟠 IN ARBEIT (seit 2026-10-21) – Vorlage mit Tabelle je Bildart vorgelegt (Zählung im Betrieb), Eigentümer per Auswahlfragen: Karte 1B, fehlendes Aussehen 2A, Gegenstand 3A, Herauslösen nur Figuren → ADR-094; Herauslösen für Gegenstände und Orte → V.39. Mockup freigegeben (alle Orte vorab angekreuzt). Umgesetzt (nur `ui`): `imagePrompts.ts` (`entryPrompt` je Art, `lacksAppearance`, `mapPrompt` mit Orten, Grenze 1.500 Zeichen für Karten), `ImageGenerate` (Hinweis als Element, Platz für Auswahl, Textfeld folgt neuer Vorbelegung), `EntryImages` (Hinweis mit Knopf), `AddMap` (Ortsliste), `LOCATION`/`PURPOSE` in `sections.ts` (Regel-003). Tests: vitest 498 (`imagePrompts.ts`, `AddMap.tsx`, `EntryImages.tsx` je 100 % Zeilen), Playwright 15, pytest 932
- **Phasentyp-Kontext:** UMSETZUNG (mit Vorlage zu Beginn)
- **Abhängigkeiten:** 9.3
- **Freigabepflichtig:** ja – ändert die Vorbelegung aus ADR-084
- **Empfohlene Klasse:** Entscheidung – Änderung einer per ADR festgelegten Vorbelegung (Eskalations-Auslöser 1).
- **Eingangskriterien:** 9.3 erledigt
- **Anforderungen (ab Klasse M):** FR-035
- **Zu tun:** Je Bildart (Figur, Gegenstand, Ort, Karte, Sonstiges) festlegen, welche Angaben das Bild braucht, und prüfen, ob sie nach 9.3 verlässlich vorliegen (G4); „Karte erzeugen“ mit den Orten der Welt vorbelegen statt nur mit „Geografie – Name der Karte“ (B4, `ui/src/imagePrompts.ts`).
- **Akzeptanzkriterien:** Vorlage mit Tabelle je Bildart und ADR; Tests; Eigentümer bestätigt.
- **Betroffene Module:** ui, ggf. canon
- **Reifegrad-Wirkung:** keine
- **Artefakte:** Code, Tests, ADR
- **Notizen:** Aus V.35 (ADR-090).

#### 9.6: Herkunft von Bildern – Modell und Anweisung speichern (V.35 B1)

- **Status:** ✅ ERLEDIGT (2026-10-25) – eingespielt `adda4b9`, vom Eigentümer bestätigt („9.6 hat erfolgreich funktioniert“). Verlauf: 🟠 IN ARBEIT (seit 2026-10-25) – Vorlage vorgelegt, Eigentümer per Auswahlfragen: Begleitdatei, aufklappbar mit „Neu erzeugen“, mit Kosten, Nebenfrage KI-Text später → ADR-095, V.42. Umgesetzt (Notiz); PR #187: CI grün (4 von 4), auf Anweisung des Eigentümers zusammengeführt (`b66196e`); eingespielt und geprüft (siehe oben)
- **Phasentyp-Kontext:** UMSETZUNG (mit Vorlage zu Beginn)
- **Abhängigkeiten:** keine
- **Freigabepflichtig:** ja – neue Angaben im Dateikopf (Kategorie 4)
- **Empfohlene Klasse:** Entscheidung – Datenmodell (Eskalations-Auslöser 1).
- **Eingangskriterien:** keine
- **Anforderungen (ab Klasse M):** FR-035
- **Zu tun:** Beim Übernehmen eines erzeugten Bildes Modell und Anweisung mit dem Bild ablegen (Kopffeld `bilder`, `canon/images.py`), ebenso bei Titelbildern und Karten; in der Oberfläche anzeigen. Nebenfrage aus V.35 mit vorlegen: auch für KI-Text die vollständige Anfrage festhalten?
- **Akzeptanzkriterien:** Vorlage und ADR; Tests; Bilder ohne Angaben bleiben gültig; Eigentümer bestätigt.
- **Betroffene Module:** canon, manuscript, api, ui
- **Reifegrad-Wirkung:** keine
- **Artefakte:** Code, Tests, ADR
- **Notizen:** Aus V.35 (ADR-090). Umsetzung (ADR-095): `storage/origins.py` (`ImageOrigin`, Felder `modell`, `anweisung`, `seitenverhaeltnis`, `kosten_usd`, `datum`), `DocumentStore.write_image(..., origin)` schreibt `<bild>.herkunft.yml`, `read_image_origin`, `delete_image` löscht sie mit (auch wenn das Bild von Hand gelöscht wurde); `canon` (Eintragsbild, Karte) und `manuscript` (Titelbild) reichen durch, `api` nimmt optional `herkunft` an (Länge und Form geprüft, Datum vom Server) und liest sie über `…/origin` (`null` ohne Herkunft). Oberfläche: `ImageGenerate` übergibt beim Übernehmen Modell, Anweisung, Format und gemeldete Kosten und nimmt ein vorgewähltes Modell an; `ImageOriginPanel` zeigt „Herkunft“ aufklappbar in der großen Ansicht von Eintragsbild und Karte, beim Titelbild unter dem Bild (es hat keine große Ansicht), mit „✨ Mit dieser Anweisung neu erzeugen“ (öffnet „Bild erzeugen“ bzw. „Karte erzeugen“ vorbelegt; nicht, wenn die Höchstzahl erreicht ist). Hochgeladene und vor 9.6 erzeugte Bilder zeigen nichts. Beim reinen Hochladen bleibt der Körper unverändert (kein `herkunft`). Tests: pytest 956 (Abdeckung 99 %; `storage/origins.py`, `storage/store.py`, `canon/images.py`, `canon/maps.py`, `manuscript/stories.py`, `api/*_routes.py` je 100 %), `test_security.py` zählt 3 neue geschützte Routen; vitest 506 (98,72 / 95,35 / 97,97 / 98,91 % Anweisungen / Zweige / Funktionen / Zeilen; `ImageOriginPanel.tsx` 100 %), 7 bestehende Komponenten-Tests auf die zusätzlichen Abfragen und den neuen Körper angepasst (Hilfe `withoutOrigins` in `ui/fake-api.ts`); Playwright 15/15; ruff, mypy --strict, bandit, eslint, prettier, tsc grün.

#### 9.7: Einstellungsseite – Modell je Aufgabe (V.35 G3, B6)

- **Status:** ✅ ERLEDIGT (2026-10-26) – eingespielt `7bc5333`, vom Eigentümer bestätigt („Funktioniert alles.“). Verlauf: 🟠 IN ARBEIT (seit 2026-10-25) – Mockup vorher/nachher und Vorlage vorgelegt, Eigentümer per Auswahlfragen: eigene Seite „Einstellungen“, Wahl in der Aufgabe nur für dieses Mal, Ablage in `system/modelle.md` → ADR-096. Umgesetzt in `api` und `ui` (Commits `9a7e5aa`, `6252f35`): Kopffeld `aufgaben` in `system/modelle.md` (Favoriten und Aufgaben erhalten einander), `GET /api/models` mit `tasks`, `PUT /api/models/aufgaben`, Auflösung Anfrage → Modell der Geschichte (nur Schreiben) → Einstellung im Angebot → Voreinstellung für Schreiben, Weltenbauer, Aussehen, Kurzfassung und Gesamtzusammenfassung (jetzt mit dem ganzen Katalog), `GET /api/images/models` mit gespeichertem Bildmodell; Seite „Einstellungen“ (`ui/src/views/Settings.tsx`, Knopf in der Leiste), Vorbelegung in Schreiben, Weltenbauer, Bild beschreiben, Aussehen herauslösen, Bild erzeugen. Prüfungen: pytest 978 (gesamt 99,85 %; `favorites.py`, `writing_routes.py`, `image_routes.py` je 100 %), vitest 521 (98,75 % Zeilen, 95,5 % Zweige; `Settings.tsx` 100 % Zeilen), Playwright 15/15, ruff, mypy --strict, eslint, prettier, tsc grün; lokal mit echtem Katalog geprüft (Speichern, Neuladen, Smartphone-Breite); PR #190: CI grün (4 von 4, keine neue Warnung im Protokoll), auf Anweisung des Eigentümers zusammengeführt (`7bc5333`), CI auf `main` grün, eingespielt 2026-10-26, vom Eigentümer bestätigt
- **Phasentyp-Kontext:** UMSETZUNG (mit Mockup und Vorlage zu Beginn)
- **Abhängigkeiten:** keine
- **Freigabepflichtig:** ja – neue Ablage unter `system/` und neue Endpunkte (Kategorien 4 und 5, additiv)
- **Empfohlene Klasse:** Entscheidung – Datenmodell und API-Vertrag (Eskalations-Auslöser 1).
- **Eingangskriterien:** keine
- **Anforderungen (ab Klasse M):** FR-018, FR-028
- **Zu tun:** Eine Seite, auf der der Eigentümer je Aufgabe ein Modell festlegt – Schreiben (Voreinstellung), Weltenbauer, Kapitel-Kurzfassung, Gesamtzusammenfassung, Bild beschreiben, Aussehen herauslösen, Bilder erzeugen – nach dem Muster der Favoriten (ADR-055); das Bildmodell wird gespeichert (B6). Das Modell je Geschichte (ADR-023) bleibt.
- **Akzeptanzkriterien:** Mockup und ADR; Tests; Eigentümer bestätigt.
- **Betroffene Module:** api, ai_gateway, ui
- **Reifegrad-Wirkung:** keine
- **Artefakte:** Code, Tests, ADR, Mockup
- **Notizen:** Aus V.35 (ADR-090).

#### 9.8: Bild zu Bild (V.35 B7)

- **Status:** ✅ ERLEDIGT (2026-10-26) – eingespielt `48b8f8f`, vom Eigentümer bestätigt („Funktioniert“, zugleich erste echte Probe mit einem Bild). Verlauf: 🟠 IN ARBEIT (seit 2026-10-26) – Mockup vorher/nachher und Vorlage (Modelle mit Grundlage und Preise aus der Modellliste von OpenRouter) vorgelegt; Eigentümer per Auswahlfragen: genau ein Ausgangsbild, nur gespeicherte Bilder → ADR-097. Umgesetzt in `ai_gateway`, `storage`, `api`, `ui` (Commits `043cf52`, `9f27d2a`, `49054fc`, `301bd67`, Nachbesserung nach Prüfung); nebenbei: Preis des Ergebnisbildes liest nur noch Zeilen `output_image` (FLUX.2 Flex nennt das Eingabebild zuerst). Titelbild präzisiert: aus dem Titelbild erzeugt, ersetzt das neue das bisherige (eine Geschichte hat ein Titelbild). Prüfungen: pytest 999 (99,85 %; `images.py`, `openrouter_images.py`, `image_routes.py`, `origins.py` je 100 %), vitest 532 (98,8 % Zeilen, 95,6 % Zweige), Playwright 15/15, ruff, mypy --strict, bandit, eslint, prettier, tsc grün. Getrennte Prüfung (Kategorie 6, 2026-10-26, Sonnet 5.5 ohne Gesprächsverlauf, nur Diff und Bedrohungsmodell): keine Befunde hoch/mittel; Befund 1 (niedrig, zu lange Bezeichnung der Grundlage → 422 nach bezahltem Bild) behoben; optional vorgelegt: Bezeichnung trimmen und Steuerzeichen ablehnen, Bezeichnung gegen die Grundlage prüfen, Obergrenze der Anfrage an den Anbieter, Anbieterpreise auf Endlichkeit prüfen – vom Eigentümer abgelehnt („Die optionalen Härtungen lassen wir weg.“, 2026-10-26). Echte Probe lokal nicht möglich (Schlüssel 401) → mit der Prüfung des Eigentümers nach dem Einspielen; PR #192: CI grün (4 von 4, keine neue Warnung im Protokoll), auf Anweisung des Eigentümers zusammengeführt (`48b8f8f`); Einspielen zunächst zurückgestellt, dann auf Anweisung („Doch einspielen“) eingespielt 2026-10-26, vom Eigentümer geprüft und bestätigt
- **Phasentyp-Kontext:** UMSETZUNG (mit Vorlage zu Beginn)
- **Abhängigkeiten:** 9.6
- **Freigabepflichtig:** ja – Bild geht an den Anbieter (Kategorie 6 prüfen), neue Eingabe der Schnittstelle (Kategorie 5)
- **Empfohlene Klasse:** Entscheidung – neuer Ablauf mit Datenfluss nach außen (Eskalations-Auslöser 1).
- **Eingangskriterien:** 9.6 erledigt (Herkunft auch für abgeleitete Bilder)
- **Anforderungen (ab Klasse M):** FR-035
- **Zu tun:** Ein vorhandenes Bild als Grundlage einer Bilderzeugung nutzen (`ai_gateway/images.py`, `ImageOrder`); welche Modelle über OpenRouter das können und was es kostet, gehört in die Vorlage; getrennte Prüfung, falls Kategorie 6 berührt ist.
- **Akzeptanzkriterien:** Vorlage mit unterstützten Modellen und Kosten, ADR; Tests; Probe mit echtem Bild; Eigentümer bestätigt.
- **Betroffene Module:** ai_gateway, api, ui
- **Reifegrad-Wirkung:** keine
- **Artefakte:** Code, Tests, ADR
- **Notizen:** Aus V.35 (ADR-090). V.33 (Bilder beim Schreiben mitschicken) ist etwas anderes und bleibt bei 9.15.

#### 9.9: Geschichten, Welten und Kapitel löschen oder archivieren (V.35 B5)

- **Status:** ✅ ERLEDIGT (2026-11-04) – zusammengeführt (PR #195), eingespielt `e52d69a`; Eigentümer prüfte mit einer Wegwerf-Welt und bestätigte („9.9 passt“)
- **Phasentyp-Kontext:** UMSETZUNG (mit Vorlage und Mockup zu Beginn)
- **Abhängigkeiten:** keine
- **Freigabepflichtig:** ja – Löschen ist destruktiv (`CLAUDE.md` Abschnitt 8, Kriterium 6), Datenmodell und API (Kategorien 4 und 5)
- **Empfohlene Klasse:** Entscheidung – destruktiver Ablauf und Datenmodell (Eskalations-Auslöser 1).
- **Eingangskriterien:** keine
- **Anforderungen (ab Klasse M):** FR-036 (angelegt 2026-11-04)
- **Zu tun:** ~~Für Geschichten, Welten und Kapitel klären, ob gelöscht, archiviert oder beides; Kaskade festlegen; Rückweg benennen~~ – entschieden 2026-11-04, ADR-098 (Mockup `mockup-9.9.html`, lokal). Umsetzung nach ADR-098: (1) `storage`: Ordner löschen samt Indexzeilen; (2) `canon`/`manuscript`: Kopffeld `archiviert`, Archivieren/Zurückholen, endgültiges Löschen von Welt und Geschichte nur für Archiviertes, Kapitel löschen mit Umnummerierung von Kapiteln und `verlauf/NN.md`, Kurzfassungen der nachrückenden Kapitel als veraltet; (3) `api`: Routen, Vorschau der Löschfolgen, Entfernen der Gast-Verbindungen samt Fakten und geführten Figuren in Geschichten anderer Welten, Name als Bestätigung; (4) `ui`: Bereich „Archiv“ in den Listen, Dialog mit Folgenliste und Eintippen des Namens, Kapitel löschen; archivierte Welt nicht als neue Gast-Quelle.
- **Akzeptanzkriterien:** Vorlage mit Mockup und ADR (erledigt 2026-11-04); Tests der Kaskade (Welt mit Gästen in fremder Welt, Geschichte, mittleres Kapitel mit Verlauf); Akzeptanzkriterium FR-036; Eigentümer bestätigt.
- **Betroffene Module:** canon, manuscript, storage, api, ui
- **Reifegrad-Wirkung:** keine
- **Artefakte:** Code, Tests, ADR, Mockup
- **Notizen:** Aus V.35 (ADR-090).
- **Umgesetzt (lokal, 2026-11-04, noch nicht abgenommen):** (1)–(4) nach ADR-098 auf dem Arbeitszweig; neun neue Routen (Routenzahl 71 → 80, alle mit Sitzung). Neue Tests: Python 38 (storage 9, canon 7, manuscript 12, api 8, context 2; Vertragsdatei neu geschrieben; Gesamtlauf 1030 bestanden, rot nur die 7 bekannten Pwned-Passwords-Fälle der Cloud-Umgebung; Abdeckung 99,67 %, canon 100 %, context 99,64 %), Oberfläche 13 (12 in `Archive.test.tsx`, 1 in `Summary.test.tsx`; 545 bestanden; Abdeckung 98,84 / 95,70 / 98,23 / 99,01 % Anweisungen/Zweige/Funktionen/Zeilen), E2E 15 bestanden (unverändert, kein neuer Fall). Kurzfassungen der nachrückenden Kapitel (Entscheidung des Eigentümers 2026-11-04, „A“): neuer Wert `veraltet` für `kurzfassung_status`; beim Nachrücken werden `erzeugt` und `geprüft` zu `veraltet`, `fehlt` bleibt. Neu erstellen setzt wie bisher `erzeugt`, Bestätigen `geprüft`; in der Anfrage an die KI zählt eine veraltete Kurzfassung wie eine erzeugte. Oberfläche: Status „veraltet – nach dem Löschen eines Kapitels neu erzeugen“ als Warnhinweis, Markierung am Reiter „Kurzfassung“, Rückfrage vor dem Löschen nennt die Markierung. `TODO(fahrplan-ref: 9.9)` entfernt; nichts mehr offen.

#### 9.10: Cache-Treffer der KI-Anbieter festhalten (V.36)

- **Status:** ✅ ERLEDIGT (2026-11-04) – Messung (4) im Logbuch, Eigentümer bestätigt („Ja, 9.10 erledigt“). Verlauf: Eigentümer wählte am 2026-11-04 **C** (Empfehlung): Verbrauchsdatei bekommt `cache_gelesen` und `cache_geschrieben` jetzt, Anzeige mit der Statistik von 9.11 → ADR-099. Vorher wartete der Schritt auf Freigabe (Vorlage A nur Protokollzeile / B Datei und Anzeige / C, Entwurfs-PR #196). Protokollzeile in jedem Fall (freigabefrei). Messung (4) braucht echte Anfragen – erst nach dem Einspielen (Mac-Session bzw. Alltag), in der Cloud-Session kein Schlüssel. Bestand vorher: Verbrauchszeile `zeit`, `art`, `modell`, `ergebnis`, `token_ein`, `token_aus`, `kosten_usd` (`api/usage.py`)
- **Phasentyp-Kontext:** UMSETZUNG
- **Abhängigkeiten:** keine
- **Freigabepflichtig:** wie V.36 – nein für die Protokollzeile; ja, falls Verbrauchsdateien oder `/api/usage` ein neues Feld bekommen (Kategorien 4 bzw. 5, additiv)
- **Empfohlene Klasse:** Routine – klar umrissene Erweiterung des Adapters mit Tests; Entscheidung, falls Verbrauchsdateien oder `/api/usage` erweitert werden.
- **Eingangskriterien:** keine
- **Anforderungen (ab Klasse M):** keine (Kostenziel Vision 4)
- **Zu tun:** wie V.36.
- **Akzeptanzkriterien:** wie V.36.
- **Betroffene Module:** ai_gateway, ggf. api und ui
- **Reifegrad-Wirkung:** keine
- **Artefakte:** Code, Tests, Logbuch-Eintrag, ggf. ADR
- **Notizen:** Aus V.36 (ADR-090).
- **Umgesetzt (2026-11-04, Cloud-Session, noch nicht abgenommen):** (1) `Usage` um `cache_read_tokens`/`cache_write_tokens` (Vorgabe `None`), der OpenRouter-Adapter liest sie aus `usage.prompt_tokens_details` (`cached_tokens`, `cache_write_tokens`; Ort laut Dokumentation „Prompt Caching“ geprüft); fehlende, fehlerhafte oder auf oberster Ebene gemeldete Werte bleiben `None`. (2) Protokollzeile `ki_anfrage … kosten_usd=… cache_gelesen=… cache_geschrieben=…`. (3) nach ADR-099 (C): Verbrauchszeile mit `cache_gelesen`, `cache_geschrieben`; Monatssumme und `/api/usage` unverändert, Vertragstest unverändert. Tests: ai_gateway 8 neue Fälle (davon 5 mit fehlenden oder fehlerhaften Werten) und 1 erweiterter, api 1 neuer und 1 erweiterter; pytest 1046 grün, Abdeckung 99,86 %, `openrouter.py`, `provider.py`, `api/usage.py` 100 % Zeilen; ruff, ruff format, `mypy --strict`, bandit grün. Oberfläche nicht berührt. Offen: (4) Messung an echten Anfragen nach dem Einspielen, Bestätigung des Eigentümers.
- **Messung (4) (2026-11-04, eingespielt `7319b26`):** Testanfragen des Eigentümers, `qwen/qwen3.8-max-0902` über Alibaba. Zweite gleiche Anfrage: Schreiben 99,7 % der Eingabe aus dem Zwischenspeicher (0,0546 $ → 0,0155 $), Weltenbauer 98,2 % (0,0269 $ → 0,0134 $), Kurzfassung 99,6 % (0,0533 $ → 0,0114 $); Gesamtzusammenfassung (ca. 1.550 Token) ohne Treffer; `cache_geschrieben` meldet Alibaba nie. Gelesene Eingabe kostet ein Achtel. Einzelheiten Logbuch 2026-11-04 22:20. Eigentümer bestätigte am 2026-11-04.

#### 9.11: Verbrauchsstatistik je Welt und je Geschichte (V.37)

- **Status:** ✅ ERLEDIGT (2026-11-04) – eingespielt `7319b26`, Eigentümer bestätigt („9.11 passt“). Verlauf: Bestandsaufnahme, Zählung auf dem Server und Mockup vorher/nachher vorgelegt; Eigentümer per Auswahlfragen: Ort A (eigene Seite „Verbrauch“), Speicher 1 (Format bleibt, libyaml), Zuordnung nach Vorschlag → ADR-100, FR-037. Begonnen, während 9.10 noch auf die Messung (4) wartet: Der Code von 9.10 liegt vor (Cache-Felder), das Eingangskriterium ist inhaltlich erfüllt – Abweichung mit Zustimmung des Eigentümers („dann 9.11“)
- **Phasentyp-Kontext:** UMSETZUNG (mit Vorlage und Mockup zu Beginn)
- **Abhängigkeiten:** 9.10
- **Freigabepflichtig:** ja – wie V.37: Datenmodell (Option C aus ADR-023, Kategorie 4), neuer Endpunkt (Kategorie 5, additiv)
- **Empfohlene Klasse:** Entscheidung – Datenmodelländerung gegen eine bestehende Entscheidung (Eskalations-Auslöser 1).
- **Eingangskriterien:** 9.10 erledigt
- **Anforderungen (ab Klasse M):** FR-037 (angelegt 2026-11-04)
- **Zu tun:** ~~wie V.37; dazu das Speicherlayout der Verbrauchsdateien entscheiden – Befund 2 der Bewertung (je Anfrage wird die ganze Monatsdatei neu geschrieben: 83 ms bei 400, 431 ms bei 2.000 Einträgen) mit der echten Zahl der Anfragen je Monat auf dem Server (nur Anzahl, lesend).~~ – entschieden 2026-11-04, ADR-100 (Mockup `mockup-9.11.html`, lokal; Zählung: 2026-10 1.094, 2026-11 bis zum 04. 81 Anfragen). Umsetzung nach ADR-100: (1) `storage`: Dateikopf über libyaml lesen und schreiben, Rückfall ohne libyaml, gleiche strenge Regeln; (2) `api`: Verbrauchszeile mit `welt` und `geschichte` aus allen Abläufen, `POST /api/images/generate` mit optionalem Ziel, `GET /api/usage/stats`; (3) `ui`: Seite „Verbrauch“ (Tabelle bzw. Karten, Zeitraum, Aufklappen, Art, Modelle sortierbar), Ziel beim Bild erzeugen, Verweis im Konto.
- **Akzeptanzkriterien:** wie V.37 (Vorlage mit Mockup und ADR erledigt 2026-11-04); Tests für Zuordnung je Ablauf, Summen, Sortierung, alte Zeilen ohne Welt, gelöschte Welt; Summen je Welt plus „ohne Zuordnung“ ergeben die Monatssumme; gleiche Ergebnisse beider YAML-Leser an den gemeinsamen Testfällen; Bildschirmfotos Desktop und Smartphone; Eigentümer bestätigt.
- **Betroffene Module:** storage, api, ui
- **Reifegrad-Wirkung:** keine (Datenmodell bleibt `[BELASTBAR]` nach ADR)
- **Artefakte:** Code, Tests, ADR, Mockup
- **Notizen:** Aus V.37 (ADR-090).
- **Umgesetzt (lokal, 2026-11-04, noch nicht abgenommen):** (1) `storage/frontmatter.py`: Leser und Schreiber auf libyaml (`FAST`), Rückfall `PURE`; alle Fälle von `tests/storage/test_frontmatter.py` laufen mit beiden, gleicher Text für beide; 64 Markdown-Dateien des Repos mit beiden gelesen und neu geschrieben – 0 Unterschiede. (2) `api/usage.py`: `recorder(welt, geschichte)` prüft die Kennungen und hängt `welt`/`geschichte` an jede Zeile; `stats(monat | None)` mit `Totals`, `Group`, `WorldGroup`, `UsageStats`; neue Datei `api/usage_routes.py` mit `GET /api/usage/stats` (Routen 80 → 81, mit Sitzung); Schreiben, Kurzfassung, Gesamtzusammenfassung, Weltenbauer, Aussehen, Bild beschreiben und Bild erzeugen (`world`/`story` im Körper) ordnen zu. (3) `ui`: Seite `views/Usage.tsx` unter `/verbrauch` mit Knopf „Verbrauch“ in der Leiste, Tabelle bzw. Karten auf dem Smartphone, Zeitraum, Aufklappen, Art, Modelle sortierbar; `ImageGenerate` mit Pflichtangabe `target`; Verweis im Konto. Prüfungen: pytest 1094 grün (neu `tests/api/test_usage_stats.py` 13 Fälle, Frontmatter 33 Fälle je Leser), Abdeckung 99,86 %, `usage.py`, `usage_routes.py`, `frontmatter.py`, `image_routes.py`, `writing_routes.py` je 100 %; vitest 551 grün (neu `Usage.test.tsx` 6), 98,83 / 95,57 / 98,2 / 99 % Anweisungen / Zweige / Funktionen / Zeilen (`Usage.tsx` 100 % Zeilen, 91 % Zweige); Playwright 15/15 mit neu gebauter Oberfläche; ruff, mypy --strict, eslint, prettier, tsc grün; Vertragsdatei um `usageStats` ergänzt (nur hinzugefügt). Bildschirmfotos der echten Seite (Desktop 1280 px, Smartphone 375 px, Testwelten Salzmark und Glimmergrund) entsprechen dem Mockup; auf dem Smartphone Hintergrund der Unterzeilen und Trennpunkte nachgebessert. Bildschirmfotos vom Eigentümer freigegeben (2026-11-04); PR #199: CI grün (4 von 4, keine Bündelgrößen-Warnung, größtes Bündel 416,65 kB; der Test „libyaml vorhanden“ grün auf Linux), auf Anweisung des Eigentümers („Merge?“) zusammengeführt (`7319b26`), eingespielt 2026-11-04; im Container `yaml.__with_libyaml__` wahr und `FAST` aktiv. Offen: Bestätigung des Eigentümers; erste Zeilen mit `welt` entstehen mit der nächsten KI-Anfrage.

#### 9.12: Quellen für Worldbuilding und Namen; eigener Recherche-Baustein – Erkundung (V.35 H1, V1)

- **Status:** ✅ ERLEDIGT (2026-11-05) – Erkenntnisdokument `docs/research/quellen-und-recherche.md`, Vorlage per Auswahlfragen, Entscheidung ADR-101; Umsetzung als V.44, V.45, V.46 mit Landeplatz 9.15
- **Phasentyp-Kontext:** ERKUNDUNG innerhalb der UMSETZUNG-Phase (wie 8.12)
- **Schritt-Art (nur ERKUNDUNG):** Vergleichsstudie
- **Zeitbox (nur ERKUNDUNG):** eine Session, dann Zwischenstand
- **Abhängigkeiten:** keine
- **Freigabepflichtig:** nein für die Erkundung; jede Anbindung ist eine neue externe Abhängigkeit (Kategorie 3)
- **Empfohlene Klasse:** Entscheidung – bereitet eine Abhängigkeits- und Kostenentscheidung vor.
- **Eingangskriterien:** keine
- **Anforderungen (ab Klasse M):** FR-029
- **Zu tun:** H1: Anleitungen zum Worldbuilding und Seiten zur Namensbildung sichten – Verlässlichkeit, Nutzungsbedingungen, Einbindung in den Weltenbauer. V1: eigener Recherche-Baustein gegen die Websuche über OpenRouter (ADR-064) – Kosten je Anfrage, Abhängigkeit, Datenschutz.
- **Akzeptanzkriterien:** Erkenntnisdokument `docs/research/quellen-und-recherche.md` mit Optionen und Kosten; Vorlage an den Eigentümer; Umsetzung als eigener Schritt mit Landeplatz 9.15.
- **Betroffene Module:** keine (nur lesen)
- **Reifegrad-Wirkung:** keine
- **Artefakte:** Erkenntnisdokument, Logbuch-Eintrag
- **Notizen:** Aus V.35 (ADR-090).

#### 9.13: Gast-Figuren ausbauen – Weltbezug je Gast (V.34)

- **Status:** ✅ ERLEDIGT (2026-11-05) – eingespielt `e809696`, Eigentümer bestätigt („Hat funktioniert.“). Verlauf: Bestandsaufnahme: Probe des Eigentümers 2026-10-21 ohne benannten Mangel („Gastfiguren funktionieren auch“); auf dem Server 0 Gast-Verbindungen und 0 Fakten „nur diese Geschichte“ in 11 Geschichten (5 Welten). Eigentümer auf Rückfrage (Empfehlung war „auf später“): „A wie geplant“. Mockup `mockup-9.13.html` (lokal) vorgelegt; Auswahlfragen: Bedienung wie Mockup, Geltung je Geschichte, Heimatwelt-Abschnitt weglassen, wenn ein Weltbezug da ist → ADR-102. Umsetzung läuft
- **Phasentyp-Kontext:** UMSETZUNG (mit Vorlage zu Beginn)
- **Abhängigkeiten:** 9.1
- **Freigabepflichtig:** ja – wie V.34: Datenmodell und Kontext-Zusammenstellung (Kategorien 1 und 4)
- **Empfohlene Klasse:** Entscheidung – Datenmodell und Kontext-Zusammenstellung (Eskalations-Auslöser 1).
- **Eingangskriterien:** Probe des Eigentümers mit einer Gast-Figur (Eingangskriterium aus V.34); 9.1 erledigt
- **Anforderungen (ab Klasse M):** FR-016, FR-017
- **Zu tun:** wie V.34 (Option A aus `docs/research/wandernde-figuren.md`).
- **Akzeptanzkriterien:** wie V.34.
- **Betroffene Module:** manuscript, context, api, ui
- **Reifegrad-Wirkung:** keine
- **Artefakte:** Code, Tests, ADR
- **Notizen:** Aus V.34 (ADR-090). Eigentümer 2026-10-18: Probe „später“.
- **Umgesetzt (lokal, 2026-11-05, noch nicht abgenommen):** nach ADR-102. `manuscript`: `GuestLink.relation` (Kopffeld `weltbezug` nur, wenn gesetzt; nicht Teil der Gleichheit), `set_guest_relation` (höchstens 4.000 Zeichen). `canon`: `drop_world_sections` (Abschnitte „In/Im …“ mit dem Namen der Heimatwelt ohne Artikel). `context`: Gast mit Weltbezug bekommt „### In dieser Welt („‹Welt›“)“, Heimatwelt-Abschnitte fallen weg; neue Anfrage `guest_fit` (Rahmen, neue Welt, Namen, Regeln, Gast, bisheriger Weltbezug, Wunsch). `api`: `PUT …/guests/{welt}/{eintrag}`, `POST …/fit` (Strom, Modell der Aufgabe `weltenbau`, gezählt bei Welt und Geschichte); Routen 81 → 83. `ui`: Feld je Gast, `GuestFit` mit Modell, Wunsch, Vorschlag, „In das Feld übernehmen“. Tests: Python 29 neue (canon 10, manuscript 7, context 5, api 6, ohne Anbieter 1) und 3 angepasste (Routenzahl, Gast-Antwort, Vertragstest); 1123 bestanden, Abdeckung 100 % Zeilen (99 % mit Zweigen); Oberfläche 7 neue (3 in `Guests.test.tsx`, 4 in `GuestFit.test.tsx`), 558 bestanden, Abdeckung 98,83 / 95,41 / 98,24 / 98,99 % (Anweisungen/Zweige/Funktionen/Zeilen), `GuestFit.tsx` 98 %; E2E 15 bestanden; Vertragsdatei neu aufgenommen (nur Feld `relation` und die zwei neuen Aufrufe). Regel-002: Anfragen ohne Weltbezug sind gleich (Test `test_without_relation_the_guest_stays_as_it_was`), die Testgeschichten haben keine Gäste – keine Probeschreib-Reihe nötig. Bildschirmfotos zur Abnahme vorgelegt.

#### 9.14: Kontexttreue beim Referenzumfang erneut prüfen

- **Status:** ✅ ERLEDIGT (2026-11-05) – Messung an der größten Geschichte des Eigentümers (94.682 Wörter, 9 Kapitel): Anfrage für Kapitel 9 geschätzt 29.793 von 30.000 Token, Handlungsstand und alle 8 Kurzfassungen, alle 20 Kanon-Einträge, letzte Seiten 14.944 Token. Eigentümer: „Belastbar bis ~30 Kapitel“ → ADR-103, NFR `[BELASTBAR]` mit Grenze; Nachmessen als D.25
- **Phasentyp-Kontext:** ERKUNDUNG innerhalb der UMSETZUNG-Phase
- **Schritt-Art (nur ERKUNDUNG):** Messung
- **Zeitbox (nur ERKUNDUNG):** eine Session
- **Abhängigkeiten:** 9.4 (9.1–9.4 können die Anfrage ändern)
- **Freigabepflichtig:** nein für die Messung; die Beförderung per ADR
- **Empfohlene Klasse:** Entscheidung – kann die NFR Kontexttreue auf `[BELASTBAR]` befördern (Eskalations-Auslöser 4).
- **Eingangskriterien:** 9.4 erledigt
- **Anforderungen (ab Klasse M):** FR-010
- **Zu tun:** An der dann längsten Geschichte des Eigentümers messen, ob Handlungsstand und genannte Kanon-Einträge vollständig in der Anfrage stehen und die Anfrage unter 30.000 Token bleibt – Verfahren wie D.4 (ADR-057), lesend und mit Freigabe des Eigentümers.
- **Akzeptanzkriterien:** Messung im Logbuch; ADR mit Beförderung auf `[BELASTBAR]` oder begründetem Erkundungsbedarf.
- **Betroffene Module:** keine (nur lesen)
- **Reifegrad-Wirkung:** NFR Kontexttreue Referenzumfang `[VORLÄUFIG]` → `[BELASTBAR]` oder bleibt mit Begründung
- **Artefakte:** Logbuch-Eintrag, ADR
- **Notizen:** Befund des Vision-Abgleichs in 8.13: Die Bedingung aus ADR-062 (Abnahme durch den Eigentümer) ist seit 2026-10-11 erfüllt; Eigentümer 2026-10-18: „Erst später messen“ (ADR-090).

#### 9.15: Planung der nächsten Ausbaustufe

- **Status:** ✅ ERLEDIGT (2026-11-05) – Vision-Abgleich ohne verwaiste Elemente; Onboarding-Pfad auf frischem Worktree grün; Pflichtfrage mit getrennter Instanz: weiterbauen mit drei kleinen Umbauten (ADR-104, `docs/research/bewertung-phase-9.md`); Phase 10 geplant (ADR-105): V.43 → 10.1, V.38 → 10.2, V.39 → 10.3, neu 10.4 und 10.5, V.23 → 10.6, V.33 → 10.7, V.24 → 10.8, V.42 → 10.9, V.41 → 10.10; V.21, V.40, V.44–V.46 → 10.11; V.20 verworfen
- **Phasentyp-Kontext:** UMSETZUNG
- **Abhängigkeiten:** 9.1–9.14
- **Freigabepflichtig:** ja – neue Phasen sind Replanning
- **Empfohlene Klasse:** Entscheidung – inhaltliche Neuplanung mit Vision-Abgleich.
- **Eingangskriterien:** Vision-Abgleich an der Phasengrenze nach Phase 9
- **Anforderungen (ab Klasse M):** keine
- **Zu tun:** V.20, V.21, V.23, V.24, V.33, V.38, V.39, V.40, V.41, V.42, V.43, V.44, V.45, V.46 (und weitere neue V-Schritte) in eine neue Phase überführen oder per ADR verwerfen.
- **Akzeptanzkriterien:** Jeder verschobene Schritt hat einen neuen Schritt mit ID oder `[VERWORFEN]` mit ADR.
- **Betroffene Module:** keine (Planung)
- **Reifegrad-Wirkung:** keine
- **Artefakte:** Logbuch-Eintrag, ADR
- **Notizen:** Angelegt 2026-10-18 (ADR-090).
