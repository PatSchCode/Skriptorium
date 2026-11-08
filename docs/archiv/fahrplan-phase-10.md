# Archiv – Fahrplan Phase 10

<!-- Quelle: docs/fahrplan.md, Abschnitt „Aktuelle Phasen". Ausgelagert am 2026-11-08 (CLAUDE.md Abschnitt 14:
     Phase vollständig erledigt). Abgedeckter Zeitraum: 2026-11-05 bis 2026-11-08. -->

## Aktuelle Phasen

### Phase 10: Kanon-Pflege, Bilder und Nachvollziehbarkeit – Typ: UMSETZUNG – ABGESCHLOSSEN (2026-11-08)

**Ziel:** Die drei kleinen Umbauten aus der Pflichtfrage (ADR-104) vor die Funktionen setzen, die sie brauchen; den Kanon beim Löschen und beim Herauslösen von Teilen verlässlich halten; Bilder größer, im Manuskript und beim Schreiben nutzbar machen und einen zweiten Bildanbieter anbinden; KI-Texte nachvollziehbar machen.

**Abschlusskriterium:** Schritte 10.1–10.11 `[ERLEDIGT]`, `[VERWORFEN]` mit ADR oder `[VERSCHOBEN]` mit Ziel-Schritt.

**Reifegrad-Erwartung am Phasenende:** unverändert `[BELASTBAR]`; Datenmodell-, Ablauf- und Abhängigkeits-Entscheidungen (10.1, 10.3, 10.5–10.9) werden per ADR entschieden, bevor gebaut wird.

**Ursprünglicher Schrittplan:** 11 Schritte, festgehalten am 2026-11-05 (ADR-104, ADR-105). Wucherungs-Schwelle: Default aus `docs/project-context.md` Abschnitt 6 (Faktor 2 und mindestens 5 zusätzliche Schritte, also mehr als 22); neue Wünsche während der Phase werden V-Schritte mit Landeplatz 10.11.

**Reihenfolge (Eigentümer, 2026-11-05; ADR-104, ADR-105):** Kanon 10.1–10.3, Bilder 10.4–10.8 (10.4 Umbau zuerst), Nachvollziehen 10.9–10.10; zuletzt 10.11.

**Pflichtfrage am Phasenende:** ADR „Weiterbauen, umbauen oder neu aufsetzen" – Nummer wird beim Phasenabschluss vergeben

#### 10.1: Löschkaskade für Kanon-Einträge (V.43)

- **Status:** ✅ ERLEDIGT (2026-11-05) – eingespielt mit Stand `7900e9d`; Abnahme durch den Eigentümer: Löschdialog für eine Figur zeigt die Folgenliste („4 Bilder“), stimmt mit der Vorschau auf dem Server überein (4 Bilder, 0 Markierungen, 0 Geschichten, 1 Erwähnung mit @); erster Versuch zeigte noch die alte Abfrage, weil die Seite vor dem Einspielen geöffnet war – nach Neuladen richtig. Bestandsaufnahme: `CanonService.delete_entry` entfernt Datei, Bilder und Kartenmarkierungen; Fakten, geführte Figuren und Gast-Verbindungen (samt Weltbezug) in Geschichten bleiben; Oberfläche fragt nur `window.confirm` (`ui/src/views/EntryForm.tsx`). Server 2026-11-05 (nur Anzahlen): 148 Einträge, 0 geführte Figuren, 0 Fakten, 1 Gast-Verbindung, 0 verwaiste Verweise. Mockup `mockup-10.1.html` (lokal) vorgelegt; Eigentümer: „Mitlöschen mit Folgenliste“, „Klick im Dialog“ → ADR-106. Umsetzung läuft
- **Phasentyp-Kontext:** UMSETZUNG (mit Vorlage zu Beginn)
- **Abhängigkeiten:** keine
- **Freigabepflichtig:** ja – Löschkaskade, destruktiv (Kategorie 4, `CLAUDE.md` Abschnitt 8, Kriterium 6)
- **Empfohlene Klasse:** Entscheidung – destruktiver Ablauf und Datenmodell (Eskalations-Auslöser 1).
- **Eingangskriterien:** keine
- **Anforderungen (ab Klasse M):** FR-036 (Nachbar), FR-024
- **Zu tun:** wie V.43: Beim Löschen eines Kanon-Eintrags Fakten, geführte Figuren und Gast-Verbindungen mit seiner Kennung in allen Geschichten mitnehmen (wie ADR-098), Vorschau der Folgen; klären, ob Kennungen gelöschter Einträge wiederverwendet werden dürfen (Befund 4 der Bewertung).
- **Akzeptanzkriterien:** Vorlage und ADR; Tests der Kaskade; Eigentümer bestätigt.
- **Betroffene Module:** canon, manuscript, api, ui
- **Reifegrad-Wirkung:** keine
- **Artefakte:** Code, Tests, ADR
- **Notizen:** Aus V.43 und U.3 der Bewertung (ADR-104).
- **Umgesetzt (lokal, 2026-11-05, noch nicht abgenommen):** nach ADR-106. `manuscript`: `remove_entry_uses` (Gast-Verbindung, geführte Figur, Fakten; gemeinsamer Helfer mit `remove_guest_world`). `api/flows/removal.py`: `entry_deletion` (Bilder, Markierungen, betroffene Geschichten der eigenen und anderer Welten) und `delete_entry_with_traces` mit der Regel aus ADR-098 (Spuren bleiben, wo die Kennung in derselben Geschichte einen anderen Eintrag meinen kann). Neue Route `GET …/entries/{eintrag}/deletion-preview`; `DELETE …/entries/{eintrag}` nimmt die Spuren mit; Routen 83 → 84. `ui`: Dialog mit Folgenliste (`EntryDeletionList`) statt `window.confirm`, `DeleteDialog` ohne Eintippen bei fehlendem Namen, Erwähnungen mit `@` aus „Verweise hierher“. Tests: Python 6 neue (`tests/api/test_entry_deletion.py`) und 3 angepasste (Archivtest auf von Hand gelöschte Datei, Routenzahl, Vertragsdatei um `entryDeletion`); 1129 bestanden, Abdeckung 100 % Zeilen, `removal.py` und `extras.py` 100 %. Oberfläche 3 neue (`EntryDeletion.test.tsx`), 2 angepasste (`views.test.tsx`); 561 bestanden, 98,81 / 95,44 / 98,25 / 98,97 %. E2E 15 bestanden. Bildschirmfotos zur Abnahme vorgelegt.

