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

Das Logbuch beginnt mit der ersten regulären Session nach dem Initialisierungs-Commit (Modus 2, abgeschlossen 2026-09-26). Verlauf und Begründungen der Initialisierung stehen in `docs/decisions.md` (ADR-001 bis ADR-009). Phasen 1 bis 9 sind verdichtet; Details in `docs/archiv/logbuch-phase-1.md` bis `docs/archiv/logbuch-phase-9.md`. Die Einträge vom September 2026 (Reflexionen der Phasen 1 bis 3) stehen seit 2026-11-04 in `docs/archiv/logbuch-2026-09.md`.

---

<!-- ANCHOR:eintraege -->
## Einträge (neueste oben)

### 2026-11-05 – [ADR-ANGELEGT] ADR-110 Bilder im Manuskript und im E-Book (10.6)

- Vorlage mit `mockup-10.6.html` (lokal) und `ENTSCHEIDUNG ERFORDERLICH`; vier Auswahlfragen, Eigentümer jeweils die Empfehlung. Mini-Reibung beim Messen: Kapitel liegen unter `stories/<id>/chapters/`, nicht `kapitel/` – zwei Fehlversuche, dann in `manuscript/layout.py` nachgesehen.
- Reaktiv-Quote 0/10 (ADR-101 bis ADR-110). Zweig `feat/10.6-bilder-im-manuskript` von `docs/10.5-erledigt`.

### 2026-11-05 – [BEOBACHTUNG] Nachtrag 10.5 eingespielt

- Eigentümer: „Ja, einspielen“. Nach Runbook (ADR-039), `REVISION` `56e5d1b`, Rückweg `skriptorium:vorher` und `app.vorher`. Vorher lief `17ea244`.
- Prüfung: `/api/health` 200 nach 60 s, Anmeldeseite 200; eine SSH-Prüfung: `(healthy)`, `56e5d1b`, 0 Fehlerzeilen in 3 Minuten.

### 2026-11-05 – [BEOBACHTUNG] 10.5 erledigt, V.49 vorgemerkt

- PR #209 (Nachtrag Preisregel), CI vier Jobs grün, zusammengeführt mit `--match-head-commit` → `56e5d1b`. 10.5 → ERLEDIGT; Phase 10: 5 von 11. Nicht eingespielt: Server läuft `17ea244` ohne Nachtrag.
- Eigentümer: Hineinzoomen in der Großansicht geht nicht, 4K und 2K erscheinen gleich groß. Auf Auswahlfrage „Als V.49 vormerken“ → V.49 mit Landeplatz 10.11; `MapViewer` hat schon Zoom (`useMapZoom`) als Vorbild.

### 2026-11-05 – [BEOBACHTUNG] Probe 10.5 mit 4K: abgenommen, Nachtrag Preisregel

- Eigentümer hat mit Seedream 5.0 Lite in 4K erzeugt: Server 2.732 × 4.096 WebP, 294 KB, Herkunft `4K`, 0,035 $, 26 s. „Es sieht deutlich schärfer aus“ – schwer zu beurteilen, weil die Großansicht jedes Bild auf dieselbe Größe einpasst. Abnahme „Ja“.
- Vor dem Erzeugen stand „Preis für 4K nicht ausgewiesen“, abgerechnet wurde der Grundpreis. Eigentümer: Regel ändern. Nachtrag auf `fix/10.5-preis-ohne-stufen`: Grundpreis eines Anbieters ohne jede Preisvariante gilt für jede Stufe. 2 neue Testfälle, 1171 Python-Tests bestanden.

### 2026-11-05 – [BEOBACHTUNG] Probe 10.5: 2K-Bild sieht aus wie vorher

