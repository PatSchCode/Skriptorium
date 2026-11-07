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

### 2026-11-07 – [BEOBACHTUNG] Joschek's Spreader Gag (Krea 2): gut bei 0,6, bei 1,0 unstimmig

- Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Harness Gag erzwingt gebundenes Haar

- Zwei Anläufe für offenes Haar (9 Bilder) ohne Erfolg. Details in `docs/research/bildanbieter.md`.
- Eigentümer: Offenes Haar unter einem Kopfgeschirr ist unrealistisch; das gebundene Haar ist richtig. Erste Kombination gilt.

### 2026-11-07 – [BEOBACHTUNG] Zwei LoRAs kombiniert (Leather Cuffs + Harness Gag): funktioniert

- Beide Elemente in allen drei Seeds, Hände stimmig; Haar wird zum Zopf. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [GELÖST] Fehlbewertung Seed 101 (Hände) korrigiert

- Eigentümer: bei Seed 101 passt die Anatomie der Hände nicht. Nachgeprüft, bestätigt; Bewertung in der Recherche korrigiert. Ursache: Hände nicht in voller Auflösung geprüft, nur Seil-Ausschnitte. Lehre (erneut): bei Fesselung hinter dem Rücken immer die Hände im Ausschnitt prüfen.

### 2026-11-07 – [BEOBACHTUNG] Testavatar in Sport-BH und Shorts mit Rope Bondage: Seilwirkung auf der Haut sichtbar

- Seil eng auf der Haut mit leichter Wölbung; Seed 404 hinten bestes Takate Kote bisher. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Joschek's Getting Gagged (Krea 2): Handlung erst bei 1,0, Stoff wird durchscheinend

- Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Joschek's Panel Gag (Krea 2): erst bei 1,0

- Bei 0,6 kein Knebel, bei 1,0 vollständig. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Spider Gag: Gurt realistisch, wenn er auf der Haut unter dem Haar verläuft

- Zopf löst das Gurtproblem, lässt sie aber jünger wirken; offenes Haar über dem Gurt ist die bessere Lösung. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Joschek's Spider Gag (Krea 2): gut ab 0,6

- Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Joschek's Shiny Latex Bodysuits (Krea 2): echter Latex ab 0,6

- Ohne LoRA nur matter Elasthan. Einmal Antwort ohne Bild von Runware, Wiederholung lief. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Joschek's Bolero Straitjacket (Krea 2): stimmig ab 0,6, weiß gegen schwarz

- Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Metalstocks bei 1,0 mit Seitenansicht: gleiches Muster in sechs Seeds

- Hals weiter nicht im Balken, Rückenausschnitt trotz Gegenanweisung. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Metalstocks mit tiefer Vorbeuge: Vorbeuge gelingt, Hals im Balken nicht

- Zwei Anläufe, je sechs Bilder; tiefe Vorbeuge und vollständiger Pranger schließen sich bisher aus. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Joschek's Metalstocks (Krea 2): stimmig bei 0,6, bei 1,0 uneinheitlich; Metall-Yoke per Prompt

- Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Joschek's Yoke (Krea 2): stimmig erst bei 1,0

- Bei 0,6 Hals nicht im Joch, bei 1,0 vollständig. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Joschek's Harness Gag (Krea 2): sehr glaubwürdig ab 0,6

- Kopfgeschirr mit Ballknebel in beiden Seeds; ohne LoRA keiner. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Joschek's Hogtied (Krea 2): stimmig ab 0,6; Famegrid nicht verarbeitet

- Hogtie mit Verbindungsseil in beiden Seeds; ohne LoRA keiner. Famegrid nach über 40 Minuten bei Runware nicht bereit. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Joschek's Leather Cuffs (Krea 2): sehr glaubwürdig ab 0,6

- Lederfesseln an Hand- und Fußgelenken mit Karabinern, Hände natürlich; ohne LoRA keine Fesseln. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Alter bei Krea 2 Turbo: 21 behalten, Seed-Wahl wirkt am stärksten

- Eigentümer fragte nach Alter 18 im Prompt; abgeraten (Jugend-Bildsprache, Risiko minderjährig wirkender Figuren). Alter vorn, weiches Licht, glatte Haut: leicht jünger; Seeds 101 und 404 am nächsten an 21. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Joschek's Ball Gags (Krea 2): sicher ab 0,6

- Ohne LoRA kein Knebel; 0,6 glaubwürdig mit erhaltenem Gesicht; 1,5 verzerrt. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Fotorealismus-LoRAs: Skin Texture für Z-Image überzeugt, LoKr-LoRAs laden nicht

- Realistic Skin Texture macht Z-Image deutlich fotografischer. Amateur Photography und Realism Engine (LoKr) laden bei Runware nicht. Krea 2 Turbo sehr natürlich, Porträt aber zu alt; Mystic XXX verjüngt und rundet. Waist slider: negativ = schlanker; Runware begrenzt LoRA-Gewichte auf ±4, die Anwendung auf ±2. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Nachschärfen auf Z-Image: höhere Auflösung, aber glattere Haut

- Hochrechnen und Bild-zu-Bild (0,15/0,3) glätten die Hautstruktur; kein Gewinn an Natürlichkeit. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Z-Image mit niedrigerem CFG: Natürlichkeits-Wörter wirken stärker als der CFG-Wert

- CFG 3 und 2,5 kaum verschieden; „candid photo, natural skin texture …“ macht das Bild deutlich natürlicher. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Civitai-Bild nachgestellt: SDXL-Grundmodell mit kurzem Prompt

- Erzeugungsdaten über die Civitai-Schnittstelle gelesen und ohne Hires nachgestellt; Vergleich mit Testavatar auf SDXL und Z-Image. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] SDXL-Checkpoints scheiden aus

- RealVisXL, epiCRealism XL, CyberRealistic XL: schwache Prompt-Treue, ein unverlangtes Bild mit nacktem Oberkörper trotz Negativ-Prompt, Gesichter jünger als 21. Problematische Bilder gelöscht, nicht weitergegeben. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Vergleich von vier Checkpoints: Z-Image und Juggernaut Z vorn

- Negativ-Prompt löst das Shorts-Problem bei voller Körperbeschreibung. Krea 2 Raw mit Bildfehlern bzw. zu jung wirkend, LUSTIFY ignoriert die Kleidung und lieferte ungefragt ein Aktbild (gelöscht, nicht weitergegeben). Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Suche nach anderem Checkpoint bei Runware

- Kandidaten: Z-Image (Grundmodell), Juggernaut Z, Krea 2 Raw, SDXL-Fotorealismus (RealVisXL, epiCRealism XL, LUSTIFY), Qwen-Image; Chroma nicht vorhanden. Liste in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Oberweite im Bikini: Abstufung erkennbar, aber mild

- Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Oberweite in drei Stufen: Unterschiede gering

- „small“ etwas kleiner, „medium“ und „full“ kaum verschieden; schwarzer Bodysuit und Zusatz „in proportion“ dämpfen. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Pool mit voller Körperbeschreibung: gleiches Muster, Shorts entfallen auch hier

- Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Strand mit voller Körperbeschreibung: einheitlichste Reihe, Shorts entfallen

- Vier Bademoden wie verlangt mit Figur und jungem Gesicht; Tankini und Surf werden zu Badeanzügen. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Volle Körperbeschreibung bei Bademode: Figur zurück, Surf-Shorts werden Slip

- Badeanzug und Bikini mit Figur wie im Referenzbild und jungem Gesicht; Surf-Set knapper. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Mittelweg am See: jung trotz Sonne, Figur bleibt schlanker

- Alter vorn reicht auch bei Sonne; „athletic curvy build“ ändert die Figur kaum. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Avatar wirkt am See älter: Alter vorn im Prompt und weiches Licht helfen

- Eigentümer bemerkt älteres Aussehen am See. Alter an den Anfang, weiches Licht: wirkt wie 21, aber Figur schlanker. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Bademoden am See: vier wie verlangt, Tankini und Surf-Shorts abweichend

- Gesamtbild über vier Umgebungen: Badeanzug und Bikini verlässlich, Shorts zur Bademode Glückssache. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Bademoden am Pool: alle sechs wie verlangt

- Tankini mit Shorts und Surf-Set mit Boardshorts gelingen hier; Gesicht am einheitlichsten. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Bademoden am Strand: Bademode bleibt, Licht und Haare ändern sich

- Tankini weiter mit Slip, Surf-Shorts kürzer; Haut dunkler, Haare lockiger. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Sechs Bademoden am Testavatar: alle wie verlangt

- Nur beim Tankini Slip statt Shorts. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Kleidung zuerst im Prompt: vier von fünf Stilen jetzt wie verlangt

- Reihenfolge Kleidung → Person, Körper knapp, Längen genannt; Rock-Stil noch mit schmalem Spalt; Figur weniger kurvig. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Zehn Kleidungsstile: fünf wie verlangt, vier freizügiger, Tracht gescheitert

- Körperbeschreibung zieht bei lockerer Kleidung Bauchfreiheit und kurze Säume nach sich. Einmal `internalError` bei Runware, Wiederholung lief. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Neuer Testavatar: Mexiko, sportlich-kurvig, Bodysuit

- Eigentümer wählt Herkunft Mexiko und Proportions-Entwurf 3. Bauchfreies Top trotz Gegenanweisung; gelöst mit „toned core“ und Bodysuit. Neue Beschreibung in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Testavatar: Herkunft Mexiko bzw. Mittelamerika ändert wenig

- Vergleich Kolumbien/Mexiko/Guatemala mit Seed 101: nur leichte Verschiebungen bei Hautton, Gesichtsform und Brauen. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Alle mit dem Testavatar geprüften LoRAs als brauchbar bestätigt