#### 10.2: Abschnittsregel im Server nutzen; SillyTavern-Export liest „Wesen“ (V.38)

- **Status:** ✅ ERLEDIGT (2026-11-05) – zusammengeführt PR #206, `7900e9d`, CI vier Jobs grün, eingespielt; Abnahme durch den Eigentümer an der Karte einer Figur mit Abschnitt „Wesen“ („Wesen ist auch vorhanden“), auf dem Server nachgerechnet: „personality“ 450 Zeichen ohne Überschriften, „description“ 743 Zeichen mit Aussehen, Fähigkeiten, Geschichte, Beziehungen und ohne „Wesen“. Vorher – Server 2026-11-05 (nur Anzahlen): 29 Figuren, 3 mit Wesen-Text (alle Ebene 3), davon 2 mit zu viel in „personality“; 0 mit „Wesen und Geschichte“ oder nur Zeile „- **Wesen:** …“; 0 Überschriften „In/Im ‹Welt›“. Vergleich `mockup-10.2.html` (lokal) vorgelegt; Eigentümer: nur Abschnitt „Wesen“, Rückimport wie heute, Funktionen behalten mit ehrlicher Doku → ADR-107. Umsetzung läuft
- **Phasentyp-Kontext:** UMSETZUNG (mit Vorlage zu Beginn)
- **Abhängigkeiten:** keine
- **Freigabepflichtig:** ja – Ausgabe der Figurenkarte ändert sich (Kategorie 5, ADR-066)
- **Empfohlene Klasse:** Entscheidung – berührt Regel-003 und ADR-102.
- **Eingangskriterien:** keine
- **Anforderungen (ab Klasse M):** FR-030
- **Zu tun:** (1) wie V.38: `card_for` in `canon/importers/sillytavern.py` nimmt `personality` über `read_section` (nur „Wesen“), den Rest in `description`; Folgen für den Rückimport prüfen. (2) `drop_world_sections` vergleicht auf Wortgrenze statt Teilstring (Befund 2 der Bewertung). (3) Was danach von `read_part`, `put_section`, `append_section`, `read_labelled` ohne Aufrufer bleibt, in der Vorlage benennen: behalten (Testvektoren) oder zurücknehmen; Regel-003 und `docs/architecture.md` Abschnitt 2 danach berichtigen.
- **Akzeptanzkriterien:** Vorlage, ADR; Tests (Export, Rückimport, Weltabschnitte); Eigentümer bestätigt.
- **Betroffene Module:** canon
- **Reifegrad-Wirkung:** keine
- **Artefakte:** Code, Tests, ADR
- **Notizen:** Aus V.38 und U.2 der Bewertung (ADR-104).
- **Umgesetzt (lokal, 2026-11-05, noch nicht abgenommen):** nach ADR-107. `canon/sections.py`: neues `take_section` (Abschnitt wie `read_section`, dazu der Text ohne ihn; nur im Server, wie `drop_world_sections`), Konstante `NATURE` = „Wesen“; `drop_world_sections` vergleicht auf Wortgrenze. `canon/importers/sillytavern.py`: `card_for` über `take_section`, Import schreibt `### {NATURE}`. Oberfläche und gemeinsame Testfälle unverändert. Tests: 17 neue (Export 5 mit Ebenen 1–3, Unterabschnitten, leerem Wesen, früherem Namen, Rückimport; Abschnitte 3; Weltabschnitte 9); 1146 bestanden, Abdeckung 99,87 % gesamt, `sections.py` und `sillytavern.py` 100 %. ruff, ruff format, `mypy --strict`, bandit grün.