- Eigentümer: neues 2K-Bild einer Figur „genauso“ wie bisher. Server (nur Zahlen): neues Bild 1.366 × 2.048 WebP, 108 KB, Herkunft `2K`, 0,09 $. Die fünf vorigen Seedream-5.0-Pro-Bilder: je 1.333 × 2.000, ebenfalls 0,09 $ – Seedream lieferte also schon ohne Angabe 2K (Variante `high_resolution`) und wurde nur von 2.048 auf 2.000 Pixel verkleinert. Der vorher angezeigte Preis „ca. 0,045 $“ (Grundpreis) war für dieses Modell falsch, die Abrechnung lag immer bei 0,09 $.
- Folge: Für Seedream 5.0 Pro bringt 10.5 nur 48 Pixel mehr; größere Bilder gibt es nur mit einem 4K-Modell (Katalog: z. B. Seedream 5.0 Lite 2K/4K 0,035 $, Seedream 4.5 bis 4K 0,04 $, Gemini/Nano Banana 4K nach Token, FLUX.3 4K 0,61 $). 10.5 bleibt bis zur Antwort des Eigentümers auf „wartet auf Abnahme“.

### 2026-11-05 – [BEOBACHTUNG] 10.5 eingespielt

- Eigentümer: „Ja, einspielen“. Nach Runbook (ADR-039), `REVISION` `17ea244`, Rückweg `skriptorium:vorher` und `app.vorher`. Vorher lief `1a46b59`.
- Prüfung: `/api/health` 200 nach 60 s, Anmeldeseite 200; eine SSH-Prüfung: `(healthy)`, `17ea244`, 0 Fehlerzeilen in 3 Minuten. Offen: Probe mit einem 2K-Bild (Eigentümer).

### 2026-11-05 – [GELÖST] CI-Neustart wegen HTTP 504 bei `actions/setup-python` (PR #208)

- Eigentümer: „Ja, PR und Merge“. Erster Lauf: Python, TypeScript, E2E grün; Pre-Commit rot – `actions/setup-python@v6.3.0` bekam dreimal „Unexpected HTTP response: 504“ beim Herunterladen von Python, der Job prüfte unseren Code gar nicht. Einmal neu gestartet (`gh run rerun --failed`) → alle vier grün (Pre-Commit 2:31). Kein Code geändert.
- Zusammengeführt mit `--match-head-commit` → `17ea244`. 10.5 wartet auf Einspielen und Probe. Doku-Nachtrag lokal auf `docs/10.5-zusammengefuehrt`.

### 2026-11-05 – [BEOBACHTUNG] 10.5 umgesetzt (lokal)

- Nach ADR-109 auf `feat/10.5-aufloesung-qualitaet`; Zahlen im Fahrplan bei 10.5. Abnahme braucht ein echtes 2K-Bild im Betrieb (Schlüssel lokal nicht gültig).
- Mini-Reibungen: (1) Grok hat keinen Grundpreis; `_price` fiel auf die erste Variante zurück (`low_1k`) – als Grundpreis für 1K/mittel wäre ein falscher Preis erschienen. Eigener Wert `plain` nur für den Preis ohne Variante. (2) Sieben UI-Tests scheiterten an Attrappen von `../files` ohne `GENERATED_SIDE` – die Attrappe muss jede benutzte Konstante kennen. (3) `ok()` der Test-API liefert eine Handler-Funktion, kein Ergebnis – in einem eigenen Handler direkt `{status, body}` zurückgeben. (4) mypy leitete den Typ einer Testtabelle zu eng ab (`list[dict]`), Typangabe ergänzt.
- DoD-Lücke entdeckt: CHANGELOG fehlte für 10.2 und 10.3 – nachgetragen.

### 2026-11-05 – [ADR-ANGELEGT] ADR-109 Auflösung und Qualität bei „Bild erzeugen“ (10.5)

- Vorlage mit `mockup-10.5.html` (lokal) und `ENTSCHEIDUNG ERFORDERLICH`; vier Auswahlfragen, Eigentümer jeweils die Empfehlung. Befund beim Lesen: Nicht nur die fehlende Auflösung macht Bilder klein, sondern auch `shrinkImage` mit 2.000 Pixel beim Übernehmen – 2K wäre sonst wirkungslos gewesen. Pillow fehlt im Container (Messskript scheiterte am Import) – Umwandeln auf dem Server wäre eine neue Abhängigkeit.
- Reaktiv-Quote 0/10 (ADR-100 bis ADR-109). Zweig `feat/10.5-aufloesung-qualitaet` von `docs/10.4-zusammengefuehrt`.