- Eigentümer bestätigt zusätzlich Large Ball Gag, Rope Bondage, Metal Bondage, Tape Bondage und Plastic Zip-Cuffs. Gesamtstand in V.54 und `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Megapack 0,8 vom Eigentümer bestätigt

- In V.54 nachgetragen.

### 2026-11-07 – [BEOBACHTUNG] Megapack mit Gewicht 0,8: Knebel sicher, Gesicht weitgehend erhalten

- 0,8 als Mittelweg zwischen 0,6 (kein Knebel) und 1,0 (Gesicht verschoben). Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Megapack mit Gewicht 1,0: Knebel in allen drei Seeds, Gesicht verschoben

- Tuchknebel glaubwürdig; Gesicht runder, Haare kürzer. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Testavatar mit Megapack (Krea 2), 0,6: Seil an Handgelenken sehr gut, Knebel fehlt

- Tuchknebel in keinem der drei Seeds, Handgelenk-Seil überzeugend, Knöchel nur einseitig. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Testavatar mit Plastic Zip-Cuffs (Krea 2), 0,6: auf Anhieb stimmig

- Kabelbinder-Handschellen in allen drei Seeds eng und glaubwürdig, Figur erhalten; Arme nicht hinter der Lehne. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Tape Bondage: Handgelenke eng in einem Wickel, Kreuzwicklung nicht darstellbar

- Handgelenke in allen drei Seeds eng nebeneinander in gemeinsamem Wickel mit sichtbaren Lagen; keine Kreuzwicklung, Knöchel-Band nur um einen Knöchel. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Tape Bondage: schmale Wickel per Prompt, LoRA unter 0,6 wirkungslos

- Eigentümer: Wickel unrealistisch breit. Beschreibung „one tape width wide … wrapped around the same spot many times“ ergibt bei 0,6 schmale Bänder; bei 0,4 und ohne LoRA kein Klebeband. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Tape Bondage, Rückansicht, sechs Seeds: Knöchel jetzt zusammen, Knie nie

- Handgelenke, Mund und Knöchel in allen sechs stimmig, Knie in keinem getaped; Figur leicht verjüngt, am besten 303. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Testavatar mit Tape Bondage (Krea 2), 0,6: Handgelenke und Mund gut, Beine teils unvollständig

- Von vorn stimmig; von hinten Knöchel einzeln umwickelt, Knie frei; Figur leicht verjüngt. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Metal Bondage, Rückansicht, sechs Seeds: Handschellen hinten in fünf von sechs

- Genauere Armhaltung bringt verkettete Schellen hinter dem Rücken (außer Seed 202); Figur teils verjüngt, am besten 303 und 606. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Testavatar mit Metal Bondage (Krea 2), 0,6: Füße und Halsband gut, Handgelenke ohne Kette

- Handschellen nicht hinter dem Rücken und nicht verbunden; Figur von vorn verjüngt. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Rope Bondage, Rückansicht, sechs Seeds: Armhaltung jetzt in allen richtig

- Genauere Beschreibung der Armhaltung brachte gestapelte Unterarme in allen sechs Seeds; Handgelenke einzeln statt zusammen gebunden; Seed 101 mit dritter Hand; am besten 303, 404, 606. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Testavatar mit Rope Bondage (Krea 2), 0,6: Figur hält, Arme hinten nicht stimmig

- Vorderansicht stimmig, Rückansicht mit falscher Armhaltung. Leberfleck erstmals sichtbar. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Armbinder Krea mit Seed 404 angenommen

- Eigentümer nimmt Seed 404 an. Rezept in `docs/research/bildanbieter.md`, Stand in V.54 nachgetragen.

### 2026-11-07 – [BEOBACHTUNG] Armbinder Krea, sechs Seeds: Form und Kleidung stabil, Sitz schwankt

- Form, Kleidung und Gesicht in allen sechs stabil; Sitz bei allen leicht links der Mitte, am besten Seed 404. Stützt den Wunsch V.53 (fester Seed). Details in `docs/research/bildanbieter.md`. Skript `szene.py` nimmt den Seed jetzt aus `SEED`.

### 2026-11-07 – [BEOBACHTUNG] Armbinder Krea 1,0, von hinten, Kleidung festgehalten: Kleidung bleibt

- Ausdrückliche Stoffangabe hält die Kleidung gegen die LoRA. Armbinder näher an der Mitte, ein Arm wirkt noch frei. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Armbinder Krea 1,0 mit „single sleeve“: Form stimmt, Sitz und Kleidung nicht

- Ein einziger geschnürter Ärmel, aber seitlich statt mittig hinter dem Rücken; Kleidung wird zu Netzstoff und Leder. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Testavatar mit Armbinder, Gewicht 0,6: keiner der beiden LoRAs gelingt

- Z-Image-Turbo (Armbinder-Flux): Armbinder erkennbar, Figur verloren (Gesicht, Haare, Kleidung, Körper). Krea 2 (Armbinder): Figur erhalten, aber zwei getrennte Ärmel statt eines Armbinders. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] German Handcuffs brauchbar; kleinere Schellen per Prompt

- Eigentümer bestätigt German Handcuffs als brauchbar (V.54 nachgetragen). Wunsch: Schellen passend zum Handgelenk. Zusatz „small, slim … snugly … true-to-scale“ im Prompt macht Schellen schmaler und enger, Kette kürzer; 0,6 und 0,4 kaum verschieden. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Testavatar mit German Handcuffs (Krea 2 Turbo): Reihenfolge im Prompt entscheidet

- Gewicht 0,6, Handschellen hinter der Avatar-Beschreibung: Hände nicht hinter dem Rücken. Handschellen vor die Beschreibung gestellt: bei 0,6 und 1,0 korrekt hinter der Stuhllehne. Details und Kosten in `docs/research/bildanbieter.md` (Abschnitt Testavatar). Skript `szene.py` im Scratchpad nimmt das Modell jetzt aus der Umgebungsvariable `MODEL`.

### 2026-11-07 – [BEOBACHTUNG] Alle LoRAs von „sarahpeterson“ aussortiert

- **Entscheidung des Eigentümers** nach Durchsicht aller Modelle des Erstellers auf Civitai: lieblos gemacht, mehr Fehler und Inkonsistenzen als Nutzen (Handschellen; Bound on stomach zeigt Hogtie und gleichzeitig eine Hand am Buch), Qualität fragwürdig, Frauen stark überzeichnet – kein Inhalt mit Anspruch.
- **Betroffen:** die fünf Uploads Rope tied shibari, Handcuffed, Bound on stomach, Bite gag und cuffed behind back (über die Civitai-API geprüft: auch „cuffed behind back“ stammt von „sarahpeterson“) sowie alle weiteren der Reihe. Vermerk in `docs/research/bildanbieter.md` und in V.54. Uploads bleiben im Runware-Konto, Löschen per API nicht möglich.
- **Verbleibend brauchbar:** Z-Image-Turbo – Large Ball Gag (FloorInspector), Armbinder (AI_After_Dark); Krea 2 – Plastic Zip-Cuffs, Megapack, Rope Bondage, Metal Bondage, Tape Bondage, Armbinder.
- **Nebenbei:** PR 218 auf Entwurf gestellt (Wunsch des Eigentümers); die CI läuft bei Entwürfen nicht.

### 2026-11-07 – [BEOBACHTUNG] Reihe „Sarah Petersons“: Name des Erstellers, Trainingsumfang unbekannt

- Frage des Eigentümers nach den Trainingsbildern. Befund: „sarahpeterson“ ist der Benutzername des Erstellers bei Civitai (Reihe für SD 1.5, SDXL, Chroma, Z-Image, Flux Klein, Qwen), kein Hinweis im Text auf eine bestimmte abgebildete Person. Dateiköpfe der vier Z-Image-LoRAs nennen keine Bildanzahl; nur Schritte (2.901–4.248) und je eine Bildbeschreibung, die nur aus dem Auslösewort besteht (`ss_tag_frequency` mit Zähler 1 – *Deutung, nicht belegt:* sehr kleiner Datensatz oder unvollständige Angabe). Wer auf den Trainingsbildern zu sehen ist, lässt sich aus Datei und Beschreibung nicht feststellen; Beispielbilder bei Civitai nicht angesehen.

### 2026-11-07 – [BEOBACHTUNG] Testavatar mit Large Ball Gag, Gewicht 0,6: Figur bleibt erkennbar

- Z-Image-Turbo, Seed 101, `skriptorium:999177@2731175` Gewicht 0,6, sitzend auf Stuhl, von vorne; Knebel, Hände hinter der Lehne und Knöchel ausdrücklich im Prompt (0,0025 $).
- Ergebnis: Gesicht, welliges Haar, Kleidung und kurvige Figur nahe an der Referenz; roter Ballknebel mit Riemen sitzt, Hände hinter der Lehne, Knöchel an den Stuhlbeinen gebunden. Bislang die beste Kombination aus Wiedererkennung und LoRA-Wirkung.

### 2026-11-07 – [BEOBACHTUNG] Testavatar, Shibari 0,6 mit Beinfesselung im Prompt

- Weg 1 auf Wunsch des Eigentümers: Gewicht 0,6, Prompt um „legs bound together with rope at the thighs, knees and ankles“ ergänzt (je 0,0025 $).
- Von vorne: Gesicht nahe an der Referenz (welliges Haar), Brust- und Taillenbänder, Beine an Oberschenkeln, Knien und Knöcheln gebunden – vollständige Fesselung bei erhaltener Wiedererkennung. Ausschnitt etwas eckiger als die Standardkleidung.
- Von hinten: Handgelenke hinten gebunden, Brustband, Längsseil; Beine nur an den Knöcheln sichtbar gebunden; Gesicht weiter älter mit glattem Haar – die Rückenansicht bleibt der schwache Punkt.
- Folge: Für den Testavatar mit Fessel-LoRAs Gewicht 0,6 und alle gewünschten Fesselungen ausdrücklich im Prompt.

### 2026-11-07 – [BEOBACHTUNG] Testavatar mit Shibari, Gewicht 0,6: Gesicht näher, Fesselung schwächer

- Wie zuvor, aber Gewicht 0,6 (je 0,0025 $). Vergleich mit Referenz (Seed 101) und Gewicht 1,0, Gesichter vergrößert.
- Gesicht: von vorne deutlich näher an der Referenz (jünger, welliges Haar), aber nicht gleich; von hinten weiter glattes, kürzeres Haar und älter. Kleidung jetzt durchgehend schwarz.
- Fesselung: Brust- und Taillenbänder, Arme bzw. Handgelenke hinten gebunden – aber die Beine sind nicht mehr gebunden (bei 1,0 von der LoRA selbst ergänzt, im Prompt nicht verlangt).
- Folge: Zielkonflikt Wiedererkennung gegen Wirkung der LoRA. Offen: 0,6 mit Beinfesselung ausdrücklich im Prompt, oder 0,8; dauerhaft eine eigene Figuren-LoRA.

### 2026-11-07 – [BEOBACHTUNG] Testavatar mit Rope tied shibari: Fesselung gut, Gesicht wandert

- Z-Image-Turbo, Seed 101, `skriptorium:1501202@2605811` Gewicht 1,0, Ansicht von vorne und von hinten (je 0,0025 $).
- Fesselung: vorne Seilbänder über und unter der Brust und an der Taille, Beine an Oberschenkeln, Knien und Knöcheln gebunden, Arme hinten; hinten Handgelenke gebunden, Brustbänder, Seil über die Schultern, Knöchel gebunden – straff und glaubwürdig.
- Abweichungen vom Referenzbild: Gesicht deutlich älter und anders, Haare kürzer und glatt; vorne V-Ausschnitt statt Rundhals, hinten dunkelblaue statt schwarze Leggings. Die LoRA zieht das Aussehen weg vom Testavatar. Figur (kurvig) bleibt erhalten.
- Gegenmittel (nicht erprobt): Gewicht 0,6–0,7. Unklar, ob „Sarah Petersons“ der Name des Autors oder einer realen Person auf den Trainingsbildern ist – im zweiten Fall würde die LoRA Züge einer echten Person übertragen.

### 2026-11-07 – [BEOBACHTUNG] Testavatar: Körperbau B kurvig

- Eigentümer wählt Entwurf B (kurvig). Testavatar vollständig festgelegt (Beschreibung, Körperbau, Standardkleidung, Z-Image-Turbo, Seed 101) in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Drei Körperbau-Entwürfe für den Testavatar

- Auf Wunsch des Eigentümers: A athletisch, B kurvig, C groß und langbeinig (Seed 101, 0,0039 $). B klar anders, A und C ähnlich (Körpergröße ohne Bezugsobjekt nicht darstellbar). Bewusst kein sehr zierlicher Entwurf (wirkt leicht jünger). Wahl offen.

### 2026-11-07 – [BEOBACHTUNG] Testavatar festgelegt: Seed 101

- Eigentümer wählt Seed 101. Testavatar = Beschreibung und Standardkleidung aus `docs/research/bildanbieter.md` („Testavatar“), Z-Image-Turbo, Seed 101.

### 2026-11-07 – [BEOBACHTUNG] Testavatar mit figurbetonter Kleidung

- Eigentümer: Kleidung muss figurbetont sein, damit Vergleiche aussagekräftig sind. Standardkleidung jetzt schwarzes enges Langarm-Oberteil und Leggings, barfuß; Beschreibung um „mature adult facial features“ ergänzt (vorher wirkten zwei Seeds jünger). Vier Ganzkörperbilder einheitlich und klar erwachsen. Beschreibung in `docs/research/bildanbieter.md` aktualisiert.

### 2026-11-07 – [BEOBACHTUNG] Testavatar als Ganzkörperaufnahme

- Wunsch des Eigentümers nach vollständigen Porträtaufnahmen: vier Ganzkörperbilder (Z-Image-Turbo, gleiche Seeds, 0,0065 $). Figur stimmig; bei Seeds 202 und 303 wirkt das Gesicht jünger – für eine klar erwachsene Testfigur 101 oder 404 empfohlen.

### 2026-11-07 – [BEOBACHTUNG] Testavatar angelegt

- Vorgabe des Eigentümers: 21 Jahre, weiblich, südamerikanisch. Beschreibung und erste vier Porträts (Z-Image-Turbo, 0,0052 $) in `docs/research/bildanbieter.md` („Testavatar“). Die vier sind sehr ähnlich; der Leberfleck fehlt. Auswahl offen.

### 2026-11-07 – [BEOBACHTUNG] Eigentümer: beide Armbinder brauchbar

- Eigentümer: „ja beide definitiv brauchbar“ → `skriptorium:691492@2536151` (Z-Image-Turbo) und `skriptorium:2767766@3119356` (Krea 2) als nutzbare LoRAs vorgemerkt.

### 2026-11-07 – [BEOBACHTUNG] Armbinder: nur mit LoRA, dann auf beiden Modellen gut

- Test Armbinder-Flux (Z-Image-Turbo) und Armbinder (Krea 2 Turbo), je ohne/mit, 0,021 $. Ohne LoRA in keinem Modell ein Armbinder; mit LoRA beide glaubwürdig (Schnürung, Schulterriemen), Krea etwas detailreicher, Z-Image günstiger. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Armbinder-LoRAs gesucht

- Suche auf Wunsch des Eigentümers: für Z-Image-Turbo vier (Armbinder-Flux, ArmRestraints-Set, MonoGlove, Bolero-Zwangsjacke), für Krea 2 drei (Armbinder, Boxtie armbinder, Bolero-Zwangsjacke); alle im passenden Format. Nichts hochgeladen. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Eigentümer: Kettenhandschellen

- Eigentümer: „wir bleiben bei Kettenhandschellen“ → für Handschellen Z-Image-Turbo mit „cuffed behind back“ (`skriptorium:1756180@2568521`); die Scharnier-LoRA (`skriptorium:3020654@3429711`) bleibt ungenutzt im Konto.

### 2026-11-07 – [BEOBACHTUNG] Scharnier-Handschellen: nur mit LoRA auf Krea 2

- Test auf Wunsch des Eigentümers, 0,019 $: Prompt allein liefert bei Z-Image-Turbo Kettenhandschellen, bei Krea 2 Turbo gar keine; mit „Hinged Handcuffs (held)“ (`skriptorium:3020654@3429711`, Krea 2) angelegte Schellen mit starrem Stahlteil hinter der Lehne. Hände in voller Auflösung geprüft.

### 2026-11-07 – [BEOBACHTUNG] Rigid und hinged Cuffs: kaum etwas vorhanden

- Suche auf Wunsch des Eigentümers. Nur „Hinged Handcuffs (held)“ für Krea 2 (gehalten, nicht angelegt) und „Rigidstock Cuff“ (Stockfessel, FLUX/Pony/Illustrious, kohya). Nichts hochgeladen. Details in `docs/research/bildanbieter.md`.

### 2026-11-07 – [BEOBACHTUNG] Handschellen hinter dem Rücken: die Ansicht von hinten entscheidet

- Test „cuffed behind back“ (Z-Image-Turbo) und German Handcuffs (Krea 2 Turbo), je ohne/mit, Verhörraum von schräg hinten, 0,021 $. Alle vier zeigen die Handschellen hinten; am überzeugendsten Z-Image-Turbo mit LoRA (eng sitzend, Arme hinter der Lehne). Details in `docs/research/bildanbieter.md`. Hände in voller Auflösung geprüft (Lehre aus den Korrekturen).

### 2026-11-07 – [BEOBACHTUNG] Handschellen-LoRAs gesucht

- Auf Wunsch des Eigentümers (realistische, tragende Fesselung bevorzugt). Liste in `docs/research/bildanbieter.md`: für Z-Image-Turbo „cuffed behind back“ und „arms behind back“ aus der Reihe Sarah Petersons; für Krea 2 German Handcuffs, Leather Cuffs, Standing Arrest u. a.; „Metal Cuffs (Police Style)“ im kohya-Format (vermutlich nicht ladbar). Nichts hochgeladen.

### 2026-11-07 – [GELÖST] Bewertung Shibari korrigiert

- Eigentümer meinte den Shibari-Vergleich (Frau im Schneidersitz): Mit LoRA ist die Seilverbindung realistischer. In voller Auflösung bestätigt: ohne LoRA dekoratives, aufgelegtes Muster ohne Spannung; mit „Rope tied shibari“ tragende Seilführung um Oberarme und Rumpf, ins Material eingeschnitten, Beine mehrfach gebunden. Meine Bewertung („kein Gewinn“) hatte das ordentlichere Muster höher gewichtet als die Funktion – falsch; korrigiert. Die Hogtie-Korrektur (Eintrag darunter) entstand aus einem Missverständnis der Rückmeldung, ist aber in voller Auflösung belegt und bleibt.

### 2026-11-07 – [GELÖST] Bewertung Hogtie korrigiert

- Eigentümer: Mit LoRA war die Seilverbindung realistischer. In voller Auflösung nachgeprüft: Mit „Bound on stomach“ verbindet eine weiße Kordel mit Schnallen Knöchel und gebundene Hände (echte Hogtie-Verbindung); ohne LoRA führt das Juteseil nur zur Hüfte. Meine erste Bewertung („weißer Stab, schlechter“) beruhte auf der verkleinerten Übersicht – falsch. Recherche korrigiert. Lehre: Einzelheiten von Fesselungen nur in voller Auflösung beurteilen.

### 2026-11-07 – [BEOBACHTUNG] Reihe „Sarah Petersons“ auf Z-Image-Turbo: nur der Beißknebel lohnt

- Auf Wunsch des Eigentümers vier Teile der Reihe (Shibari, Handschellen, Hogtie, Beißknebel) privat hochgeladen und je ohne/mit LoRA verglichen, 8 Bilder, 0,014 $. Ergebnis in `docs/research/bildanbieter.md`: Z-Image-Turbo zeigt Shibari über Kleidung und Hogtie schon ohne LoRA gut; Handschellen landen in beiden Fassungen vorn; Hogtie mit LoRA schlechter (Stab statt Seil); nur der Beißknebel profitiert deutlich. Nebenbefund: Das frühere Kinbaku-Problem auf Z-Image lag wohl am Motiv mit zwei Figuren, nicht an Seil allgemein (Deutung).

### 2026-11-07 – [BEOBACHTUNG] Z-Image-Turbo mit drei LoRAs: Ball Gag hilft, Hands wenig, UltraReal schadet

- Auf Wunsch des Eigentümers drei LoRAs privat hochgeladen (Hands, Large Ball Gag, Lenovo UltraReal; `z_image_turbo`), alle laden fehlerfrei. Je ein Vergleich ohne/mit LoRA, Seed 777, zusammen 0,0114 $. Details in `docs/research/bildanbieter.md`.
- Large Ball Gag: deutlich besser (Riemen, Hände hinten). Hands: kleine Verbesserung, aber das Kinbaku-Motiv scheitert an Z-Image-Turbo selbst (drei Frauen, kaum Seilbilder). Lenovo UltraReal: Porträt glatter und jünger, schlechter als ohne.
- Reibung: Upload-Skript war fest auf `krea_oss_2` eingestellt – Architektur jetzt über `ARCH` wählbar.

### 2026-11-07 – [BEOBACHTUNG] Erkundung Z-Image: Unterschied Base/Turbo, LoRA-Lage

- Auftrag des Eigentümers: Unterschied Z-Image / Z-Image-Turbo, vorhandene LoRAs, Kleidung und die bisherigen Themen. Ergebnis in `docs/research/bildanbieter.md` („Erkundung Z-Image“): Turbo = verdichtet, 8 Schritte, ohne CFG/Negativ-Prompt, sehr fotorealistisch, wenig Vielfalt; Z-Image = Grundmodell, 28–50 Schritte, CFG und Negativ-Prompt, mehr Vielfalt. Civitai 1.123 LoRAs (843 Turbo); bei Runware zu den Themen keine – Upload nötig. Stichprobe Dateiformat: alle passend (diffusers). Hand-LoRA mit 313.117 Downloads gefunden (Handproblem bei Fesselungen).

### 2026-11-07 – [BEOBACHTUNG] Modellvergleich: Z-Image-Familie vorn

- Ziel des Eigentümers: möglichst fotorealistisch, Modell ohne Einschränkungen, fehlende Dinge per LoRA. Vergleich von sieben Grundmodellen bei Runware (Porträt, Knebel am See; Motiv 3 weggelassen), 14 Bilder, 0,078 $. Tabelle und Bewertung in `docs/research/bildanbieter.md`.
- Kurz: Z-Image-Turbo (0,13 Cent, 4 s) natürlichstes Porträt und Knebel ohne LoRA (Hände aber vorn); Z-Image-NSFW-Unlock und Juggernaut Z folgen der Fesselung am besten; Krea 2 Turbo lässt Knebel und Fesseln ohne LoRA weg; SDXL-Modelle (epiCRealism, LUSTIFY) detailreich, aber mit Zusatzteilen im Knebel-Motiv; HiDream wirkt retuschiert.

### 2026-11-07 – [BEOBACHTUNG] MOSS Image: nur bei fal.ai, dort mit Prüfung und ohne LoRAs → V.55

- Interesse des Eigentümers an MOSS Image. Geprüft (nur lesend): OpenRouter nein, Runware nein (auch kein Upload, Architektur nicht vorgesehen), fal.ai ja (`fal-ai/moss-image`, 0,05 $ je Megapixel, Prüfung ohne Freischaltung immer an, kein LoRA-Feld), Replicate ungeprüft. Offenes Modell (Apache-2.0); selbst betreiben ausgeschlossen (Projektkontext Abschnitt 3). Als V.55 mit Landeplatz 10.11 angelegt.

### 2026-11-07 – [BEOBACHTUNG] Alten Shibari-Upload löschen – geht nicht per API

- Eigentümer: Upload `skriptorium:591433@3318444` löschen. Runware-Doku und CLI (`runware model …`: search, show, schema, pricing, examples, upload) kennen kein Löschen eigener Modelle; `delete` gibt es nur für Medien (`mediaStorage`). Nicht dokumentierte Aufrufe nicht ausprobiert. Weg: Dashboard von Runware durch den Eigentümer (ob dort angeboten, nicht geprüft) oder Ersetzen durch erneuten Upload (V.54). Bis dahin unschädlich: privat, lädt nicht, Speicher im Beta kostenlos.

### 2026-11-07 – [BEOBACHTUNG] V.54 angelegt: weitere LoRAs später

- Eigentümer fragte, warum der S4-Schlüssel nicht als Netzwerk-Secret geht. Antwort: S3/S4 signiert jede Anfrage mit dem geheimen Schlüssel (wechselnde Signatur), ein fester Kopfzeilen-Schlüssel vom Proxy reicht nicht – der Schlüssel müsste im Container liegen (Umgebungsvariable) oder der Mac erzeugt eine vorab signierte Upload-Adresse.
- Eigentümer: „wir lassen das Thema vorerst und greifen später weitere LoRAs auf“ → V.54, Landeplatz 10.11. Die umgewandelte Shibari-Datei lag nur im Scratchpad dieser Session und geht mit ihr verloren; das Umwandlungsverfahren steht im Logbuch-Eintrag „Shibari umgewandelt“.

### 2026-11-07 – [BEOBACHTUNG] 10.8: Shibari umgewandelt, Upload zu Runware blockiert

- Eigentümer: „wandle Shibari um und lade sie neu hoch“, Ablage „Kurzzeit-Dateihoster“. Runware nimmt Modelle nur über eine Download-Adresse an (auch die CLI, `runware model upload --download-url`).
- Umwandlung in der Session (Skripte im Scratchpad, ohne Zusatzpakete): Original 234,7 MB, kohya-Format, F32, Rang 16, Alpha 16 (Faktor 1). 256 von 264 Modulen eindeutig den Modulen der funktionierenden LoRAs zugeordnet (`lora_unet_blocks_…` → `diffusion_model.blocks.…`, `lora_down`/`lora_up` → `lora_A`/`lora_B`); weggelassen 8 Module ohne Gegenstück (`first`, `last_linear`, `tmlp_0/2`, `tproj_1`, `txtfusion_projector`, `txtmlp_1/3` – Namen im Original von Krea 2 Raw nicht nachprüfbar, Hugging Face verlangt Anmeldung). Ergebnis 228,6 MB, Kopf gegen Tape Bondage geprüft: gleiche 512 Schlüssel, keine Formfehler.
- Upload: litterbox.catbox.moe antwortete „Invalid uploader“; ein zweiter Versuch mit Testdatei (litterbox, tmpfiles.org) wurde von der Sicherheitsprüfung der Umgebung als möglicher Datenabfluss blockiert – nicht umgangen. Umgewandelte Datei liegt nur im Scratchpad dieser Session.
- Eigentümer: „Freigabe“ für den Upload zu einem Kurzzeit-Hoster. litterbox mit der echten Datei erneut „Invalid uploader“ (wohl Sperre der Herkunftsadresse); file.io (Löschen nach erstem Abruf) von der Sicherheitsprüfung der Umgebung blockiert – die Freigabe im Gespräch genügt ihr nicht, nötig wäre eine Berechtigungsregel in den Einstellungen. Nicht weiter versucht.
- Eigentümer: Berechtigungsregel „nur für diese Session“ → eng gefasste Erlaubnis für genau den einen Upload-Befehl in `.claude/settings.local.json` (nicht committet). Die Regel griff (Befehl lief durch die Prüfung), aber file.io ist aus der Umgebung nicht erreichbar: zweimal Verbindungsabbruch, auch die Startseite (`ws_closed_mid_exchange` am Proxy). Regel danach gelöscht.
- Offen: Weg zu einer Download-Adresse (Eigentümer entscheidet). Alter Upload `skriptorium:591433@3318444` (nicht ladbar) liegt weiter im Konto.

### 2026-11-07 – [BEOBACHTUNG] 10.8: drei weitere LoRAs – zwei wirken stark, Shibari lädt nicht

- Eigentümer wählt alle drei geprüften Kandidaten. Privat hochgeladen: `skriptorium:2728181@3066750` (Metal Bondage), `skriptorium:591433@3318444` (Shibari, Gewicht 0,4, Auslösewort), `skriptorium:2351806@3096239` (Tape Bondage); alle nach einigen Minuten in der Modellsuche.
- Vergleich auf Krea 2 Turbo (Seed 777, je ohne und mit LoRA, bekleidete erwachsene Figuren): Metal Bondage (Gewicht 1,0, 0,0136 $) – ohne LoRA Schellen an den Handgelenken mit loser Kette, mit LoRA Handschellen an der Wand und Fußschellen mit Kette sichtbar; Abweichung 34,6. Tape Bondage (1,0, 0,0161 $) – ohne LoRA gar kein Klebeband (und eine ältere Frau ohne Fesseln), mit LoRA Klebeband über dem Mund, um Rumpf und Stuhl, an den Beinen; Abweichung 38,6. Nebenwirkung Tape: Kleidung wechselt von Hose zu Rock mit Strumpfhose.
- Shibari: Bild mit LoRA → HTTP 400 `failedLoraLoad` („incompatible format or configuration“) – das kohya-Format des Dateikopfs (`lora_unet_…`) nimmt Runware für Krea 2 nicht. Upload liegt trotzdem im Konto. Möglichkeiten: Datei ins diffusers-Format umwandeln und neu hochladen (Lizenz erlaubt Abwandlungen), oder den Upload löschen.

### 2026-11-07 – [SESSIONENDE] Nachtrag: LoRAs erprobt, Wiedereinstieg

- **Seit dem letzten Sessionende:** Civitai-Schlüssel als Netzwerk-Secret; drei LoRAs privat zu Runware hochgeladen (`skriptorium:2964163@3386627`, `…2767605@3115420`, `…2742699@3142259`), auf Krea 2 Turbo sauber (Raw mit Bildfehlern); Krea 2 Raw/Turbo als eine Familie im Code (`fb29b82`); Proben zu Seil, Knebel, Takate Kote, Kinbaku; V.53 (fester Seed) angelegt. KI-Kosten der Proben zusammen rund 0,20 $ (Runware-Guthaben).
- **Wiedereinstieg:** neue Session auf `feat/10.8-zweiter-bildanbieter`; CI von [PatSchCode/Skriptorium#218](https://github.com/PatSchCode/Skriptorium/pull/218) prüfen; Bestätigung des Eigentümers zu 10.8; Einspielen vom Mac (`RUNWARE_API_KEY` mit dem zeilenweisen Befehl aus dem Runbook in `.env`, Durchreichen in der Compose-Datei prüfen); danach 10.9.
- **Kontextgröße:** weit über der Grenze (Eigentümer: „Weiter hier“); nächste Session neu beginnen.

### 2026-11-07 – [BEOBACHTUNG] V.53 angelegt: fester Seed beim Bilderzeugen

- Eigentümer: „nimm den festen Seed als Wunsch für 10.11 auf“ → V.53 im Fahrplan, Landeplatz 10.11 (Startwert wählbar, anzeigen, in der Herkunft festhalten; Unterstützung je Anbieter klären). Kein Code.

### 2026-11-07 – [GELÖST] 10.8: Hände bei der Box-Fesselung – mehrere Seeds statt genauer Beschreibung

- Weg 1 auf Wunsch des Eigentümers: einfachere Beschreibung (Kinbaku-Prompt ohne Handdetails), Rope Bondage 1,2, Krea 2 Turbo, fünf Seeds (11, 222, 3333, 4444, 5555), je 0,0037 $, zusammen 0,0185 $.
- Ergebnis: Seed 5555 unbrauchbar (drei statt zwei Figuren); bei 11, 222, 3333, 4444 Unterarme waagerecht übereinander, Handgelenke mittig gebunden, Hände locker am anderen Unterarm – deutlich besser als mit der ausführlichen Handbeschreibung. Am saubersten 4444, dann 222.
- Folge für die Arbeit mit dem Skriptorium: bei schwierigen Posen mehrmals „Neu erzeugen“ statt die Beschreibung aufzublähen. Feste Seeds kann das Skriptorium heute nicht vorgeben (jedes Bild ein neuer Zufallswert).

### 2026-11-07 – [BEOBACHTUNG] 10.8: Hände bei der Box-Fesselung – genaue Beschreibung verschlechtert sie

- Eigentümer: „Die Hände passen nicht.“ Prompt um Handhaltung ergänzt (Handgelenke in der Rückenmitte gekreuzt und gebunden, Handflächen flach am anderen Unterarm, Finger locker); Seeds 777 und 1903, sonst unverändert; je 0,0037 $.
- Ergebnis: Handgelenke jetzt mittig gestapelt und umwickelt, aber Hände zeigen mit offenen Handflächen nach außen, bei Seed 777 hat die jüngere Figur zu viele Hände. Die ausführliche Handbeschreibung macht das Modell eher unsicherer.
- Möglichkeiten (nicht erprobt): mehrere Seeds erzeugen und das beste wählen; Hände nur knapp beschreiben oder verdecken (Ausschnitt, Ärmel); Hände nachträglich ausbessern (Inpainting – das Skriptorium kann das heute nicht, wäre ein neuer V-Schritt).

### 2026-11-07 – [BEOBACHTUNG] 10.8: Kinbaku mit zwei Figuren – Ansicht von hinten trifft die Box-Fesselung

- Wunsch des Eigentümers: enges Kinbaku, Trainerin ebenfalls gebunden. Krea 2 Turbo, Rope Bondage Gewicht 1,2, Seed 777, Querformat 1216 × 832, Prompt mit Dreiviertelansicht von hinten, zwei erwachsene Frauen kniend im Dojo, schwarze enge Kleidung, Unterarme waagerecht gestapelt, Bänder über und unter der Brust, Längsseil am Rücken; 0,005 $.
- Ergebnis: beide gebunden; Unterarme waagerecht hinter dem Rücken, zwei Brustbänder, Knoten und Längsseil am Rücken gut erkennbar – deutlich näher an Takate Kote als die Ansicht von vorn. Abweichung: Schulterseile laufen als X nach oben (eher Geschirr), Hände greifen die Ellbogen.
- Folge: Bei Fesselungen auf dem Rücken die Ansicht von hinten oder schräg hinten in den Prompt; Gewicht 1,2 ohne sichtbare Bildfehler.

### 2026-11-07 – [BEOBACHTUNG] 10.8: Takate Kote – keine der Varianten trifft die Fesselung

- Wunsch des Eigentümers. Krea 2 Turbo, Seed 777, Gewicht 1,0, Prompt: Frau im Yukata kniend auf Tatami, Takate Kote (Unterarme waagerecht hinter dem Rücken, zwei Seilbänder über und unter der Brust, Seil unter den Armen). Ohne LoRA 0,0037 $, Rope Bondage 0,005 $, Megapack 0,005 $.
- Ohne LoRA: kein Seil, Arme vorne verschränkt („folded“ falsch gedeutet). Rope Bondage: drei Seilbänder um Brust und Taille, Hände hinten auf Hüfthöhe – kommt am nächsten, aber keine waagerecht gestapelten Unterarme. Megapack: zwei Bänder um die Brust, Handgelenke hinten seitlich gebunden. Bei keiner Fassung ist die eigentliche Box-Fesselung von hinten erkennbar.
- Möglichkeiten (nicht erprobt): Ansicht von hinten oder schräg hinten im Prompt, Gewicht 1,2, die spezialisierte LoRA 縛り/shibari (`591433@3318444`, 25.521 Downloads) hochladen.
- Nebenbefund: Alle drei PNG-Dateien von Runware genau 3.037.407 Byte groß, Inhalt verschieden (Prüfsummen) – vermutlich kaum komprimiert.

### 2026-11-07 – [BEOBACHTUNG] 10.8: Megapack wirkt bei Knebel deutlich

- Wunsch des Eigentümers: Vergleich mit Knebel am See. Krea 2 Turbo, Seed 777, Gewicht 1,0, Prompt: Frau im Sommerkleid am Seeufer, Hände hinten mit Seil, roter Ballknebel mit Lederriemen. Ohne LoRA 0,0037 $, mit Megapack 0,0037 $ (vorher 0,0124 $ – Abrechnung nach Rechenzeit; *Deutung:* LoRA diesmal schon geladen).
- Ergebnis: ohne LoRA weder Knebel noch Fesseln – das Grundmodell lässt beides einfach weg; mit Megapack Ballknebel mit Riemen, Seil um Oberarme und Handgelenke hinten. Knebel sitzt leicht seitlich im Mund. Mittlere Pixelabweichung 26,3 von 255.
- Folge: Die LoRAs lohnen sich bei Motiven, die Krea 2 allein nicht darstellt (hier: Knebel, Fesselung überhaupt); bei einfachen Seilszenen kaum (Eintrag darunter).

### 2026-11-07 – [BEOBACHTUNG] 10.8: Wirkung der Seil-LoRAs gering – Krea 2 Turbo kann Seile schon

- Eigentümer: „Die Bilder der unterschiedlichen LoRAs sehen identisch aus.“ Kontrollvergleich auf Krea 2 Turbo, gleicher Prompt (Frau auf Stuhl im Keller, Seil um Rumpf, Hände hinten, Knöchel an Stuhlbeinen), Seed 777, Gewicht 1,0: ohne LoRA 0,0037 $, Megapack 0,0124 $, Rope Bondage 0,0149 $.
- Ergebnis: Schon ohne LoRA Seil um Rumpf und Handgelenk; die LoRAs ändern Einzelheiten – Megapack fesselt zusätzlich die Knöchel und lässt Seil herabhängen, Rope Bondage legt ein Brustgeschirr (Seil über und unter der Brust) und bindet die Knöchel. Mittlere Pixelabweichung zur Fassung ohne LoRA 18,6 (Megapack) und 11,4 (Rope) von 255. Hände in keiner Fassung hinter der Lehne.
- Deutung: Bei einfachen Seilmotiven bringt das Grundmodell das meiste selbst; die LoRAs sollten sich bei Motiven zeigen, die Krea 2 allein nicht kann (Knebel, Klebeband, Hogtie, Aufhängung) – noch nicht geprüft.

### 2026-11-07 – [BEOBACHTUNG] 10.8: zwei weitere LoRAs hochgeladen und erprobt

- Eigentümer wählt aus der Liste: Bondage & Gags Megapack (`2767605@3115420`) und Joschek's Rope Bondage v2 (`2742699@3142259`). Dateiköpfe: beide auf Krea 2 Raw, Rang 64 (431 bzw. 678 Trainingsbilder), keine Auslösewörter – beschreibende Prompts. Lizenz: keine Abwandlungen, Namensnennung beim Weitergeben, kommerziell nur Bilderzeugungsdienste (*Deutung:* privater Upload für eigene, nicht verkaufte Bilder unberührt).
- Privat hochgeladen als `skriptorium:2767605@3115420` und `skriptorium:2742699@3142259` (Architektur `krea_oss_2`); nach wenigen Minuten in der Modellsuche.
- Reibungen: Pythons `http.client` geht nicht über den Proxy (kein Civitai-Schlüssel, 401) → Weiterleitung mit curl holen; diese Dateien liegen bei Cloudflare R2 (`…r2.cloudflarestorage.com`) statt bei `b2.civitai.com`; die Antwort des Uploads ließ sich nicht auswerten, die Bereitstellung wurde über die Modellsuche bestätigt.
- Probebilder auf Krea 2 Turbo (Seed 4242, Gewicht 1,0, bekleidete erwachsene Figur): Megapack, Frau auf Stuhl im Keller mit Seil um Rumpf und Stuhlbeine, 0,0096 $ – sauber, Hände nicht ganz wie verlangt hinter der Lehne; Rope Bondage, Frau in Scheune, Arme hinten, Seil um Oberkörper, 0,0083 $ – sauber, folgt dem Prompt. Keine Bildfehler wie bei Raw.

### 2026-11-07 – [GELÖST] 10.8: Krea 2 Raw und Turbo als eine Familie

- `api/runware_models.py` `_FAMILIES`: `krea_oss_2` und `krea_oss_2_turbo` → Familie `krea_oss_2`; Test in `test_families_decide_which_lora_fits` (Turbo und Raw passen, Krea 2 Medium `krea_2` nicht). 1.273 Tests grün, Abdeckung 99,92 %.
- Gegenprobe über den Server-Weg mit echtem Schlüssel (ohne Bild): `krea:krea@2-turbo` und `skriptorium:2964163@3386627` hinzugefügt → die LoRA steht bei Turbo unter „passende LoRAs“.

### 2026-11-07 – [GELÖST] 10.8: Plastic Zip-Cuffs läuft sauber auf Krea 2 Turbo

- Gleicher Aufbau wie der Vergleich mit Raw (Seed 4242, keine Schritte/CFG), Modell `krea:krea@2-turbo`: ohne LoRA 0,0037 $ – sauber, Fesseln als breite Armbänder; mit LoRA 0,6 0,0136 $ – **sauber, ohne Bildfehler**, Kabelbinder richtig geformt, keine Verletzungen im Gesicht.
- Folge: Die LoRA (Architektur `krea_oss_2`) mit Krea 2 Turbo nutzen, nicht mit Raw. Damit der Dialog sie bei Turbo anbietet, muss die Familien-Lücke in `api/runware_models.py` geschlossen werden (`krea_oss_2_turbo` → Familie `krea_oss_2`) – heute würde sie nur bei Raw erscheinen.

### 2026-11-07 – [BEOBACHTUNG] 10.8: Vergleich Krea 2 Raw ohne und mit LoRA – Fehler kommen von der LoRA

- Direkt über die API, Einstellungen wie der Adapter (keine Schritte/CFG), Seed 4242, gleicher Prompt (mit LoRA plus Auslösewort): ohne LoRA 0,0122 $, mit LoRA 0,6 0,0128 $.
- Ohne LoRA: sauberes Bild ohne Bildfehler; die Fesseln sehen aber aus wie klobige Kunststoff-Manschetten, nicht wie Kabelbinder. Verletzungen im Gesicht auch ohne LoRA → kommen vom Grundmodell bzw. vom Prompt („grim“, „interrogation room“), nicht von der LoRA.
- Mit LoRA 0,6: Kabelbinder richtig geformt, aber dieselben weißen, rot-blau umrandeten Bildfehler wie bei 1,0 → Ursache ist die LoRA in der Umgebung von Runware (Gewicht allein erklärt es nicht; Voreinstellungen ebenso nicht, da das Bild ohne LoRA sauber ist). Vermutung, nicht belegt: Die LoRA (diffusers-Format, ai-toolkit) passt nicht sauber zur Krea-2-Umsetzung bzw. Optimierung von Runware.
- Mögliche nächste Proben (mit Freigabe): Gewicht 0,3; dieselbe LoRA auf `krea:krea@2-turbo`; die ältere Version V0.1 (`@3358423`); Meldung an Runware.

### 2026-11-07 – [BEOBACHTUNG] 10.8: Probebild Krea 2 Raw mit eigener LoRA – läuft, aber Bildfehler

- Über den Server-Weg (Testclient, eigenes Datenverzeichnis): `krea:krea@2-raw` und `skriptorium:2964163@3386627` per „Prüfen und hinzufügen“ übernommen (Familie `krea_oss_2`, LoRA wird beim Grundmodell angeboten, Auslösewort angehängt); Bild 832 × 1216 in 40 s für 0,0186 $.
- Ergebnis: Die Kabelbinder sind da (übergroß), aber deutliche Bildfehler – weiße, rot-blau umrandete Flächen über Haar, Mantel und Bank; dazu Verletzungen im Gesicht, die der Prompt nicht verlangte. Ursache offen: Gewicht 1,0 zu hoch, oder die Voreinstellungen von Runware für Schritte und CFG bei Krea 2 Raw (der Adapter schickt keine), oder die LoRA selbst (V0.4, 32 Trainingsbilder). Klärung nur mit Vergleichsbildern (ohne LoRA, Gewicht 0,6).

### 2026-11-07 – [GELÖST] 10.8: LoRA Plastic Zip-Cuffs (Krea 2) privat zu Runware hochgeladen

- Auf Frage des Eigentümers („kannst du das Modell direkt zu Runware hochladen?“): `modelUpload` mit `downloadURL` = signierte, kurzlebige Speicheradresse, auf die Civitai den angemeldeten Download weiterleitet (Host `b2.civitai.com`, Token nur für diese Datei; der Civitai-Schlüssel ging nicht an Runware; Adresse nicht ausgegeben, danach gelöscht).
- Reibung: erster Versuch `missingAIR` – eigene Kennung nötig; Präfix des Kontos laut `getDetails`/`AIRSource` = `skriptorium` (nur dieses Feld gelesen) → `skriptorium:2964163@3386627`.
- Antwort zuerst nur `validated`, danach im Hintergrund verarbeitet; nach wenigen Minuten in `modelSearch` gefunden: LoRA, `krea_oss_2`, privat, Auslösewort `pla5ticz1pcuff5`, Gewicht 1. Damit belegt: Die Modellsuche findet private Modelle des eigenen Kontos – „Prüfen und hinzufügen“ funktioniert dafür.
- Offen: Probebild mit `krea:krea@2-raw` + LoRA; Familien-Lücke Raw/Turbo im Code.

### 2026-11-07 – [BEOBACHTUNG] 10.8: Plastic Zip-Cuffs für Krea 2 – Stand zum Weitermachen

- Hinweis des Eigentümers: Die LoRA gibt es auch für Krea 2. Geprüft (nur lesend, `docs/research/bildanbieter.md`): Krea-2-Versionen `@3386627` und `@3358423` bei Runware nicht gelistet; Grundmodelle `krea:krea@2-raw` / `krea:krea@2-turbo` (offene Gewichte, LoRAs möglich, ca. 0,015 $) vorhanden; Nutzung der LoRA nur per eigenem privatem Upload zu Runware; Civitai-Download braucht Anmeldung.
- Vorgelegt: (1) Eigentümer lädt selbst hoch, (2) Upload durch die KI mit Civitai-Schlüssel über das sichere Formular, (3) erstmal nicht. Antwort: „Merk dir wo wir sind, wir machen morgen weiter“ – **Frage offen**, nichts hochgeladen, kein Code geändert.
- Gefundene Lücke (noch nicht behoben): `api/runware_models.py` `_FAMILIES` kennt `krea_oss_2` und `krea_oss_2_turbo` nicht als eine Familie – eine Turbo-LoRA würde bei Krea 2 Raw nicht angeboten (Runware: Turbo-LoRAs laufen auch auf Raw). Ein Eintrag plus Test, innerhalb von 10.8.
- Civitai-Schlüssel vom Eigentümer als Netzwerk-Secret der Umgebung für `civitai.com` hinterlegt (Proxy setzt ihn ein, kein Wert im Container oder Gespräch). Probe nur mit Status: Download-Adresse der LoRA antwortet jetzt 307 (Weiterleitung) statt 401 – Zugang wirkt; nichts heruntergeladen.
- LoRA identifiziert über den Dateikopf (Teilabruf, 65 KB statt 218 MB): Krea 2 Raw, Rang 32, 32 Trainingsbilder – Upload mit Architektur `krea_oss_2` (Details `docs/research/bildanbieter.md`).
- **Wiedereinstieg morgen:** Upload erledigt (siehe Eintrag darüber); Familien-Lücke schließen; vor einem Upload klären, ob `modelSearch` private Modelle findet und ob CLI/Dashboard eine lokale Datei annehmen; dann wie im Sessionende darüber (CI von #218, Bestätigung, Einspielen).

### 2026-11-07 – [SESSIONENDE] 10.8 gebaut und geprüft, Pull Request #218 aktualisiert

- **Dauer:** 2026-11-07 ca. 01:08 bis 02:20 (Cloud-Session, zweimal Neustart des Arbeitsprozesses ohne Verlust).
- **Bearbeitet:** 10.8 – Modellsuche und Probebilder bei Runware, zweite Vorlage (ADR-115, V.52), Prüfung der Civitai-Wunschmodelle, Bau (Server `24d955e`, Oberfläche `ade0df6`), Probe über den eigenen Server-Weg, getrennte Prüfung, Härtung `778e165` mit Nachprüfung; Doku (Kontext, Architektur, Anforderungen, README, CHANGELOG, Runbook). Pull Request [PatSchCode/Skriptorium#218](https://github.com/PatSchCode/Skriptorium/pull/218) – Titel und Beschreibung auf den Bau umgestellt (das Repository liegt jetzt unter `PatSchCode`).
- **Stand:** 10.8 `[IN ARBEIT]` – Code fertig, Tests grün (Python 1.273, 99,88 %; Oberfläche 597; End-to-End 17), getrennt geprüft ohne Befund hoch/mittel. CI des Pull Requests noch nicht gesehen.
- **Offen:** Bestätigung des Eigentümers (Akzeptanzkriterium); Einspielen vom Mac: `RUNWARE_API_KEY` in `/opt/docker/skriptorium/.env` (mit dem zeilenweisen Befehl aus dem Runbook), Compose-Datei auf Durchreichen prüfen, dann Probe auf dem Server. Danach 10.8 `[ERLEDIGT]`.
- **Nächster Schritt:** CI von #218 prüfen, mergen nach Freigabe, Einspielen auf Anweisung; dann 10.9. Datiert: D.5 ab 2026-11-12; D.11 Frist überschritten.
- **Sessionende-Prüfungen:** README gegen Fahrplan (8 von 11, 10.8 in Arbeit) abgeglichen; Drift: ADR-115 → 10.8 und V.52 vorhanden, Reaktiv-Quote 0/10 (ADR-106 bis ADR-115), Reifegrade unverändert (Erweiterungen vermerkt), Modul-Liste unverändert, 0 Blocker, Phase 10 bei 11 Schritten; FR-025/FR-035 nachgetragen. Größen: Logbuch rund 630 Zeilen (Trigger 800), Kontext 351 Zeilen (Budget 600). Ablaufdaten-Register: kein neuer Vorlauf.
- **Modell-Bilanz:** durchgehend Opus 5.5 (Entscheidungs-Klasse, Sitzungsabfrage), Empfehlung für 10.8; oberhalb: Logbuch, README, Doku-Pflege (Routine), nicht abgegeben (Routine-Abgabe ruht bis D.22). Abgegeben: zwei getrennte Prüfungen an Unteragenten auf Sonnet (als getrennte Instanz, nicht zur Ersparnis).
- **Kontextgröße:** 486.458 Token am Ende (Grenze 200.000; überschritten ab etwa 262.000 nach ADR-115, Eigentümer: „Weiter hier“).

### 2026-11-07 – [BEOBACHTUNG] 10.8: optionale Befunde umgesetzt, Nachprüfung ohne Befund

- Eigentümer: „Beide umsetzen“ → `778e165`: Runware-Antwort gestreamt gelesen, Abbruch ab 56 MB vor dem Dekodieren; beschädigte `system/runware-modelle.md` zeigt die Startliste (Warnzeile `runware_liste_defekt`), Erzeugen damit bleibt abgelehnt. 1.273 Python-Tests grün, Abdeckung 99,88 %.
- Getrennte Nachprüfung (Sonnet, nur `git show 778e165`): kein Befund mittel oder höher. Hinweise ohne Änderung: eine entpackte Teilmenge kann die Grenze kurz überschreiten (begrenzt); 150 s gelten je Lesevorgang (wie vorher); bei kaputter Liste zeigt die Auswahl Modelle, die dann mit 422 scheitern – ein Feld zur Erklärung wäre optional, nicht umgesetzt (Fall nur bei Handbearbeitung der Datei).
- Eigentümer: „Pull Request anlegen“.

### 2026-11-07 – [BEOBACHTUNG] 10.8: getrennte Prüfung ohne Befund hoch oder mittel

- Getrennte Instanz (Unteragent auf Sonnet, nur Diff `c8c2ea6..HEAD`, Bedrohungsmodell und Regeln; kein Gesprächsverlauf, kein Netz zu den Anbietern), 2026-11-07: keine Befunde hoch oder mittel, keine Anforderung von ASVS 5.0.0 L1 / Auth L2 verletzt; 102 Tests grün nachgeprüft.
- Niedrig, optional: (1) keine Größengrenze der Runware-Antwort vor dem Dekodieren (nur ein fehlerhafter Anbieter könnte Speicher binden; bei OpenRouter vermutlich ebenso); (2) eine von Hand beschädigte `system/runware-modelle.md` lässt `GET /api/images/models` mit 422 scheitern. Hinweise: keine Mengenbegrenzung je Sitzung (über L1 hinaus; Guthaben begrenzt), 150 s Lesezeit ohne Befund.
- Geprüft ohne Befund: Schlüssel nicht in Antworten, Logs, `repr` oder Fehlerketten; kein Aufruf von `accountManagement`; Kennungen und Civitai-Links nur nach festem Muster, kein Abruf fremder Adressen; Bilder durch `inspect_image`; `checkContent` fest im Code; Sitzungs- und Origin-Pflicht auf den neuen Routen; keine HTML-Darstellung in der Oberfläche.
- Nach „Schutzbedarf ist Obergrenze“ dem Eigentümer als optional vorgelegt, nicht still umgesetzt.

### 2026-11-07 – [BEOBACHTUNG] 10.8: Bau fertig, Probe über den eigenen Server-Weg

- Server (`24d955e`): Adapter `ai_gateway/runware.py` (Bild als base64, `includeCost`, `checkContent: false`, LoRAs, Modellsuche), Liste `system/runware-modelle.md` (`api/runware_models.py`), Zuordnung am Kennungsformat in `image_routes.py`, Routen `POST`/`PUT /api/images/runware` (89 Routen). Tests: 40 Adapter, 37 Routen/Liste; Python-Abdeckung 99,88 %, `runware.py`, `runware_models.py`, `image_routes.py` je 100 %.
- Oberfläche (`ade0df6`): Gruppen OpenRouter/Runware im Dialog, LoRAs mit Gewicht, Bereich „Bildmodelle bei Runware“ in den Einstellungen; 597 Tests, Abdeckung 98,81 / 95,22 / 98,36 / 98,95 %. End-to-End 17 von 17 grün.
- Probe über `create_app` mit echtem Schlüssel (Testclient, eigenes Datenverzeichnis): LoRA `civitai:536201@596079` per Kennung übernommen (Auslösewort „handcuffs, cuffs“, Gewicht 0,8); Link zur nicht gelisteten Version mit Meldung abgelehnt; epiCRealism XL VXIV mit LoRA 0,7 → Bild in 9,5 s für 0,0037 $, LoRA sichtbar wirksam (Pony-LoRA auf SDXL-Modell, gleiche Familie).
- Getrennte Prüfung (Kategorie 6) gestartet, Ergebnis folgt.

### 2026-11-07 – [GELÖST] 10.8: Reibungen beim Bau

- Pre-Commit prüft mit mypy auch ungestagte, aber vorhandene Testdateien → Server-Teil als ein Commit statt zwei.
- Vertragsdatei `tests/shared/api-responses.json` zeigte `runware_ready: true`, weil in der Cloud-Session der echte Schlüssel gesetzt ist → Test-Fixture bekommt einen gefälschten Runware-Server (`FakeRunware`), sonst wäre die CI ohne Schlüssel rot.
- Gewichtsfeld: Leeren setzte sofort 0 → eigenes Feld `WeightInput` (Zwischenstände beim Tippen, beim Verlassen wieder der gültige Wert).
- Playwright 1.62.1 findet den vorinstallierten Browser nicht unter seinem Pfad → Lauf mit Hilfskonfiguration (`launchOptions.executablePath` `/opt/pw-browsers/chromium`), danach gelöscht; nichts im Repo geändert.
- Notfall-Handbuch: Der Befehl zum Schlüsseltausch schrieb `.env` ganz neu und hätte den zweiten Schlüssel gelöscht → ersetzt nur noch die eine Zeile (an einer Probe-Datei geprüft). Offen fürs Einspielen: ob die Compose-Datei auf dem VPS `RUNWARE_API_KEY` in den Container durchreicht (nur lokal beim Eigentümer einsehbar).

### 2026-11-07 – [BEOBACHTUNG] Sessiongröße überschritten, Eigentümer: „Weiter hier“

- Sitzungsabfrage nach ADR-115: 261.581 Token Kontext (Grenze 200.000, `docs/project-context.md` Abschnitt 6); zu Sessionbeginn meldete die Abfrage 0. Vorschlag „neue Session für den Bau“; Eigentümer: „Weiter hier“ – Abweichung nach `CLAUDE.md` Abschnitt 0 („Sessiongröße“, Ausnahme). Bau von 10.8 läuft in dieser Session weiter.

### 2026-11-07 – [ADR-ANGELEGT] ADR-115: Runware – Erwachseneninhalte ohne Prüfung, Modelle und LoRAs in den Einstellungen

- Zweite Vorlage zu 10.8 vollständig beantwortet (Auswahlfragen, siehe ADR-115): Prüfung bei Runware fest aus; Fließtext-Prompt, Schlagwort-Knopf als V.52 → 10.11; Technik wie vorgeschlagen; LoRAs gleich in 10.8; Liste in den Einstellungen mit Prüfung per `modelSearch`.
- Mockup (vom Eigentümer mit „Ja, so bauen“ bestätigt):

```text
Einstellungen › Bildmodelle bei Runware
  Grundmodelle                                   Zusatz zum Prompt
  FLUX.2 [dev]            runware:400@1          –
  Z-Image-Turbo           runware:z-image@turbo  –
  HiDream I1 Dev          runware:97@2           –
  epiCRealism XL VXIV     civitai:277058@1405120 –
  [ Kennung oder Civitai-Link einfügen ] [Prüfen und hinzufügen]
  LoRAs                                   Basis   Auslösewort   Gewicht
  [ Kennung oder Civitai-Link einfügen ] [Prüfen und hinzufügen]