#### 10.3: „Aussehen herauslösen“ auch für Orte und Gegenstände (V.39)

- **Status:** ✅ ERLEDIGT (2026-11-05) – zusammengeführt PR #207 (`1a46b59`), CI vier Jobs grün, eingespielt; Probe mit echter KI durch den Eigentümer im Betrieb: Herauslösen klappt, neuer Abschnitt „Aussehen“ im Eintrag, Vorschlag nur Sichtbares ohne Erfundenes, Übernehmen funktioniert („Ja, es hat alles funktioniert“). Vorher – Server 2026-11-05 (nur Anzahlen): 19 Orte, 0 mit „Aussehen“, 0 gegliedert; 44 Gegenstände, 4 mit „Aussehen“, 39 mit Zweck/Verwendung/Auswirkung; grobe Wortzählung: Sichtbares bei 6 Orten und 13 Gegenständen. Vergleich `mockup-10.3.html` (lokal) vorgelegt; Eigentümer: Knopf im Eintrag und im Fenster, „Lage“ bleibt draußen, beide Knöpfe → ADR-108. Umsetzung läuft
- **Phasentyp-Kontext:** UMSETZUNG (mit Vorlage zu Beginn)
- **Abhängigkeiten:** 10.2
- **Freigabepflichtig:** ja – ändert ADR-083 und die Anweisung an die KI
- **Empfohlene Klasse:** Entscheidung – Anfrage an die KI (Eskalations-Auslöser 1).
- **Eingangskriterien:** keine
- **Anforderungen (ab Klasse M):** FR-035
- **Zu tun:** wie V.39; die Anfrage liest vorhandene Abschnitte über die Abschnittsregel des Servers.
- **Akzeptanzkriterien:** Vorlage mit Mockup, ADR; Tests; Probe mit echtem Eintrag; Eigentümer bestätigt.
- **Betroffene Module:** context, api, ui
- **Reifegrad-Wirkung:** keine
- **Artefakte:** Code, Tests, ADR, Mockup
- **Umgesetzt (lokal, 2026-11-05, noch nicht abgenommen):** nach ADR-108. `context/appearance.py`: Anweisung je Art (Figur unverändert, Ort, Gegenstand), gemeinsame Regeln; bei Orten ohne Abschnitt „Lage“ (`take_section`); andere Arten 422. `canon`: Konstante `LOCATION`, `take_section` und `LOCATION` exportiert. `ui`: „✨ Aussehen herauslösen“ im Eintrag auch bei Ort und Gegenstand (`EntryArticle`), im Fenster „Bild erzeugen“ für alle drei, bei Ort und Gegenstand daneben „✎ Selbst ergänzen“ (`EntryImages`). Tests: Python 7 neue bzw. umgeschriebene (Anweisung je Art, „Lage“ auf jeder Ebene samt Unterabschnitt, ungegliederter Ort, leere „Lage“, andere Arten, Route mit Ort); 1151 bestanden, Abdeckung 99,87 %, `context/appearance.py` und `canon/sections.py` 100 %. Oberfläche 1 neuer, 1 angepasster Test; 562 bestanden, 98,81 / 95,45 / 98,26 / 98,97 %. E2E 15 bestanden. ruff, ruff format, `mypy --strict`, bandit, eslint, tsc, prettier, Build grün. Probe mit echter KI steht aus (nach dem Einspielen, Eigentümer).
- **Notizen:** Aus V.39.

#### 10.4: Bildansichten zerlegen