### 2026-11-05 – [BEOBACHTUNG] 10.3 abgenommen

- Probe des Eigentümers mit echter KI im Betrieb: Herauslösen klappt, neuer Abschnitt „Aussehen“, Vorschlag nur Sichtbares, Übernehmen funktioniert. 10.3 → ERLEDIGT. FR-035 schon in 10.3 ergänzt. Phase 10: 4 von 11.

### 2026-11-05 – [BEOBACHTUNG] 10.3 und 10.4 eingespielt

- Eigentümer: „Ja, einspielen“. Nach Runbook (ADR-039), `REVISION` `1a46b59`, Abbild `skriptorium:vorher` und `app.vorher` als Rückweg. Vorher lief `7900e9d`.
- Prüfung: `/api/health` 200 nach 60 s, Anmeldeseite 200; eine SSH-Prüfung: `(healthy)`, `1a46b59`, 0 Fehlerzeilen in 3 Minuten. Offen: Probe 10.3 mit echter KI (Eigentümer).

### 2026-11-05 – [BEOBACHTUNG] 10.3 und 10.4 zusammengeführt

- Eigentümer: „Ja, PR und Merge“. PR #207 (10.3, 10.4 und die Doku seit dem Einspielen von 10.1/10.2), CI vier Jobs grün (Python 1:42, TypeScript 1:44, Pre-Commit 2:03, E2E 2:15), keine Hinweise außer der bekannten Ubuntu-26-Meldung (D.19). Zusammengeführt mit `--match-head-commit` → `1a46b59`.
- 10.4 → ERLEDIGT. 10.3 wartet auf Einspielen (Wort des Eigentümers) und Probe mit echter KI. Server läuft weiter `7900e9d`. Doku-Nachtrag lokal auf `docs/10.4-zusammengefuehrt`.

### 2026-11-05 – [BEOBACHTUNG] 10.4 umgesetzt (lokal)

- Zahlen im Fahrplan bei 10.4. Verhalten unverändert: alle vorhandenen Tests ohne Änderung grün, E2E 15.
- Mini-Reibung: Nach dem ersten Zerlegen sank die Zweig-Abdeckung um 0,09 Punkte (95,45 → 95,36 %) – die Prüfung „Entfernen gelungen?“ steht jetzt in zwei Komponenten, ihr Fehlerzweig war nie getestet. Neuer Test „Entfernen scheitert“ und Bild als Prop statt `images[at] ?? ""` → 95,49 %. Zählskript für Hooks fand `useState<…>(` nicht (Generic vor der Klammer) – von Hand nachgezählt.

### 2026-11-05 – [BEOBACHTUNG] 10.4 begonnen, oberhalb der empfohlenen Klasse

- Eigentümer: „Noch nicht“ zum PR für 10.3; dann „Ja, 10.4 beginnen“ auf die Empfehlung (10.4 öffnet 10.5–10.8). 10.3 → wartet auf Freigabe, damit nur 10.4 in Arbeit ist. 10.4 auf dem Zweig von 10.3, weil beide `EntryImages.tsx` ändern.
- Empfohlene Klasse Routine, aktiv ist die Entscheidungs-Klasse (Opus 5.5, laut Systemkontext); Warnung zu Beginn gegeben. Keine Abgabe an einen Unteragenten: Der Umbau braucht den bereits geladenen Kontext von `EntryImages.tsx`, ein Unteragent müsste ihn neu lesen.

### 2026-11-05 – [BEOBACHTUNG] 10.3 umgesetzt (lokal)