Bild erzeugen
  Modell  [ epiCRealism XL VXIV (Runware) ▾ ]   (Gruppen OpenRouter / Runware)
  Zusätze [✓] <LoRA>  Gewicht [0,8]     ← nur LoRAs mit passender Basis
  Prompt  [ … aus dem Kanon … ] (Zusatz und Auslösewort werden angehängt)
  Preis   ab 0,0025 $ bzw. „Preis nach dem Erzeugen“
```

- Reaktiv-Quote 0/10 (ADR-106 bis ADR-115).

### 2026-11-07 – [BEOBACHTUNG] 10.8: erstes Probebild über die Runware-API

- Freigabe des Eigentümers: Probebild ja, LoRAs „gleich in 10.8“.
- Gewünschte Version epiCRealism XL `@1552721` abgelehnt (`invalidModel`, ohne Kosten): Runware lädt nicht gelistete Civitai-Versionen nicht nach. Gelistete Version `@1405120`: Bild in 7 s für 0,0025 $, `checkContent: false` gesetzt. Folge: Kennungen beim Hinzufügen per `modelSearch` prüfen.

### 2026-11-07 – [BEOBACHTUNG] 10.8: Wunschmodelle aus Civitai geprüft

- Eigentümer nennt zwei Civitai-Links (Domain `civitai.red`, gleiche Kennungen wie `civitai.com`). Ergebnis in `docs/research/bildanbieter.md`: epiCRealism XL bei Runware in 20 Versionen, die gewünschte „VXVI – LastFAME DMD2“ (`@1552721`) nicht gelistet; Plastic Zip-Cuffs ist eine LoRA für das Grundmodell „MOSS Image“, das Runware nicht anbietet – dort nicht nutzbar.
- Neu für die Vorlage: LoRAs (Zusätze zu einem Grundmodell) waren in der Modell-Liste nicht vorgesehen. Rückfrage an den Eigentümer: Probebild mit der nicht gelisteten Version, LoRA-Unterstützung ja oder nein.

### 2026-11-07 – [BEOBACHTUNG] 10.8: zweite Vorlage teilweise beantwortet

- Vorlage mit vier Fragen (Inhaltsvorgabe, Modell-Liste, Schlagwort-Prompts, Technik) und Mockup der Bildauswahl gestellt.
- Antworten des Eigentümers: Inhalte „Erlauben, Prüfung aus“ (Runware `checkContent` fest aus im Code; Darstellungen Minderjähriger bleiben verboten); Schlagworte „Fließtext, ich passe an“ (Knopf „in Schlagworte umsetzen“ wird V.52 mit Landeplatz 10.11); Technik „Ja, so bauen“ (Zuordnung am Kennungsformat, `RUNWARE_API_KEY` nur auf Server und in der Cloud-Session, Kosten-Bremse über Vorab-Guthaben, Kosten per `includeCost`, getrennte Prüfung).
- Modell-Liste offen: „civitai will ich jetzt klären“ – Rückfrage läuft. ADR folgt, wenn alle vier Punkte beantwortet sind; kein Code vorher.

### 2026-11-07 – [BEOBACHTUNG] 10.8: Modellsuche bei Runware

- Nur lesend, kein Bild erzeugt; Befunde in `docs/research/bildanbieter.md` („Modellsuche mit Schlüssel“). FLUX.2 [dev], FLUX.1 [dev], Z-Image (Turbo), HiDream I1 verfügbar, 0,003–0,02 $ je Bild; Community-Modelle aus Civitai (Pony, Illustrious, NoobAI, LUSTIFY!) über `civitai:<Modell>@<Version>`, abgerechnet nach Rechenzeit. Nicht gefunden: BigASP, Chroma, Pony V7.
- Inhaltsprüfung `safety.checkContent` in 122 von 127 Bildschemata, nirgends mit Voreinstellung – der Adapter muss sie ausdrücklich setzen.
- Reibung: Die Doku-Adressen aus dem Recherche-Stand vom 2026-10-12 leiten um oder liefern 404; Einstieg jetzt über `https://runware.ai/llms.txt` und `docs/models/index.json`. `getUsageActivity` braucht `groupBy` als Liste, nicht als Text (Fehler `invalidGroupBy`), und lieferte trotzdem keine Zeilen für die 29 Anfragen aus dem Playground.
- Vorsicht: `accountManagement`/`getDetails` gibt die Schlüssel des Kontos mit aus – ausgewertet wurden nur Guthaben (21,07 $) und Verbrauch (3,99 $, 29 Anfragen); kein Wert in der Ausgabe.