- **Status:** ✅ ERLEDIGT (2026-11-05) – zusammengeführt mit PR #207 (`1a46b59`), CI vier Jobs grün; Akzeptanzkriterien erfüllt (vorhandene Tests unverändert grün, Abdeckung nicht gesunken, E2E grün). Ausgang: Hauptkomponente `ImageGenerate` 322 Zeilen und 14 Hooks, `EntryImages` 285 Zeilen und 9 Hooks. Ergebnis: `ImageGenerate` 173 Zeilen/7 Hooks mit `ImageGenerateForm`, `BasisPreview`, `FormatChoice`, `GeneratedPreview` und den Hooks `useImageRequest`, `useImageModels`, `useImagePrice`, `useElapsed` (je eigene Datei); `EntryImages` 145 Zeilen/6 Hooks mit `EntryImageStrip` (119/2) und `EntryImageView` (112/1); `ImageViewer` (166/3) und `LooksHint` in eigene Dateien. Tests: alle 562 vorhandenen unverändert grün, 1 neuer (Entfernen scheitert – deckt die nun doppelt vorhandene Prüfung ab); Abdeckung 98,82 / 95,49 / 98,28 / 98,98 % (vorher 98,81 / 95,45 / 98,26 / 98,97); E2E 15 bestanden; eslint, tsc, prettier, Build grün
- **Phasentyp-Kontext:** UMSETZUNG
- **Abhängigkeiten:** keine
- **Freigabepflichtig:** nein – Umbau innerhalb eines Moduls, Verhalten unverändert
- **Empfohlene Klasse:** Routine – Umbau ohne Schnittstellenänderung mit vorhandenen Tests.
- **Eingangskriterien:** keine
- **Anforderungen (ab Klasse M):** keine
- **Zu tun:** `ui/src/views/ImageGenerate.tsx` (Zustand, Preis, Vorschau, Grundlage) und `ui/src/views/EntryImages.tsx` (`ImageViewer`, Herkunft) in kleinere Komponenten und Hooks; Ziel: keine Hauptkomponente über ca. 200 Zeilen, höchstens ca. 8 Hooks je Komponente.
- **Akzeptanzkriterien:** Alle vorhandenen Tests unverändert grün; Abdeckung nicht gesunken; E2E grün.
- **Betroffene Module:** ui
- **Reifegrad-Wirkung:** keine
- **Artefakte:** Code
- **Notizen:** U.1 der Bewertung (ADR-104); vor 10.5–10.8.

#### 10.5: Auflösung und Qualität bei der Bilderzeugung