- Nach ADR-108 auf `feat/10.3-aussehen-orte-gegenstaende`; Zahlen im Fahrplan bei 10.3. Keine Bildschirmfotos – die Abnahme braucht ohnehin eine echte KI-Antwort im Betrieb (Schlüssel lokal nicht gültig).
- Mini-Reibung: eigener Test erwartete Text nach `## Lage` außerhalb des Abschnitts – ein Abschnitt reicht bis zur nächsten Überschrift gleicher oder höherer Ebene (ADR-083); Beispiel berichtigt. Ersetzen per Python-Skript scheiterte an einem doppelt vorkommenden JSX-Ausschnitt (Figurenkarte und Knopf hatten dieselbe Bedingung) – mit Edit und mehr Kontext gelöst. ruff RUF002 (Gedankenstrich im Docstring) und RUF022 (`__all__` sortieren) behoben. Pre-Commit-Hook fand `mypy --strict` in einem Test (Art als `str` statt `Category`) – die lokale mypy-Prüfung lief nur über `src`; künftig `src tests` prüfen.

### 2026-11-05 – [ADR-ANGELEGT] ADR-108 „Aussehen herauslösen“ auch für Orte und Gegenstände (10.3)

- Vorlage mit `mockup-10.3.html` (lokal, `.git/info/exclude`) und `ENTSCHEIDUNG ERFORDERLICH`; drei Auswahlfragen, Eigentümer jeweils die Empfehlung: Knopf im Eintrag und im Fenster „Bild erzeugen“, „Lage“ bleibt draußen (Server über `take_section`), daneben „✎ Selbst ergänzen“. Messung im Fahrplan bei 10.3. Reaktiv-Quote 0/10 (ADR-099 bis ADR-108).
- Zweig `feat/10.3-aussehen-orte-gegenstaende` von `docs/10.2-zusammengefuehrt` (Doku-Commits gehen mit).

### 2026-11-05 – [BEOBACHTUNG] „Wesen:“ im Fließtext → V.48

- Server (nur Anzahlen und kurze Ausschnitte ohne Inhalt): 3 Figuren mit Abschnitt „Wesen“ (zwei Welten), 11 Figuren in einer Welt mit „Wesen: …“ mitten im Absatz. Die Messung zu 10.2 hatte nur Zeilen „- **Wesen:** …“ gezählt – die Form im Fließtext fehlte dort.
- Eigentümer verstand die Frage im Kurzformat nicht; nach Erklärung mit Beispiel (Feld „personality“ bleibt leer, alles steht in „description“): „Vormerken“ → V.48, Landeplatz 10.11.

### 2026-11-05 – [BEOBACHTUNG] 10.2 abgenommen

- Eigentümer an der heruntergeladenen Karte: „Wesen ist auch vorhanden.“ Auf dem Server nachgerechnet (nur Überschriften und Längen): „personality“ 450 Zeichen, „description“ mit Aussehen, Fähigkeiten, Geschichte, Beziehungen, Wort „Wesen“ dort 0-mal – kein doppelter Inhalt. 10.2 → ERLEDIGT. FR-030 war schon erledigt, keine Änderung in `docs/requirements.md`.
- Offen: Antwort des Eigentümers zu V.48 („Wesen: …“ im Fließtext bei 11 Figuren einer Welt).

### 2026-11-05 – [BEOBACHTUNG] 10.1 abgenommen

- Eigentümer nach Neuladen: „Die Folgenliste entspricht jetzt 4 Bilder.“ – passt zur Vorschau auf dem Server. 10.1 → ERLEDIGT. FR-024 und FR-036 waren schon erledigt (10.1 nur Nachbar), keine Änderung in `docs/requirements.md`.
- Offen: Abnahme 10.2 (Figurenkarte „Das Phantom“, Feld „personality“); Antwort des Eigentümers zu V.48 („Wesen: …“ im Fließtext bei 11 Figuren einer Welt).

### 2026-11-05 – [GELÖST] Abnahme 10.1: alte Abfrage statt Folgenliste