### 2026-11-07 – [SESSIONSTART] 10.8 Zweiter Bildanbieter – Modellsuche bei Runware

- **Umgebung:** Cloud-Session (Linux), Branch `feat/10.8-zweiter-bildanbieter` (`a4bf01c`) vom Remote ausgecheckt; vom Werkzeug vorgegeben war `claude/happy-lovelace-abnbdc`, der Eigentümer hat ausdrücklich den Feature-Branch genannt. `RUNWARE_API_KEY` gesetzt (nur Vorhandensein und Länge geprüft), `OPENROUTER_API_KEY` gesetzt.
- **Modell:** eingestellt `claude-opus-5-5`, bedient `claude-opus-5-5` (Sitzungsabfrage `get_session`) → **Entscheidungs-Klasse**, entspricht der Empfehlung für 10.8.
- **Kontextgröße:** Sitzungsabfrage meldet `used_tokens: 0` – kein verwertbarer Wert, Regel der Sessiongröße entfällt.
- **Mindest-Lektüre:** Kontext vollständig, Logbuch ab letztem Sessionende, Fahrplan (Stand, Phase 10), Architektur 1/2/9, Entscheidungen Teil A und C, aktive Blocker (keine).
- **Vorhaben:** 10.8 fortsetzen – Modellsuche bei Runware nur lesend, danach zweite Vorlage.

