# Quellen für Worldbuilding und Namen; eigener Recherche-Baustein (Erkundung 9.12)

<!-- Schritt 9.12 (V.35 H1, V1; ADR-090). Stand 2026-11-05. Vergleichsstudie, nur gelesen – nichts gebaut.
     Preise und Bedingungen aus den genannten Quellen am 2026-11-05; Preise ändern sich, vor einer Umsetzung neu prüfen. -->

## 1. Frage

- **V1:** Lohnt sich ein eigener Recherche-Baustein im Skriptorium statt der Websuche über OpenRouter (ADR-064) – um Kosten zu sparen und nicht alles über OpenRouter laufen zu lassen?
- **H1:** Welche Anleitungen zum Worldbuilding und welche Seiten zur Namensbildung sind verlässlich, was erlauben ihre Nutzungsbedingungen, und wie kämen sie in den Weltenbauer?

## 2. Ausgangslage

- Websuche im Weltenbauer: Kästchen „mit Websuche“ je Antwort; Plugin `web` von OpenRouter, `max_results` 5, keine Wahl der Suchmaschine (`ai_gateway/openrouter.py`). Ohne Angabe nimmt OpenRouter bei SpaceXAI (Grok), OpenAI, Anthropic, Google und Perplexity die **eigene Suche des Anbieters**, sonst Exa.
- Messung in 6.7 (Grok 4.6, also eigene Suche von SpaceXAI): 5,9–7,0 ct je Antwort, weil 17.000–22.000 Token Suchergebnisse als Eingabe zählen.
- **Verbrauch Oktober und November** (Server, 2026-11-05, nur Zahlen gelesen): 141 Weltenbauer-Anfragen. Die Verbrauchsdatei kennt kein Merkmal „Websuche“; Anfragen, deren Eingabe gegenüber der vorigen im selben Gespräch um mehr als ca. 10.000 Token springt, sind höchstwahrscheinlich Websuchen (einige können Manuskript-Treffer aus 8.9 sein). Das sind etwa 26, fast alle mit Grok zwischen 2026-10-12 und 2026-10-20, mit 15.000–83.000 Token Eingabe und 4–15 ct je Antwort, zusammen **ca. 1,90 $** – Obergrenze. Seit 2026-10-21 keine solche Anfrage mehr; die Weltenbauer-Anfragen mit qwen3.8-max liegen bei 1–3 ct.
- Folgerung: **Die Suchgebühr ist der kleine Teil. Teuer ist, wie viel Suchtext ins Sprachmodell geht** – und wer sucht.

## 3. V1 – Recherche: Optionen

Preise je Suche ohne den Sprachmodell-Anteil; dieser kommt hinzu und hängt an der Menge des Suchtexts (bei 2 $ je Million Eingabe-Token kosten 5.000 Token 1 ct, 20.000 Token 4 ct).

| | Option | Suchgebühr | Suchtext ins Modell | Abhängigkeit, Konto, Schlüssel | Daten nach außen |
|---|---|---|---|---|---|
| A | **Plugin `web` wie heute, aber eingestellt:** Suchmaschine fest auf Exa (oder Parallel), 3 statt 5 Treffer | Exa 0,7 ct, Parallel (Turbo/Fast) 0,1 ct je Anfrage (OpenRouter, Stand heute) | Exa liefert Auszüge von ca. 2.000–4.000 Zeichen je Treffer → bei 3 Treffern grob 2.000–3.000 Token statt 15.000–80.000 bei der eigenen Grok-Suche (zu messen) | keine neue; läuft weiter über OpenRouter und dessen Schlüssel | Suchanfrage an OpenRouter und Exa bzw. Parallel |
| B | **Eigener Baustein „Wikipedia“:** Server sucht über die MediaWiki-API (de und en), holt die Einleitungen der 2–3 besten Artikel, gibt sie gekürzt mit Fundstelle an das Modell | 0 | wir bestimmen die Menge, z. B. höchstens 3.000 Token | neuer externer Dienst (Kategorie 3), **ohne Konto und Schlüssel**; Pflicht: eigener User-Agent mit Kontakt (z. B. Repo-Adresse), Anfragen nacheinander, Rückzug bei `ratelimited` | Suchbegriff an Wikimedia; Texte frei unter CC BY-SA – Fundstelle nennen, nichts wörtlich in den Kanon übernehmen ohne Hinweis |
| C | **Eigener Baustein mit Such-API** (Brave oder Tavily), Auszüge selbst gekürzt | Brave: 5 $ je 1.000 Anfragen, 5 $ Guthaben je Monat (≈ 1.000 Anfragen frei, Kreditkarte nötig, Überziehung ohne Obergrenze); Tavily: 1.000 Anfragen je Monat frei ohne Karte, danach ca. 0,8 ct | wir bestimmen die Menge | neuer Dienst **mit Konto und Schlüssel** (Secret auf dem Server, Rotationsweg, Kategorie 3 und 6) | Suchbegriff an Brave bzw. Tavily (Tavily gehört seit 2026 zu Nebius) |
| D | Nichts ändern | – | – | – | – |