- Eigentümer beim Löschen von „Hannah Brandt“: nur die Frage „wirklich löschen?“, keine Folgenliste. Das ist wörtlich die alte Abfrage (`window.confirm` in `e809696`).
- Geprüft: Server liefert das neue Bündel aus (`index-CmVil8ey.js` enthält den Dialog), einzige Löschstelle für Einträge ist `EntryForm` mit `DeleteDialog`; Vorschau für den Eintrag auf dem Server: 4 Bilder, 0 Markierungen, 0 Geschichten, 1 Erwähnung mit @ – der neue Dialog hätte das gezeigt.
- Ursache (wahrscheinlich): Seite war vor dem Einspielen geöffnet; die Oberfläche lädt neuen Code erst beim Neuladen. Lösung: Seite neu laden. `index.html` kommt ohne `Cache-Control` (nur ETag/Last-Modified).

### 2026-11-05 – [BEOBACHTUNG] 10.1 und 10.2 eingespielt

- Eigentümer: „Ja, einspielen“. Nach Runbook (ADR-039): `git archive main` → `app.neu`, `REVISION` `7900e9d`, Abbild `skriptorium:vorher` getaggt, `app.vorher` behalten, `docker compose build` und `up -d`.
- Prüfung: `https://…/api/health` 200 nach 60 s, Anmeldeseite 200; eine SSH-Prüfung: Container `(healthy)`, `REVISION` `7900e9d`, 0 Fehlerzeilen im Log der letzten 3 Minuten. Vorher lief `e809696`.
- Offen: Abnahme 10.1 (Eintrag löschen, Folgenliste) und 10.2 (Figurenkarte, Feld „personality“) durch den Eigentümer. `docs/project-context.md` Status nachgezogen (stand noch auf Phase 9).

### 2026-11-05 – [BEOBACHTUNG] 10.2 zusammengeführt

- Eigentümer: „Ja, PR und Merge“. PR #206 (mit den zwei Doku-Commits aus dem Abschluss von 10.1), CI vier Jobs grün (Python 1:43, Pre-Commit 2:02, E2E 2:14, TypeScript 2:27); einziger Hinweis der Plattform: Ubuntu-26-Umstellung, bekannt und erledigt (D.19). Zusammengeführt mit `--match-head-commit` → `7900e9d`.
- Nicht eingespielt: Server läuft weiter `e809696`. 10.1 und 10.2 warten auf Einspielen und Abnahme; Doku-Nachtrag lokal auf `docs/10.2-zusammengefuehrt`, geht mit dem nächsten PR.

### 2026-11-05 – [BEOBACHTUNG] 10.2 umgesetzt (lokal)

- Nach ADR-107 auf `feat/10.2-wesen-im-export` (abgezweigt von `docs/10.1-zusammengefuehrt`, damit die Doku-Commits mitgehen). Zahlen im Fahrplan bei 10.2. Keine Änderung an der Oberfläche, daher kein E2E-Lauf nötig und keine Bildschirmfotos; Abnahme über eine heruntergeladene Figurenkarte nach dem Einspielen.
- Mini-Reibung: `grep --include=*.py` scheitert in zsh ohne Anführungszeichen („no matches found“) – wie schon in 10.1; Muster in Anführungszeichen setzen.
- Statuspflege: 10.1 auf „wartet auf Freigabe“ (Abnahme nach dem Einspielen) gesetzt, damit nur 10.2 in Arbeit ist; `docs/architecture.md` Routenzahl 83 → 84 nachgezogen (Drift aus 10.1).

### 2026-11-05 – [ADR-ANGELEGT] ADR-107 Figurenkarte nimmt „Wesen“ über die Abschnittsregel (10.2)

- Vergleich `mockup-10.2.html` (lokal, ausgeschlossen) vorgelegt. Server (eine Prüfung plus eine Nachzählung, nur Anzahlen): 29 Figuren, 3 mit Wesen-Text (Ebene 3), 2 davon mit zu viel in „personality“; 0 „Wesen und Geschichte“, 0 Zeilen „- **Wesen:** …“, 0 Überschriften „In/Im ‹Welt›“.
- Eigentümer per Auswahlfragen: „Nur Abschnitt Wesen“, Rückimport „Am Ende, wie heute“, Funktionen „Behalten, Doku ehrlich“ – jeweils die Empfehlung. Kategorie 5, nicht reaktiv; Regel-003 um den Stand ergänzt.