### 2026-11-07 – [SESSIONENDE] 10.8 Runware gewählt, weiter in der Cloud-Session

- **Dauer:** 2026-11-06 ca. 22:50 bis 2026-11-07 (lokale Session auf dem Mac).
- **Bearbeitet:** 10.8 – Modellwechsel auf die Entscheidungs-Klasse, Nachprüfung von Katalogen, Preisen und Filtern (`docs/research/bildanbieter.md`), Vorlage mit vier Optionen, Erklärung der Freischaltung bei fal.ai, Wahl Runware (ADR-114); Hilfe zur Probe des Eigentümers im Playground (Modelle, Prompts, Scheduler); Wunsch nach Erwachseneninhalten festgehalten, Bedingungen von Runware §10 geprüft (offen formuliert), Community-Modelle über Kennungen `civitai:<Modell>@<Version>` (Runware-CLI).
- **Stand:** Branch `feat/10.8-zweiter-bildanbieter`, nur Doku, als Pull Request zum Weiterarbeiten in der Cloud-Session (Wunsch des Eigentümers). Kein Code geändert, kein Einspielen nötig.
- **Offen:** Eigentümer legt `RUNWARE_API_KEY` in der Cloud-Umgebung an. Dort: Modellsuche bei Runware nur lesend (Verfügbarkeit von FLUX.2 [dev], Z-Image Turbo, HiDream I1 und der Kandidaten für Erwachseneninhalte, Voreinstellung der Inhaltsprüfung), Wert des Schlüssels nie ausgeben (nur gesetzt/nicht gesetzt). Danach zweite Vorlage zu 10.8: Modell-Liste, Zuordnung Modell → Anbieter, Mockup der Bildauswahl, Vorbelegung bei Modellen mit Schlagwort-Prompts, Stil-Zusatz als Option, neue Inhaltsvorgabe statt „keine pornografischen Inhalte“ (ADR-077), Schlüssel und Kosten-Bremse, getrennte Prüfung. Unbeantwortet: welche Modelle im Playground taugten, ob die düstere Szene durchging, ob heute Bilder an Filtern scheitern. In der Cloud-Session greift D.28 (Pre-Commit-Hook markdownlint; Umweg `PATH=/usr/local/bin:$PATH` nur für den Commit).
- **Nächster Schritt:** 10.8 in der Cloud-Session fortsetzen (Modellsuche, dann zweite Vorlage). Datiert: D.5 ab 2026-11-12; D.11 Frist 2026-10-31 überschritten.
- **Sessionende-Prüfungen:** README gegen Fahrplan (8 von 11, 10.8 in Arbeit, 10.9 als Nächstes), Kontext (Runware in Abschnitt 5), Blocker (0) abgeglichen. Drift: ADR-114 → 10.8 vorhanden; Reaktiv-Quote 0/10 (ADR-105 bis ADR-114) nachgezogen; Reifegrade unverändert; Modul-Liste unverändert; 0 blockierte Schritte; Phase 10 bei 11 geplanten Schritten. Größen: Logbuch rund 530 Zeilen (Trigger 800), `docs/project-context.md` 350 Zeilen (Budget 600). Ablaufdaten-Register: kein neuer Vorlauf erreicht.
- **Modell-Bilanz:** Beginn auf Sonnet 5.5 (Routine) → Stopp nach Abschnitt 0, Wechsel auf Opus 5.5 (Entscheidungs-Klasse; Sitzungsabfrage bestätigt). Schritt 10.8 auf seiner Empfehlung; oberhalb: Doku-Pflege, Logbuch und README (Routine), nicht abgegeben (kleine Teilarbeiten mit geladenem Kontext; Routine-Abgabe ruht bis D.22).
- **Kontextgröße:** nicht feststellbar (Sitzungsabfrage meldet keinen Wert).