- **Status:** ✅ ERLEDIGT (2026-11-05) – zusammengeführt PR #208 (`17ea244`), eingespielt 2026-11-05; Nachtrag PR #209 (`56e5d1b`, CI vier Jobs grün), eingespielt 2026-11-05. Probe des Eigentümers: Seedream 5.0 Pro 2K → 1.366 × 2.048, kaum Unterschied (Seedream lieferte schon vorher 2K für 0,09 $ und wurde nur auf 2.000 verkleinert); Seedream 5.0 Lite 4K → 2.732 × 4.096, 0,035 $, „deutlich schärfer“ – abgenommen. Nachtrag auf Wunsch des Eigentümers: Grundpreis ohne Varianten gilt für jede Stufe (ADR-109, Nachtrag); zusammengeführt. Befund: zwei Ursachen – keine Auflösung in der Anfrage (Modell nimmt meist 1K) und Verkleinern im Browser auf 2.000 Pixel beim Übernehmen. Katalog 2026-11-05: 27/63 mit `resolution`, 11 mit `quality`, Preisvarianten uneinheitlich. Server: eingestellt Seedream 5.0 Pro (1K 0,045 $, 2K 0,09 $), 27 von 67 Bildern; FLUX.2 Pro 19, Grok Imagine 2.0 15. Vergleich `mockup-10.5.html` (lokal) vorgelegt; Eigentümer: 2K voreingestellt, bis 4.096 Pixel, Qualität wo angeboten, Fotos bei 2.000 → ADR-109. Umsetzung läuft
- **Phasentyp-Kontext:** UMSETZUNG (mit Vorlage zu Beginn)
- **Abhängigkeiten:** 10.4
- **Freigabepflichtig:** ja – Schnittstelle (Kategorie 5, additiv), Grenze gespeicherter Bilder (`storage/images.py`: 5 MB, 4.096 Pixel)
- **Empfohlene Klasse:** Entscheidung – Schnittstelle und Speichergrenze (Eskalations-Auslöser 1).
- **Eingangskriterien:** keine
- **Anforderungen (ab Klasse M):** FR-035
- **Zu tun:** Frage des Eigentümers (2026-11-05): Bilder kommen immer klein. Das Skriptorium schickt nur `aspect_ratio`; 27 von 63 Bildmodellen bieten `resolution` (z. B. 1K/2K/4K), 11 eine Stufe `quality` (Katalog 2026-11-05). Vorlage: Auswahl nur bei Modellen, die sie anbieten, Preis je Stufe soweit genannt, Voreinstellung; Grenze für gespeicherte Bilder (Größe, Seitenlänge, ggf. Umwandeln) so, dass 4K-Bilder angenommen werden.
- **Akzeptanzkriterien:** Vorlage mit Mockup, ADR; Tests; Probe mit echtem 2K- oder 4K-Bild; Eigentümer bestätigt.
- **Betroffene Module:** ai_gateway, storage, api, ui
- **Reifegrad-Wirkung:** keine
- **Artefakte:** Code, Tests, ADR, Mockup
- **Umgesetzt (lokal, 2026-11-05, noch nicht abgenommen):** nach ADR-109. `storage`: Herkunft mit `aufloesung`/`qualitaet`, Bildgrenze 12 MB. `ai_gateway`: Stufen im Katalog, `ImageOrder.resolution`/`quality`, Preise je Stufe (`level_price`, Grundpreis ohne Variante getrennt von `price`). `api`: Stufen in Modellliste, Preis und Erzeugen (422 bei nicht angebotenen), Herkunft; gelieferte Bilder bis 40 MB. `ui`: `useImageLevels` (2K/„auto“ voreingestellt, Herkunft übernimmt), `useImagePrices` (Preis je Auflösung), Auswahl „Auflösung“ mit Preisen und „Qualität“ mit deutschen Namen, Herkunft zeigt die Auflösung, erzeugte Bilder und Titelbilder bis 4.096 Pixel (`GENERATED_SIDE`). Tests: Python 18 neue (Katalog, Preisstufen, Anfrage, API, Herkunft), 1169 bestanden, 99,87 %, geänderte Dateien 100 %; Oberfläche 6 neue, 4 angepasste (Saat, Titelbild 4.096, Attrappe `GENERATED_SIDE`), 569 bestanden, 98,83 / 95,51 / 98,30 / 98,98 %; E2E 15. Vertragsdatei: `resolutions`, `qualities` je Modell. ruff, mypy, bandit, eslint, tsc, prettier, Build grün. CHANGELOG für 10.2, 10.3 und 10.5 nachgetragen (10.2 und 10.3 fehlten).
- **Notizen:** Neu in 9.15 (ADR-105).

#### 10.6: Bilder im Manuskript und im E-Book (V.23)

- **Status:** ✅ ERLEDIGT 2026-11-06 (Eigentümer nach dem Einspielen von `de64667`: „Hat funktioniert.“) – zusammengeführt 2026-11-05, PR #210, `5aa544a`, CI vier Jobs grün; eingespielt 2026-11-05; Abnahme offen. Befund des Eigentümers 2026-11-06: „es erscheint kein Bild und keine Vorschau“ – auf schmalen Bildschirmen (unter 56rem) klappte „＋ Bild“ die Knöpfe hinter „⋯“ zu und versteckte sein Menü; behoben mit End-to-End-Test, PR #214 → `25a9220`, CI vier Jobs grün; eingespielt 2026-11-06. Zweiter Befund des Eigentümers 2026-11-06 (Desktop): „Aus dem Kanon“ – „passiert gar nichts“; das Fenster öffnete sich über dem Text außerhalb des Bildes (vom Eigentümer durch Hochscrollen bestätigt) – behoben mit End-to-End-Test, PR #215 → `de64667`, CI vier Jobs grün; eingespielt 2026-11-06; Abnahme bestanden) – Server 2026-11-05 (nur Anzahlen): 11 Geschichten, 33 Kapitel (Median rund 10.000 Wörter), 0 Bilder in Kapiteln, 30 Eintragsbilder. Vergleich `mockup-10.6.html` (lokal) vorgelegt; Eigentümer: Hochladen, Erzeugen und Kanon; Kopie; Zeile mit Vorschau; Bilder bleiben bis zum Löschen der Geschichte → ADR-110. Umsetzung läuft
- **Phasentyp-Kontext:** UMSETZUNG (mit Vorlage zu Beginn)
- **Abhängigkeiten:** 10.4
- **Freigabepflichtig:** ja – Datenmodell (Bildverweise im Kapiteltext, Kategorie 4), Editor
- **Empfohlene Klasse:** Entscheidung – Datenmodell (Eskalations-Auslöser 1).
- **Eingangskriterien:** keine
- **Anforderungen (ab Klasse M):** FR-034, FR-035
- **Zu tun:** wie V.23.
- **Akzeptanzkriterien:** Vorlage mit Mockup, ADR; Tests; E-Book mit Bild geprüft; Eigentümer bestätigt.
- **Betroffene Module:** manuscript, api, ui
- **Reifegrad-Wirkung:** keine
- **Artefakte:** Code, Tests, ADR, Mockup
- **Umgesetzt (lokal, 2026-11-05, noch nicht abgenommen):** nach ADR-110 (mit Nachtrag: Kapitelbilder als JPEG, Kopie aus dem Kanon im Browser, keine Route `from-entry`). `manuscript`: `pictures.py`, Ablage `bilder/`, drei Methoden, E-Book mit `<figure>`. `context`: `readable`. `api`: drei Routen (84 → 87). `ui`: `pictures.ts` (Zeile, Einfügestelle), `picturePreviews` (Block-Widget), `StoryPictureButton`/`StoryPictureDialog`, `CanonPicturePicker`, `ManuscriptEditor` mit `pictureSrc`/`insertion`. Tests: Python 18 neue (Zeilenform, Ablage, E-Book, fehlende Datei, KI-Anfragen, Routen), Sicherheitstest Routenzahl; 1189 bestanden, 99,87 %, geänderte Dateien 100 %. Oberfläche 11 neue, 580 bestanden, 98,77 / 95,31 / 98,28 / 98,91 % (vorher 98,83 / 95,51 / 98,30 / 98,98; über allen Schwellen). E2E 15. Vertragsdatei: `addStoryPicture`. Nicht im Browser angesehen (kein lokaler Zugang mit Daten) – Sichtprüfung bei der Abnahme.
- **Notizen:** Aus V.23.

