# Auftrag an die Bewerter-Instanz (Sprache) – salzmark

Du bewertest KI-Fortsetzungen einer deutschen Geschichte auf **sprachliche Qualität**. Du kennst das Projekt nicht und brauchst es nicht zu kennen. Arbeite nur lesend; schreibe am Ende genau eine Datei (unten). Kanon-Treue und Handlung sind **nicht** Gegenstand dieser Bewertung.

## Material

- Text vor der Schreibstelle: `/tmp/claude-0/-home-user-Skriptorium/212d84f8-7198-5c8a-aa07-cca4f7db95ba/scratchpad/blind2/salzmark/start.txt` – er zeigt Ton und Stil, an den die Fortsetzungen anschließen sollen (düstere Low Fantasy auf Inseln am Meer, karg und kalt; Ich-Erzählerin Ilka Varn, Präteritum). Nur als Maßstab, nicht bewerten.
- Zwölf Ketten `/tmp/claude-0/-home-user-Skriptorium/212d84f8-7198-5c8a-aa07-cca4f7db95ba/scratchpad/blind2/salzmark/K01` … `/tmp/claude-0/-home-user-Skriptorium/212d84f8-7198-5c8a-aa07-cca4f7db95ba/scratchpad/blind2/salzmark/K12`, je sieben Vorschläge `01.txt` … `07.txt`, nacheinander zu derselben Stelle geschrieben (jeder Vorschlag wurde übernommen, der nächste setzt ihn fort). Alle Ketten bekamen dieselben sieben Anweisungen des Autors; die fünfte war leer („Weiter“). Die Reihenfolge ist zufällig; woher eine Kette stammt, weißt du nicht und sollst es nicht erraten. Öffne nichts unter `spikes/`.

## Bewertung je Kette

1. **Deutsch** (Note 1–5; 5 = einwandfreies, idiomatisches Deutsch wie von einer guten Autorin, 1 = häufig falsch oder unidiomatisch): Grammatik, Rechtschreibung, Wortwahl, Übersetzungsdeutsch und Anglizismen, schiefe Bilder, falsche Redewendungen.
2. **Sprachfehler** (Anzahl): eindeutige Fehler – Grammatik, falsches Wort, Wort in fremder Sprache, missglückte Redewendung, Satzbruch. Je Fehler Schritt und Zitat (höchstens 15 Wörter). Keine Geschmacksfragen.
3. **Schleifen** (Anzahl): Stellen, an denen sich innerhalb eines Vorschlags ein Satz, Halbsatz oder Absatz wörtlich oder fast wörtlich wiederholt, oder an denen derselbe Vorgang mehrmals hintereinander erzählt wird. Zwischen Vorschlägen zählt nur, was eindeutig dieselbe Formulierung immer wieder bringt (z. B. dieselbe Schlussformel in drei Vorschlägen). Je Stelle Schritt und Zitat.
4. **Stil** (Note 1–5): Trifft der Text Ton und Erzählweise des Ausgangstextes (Erzählperspektive, Tempus, Satzlänge, Ton)? Floskeln, Pathos, Kitsch, Erklären statt Zeigen senken die Note.
5. **Gesamt** (Note 1–5): Würde eine Autorin den Text so übernehmen?

Bewerte jede Kette für sich, aber mit demselben Maßstab für alle zwölf; lies zuerst alle Ketten an, bevor du Noten vergibst.

## Ergebnis

Schreibe **`/tmp/claude-0/-home-user-Skriptorium/212d84f8-7198-5c8a-aa07-cca4f7db95ba/scratchpad/bewertung2-sprache-salzmark.md`** als Markdown:

1. Tabelle: Zeilen = K01–K12, Spalten „Deutsch“, „Sprachfehler“, „Schleifen“, „Stil“, „Gesamt“.
2. Je Kette ein Abschnitt `### Knn` mit den Fehlern und Schleifen (Schritt, Zitat) und zwei Sätzen Begründung der Noten.
3. Ein Absatz „Auffälligkeiten“: Muster, die mehrere Ketten teilen (z. B. Gruppen ähnlicher Ketten), ohne Vermutung über ihre Herkunft.

Antworte am Ende in höchstens fünf Sätzen, was du geschrieben hast.