### 2026-11-07 – [BEOBACHTUNG] 10.8: Probe im Playground, neuer Wunsch Erwachseneninhalte

- Eigentümer probiert im Runware-Playground (Prompt-Vorschläge und Scheduler-Frage beantwortet: Voreinstellung lassen): „Bisher scheint das, was ich brauche, brauchbar zu sein. Nur das Prompting ist halt sehr umfangreich.“ Modelle und Filterergebnis der düsteren Szene noch nicht gemeldet.
- Neuer Wunsch: Modelle, die Erwachseneninhalte liefern, „vielleicht sogar Bondage“. Das ändert die bisherige Vorgabe „keine pornografischen Inhalte geplant“ (ADR-076, ADR-077, ADR-114 Vision-Frage) – Gegenstand der zweiten Vorlage zu 10.8, kein Eingriff vorher. Befund: Runwares Bedingungen §10 lassen offen, ob Erwachseneninhalte erlaubt sind (`docs/research/bildanbieter.md`); Kandidaten nur offene bzw. Community-Modelle, teils mit Schlagwort-Prompts statt Fließtext.

### 2026-11-07 – [ADR] ADR-114: Runware als zweiter Bildanbieter

- Vorlage 10.8 mit vier Optionen (Runware, Replicate, fal.ai, keiner) nach Nachprüfung von Katalogen und Preisen (`docs/research/bildanbieter.md`, „Nachprüfung für 10.8“). Befund: OpenRouter führt inzwischen 63 Bildmodelle; ein zweiter Anbieter bringt vor allem offene Modelle mit eigenem Filterschalter.
- Nachfrage des Eigentümers: Freischaltung bei fal.ai und Unterschied zu Runware. Nachgeprüft: fal-Schemata (FLUX dev, Z-Image Turbo, Pony V7) verlangen weiter eine Freischaltung des Kontos, sonst immer Prüfung mit schwarzem Bild; Runware prüft laut Integrationsdoku nur auf Anforderung (offizielle Seite 404).
- Eigentümer: „Runware“ → ADR-114. Offen: Frage, ob heute Bilder an Filtern scheitern (nicht beantwortet); Probe im Playground; zweite Vorlage.

### 2026-11-06 – [SESSIONSTART] 10.8 Zweiter Bildanbieter – Stopp wegen Modellklasse