Beobachtungen:

- **A** ist eine Einstellung im vorhandenen Adapter (`plugins: [{id: web, engine: exa, max_results: 3}]`); bei qwen und anderen Modellen ohne eigene Suche ist Exa schon heute die Vorgabe, nur bei Grok würde sich etwas ändern. Spart den größten Teil, aber nicht die Abhängigkeit von OpenRouter.
- **B** trifft den häufigsten Fall „alltagsbekannter Gegenstand, Handwerk, Geschichte“ (Probe in 6.7: Salzsiederei – Fundstellen waren en- und de-Wikipedia plus ein Lexikon) und ist der einzige Weg ohne laufende Kosten und ohne neues Konto. Grenzen: nur, was in Wikipedia steht; keine aktuellen Seiten, keine Foren.
- **C** ist am flexibelsten, bringt aber ein weiteres Konto mit Secret und Abrechnung – für ca. 2 $ im Monat (Abschnitt 2) ist das ein ungünstiges Verhältnis von Aufwand zu Ersparnis.
- Ersparnis absolut: Am Verbrauch von Oktober gemessen höchstens ca. 1,50–1,80 $ im Monat; seit dem Wechsel auf qwen fast null. Der Hauptnutzen von B ist die **Unabhängigkeit** der Recherche von OpenRouter und eine planbare Größe der Anfrage, nicht die Ersparnis.
- Bekannte Lücke: Die Verbrauchsdatei weiß nicht, ob eine Anfrage mit Websuche lief. Ein Feld `websuche` (Kategorie 4, additiv) würde das künftig zeigen – gehört zur Umsetzung, falls gewählt.

## 4. H1 – Namen: Optionen

| | Quelle | Was sie liefert | Nutzungsbedingungen | Einbindung |
|---|---|---|---|---|
| N1 | Sprachmodell im Weltenbauer (heute) | erfundene Namen nach Wunsch („klingt kanadisch“) | keine Einschränkung | vorhanden; neigt zu immer gleichen Mustern, keine Gewähr für „klingt echt“ |
| N2 | **Offene Namenslisten, im Skriptorium ausgewertet:** GeoNames (Orte je Land, z. B. Kanada), Wikidata (Vor- und Nachnamen) | echte Orts- und Personennamen je Land; daraus ließen sich neue, ähnlich klingende Namen bilden (Silben- oder Markov-Verfahren) oder echte Namen als Vorbild an das Modell geben | GeoNames: CC BY – GeoNames als Quelle nennen; Wikidata: CC0 | Daten einmal herunterladen, verdichten (wenige 100 KB je Land) und mit dem Programm ausliefern; kein Dienst zur Laufzeit |
| N3 | Behind the Name (API) | echte Vornamen mit Herkunft und Bedeutung, Zufallsnamen | kostenlos, Schlüssel nötig; 2 je Sekunde, 4.000 am Tag; gewerbliche Nutzung der API nicht geregelt, Daten zum Herunterladen unter CC BY-SA | neuer Dienst mit Schlüssel – für Vornamen allein zu viel Aufwand |
| N4 | Namensgeneratoren im Netz (z. B. Fantasy Name Generators) | sehr viele Stilrichtungen | keine Schnittstelle; Seite sperrt automatische Abrufe (HTTP 403); erzeugte Namen dürfen laut Lizenzhinweis in eigenen Werken genutzt werden, der übrige Inhalt nicht kopiert werden | nur als Verweis für den Autor, nicht einbindbar |