#### 10.7: Bilder beim Schreiben mitschicken (V.33)

- **Status:** ✅ ERLEDIGT 2026-11-06 – zusammengeführt (PR #211 → `39c9db4`), eingespielt 2026-11-06 (`8e87aab`); Eigentümer: „Aussehen, Kleidung und Umgebung passen zum Bild und der Haken verschwindet auch wieder, nachdem man Weiterschreiben angeklickt hat.“ Token je Bild: erste Anfrage mit Bildern (Qwen 3.8 Max, 25.703 Token ein gegen rund 23.200 bei den Grok-Anfragen davor) nicht eindeutig – anderes Modell, Bildzahl nicht gespeichert; Schätzung 2.500 bleibt (Vorlage freigegeben 2026-11-05, ADR-111: Haken bei den Einträgen, nur Hauptbild, höchstens 4, Text gilt)
- **Phasentyp-Kontext:** UMSETZUNG (mit Vorlage zu Beginn)
- **Abhängigkeiten:** 10.4
- **Freigabepflichtig:** ja – Anfrage-Zusammenstellung (Kategorie 1)
- **Empfohlene Klasse:** Entscheidung – Anfrage an die KI (Eskalations-Auslöser 1).
- **Eingangskriterien:** keine
- **Anforderungen (ab Klasse M):** FR-035
- **Zu tun:** wie V.33; Token-Schätzung für Bildteile (Bewertung, Tabelle zu V.33).
- **Akzeptanzkriterien:** Vorlage, ADR; Tests; Probe nach Regel-002, soweit die Anfrage ohne Bilder gleich bleibt per Test belegt; Eigentümer bestätigt.
- **Betroffene Module:** context, ai_gateway, api, ui
- **Reifegrad-Wirkung:** keine
- **Artefakte:** Code, Tests, ADR
- **Umgesetzt (lokal, 2026-11-05, noch nicht abgenommen):** nach ADR-111. `context`: Baustein `bilder` (`pictures`, vor der Anweisung; ohne Bilder unverändert). `api`: `WriteOrder.images`, Auswahl `_pictured` (Hauptbild, höchstens `MAX_PICTURES` = 4, Reihenfolge der Nennung inkl. Szene und Gäste), Bildteile an der letzten Nachricht, Sperre ohne Bildlesen, `start` trägt `images`, Schätzung +`PICTURE_TOKENS` (2.500) je Bild. `ui`: `PictureSwitch` (Haken, Vorschauen, Aufpreis, „ohne Bild: …“), Verbrauchszeile „mit N Bildern“. Tests: 4 neue in `tests/api/test_writing_pictures.py` (1.193 Python-Tests, 99,87 %), 5 neue in `ui/src/views/WritingPictures.test.tsx` (585 Komponenten-Tests; Zeilen 98,92 %, Zweige 95,25 %), 15 End-to-End-Tests grün. Nicht im Browser angesehen (lokal keine Daten, kein Schlüssel). Offen: Token je Bild nach den ersten Anfragen aus dem Verbrauch nachprüfen.
- **Notizen:** Aus V.33.

#### 10.8: Zweiter Bildanbieter (V.24)

- **Status:** ✅ ERLEDIGT (2026-11-08) – Anbieter gewählt 2026-11-07: Runware (ADR-114). Zweite Vorlage beantwortet 2026-11-07 (ADR-115): Erwachseneninhalte ohne Prüfung bei Runware, mehrere Bildanbieter nach Kennungsformat, Grundmodelle und LoRAs in den Einstellungen, Schlüssel nur serverseitig, Kosten-Bremse über Vorab-Guthaben; Modellsuche und Probebild in `docs/research/bildanbieter.md`. Gebaut 2026-11-07 (`24d955e`, `ade0df6`; Tests grün, Probe mit echtem Bild 0,0037 $), getrennte Prüfung ohne Befund hoch/mittel. Zwei optionale Befunde umgesetzt (`778e165`, nachgeprüft). Krea 2 Raw/Turbo als eine Familie; eigene LoRA `skriptorium:2964163@3386627` privat hochgeladen, sauber auf Krea 2 Turbo (auf Raw Bildfehler). Eigentümer bestätigt 2026-11-08; offen nur noch Einspielen vom Mac (Schlüssel auf dem VPS, Durchreichen in der Compose-Datei prüfen, Probe auf dem Server). Erkundung der Bildmodelle und LoRAs 2026-11-07 (ohne Code; Ergebnisse in `docs/research/bildanbieter.md`, Folgewünsche V.56); PR 218 als Entwurf. 2026-11-08: Eigentümer „Abschließen“ – PR 218 auf „Ready for review“ für die CI; Checkpoint-Versuch nicht vorher, er bleibt in V.56 (6) mit Landeplatz 10.11. CI grün (alle vier Jobs, keine Warnungen), Eigentümer bestätigt, gemergt in `main` (`96e56bc`); eingespielt 2026-11-08 (`25c9bd6`), Schlüssel auf dem VPS eingetragen, Anbindung vom Eigentümer am Server bestätigt → ERLEDIGT 2026-11-08. Befund des Eigentümers dabei: die Kanon-Beschreibung einer Figur reicht für gutes Prompten nicht aus → V.58 (Landeplatz 10.11), kein neuer Schritt
- **Phasentyp-Kontext:** UMSETZUNG (mit Vorlage zu Beginn)
- **Abhängigkeiten:** 10.4, 10.5
- **Freigabepflichtig:** ja – neuer externer Dienst (Kategorie 3), Schlüssel im Betrieb (Kategorie 6)
- **Empfohlene Klasse:** Entscheidung – Abhängigkeit und Secrets (Eskalations-Auslöser 1).
- **Eingangskriterien:** keine
- **Anforderungen (ab Klasse M):** FR-025, FR-035
- **Zu tun:** wie V.24 (Kandidaten in `docs/research/bildanbieter.md`); `Services.images` ist ein einzelner Platz – Zuordnung Modell → Anbieter (Bewertung, Tabelle zu V.24); getrennte Prüfung für den Umgang mit dem Schlüssel.
- **Akzeptanzkriterien:** Vorlage, ADR, aktuelle Preise; Tests; Probe mit echtem Bild; Prüfung durch eine getrennte Instanz; Eigentümer bestätigt.
- **Betroffene Module:** ai_gateway, api, ui
- **Reifegrad-Wirkung:** keine
- **Artefakte:** Code, Tests, ADR
- **Notizen:** Aus V.24.

#### 10.9: Vollständige Anfrage zum KI-Text festhalten (V.42)

- **Status:** ✅ ERLEDIGT (2026-11-08) – Vorlage mit Mockup beantwortet 2026-11-08 (ADR-116): alle Schreib-Anfragen auch verworfene, letzte 50 je Geschichte, mit Antwort der KI, eigener Reiter „Anfragen“. Gebaut 2026-11-08 (`cc09b88`, `316bf34`, `89861cb`; 1.293 Python-Tests 99,90 %, 604 Komponenten-Tests 98,83 / 95,3 / 98,39 / 98,96 %, 17 End-to-End-Tests grün) – gemergt (PR #221) und eingespielt 2026-11-08 (`25c9bd6`); Probe des Eigentümers am Server bestanden (Anfrage im Reiter „Anfragen“)
- **Phasentyp-Kontext:** UMSETZUNG (mit Vorlage zu Beginn)
- **Abhängigkeiten:** keine
- **Freigabepflichtig:** ja – neue Ablage (Kategorie 4), ggf. Schnittstelle (Kategorie 5)
- **Empfohlene Klasse:** Entscheidung – Datenmodell (Eskalations-Auslöser 1).
- **Eingangskriterien:** keine
- **Anforderungen (ab Klasse M):** FR-027
- **Zu tun:** wie V.42; Ablage getrennt von der Verbrauchsdatei (Befund 6 der Bewertung).
- **Akzeptanzkriterien:** Vorlage mit Mockup, ADR; Tests; Eigentümer bestätigt.
- **Betroffene Module:** manuscript, api, ui
- **Reifegrad-Wirkung:** keine
- **Artefakte:** Code, Tests, ADR, Mockup
- **Notizen:** Aus V.42.

#### 10.10: Textqualität von Hermes 4 messen (V.41)

- **Status:** ✅ ERLEDIGT (2026-11-06) – Messung nach Regel-002 in der Cloud-Session, Bericht `spikes/hermes-10.10/README.md` (42 Ketten, 3,20 $ KI-Kosten; zwei verblindete Bewertungsrunden); Ergebnis: Denken bei Hermes nicht nutzbar (Denktext ohne Trennmarke im Vorschlag), Schleifen nachgestellt, keine Einstellung mit Wirkung nach Regel-002 (Nachlauf auf Wahl des Eigentümers). Eigentümer: „Hermes nutze ich nur, wenn andere Modelle sperren“, „Ja, nichts übernehmen“ → ADR-113. Folgevorschlag Längengrenze → V.51
- **Phasentyp-Kontext:** ERKUNDUNG innerhalb der UMSETZUNG-Phase
- **Schritt-Art (nur ERKUNDUNG):** Messung
- **Zeitbox (nur ERKUNDUNG):** eine Session
- **Abhängigkeiten:** keine
- **Freigabepflichtig:** nein für die Messung; ja für Einstellungen je Modell (Kategorie 1 prüfen)
- **Empfohlene Klasse:** Entscheidung – Vergleich von Modellen und Einstellungen nach Regel-002.
- **Eingangskriterien:** keine
- **Anforderungen (ab Klasse M):** FR-028
- **Zu tun:** wie V.41; Messung nach Regel-002 an beiden Testgeschichten (KI-Läufe in der Cloud-Session).
- **Akzeptanzkriterien:** Messung im Logbuch; ADR mit Ergebnis.
- **Betroffene Module:** ai_gateway, api (nur bei Umsetzung)
- **Reifegrad-Wirkung:** keine
- **Artefakte:** Logbuch-Eintrag, ADR
- **Notizen:** Aus V.41. Abweichung von V.41: Variante „mit Denken“ nur als Einzelanfrage gemessen (Denktext im Antworttext, `denken.py`); Strafen als drei Varianten (`frequency_penalty` 0,3, dazu Temperatur 0,6, `repetition_penalty` 1,05).

#### 10.11: Planung der nächsten Ausbaustufe

- **Status:** ✅ ERLEDIGT (2026-11-08) – Pflichtfrage mit getrennter Instanz (`docs/research/bewertung-phase-10.md`): Eigentümer „Klein umbauen“ → ADR-117; Vision-Abgleich ohne verwaiste Elemente; Phase 11 mit 16 Schritten geplant, alle vier vorgeschlagenen Themen gewählt → ADR-118; V.21, V.54, V.55 bleiben verschoben (→ 11.16)
- **Phasentyp-Kontext:** UMSETZUNG
- **Abhängigkeiten:** 10.1–10.10
- **Freigabepflichtig:** ja – neue Phasen sind Replanning
- **Empfohlene Klasse:** Entscheidung – inhaltliche Neuplanung mit Vision-Abgleich.
- **Eingangskriterien:** Vision-Abgleich an der Phasengrenze nach Phase 10
- **Anforderungen (ab Klasse M):** keine
- **Zu tun:** V.21, V.40, V.44, V.45, V.46, V.47, V.48, V.49, V.50, V.51, V.52, V.53, V.54, V.55, V.56, V.57, V.58 (und neue V-Schritte) in eine neue Phase überführen oder per ADR verwerfen. Prüfen, ob V.52–V.58 zusammen eine eigene Phase „Figuren und Bilder“ werden (V.58 Assistent liefert das „Wer“, V.57 Rezept das „Was“).
- **Akzeptanzkriterien:** Jeder verschobene Schritt hat einen neuen Schritt mit ID oder `[VERWORFEN]` mit ADR.
- **Betroffene Module:** keine (Planung)
- **Reifegrad-Wirkung:** keine
- **Artefakte:** Logbuch-Eintrag, ADR
- **Notizen:** Angelegt 2026-11-05 (ADR-105).