- **Umgebung:** lokale Session auf dem Mac des Eigentümers (macOS, `main` = `c8c2ea6` nach `git pull --ff-only`, 11 Commits aus PR #217 nachgezogen). KI-Läufe mit dem Schlüssel gelten nur in der Cloud-Session.
- **Modell:** eingestellt `claude-sonnet-5-5`, Sitzungsabfrage (`get_session`) meldet dasselbe → **Routine-Klasse**. Empfohlene Klasse für 10.8: **Entscheidung** (Abhängigkeit und Secrets, Eskalations-Auslöser 1) → Pflicht-Eskalation, Stopp mit `Benötigte Klasse: Entscheidung`.
- **Kontextgröße:** Sitzungsabfrage liefert keinen Wert für die Kontextgröße; nicht feststellbar.
- **Mindest-Lektüre:** Kontext vollständig, Logbuch ab letztem Sessionende, Fahrplan (Stand, Phase 10), Architektur 1/2/9, Entscheidungen Teil A (Auszug) und Teil C, aktive Blocker (keine). Abgleich: Fahrplan-Übersicht „8 von 11“ passt zur Schrittliste.
- **Vorhaben:** 10.8 nach V.24 – Vorlage, ADR, aktuelle Preise, getrennte Prüfung des Umgangs mit dem Schlüssel; Arbeit beginnt nach Modellwechsel. Kein Code, kein Fahrplan-Status geändert.
- **Modellwechsel:** Eigentümer wechselte per `/model` auf `claude-opus-5-5` („Ja, gewechselt“); Sitzungsabfrage bestätigt `claude-opus-5-5` → **Entscheidungs-Klasse**, Stopp aufgehoben.

### 2026-11-06 – [SESSIONENDE] 10.10 erledigt (ADR-113), nächstes Mal 10.9 oder 10.8

- **Dauer:** 2026-11-06, ca. 00:20–01:20 UTC (Cloud-Session, Branch `scp/zealous-meitner-g94yap`).
- **Bearbeitet:** 10.10 Textqualität von Hermes 4 – Messung nach Regel-002 (5 Varianten, 30 Ketten), Nachlauf auf Wahl des Eigentümers (12 Ketten), zwei verblindete Bewertungsrunden (je 4 getrennte Instanzen); Entscheidung „nichts übernehmen“ → ADR-113, 10.10 ERLEDIGT. Neu: V.51 (Längengrenze, Landeplatz 10.11), D.28 (Pre-Commit in der Cloud-Session, freigabepflichtig). KI-Kosten 3,20 $ (Schlüssel der Cloud-Session).
- **Stand:** Alles auf `scp/zealous-meitner-g94yap` committet und gepusht; noch **nicht** in `main` (kein Pull Request – nur auf Wunsch des Eigentümers). Kein Code des Produkts geändert, kein Einspielen nötig.
- **Offen:** Pull Request für den Branch (Eigentümer); D.28 Lösung wählen; `minimatch` unter ESLint; Token je Bild (10.7) mit/ohne Haken vergleichen; überholter lokaler Zweig `feat/9.9-loeschen-archivieren` auf dem Mac.
- **Nächster Schritt:** 10.9 Vollständige Anfrage festhalten (Vorlage mit Mockup) oder 10.8 Zweiter Bildanbieter – Wahl des Eigentümers. Datiert: D.5 ab 2026-11-12; D.11 Frist 2026-10-31 überschritten.
- **Sessionende-Prüfungen:** README gegen Fahrplan (8 von 11, 10.10 erledigt, nächste Schritte), Kontext, Blocker (0) abgeglichen; Übersicht im Fahrplan stand auf „5 von 11“ (Drift seit 10.6/10.7) – berichtigt auf 8 von 11. Drift: ADR-113 → 10.10 vorhanden; V.51 und D.28 mit Schritt; Reifegrade unverändert; Modul-Liste unverändert; 0 blockierte Schritte; Reaktiv-Quote 0/10 (ADR-104 bis ADR-113); Phase 10 bei 11 geplanten Schritten. Größen: Logbuch 500 Zeilen (Trigger 800), `docs/project-context.md` 349 Zeilen (Budget 600). Ablaufdaten-Register: mypy-2-Nachprüfung heute fällig, Schritt D.5 vorhanden (ab 2026-11-12).
- **Modell-Bilanz:** aktiv Opus 5.5 (Entscheidungs-Klasse; Sitzungsabfrage: eingestellt und bedient `claude-opus-5-5`). Schritt 10.10 auf seiner Empfehlung (Entscheidung); oberhalb: D.28-Anlage und Doku-Pflege (Routine), nicht abgegeben (kleine Teilarbeiten mit geladenem Kontext; Routine-Abgabe ruht bis D.22). Abgegeben: 8 verblindete Bewertungen an getrennte Instanzen (Sonnet) – als Messinstrument, nicht als Routine-Abgabe.
- **Kontextgröße:** 382.725 Token (Sitzungsabfrage) – über der Grenze 200.000 seit dem Ende der ersten Messrunde; der Nachlauf gehörte zum laufenden Schritt 10.10, danach kein neuer Schritt begonnen. Nächste Session neu beginnen.

### 2026-11-06 – [BEOBACHTUNG] 10.10 Nachlauf: keine Wirkung der Einstellung

- Je 3 weitere Ketten `hermes` und `hermes-fp03-t06` (0,61 $), neu verblindet bewertet (12 Ketten je Geschichte, vier neue Instanzen). Über 6 Ketten je Seite: Gesamtnote Salzmark 3,00 → 2,67, Glimmergrund 2,00 → 3,17; nach Regel-002 keine Wirkung – der Befund aus 3 Ketten war Streuung (wie bei 8.11 und 9.3).
- Grobe Schleifen in Glimmergrund seltener (längster Vorschlag 1.247 gegen 6.438 Wörter), aber nicht beseitigt; Kanon-Proben mit der Einstellung im Mittel schlechter (3,00 gegen 1,83, innerhalb der Spannweite). Bericht: `spikes/hermes-10.10/README.md`, Abschnitt „Nachlauf“.

### 2026-11-06 – [BEOBACHTUNG] 10.10: Eigentümer wählt Nachlauf

- Vorlage nach der Messung (A nichts übernehmen – empfohlen, B Einstellung je Modell, C Nachlauf). Eigentümer: „Hermes nutze ich nur, wenn andere Modelle sperren“; auf Nachfrage „Nachlauf zuerst“. Über die Längengrenze gegen Endlosschleifen (V-Schritt, Landeplatz 10.11) entscheidet er nach dem Nachlauf.
- Nachlauf: je 3 weitere Ketten `hermes` und `hermes-fp03-t06` an beiden Geschichten (`ergebnisse/hermes-2/`, `…/hermes-fp03-t06-2/`), danach neue verblindete Bewertung aller 12 Ketten je Geschichte.
- Kontextgröße der Session 322.538 Token (Grenze 200.000): der Nachlauf gehört zum laufenden Schritt 10.10; danach beginnt in dieser Session kein neuer Schritt.

### 2026-11-06 – [BEOBACHTUNG] 10.10 Messung Hermes 4 nach Regel-002

- Bericht: `spikes/hermes-10.10/README.md` (Tabellen, Befunde, Grenzen); Stand `main` `478e5fd`, Länge „mittel“, je Variante 3 Ketten an Salzmark und Glimmergrund; 2,59 $.
- Varianten: grok-4.6 (Bezug), Hermes wie heute (Denken aus, Temperatur 0,8), `frequency_penalty` 0,3, dazu Temperatur 0,6, `repetition_penalty` 1,05.
- Denken bei Hermes nicht nutzbar: einziger Anbieter Nebius liefert den Denktext ohne Trennmarke im Antworttext (an der echten Anfrage rund 300 Wörter deutscher Denktext vor der Prosa).
- Schleifen nachgestellt: Hermes wie heute in Glimmergrund 2 von 3 Ketten mit Endlosschleife (1.839 Wörter; 6.438 Wörter bis zur Grenze von 8.000 Token). Keine Einstellung beseitigt die Entgleisungen: `frequency_penalty` → Wortsalat, mit Temperatur 0,6 ein Satz über 1.247 Wörter samt Anfragetext; `repetition_penalty` ohne Totalausfall, Vorschläge bis 647 Wörter.
- Verblindete Bewertung (je Geschichte und Thema eine getrennte Instanz, Sonnet; 3 Funde von Hand bestätigt): Gesamtnote grok-4.6 3,33 / 4,00, Hermes heute 2,67 / 1,33, bestes Hermes (fp03-t06) 3,33 / 2,67 – nach Regel-002 eine Wirkung auf die Gesamtnote, aber „wörtlich %“ in der Salzmark gegenläufig schlechter. Kanon-Proben Glimmergrund: grok-4.6 0,33 widersprochen, Hermes 2,0–2,67.
- Hermes kostet je Kette ein Sechstel bis ein Drittel von grok-4.6.

### 2026-11-06 – [GELÖST] Pre-Commit in der Cloud-Session: markdownlint lässt sich nicht einrichten

- Befund: Erster Commit der Session scheiterte im Hook `markdownlint-cli2` beim Einrichten: `nodeenv --prebuilt` bricht ab mit `ValueError: invalid literal for int() … '0-alpha'`.
- Ursache: pre-commit nutzt ein vorhandenes Node nur, wenn `node` und `npm` **nicht** im Home-Verzeichnis liegen (`pre_commit/lang_base.py`, `exe_exists`). `scripts/session-start.sh` legt Node 26.12.1 nach `/root/.cache/skriptorium-tools/…` und stellt es im `PATH` nach vorn – pre-commit übergeht es und lädt per nodeenv das „neueste“ Node; der Index von nodejs.org führt inzwischen eine Alpha-Version, an deren Nummer nodeenv scheitert. Auf dem Mac nicht aufgefallen (Hook-Umgebung dort schon eingerichtet).
- Lösung für diese Session: Commit mit `PATH=/usr/local/bin:$PATH` (System-Node 22.23.4 der Cloud-Umgebung, nur für den Hook); alle Hooks liefen, kein `--no-verify`.
- Offen: dauerhafte Lösung → D.28 (freigabepflichtig, Kategorie 7).

### 2026-11-06 – [SESSIONSTART] 10.10 Textqualität von Hermes 4 messen

- **Umgebung:** Cloud-Session (Branch `scp/zealous-meitner-g94yap`, Stand `478e5fd` = `main` mit den Doku-Nachträgen aus PR #216).
- **Modell:** eingestellt `claude-opus-5-5`, bedient laut Sitzungsabfrage `claude-opus-5-5` (`session_context.model`; `last_served_model` nicht gemeldet) → Entscheidungs-Klasse. Empfohlene Klasse für 10.10: Entscheidung – passt.
- **Kontextgröße:** Sitzungsabfrage meldet `used_tokens` 0 bei Sessionbeginn; Grenze 200.000 wird nach jedem Schritt geprüft.
- **Mindest-Lektüre:** Kontext vollständig, Logbuch ab letztem Sessionende, Fahrplan (Stand, Phase 10, V.41), Architektur 1/2/9, Entscheidungen Teil A und C, aktive Blocker (keine).
- **Vorhaben:** 10.10 nach V.41 – Messung nach Regel-002 an Salzmark und zweiter Testgeschichte: grok-4.6 (Bezug), Hermes 4 wie heute, mit Reasoning, mit Strafen gegen Wiederholung und ggf. niedrigerer Temperatur; Kosten vorher schätzen.

### 2026-11-06 – [SESSIONENDE] 10.6 und 10.7 erledigt, Node 26, nächstes Mal 10.10

- **Dauer:** 2026-11-05 (Sessionstart „10.2 vorbereiten“) bis 2026-11-06 (fortgesetzte, mehrfach verdichtete Session).
- **Bearbeitet seit dem letzten Sessionende:** 10.2 (ADR-107), 10.3 (ADR-108), 10.4, 10.5 (ADR-109 mit Nachtrag), 10.6 (ADR-110; zwei Befunde des Eigentümers behoben: Menü hinter „⋯“ auf schmalen Bildschirmen, PR #214; Bildfenster außerhalb des Bildes bei langen Kapiteln, PR #215 – je mit End-to-End-Test), 10.7 Bilder beim Schreiben (ADR-111, PR #211), D.1 Node 26.12.1 (ADR-112, PR #212), D.27 Vitest 4.1.12 (PR #213). Alle abgenommen bzw. erledigt; Phase 10: 7 von 11.
- **Stand:** `main` = `de64667`, auf dem Server eingespielt (`de64667`, gesund). Doku-Nachträge seit `de64667` liegen lokal auf `docs/10.6-fenster-zusammengefuehrt` (Merge und Einspielen der zweiten Korrektur, Abnahme 10.6, dieser Sessionende-Eintrag) – nicht gepusht.
- **Offen:** Doku-Zweig in `main` bringen, damit die nächste (Cloud-)Session den Stand sieht; `minimatch` unter ESLint (mittel, kein Ausweg außer ESLint 9); Token je Bild (10.7) bei Gelegenheit mit gleichem Modell mit/ohne Haken vergleichen; überholter lokaler Zweig `feat/9.9-loeschen-archivieren` (nur auf Wort des Eigentümers löschen).
- **Nächster Schritt:** **10.10 Textqualität von Hermes 4 messen** (Eigentümer: „beim nächsten Mal 10.10“) – in einer Cloud-Session (Schlüssel für KI-Läufe gilt nur dort), Regel-002 an beiden Testgeschichten. Datiert: D.5 (httpx2, mypy 2) ab 2026-11-12; D.11 Frist 2026-10-31 überschritten (Eigentümer).
- **Sessionende-Prüfungen:** README gegen Fahrplan, Kontext, Architektur, Blocker abgeglichen (7 von 11, 10.10 als Nächstes, 0 Blocker, Letzte Änderung 2026-11-06). Drift: ADR-111 → 10.7, ADR-112 → D.1 vorhanden; Reifegrade unverändert; Modul-Liste unverändert; FR-034/FR-035 mit Schritt und Test; 0 blockierte Schritte; Reaktiv-Quote 0/10 (ADR-103 bis ADR-112); Phase 10 bei 11 von 11 geplanten Schritten. Größen: Logbuch 440+ Zeilen (Trigger 1.600 bei Klasse K bzw. 800), `docs/project-context.md` 349 Zeilen (Budget 600). Ablaufdaten-Register: Node 26 bis 2029-04-30 eingetragen; mypy-2-Nachprüfung (2026-11-06) hat ihren Schritt D.5.
- **Modell-Bilanz:** aktiv Opus 5.5 (Entscheidungs-Klasse, Quelle: Systemkontext). Oberhalb der Empfehlung: D.27 (Routine), die beiden Korrekturen zu 10.6 (Bugfix, Routine), Einspielen, Doku-Nachträge und README-Pflege (Routine). Abgegeben: nichts – Abgabe an die Routine-Klasse ruht bis zum Probelauf D.22; kleine Teilarbeiten mit geladenem Kontext.
- **Kontextgröße:** nicht feststellbar; Session mehrfach verdichtet.

### 2026-11-06 – [BEOBACHTUNG] 10.6 abgenommen

- Eigentümer nach dem Einspielen von `de64667`: „Hat funktioniert.“ 10.6 → ERLEDIGT; Phase 10: 7 von 11 (offen 10.8, 10.9, 10.10, 10.11).
- Bis zur Abnahme zwei Befunde, beide nur in der Oberfläche und nur im echten Browser sichtbar (schmale Breite; langes Kapitel) – je behoben mit End-to-End-Test (PR #214, #215).

### 2026-11-06 – [BEOBACHTUNG] Zweite Korrektur zu 10.6 eingespielt

- Eigentümer: „Ja, einspielen“. Nach Runbook (ADR-039), `REVISION` `de64667`, Rückweg `skriptorium:vorher` und `app.vorher`. Vorher lief `25a9220`.
- Prüfung: `/api/health` 200 nach 60 s, Anmeldeseite 200; eine SSH-Prüfung: `(healthy)`, `de64667`, 0 Fehlerzeilen in 3 Minuten. Offen: erneute Abnahme 10.6 (Eigentümer).

### 2026-11-06 – [BEOBACHTUNG] Zweite Korrektur zu 10.6 zusammengeführt

- Eigentümer: „Ja, PR und Merge“. PR #215, CI vier Jobs grün (Python 1:55, Pre-Commit 2:01, TypeScript 2:05, E2E 1:55), Hinweise nur Ubuntu-26. Zusammengeführt mit `--match-head-commit` → `de64667`. Server läuft weiter `25a9220`.

### 2026-11-06 – [GELÖST] 10.6: Bildfenster öffnet sich außerhalb des sichtbaren Bereichs

- Befund des Eigentümers (Desktop, keine „⋯“): Absatz markiert, „＋ Bild“ → Menü erscheint, „Aus dem Kanon …“ → „passiert gar nichts“. Seine Vermutung, durch Hochscrollen bestätigt: Das Fenster stand oben über dem Text.
- Ursache: `StoryPictureDialog` steht in `ChapterEditor` über dem Manuskript; bei Kapiteln von rund 10.000 Wörtern liegt die markierte Stelle weit darunter. Das Formular „In den Kanon“ wird seit 5.2 ins Bild gerollt (`useCanonTake`), das Bildfenster nicht. Der erste End-to-End-Test hatte ein Kapitel mit einem Satz und sah das nicht.
- Nachgestellt mit Playwright (1280 px, 80 Absätze, Cursor am Ende): Fenster vorhanden, sichtbar zu 0 %.
- Lösung: beim Öffnen `scrollIntoView({ block: "start" })` wie in 5.2 (gilt auch für „✨ Bild erzeugen“). Neuer End-to-End-Test: Fenster im Bild, Zeile nach Absatz 80, Vorschau im Bild; vorher rot, danach grün. Prüfreihe grün (585 Komponenten-Tests, 17 End-to-End-Tests).
- Lehre: Abläufe im Kapitel im End-to-End-Test mit langem Text prüfen – die Kapitel des Eigentümers haben im Mittel rund 10.000 Wörter.

### 2026-11-06 – [BEOBACHTUNG] Korrektur zu 10.6 eingespielt

- Eigentümer: „Ja, einspielen“. Nach Runbook (ADR-039), `REVISION` `25a9220`, Rückweg `skriptorium:vorher` und `app.vorher`. Vorher lief `8e87aab`.
- Prüfung: `/api/health` 200 nach 65 s, Anmeldeseite 200; eine SSH-Prüfung: `(healthy)`, `25a9220`, 0 Fehlerzeilen in 3 Minuten. Offen: erneute Abnahme 10.6 (Eigentümer).

### 2026-11-06 – [BEOBACHTUNG] Korrektur zu 10.6 zusammengeführt

- Eigentümer: „Ja, PR und Merge“. PR #214, CI vier Jobs grün (Python 1:17, Pre-Commit 1:49, TypeScript 2:01, E2E 2:18 mit dem neuen Test), Hinweise nur Ubuntu-26. Zusammengeführt mit `--match-head-commit` → `25a9220`. Server läuft weiter `8e87aab`.

### 2026-11-06 – [GELÖST] 10.6: Menü von „＋ Bild“ auf schmalen Bildschirmen unsichtbar

- Befund des Eigentümers: „es erscheint kein Bild und keine Vorschau“. Server seit dem Einspielen: kein `POST …/stories/{story_id}/images`, kein Ordner `bilder/` in einer Geschichte – der Ablauf brach im Browser vor dem Hochladen ab.
- Ursache: Unter 56rem liegen die Werkzeuge hinter „⋯“; jeder Knopf darin klappt sie zu (5.2) – auch „＋ Bild“, das nur sein Menü öffnet. Das Menü steckt im zugeklappten Bereich und bleibt unsichtbar. In jsdom ohne CSS nicht sichtbar, deshalb grüne Komponenten-Tests; 10.6 hatte keinen End-to-End-Test.
- Nachgestellt mit Playwright: 1280 px – ganzer Weg grün (Kopie in die Geschichte, Zeile, Vorschau lädt); 820 px – Menü unsichtbar.
- Lösung: Knöpfe mit `aria-expanded` (öffnen nur ein Menü) klappen nicht zu (`ComposerControls`). Komponenten-Test erweitert; neuer End-to-End-Test bei 820 px: Bild aus dem Kanon, Zeile, Vorschau (48 px breit geladen), E-Book enthält `OEBPS/bilder/bild-….jpg`. Gegenprobe ohne Korrektur: Test scheitert am Menü. Prüfreihe grün (585 Komponenten-Tests, Zweige 95,22 %; 16 End-to-End-Tests).
- Lehre: Alles, was hinter „⋯“ liegt, im End-to-End-Test auch bei schmaler Breite prüfen.

### 2026-11-06 – [BEOBACHTUNG] 10.7 abgenommen

- Eigentümer: „Aussehen, Kleidung und Umgebung passen zum Bild und der Haken verschwindet auch wieder, nachdem man Weiterschreiben angeklickt hat.“ 10.7 → ERLEDIGT; Phase 10: 6 von 11 (10.6 weiter in Abnahme).
- Token je Bild nachgeprüft (Server, nur Zahlen): erste Anfrage mit Bildern 2026-11-05 23:33 UTC mit Qwen 3.8 Max, 25.703 Token ein; die Anfragen davor mit Grok 4.5 lagen bei 23.162–23.240. Kein sauberer Vergleich (anderes Modell und Zählweise, Bildzahl wird nicht gespeichert) – die Schätzung 2.500 je Bild bleibt; ein Vergleich gleiche Stelle, gleiches Modell, mit und ohne Haken würde es klären.

### 2026-11-06 – [BEOBACHTUNG] 10.7, D.1 und D.27 eingespielt

- Eigentümer: „Ja, einspielen“. Nach Runbook (ADR-039), `REVISION` `8e87aab` (enthält 10.7, D.1, D.27), Rückweg `skriptorium:vorher` und `app.vorher`. Vorher lief `5aa544a`. Erster Bau mit `node:26.12.1-slim` auf dem Server – ohne Auffälligkeit.
- Prüfung: `/api/health` 200 nach 60 s, Anmeldeseite 200; eine SSH-Prüfung: `(healthy)`, `8e87aab`, 0 Fehlerzeilen in 3 Minuten. Offen: Abnahme 10.6 und 10.7 (Eigentümer).

### 2026-11-06 – [BEOBACHTUNG] D.27 erledigt

- Eigentümer: „Ja, PR und Merge“. PR #213, CI vier Jobs grün (Python 2:01, Pre-Commit 1:27, TypeScript 1:57, E2E 2:15), Hinweise nur Ubuntu-26. Zusammengeführt mit `--match-head-commit` → `8e87aab`. D.27 → ERLEDIGT; kein Einspielen nötig (nur Testwerkzeug).

### 2026-11-06 – [BEOBACHTUNG] D.27 Vitest 4.1.12 umgesetzt (lokal)

- Eigentümer: „Ja, Vitest heben“. Schritt D.27 angelegt (Patch-Update, nicht freigabepflichtig). `vitest`/`@vitest/coverage-v8` 4.1.11 → 4.1.12 (2026-10-15); `npm install` zog `chai` 6.3.0, `std-env` und `tinyrainbow` je eine Minor höher (Bereiche von Vitest selbst).
- `npm audit`: Vitest-Befunde weg; übrig 10 mittlere Befunde, alle aus `minimatch` 7.0.0–11.0.0 über `@eslint/config-array` (eslint, typescript-eslint, `@eslint/js`). Kein Ausweg außer ESLint 9 – offen gelassen, bis ESLint nachzieht; CI prüft `--audit-level=high` (0 Befunde).
- Prüfreihe auf Node 26 grün (Zahlen bei D.27).

### 2026-11-05 – [BEOBACHTUNG] D.1 erledigt

- Eigentümer: „Ja, PR und Merge“. PR #212, CI vier Jobs grün auf Node 26.12.1 (Python 1:42, Pre-Commit 2:02, TypeScript 1:33, E2E 2:10 – Chromium-Download diesmal normal), 0 `ExperimentalWarning`/`DeprecationWarning` im Protokoll, Hinweise nur Ubuntu-26. Zusammengeführt mit `--match-head-commit` → `4a2295b`. D.1 → ERLEDIGT.
- Server läuft weiter `5aa544a` (gebaut mit Node 24); das nächste Einspielen baut den Oberflächen-Abschnitt mit `node:26.12.1-slim` und bringt 10.7 mit.

### 2026-11-05 – [ONBOARDING-VALIDATION] Node 26 (D.1)

- Frischer Worktree von `9fa8665`: `scripts/session-start.sh` lud Node 26.12.1 (SHA-256 passt), `npm ci`-Stand mit 270 Paketen, Pre-Commit-Hook; danach `npm run build` grün, 585/585 Komponenten-Tests, Stichprobe 152 Python-Tests (`tests/context`). Worktree danach entfernt. Kein Befund.

### 2026-11-05 – [ADR-ANGELEGT] ADR-112 Node 26 (D.1), umgesetzt (lokal)

- Versionstabelle vorgelegt (Quellen: `schedule.json`, `dist/index.json`, npm-Registry, Docker Hub, CI von Vite und Vitest); Eigentümer: „26.12.1“ (Empfehlung nach der Reiferegel; 26.13.0 ohne Patch). Reaktiv-Quote 0/10 (ADR-103 bis ADR-112).
- Umgestellt: CI, Dockerfile, `scripts/session-start.sh` (neue SHA-256), `package.json` (`engines`, `@types/node` 26.6.6; transitiv `undici-types` 7.24.6 → 8.9.0), README, Runbook, Projektkontext, Ablaufdaten-Register (Node 26 bis 2029-04-30).
- [GELÖST] Auf Node 26 scheiterten 18 von 585 Komponenten-Tests (`theme.test.tsx`, `CanonFact.test.tsx`) mit `ExperimentalWarning: localStorage is not available because --localstorage-file was not provided`: Node 26 bringt ein eigenes `localStorage` mit, das ohne Speicherdatei unbrauchbar ist und das von jsdom verdeckt. Lösung: `execArgv: ["--no-experimental-webstorage"]` in `vite.config.ts` (Test-Worker); danach 585/585 grün, 0 Warnungen. Die App selbst ist nicht betroffen (Browser).
- Geprüft auf Node 26.12.1 lokal: tsc, eslint, Prettier (Repo-Dateien), 585 Komponenten-Tests (Zeilen 98,92 %), `vite build`, 15 End-to-End-Tests; Docker-Bauabschnitt `ui` mit `node:26.12.1-slim` gebaut (arm64, Probe danach gelöscht).
- [BEOBACHTUNG] `npm audit` meldet zwei mittlere Befunde in Entwicklungswerkzeugen, unabhängig vom Node-Wechsel: `@vitest/mocker` ≤ 4.1.11 (GHSA-qxg6-89mg-rqv8, GHSA-xp26-3454-mjgp; behoben in vitest 4.1.12) und `minimatch` 7.0.0–11.0.0 über `@eslint/config-array` (GHSA-g3hv-75wg-m249; npm schlägt eslint 9 vor, also Rückschritt). Die CI prüft `--audit-level=high` und bleibt grün; nicht nebenbei behoben (keine Scope-Erweiterung) – dem Eigentümer vorgelegt.

### 2026-11-05 – [BEOBACHTUNG] 10.7 zusammengeführt

- Eigentümer: „Ja, PR und Merge“. PR #211, CI vier Jobs grün (Python 1:57, Pre-Commit 1:47, TypeScript 2:32, E2E 12:33), keine Hinweise außer der Ubuntu-26-Meldung. Zusammengeführt mit `--match-head-commit` → `39c9db4`. Server läuft weiter `5aa544a`. Doku-Nachtrag lokal auf `docs/10.7-zusammengefuehrt`.
- Mini-Reibung: Der E2E-Job brauchte 12:33 statt sonst rund 2:30 – davon 10:43 für „Chromium für Playwright installieren“ (Download), die Tests selbst 46 s. Kein Code-Befund; tritt es wieder auf, Cache für Playwright-Browser prüfen.

### 2026-11-05 – [BEOBACHTUNG] 10.7 umgesetzt (lokal)

- Nach ADR-111 auf `feat/10.7-bilder-beim-schreiben` (von `main` `5aa544a` plus `docs/10.6-zusammengefuehrt`); Zahlen im Fahrplan bei 10.7. 10.6 wartet weiter auf die Abnahme; 10.7 berührt die Kapitelbilder nicht.
- Mini-Reibungen: (1) Suche nach Verbrauchsdateien mit `glob('/**/…', recursive=True)` im Container lief über das ganze Dateisystem in die Zeitgrenze – abgebrochen, Datenpfad `/data` aus dem `Dockerfile` genommen. (2) `tsc -p .` im Ordner `ui/` findet keine `tsconfig.json`; sie liegt im Projektwurzel-Ordner. (3) `noUncheckedIndexedAccess`: `entry.images[0]` ist `string | undefined`, obwohl nur Einträge mit Bild gezeigt werden – `?? ""`. (4) Der Preis steht wie in der Modellauswahl in Cent („ca. +1,0 ct“), im Mockup stand „+0,01 $“.
- Messung für die Schätzung: eine Bildbeschreibung mit Grok 4.6 auf dem Server, 2.788 Token Eingabe bei rund 200 Token Text → 2.500 Token je Bild; nur eine Messung, nach den ersten Anfragen nachprüfen.

### 2026-11-05 – [ADR-ANGELEGT] ADR-111 Bilder beim Schreiben mitschicken (10.7)

- Vorlage mit `mockup-10.7.html` (lokal) und Auswahlfragen; Eigentümer jeweils die Empfehlung (Haken bei den Einträgen, nur Hauptbild, höchstens 4, Text gilt). Eigentümer prüft 10.6 später („Ich kann das jetzt nicht prüfen“).
- Server 2026-11-05 (nur Anzahlen): 23 Einträge mit Bildern (20 mit einem), Median 109 KB. Grok 4.6/4.7 und Qwen 3.8 Max lesen Bilder, Hermes 4 nicht. Reaktiv-Quote 0/10 (ADR-102 bis ADR-111).

### 2026-11-05 – [BEOBACHTUNG] 10.6 eingespielt

- Eigentümer: „Ja, einspielen“. Nach Runbook (ADR-039), `REVISION` `5aa544a`, Rückweg `skriptorium:vorher` und `app.vorher`. Vorher lief `56e5d1b`.
- Prüfung: `/api/health` 200 nach 60 s, Anmeldeseite 200; eine SSH-Prüfung: `(healthy)`, `5aa544a`, 0 Fehlerzeilen in 3 Minuten. Offen: Abnahme 10.6 (Eigentümer).

### 2026-11-05 – [BEOBACHTUNG] 10.6 zusammengeführt

- Eigentümer: „Ja, PR und Merge“. PR #210, CI vier Jobs grün (Python 1:22, Pre-Commit 2:12, TypeScript 2:25, E2E 2:34), keine Hinweise außer der Ubuntu-26-Meldung. Zusammengeführt mit `--match-head-commit` → `5aa544a`. Server läuft weiter `56e5d1b`. Doku-Nachtrag lokal auf `docs/10.6-zusammengefuehrt`.

### 2026-11-05 – [BEOBACHTUNG] 10.6 umgesetzt (lokal)

- Nach ADR-110 auf `feat/10.6-bilder-im-manuskript`; Zahlen im Fahrplan bei 10.6.
- Nachtrag zu ADR-110 während der Umsetzung (vor jedem Merge): Ältere Leseprogramme zeigen kein WebP, Eintragsbilder sind WebP, Pillow fehlt im Container → Kapitelbilder als JPEG; die Kopie aus dem Kanon macht der Browser (lädt, wandelt, lädt hoch), die Route `from-entry` entfällt.
- Mini-Reibungen: (1) Werkzeugzeile des Kapitels ist ein `span` im Schreibbereich – das Fenster „Bild erzeugen“ passte nicht hinein; Knopf (`StoryPictureButton`) und Fenster (`StoryPictureDialog`) getrennt, Fenster über dem Manuskript. (2) CodeMirror erlaubt Block-Dekorationen nur aus einem `StateField`, nicht aus einem Plugin. (3) `describeError` macht aus jedem Nicht-API-Fehler „Keine Verbindung zum Server.“ – auch für unlesbare Bilder in bestehenden Wegen (Eintragsbilder); im neuen Weg eigener Text, der Altbestand ist unverändert → V.50 (Landeplatz 10.11). (4) Zwei Leerzeichen in einer Beschriftung nach Entfernen von Klammern – Leerraum zusammengefasst.
- Abdeckung der Oberfläche leicht gesunken (Zweige 95,51 → 95,31 %), über der Schwelle 94 %; drei Tests nachgelegt (Seite der Geschichte, Fehler beim Speichern, volle Herkunft).

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