### 2026-11-05 – [SESSIONSTART] 10.2 vorbereiten

- **Modell:** Opus 5.5 (Entscheidungs-Klasse), Quelle: Systemkontext; keine Sitzungsabfrage in dieser Umgebung.
- **Stand:** `origin/main` = `c78ad0e` (10.1), lokal `docs/10.1-zusammengefuehrt` mit zwei ungepushten Doku-Commits; Server `e809696`. Mindest-Lektüre gelesen.
- **Vorhaben:** Eigentümer: „Wollen wir schon mal den nächsten Schritt machen?“ → 10.2 Vorlage; 10.1 bleibt bis zu seinem Wort uneingespielt.
- **Kontextgröße:** nicht feststellbar (Session nach Verdichtung fortgesetzt).

### 2026-11-05 – [BEOBACHTUNG] Hermes 3 ohne Anbieter bei OpenRouter → V.47

- Frage des Eigentümers: Hermes 3 erscheint als unbekanntes Modell. Befund: `nousresearch/hermes-3-llama-3.1-405b` und `-70b` haben 0 Anbieter (`/api/v1/models/<id>/endpoints`) und fehlen in `/api/v1/models` (454 Textmodelle); `hermes-4-405b` ist verfügbar. Server (eine SSH-Prüfung): Hermes 3 nur in den Favoriten (`system/modelle.md`) und im Anweisungsverlauf einer Geschichte; im Oktober 10 Anfragen, letzte am 2026-10-20 erfolgreich. Keine Änderung im Skriptorium als Ursache.
- Eigentümer: entfernt den Favoriten selbst; deutlichere Anzeige als V.47 mit Landeplatz 10.11.

### 2026-11-05 – [SESSIONENDE] Phase 9 abgeschlossen, Phase 10 geplant, 10.1 zusammengeführt