## 5. H1 – Anleitungen zum Worldbuilding

- Verbreitete Quellen: Fragenkataloge (z. B. Patricia C. Wrede, bei der SFWA veröffentlicht), Sandersons „Gesetze“ zu Magiesystemen, Worldbuilding Stack Exchange (CC BY-SA), Schreibratgeber-Blogs. Sie sind **Meinungen und Handwerk, keine Fakten** – „Verlässlichkeit“ heißt hier: anerkannt und in sich stimmig, nicht „richtig“.
- Nutzungsbedingungen: Die meisten Texte sind urheberrechtlich geschützt; Ideen und Fragen dürfen aufgegriffen, die Texte nicht übernommen werden.
- Einbindung ohne Dienst: eine **eigene kurze Fragenliste je Art** (Figur, Ort, Gegenstand, Kultur – passend zu den festen Abschnitten aus 9.3) in eigenen Worten im Programm. Der Weltenbauer kann damit sagen, was einem Eintrag noch fehlt („Wer profitiert von dieser Regel?“, „Was kostet diese Magie?“). Kein Abruf zur Laufzeit, keine Kosten außer wenigen hundert Token.

## 6. Empfehlung (zur Vorlage)

- **V1: B, dazu A als Sofortmaßnahme.** A ist eine Einstellung ohne neue Abhängigkeit und senkt die Kosten der freien Websuche sofort; B macht die häufigste Recherche unabhängig von OpenRouter und kostenlos, ohne Konto und Secret. C nicht, solange die Websuche nur wenige Dollar im Monat kostet.
- **H1 Namen: N2**, zunächst mit wenigen Ländern nach Wahl des Eigentümers; N4 als Verweis.
- **H1 Anleitungen:** eigene Fragenliste je Art.
- Umsetzung jeweils als eigener Schritt mit Landeplatz 9.15 (Akzeptanzkriterium von 9.12), mit ADR für die neuen Dienste (Kategorie 3).
- **Konfidenz:** hoch für die Kostenaussage (gemessen 6.7 und Verbrauch Oktober); mittel für die Größe des Exa-Suchtexts bei A (Herstellerangabe, nicht gemessen); mittel für den Nutzen von N2 (Klang der gebildeten Namen ist erst am Beispiel zu beurteilen). **Umkehrbarkeit:** billig – alle Optionen sind abschaltbar und ändern keine gespeicherten Daten.

## 7. Quellen

- OpenRouter, Web Search: <https://openrouter.ai/docs/guides/features/web-search> (Preise der Suchmaschinen, Vorgaben, Auszüge von Exa)
- Exa, Pricing: <https://exa.ai/docs/reference/pricing>
- Brave Search API: Preise laut mehreren Übersichten (u. a. <https://costbench.com/software/ai-search-apis/brave-search-api/>), offizielle Seite nicht abrufbar – vor Umsetzung prüfen
- Tavily: <https://costbench.com/software/web-scraping/tavily/>, <https://coldiq.com/blog/tavily-pricing>
- Wikimedia: User-Agent-Richtlinie <https://foundation.wikimedia.org/wiki/Policy:Wikimedia_Foundation_User-Agent_Policy>, API-Etikette <https://www.mediawiki.org/wiki/API:Etiquette>
- GeoNames, Export und Lizenz: <https://www.geonames.org/export/>
- Behind the Name, API: <https://www.behindthename.com/api/>
- Fantasy Name Generators: Lizenzhinweis zitiert in <https://git.neptards.moe/neptards/offline-fantasy-name-generators/file/README.md.html>; die Seite selbst lehnt automatische Abrufe ab