- **Dauer:** 2026-11-04 ca. 20:10 bis 2026-11-05 (fortgesetzte, zweimal verdichtete Session).
- **Bearbeitet seit dem letzten Sessionende:** 9.12 Erkundung Quellen und Recherche (ADR-101); 9.13 Gast-Figuren mit Weltbezug (ADR-102, eingespielt `e809696`, bestätigt); 9.14 Kontexttreue gemessen (ADR-103, `[BELASTBAR]` bis ~30 Kapitel); 9.15 Phasenabschluss mit Vision-Abgleich, Onboarding-Prüfung, getrennter Instanz (ADR-104) und Planung Phase 10 (ADR-105); 10.1 Löschkaskade für Kanon-Einträge (ADR-106, PR #205, `c78ad0e`). PRs #200–#205 zusammengeführt.
- **Stand:** 10.1 in `main`, nicht eingespielt (Eigentümer: „Später“); Doku dazu lokal auf `docs/10.1-zusammengefuehrt`, nicht gepusht. Auf dem Server läuft `e809696`.
- **Offen:** Einspielen und Abnahme 10.1; überholter lokaler Zweig `feat/9.9-loeschen-archivieren` (nur auf Wort des Eigentümers löschen).
- **Nächster Schritt:** 10.1 einspielen und abnehmen, dann 10.2 (Vorlage). Datiert: D.1 (Node 26) seit 2026-11-05 fällig, D.5 (mypy 2) am 2026-11-06; D.11 Frist 2026-10-31 überschritten (Eigentümer).
- **Sessionende-Prüfungen:** README gegen Fahrplan, Kontext, Architektur, Blocker abgeglichen (Phase 10, 10.1, 0 Blocker). Drift: ADR-104 bis ADR-106 verweisen auf bestehende Schritte; Reifegrad nur NFR Kontexttreue geändert (ADR-103, Tabelle angepasst); Modul-Liste unverändert; FR-036/FR-038 mit Schritt; Reaktiv-Quote 0/10; Phase 10 bei 11 von 11 geplanten Schritten. `docs/project-context.md` unter 600 Zeilen; Logbuch nach Verdichtung ca. 175 Zeilen. Ablaufdaten-Register: D.1 und D.5 haben Schritte.
- **Modell-Bilanz:** aktiv Opus 5.5 (Entscheidungs-Klasse, Quelle: Systemkontext). Oberhalb der Empfehlung: Einspielen, Doku-Nachträge und README-Pflege (Routine); 10.4 und 9.x nicht berührt. Abgegeben: die Pflichtfrage an einen Unteragenten mit Sonnet als getrennte Instanz (methodisch vorgeschrieben, nicht aus Kostengründen); sonst keine Abgabe – kleine Teilarbeiten mit geladenem Kontext.
- **Kontextgröße:** nicht feststellbar; Session zweimal verdichtet, Weiterarbeit nach dauerhaftem „weiter hier“ des Eigentümers.

### 2026-11-05 – [BEOBACHTUNG] PR #205 zusammengeführt (10.1), Einspielen später

- Eigentümer gab die Bildschirmfotos frei („Ja, PR und Merge“); CI 4 von 4 grün, Protokoll ohne neue Warnung. Merge-Commit `c78ad0e`. Einspielen: „Später“.

### 2026-11-05 – [BEOBACHTUNG] 10.1 umgesetzt (lokal), Bildschirmfotos zur Abnahme

- Umsetzung nach ADR-106 auf `feat/10.1-loeschkaskade`; Zahlen im Fahrplan bei 10.1. ruff, ruff format, `mypy --strict`, bandit, ESLint, Prettier, tsc grün; Build vom Projektordner, E2E 15 grün.
- Mini-Reibung: Der Archivtest aus 9.9 nutzte das alte Verhalten (gelöschter Eintrag ließ die Gast-Verbindung stehen), um den „verschwundenen Gast“ zu prüfen; jetzt wird die Datei dafür von Hand entfernt.
- Mini-Reibung: Bildschirmfoto für das Smartphone muss gleich in Handygröße entstehen; ein nachträgliches Verkleinern öffnet die Seitenleiste über dem Dialog.

### 2026-11-05 – [ADR-ANGELEGT] ADR-106 Löschen eines Kanon-Eintrags nimmt seine Verweise mit (10.1)

- Eigentümer per Auswahlfragen zum Mockup: „Mitlöschen mit Folgenliste“, „Klick im Dialog“. Kategorien 4 und 5, nicht reaktiv.

### 2026-11-05 – [BEOBACHTUNG] 10.1 begonnen: Bestandsaufnahme und Mockup

- Code: `canon/entries.py::delete_entry` löscht die Datei, `CanonService.delete_entry` dazu Bilder und Markierungen; Geschichten werden nicht berührt. Muster für die Kaskade: `api/flows/removal.py` (Welt löschen, ADR-098; `canon` und `manuscript` kennen sich nicht, der Ablauf liegt in `api`).
- Server (eine SSH-Prüfung, nur Anzahlen): 148 Einträge in 5 Welten; geführte Figuren 0, Fakten „nur diese Geschichte“ 0, Gast-Verbindungen 1; verwaiste Verweise 0.
- Mockup `mockup-10.1.html` (lokal, ausgeschlossen): Dialog mit Folgenliste statt `window.confirm`.

### 2026-11-05 – [PHASEN-WECHSEL] Reflexion Phase 9 (UMSETZUNG) → Phase 10 (UMSETZUNG)

- **Gelernt:** Messen schlägt Schätzen – Zwischenspeicher bei der zweiten gleichen Anfrage 98–99,7 % (9.10), echte Nutzung 1.094 Anfragen im Oktober statt geschätzter 400, Websuche teuer durch den Suchtext statt durch die Gebühr (9.12). Die Vertragsdatei aus 9.2 hat jede Änderung an Antworten (9.9, 9.11, 9.13) sichtbar gemacht.
- **Gelernt:** Vorlage mit Mockup und Auswahlfragen trägt: 15 von 15 Schritten ohne Wucherung, Rückfragen des Eigentümers („Baustein Wikipedia?“, „RPG-Seiten?“, „Auflösung?“) haben Pläne verbessert.
- **Kippende Annahmen:** „Die Abschnittsregel im Server wird genutzt“ – nur `drop_*`/`nest_headings` laufen, Lesen und Schreiben nur in Tests (Bewertung, Befund 1 → 10.2). Kostenschätzung 400 Anfragen/Monat (Architektur, Projektkontext berichtigt). Gast-Figuren ohne benannten Mangel – auf Wunsch trotzdem gebaut (9.13).
- **Reifegrad:** NFR Kontexttreue Referenzumfang `[VORLÄUFIG]` → `[BELASTBAR]` bis etwa 30 Kapitel (ADR-103); übrige unverändert.
- **ADRs der Phase:** ADR-089 bis ADR-105 (17), 0 reaktiv.
- **Neue Erkundungsbedarfe:** D.25 (Kontexttreue ab 25 Kapiteln), D.26 (Verbrauchsspeicher ab 3.000 Anfragen/Monat); Textqualität bei langen Geschichten misst bisher niemand (Bewertung, Befund 3).
- **Methodik-Lehren:** `npx vite build` nur vom Projektordner (Ziel `dist/ui`); Abdeckung nur über das ganze Paket messen (libyaml unter `--cov=<Modul>`); Pflichtlektüre gekürzt (Reaktiv- und Stand-Zeile in `decisions.md` Teil A archiviert); Logbuch-Monatsscheibe September ausgelagert.
- **Details:** [`docs/archiv/logbuch-phase-9.md`](archiv/logbuch-phase-9.md)

### 2026-11-05 – [ADR-ANGELEGT] ADR-104 Pflichtfrage nach Phase 9, ADR-105 Planung Phase 10

- Getrennte Instanz (Sonnet, ohne Gesprächsverlauf, nur lesend): gezielt umbauen, klein; Bericht mit Stellungnahme in `docs/research/bewertung-phase-9.md`. Befund 1 per grep bestätigt (0 Aufrufer für `read_section`, `read_part`, `put_section`, `append_section`, `read_labelled`).
- Eigentümer: „Weiterbauen mit Umbau“; Phase 10 mit Kanon-Pflege, Bildern, „Schreiben nachvollziehen“ (Weltenbauer nicht gewählt); V.20 verworfen, V.21 später (nach Rückfrage, was „Figurenkarten“ sind); auf seine Frage nach der Auflösung neuer Schritt 10.5 (27 von 63 Bildmodellen bieten `resolution`).
- Vision-Abgleich gegen `docs/vision.md` und `docs/requirements.md`: keine verwaisten Elemente (alle Muss erledigt, FR-006 verworfen, FR-038 → V.45 → 10.11).
- Pflege nach Befund 8 und 9: Reifegrad-Tabelle, Kostenschätzung (Oktober 38,31 $), Status von V.34/V.35/V.36/V.37, README-Schnellstart, Teil A gekürzt.

### 2026-11-05 – [ONBOARDING-VALIDATION] Phasengrenze Phase 9 (9.15)

- Frischer Worktree von `main` (`942eabf`) im Scratchpad: Quick Start der README genau wie dokumentiert (`uv python install 3.14.7`, `uv sync --frozen --python 3.14.7`, `npm ci`, `uv run pre-commit install`, `uv run skriptorium-einrichtung`, `npx vite build`, `uvicorn`) – alle Schritte Exit 0, `/api/health` → `{"status":"ok"}` nach 2 s; `scripts/session-start.sh` Exit 0. Befund: Text über dem Schnellstart nannte noch den Stand vom 2026-10-13 – berichtigt. Worktree entfernt, Hook im Haupt-Checkout neu eingerichtet.

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
