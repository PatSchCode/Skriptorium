# Erkundung: Bildanbieter für Schritt 7.12 (fal.ai, Replicate, Runware)

> **Ergebnis (ADR-076, 2026-10-12):** 7.12 bleibt vorerst bei OpenRouter; weitere Bildanbieter später (V.24, Landeplatz 7.8). Die Befunde unten sind für diese spätere Phase festgehalten.

Stand 2026-10-12. Anlass: Vorschlag des Eigentümers, Bilder in 7.12 über fal.ai statt OpenRouter zu erzeugen; Auftrag: „prüfen, welche Modelle mit API bei fal.ai verfügbar sind und wo sich Filter abschalten lassen“.

## Nachprüfung für 10.8 (2026-11-07)

- **OpenRouter heute:** 63 Bildmodelle im öffentlichen Katalog (`/api/v1/images/models`, selbst abgefragt), u. a. FLUX.2/FLUX 3, Seedream 4.5–5.0, Gemini/Nano Banana, GPT Image 1–2.6, Qwen Image 2.1–3, Krea 2, Recraft V3–V4.1, Grok Imagine 2.0, MAI Image, Hunyuan Image 3.5. Offene Modelle mit abschaltbarem Filter (FLUX.1 [dev], Z-Image, HiDream, SDXL, Pony, LoRA-Varianten) fehlen. Ein zweiter Anbieter bringt also vor allem **offene Modelle mit eigenem Filterschalter** und niedrigere Preise dafür, kaum neue geschlossene Modelle.
- **Runware** (Preisseite): FLUX 3 Klein 0,003 $ (512 × 512, 16 Schritte), Qwen-Image-2.1-Turbo 0,014 $, Seedream 5.0 Flash 0,019 $, FLUX 3 Image 0,041 $ (0,75K), Qwen-Image-2.1-Pro 0,075 $ je Bild; „Community 300k+“. Startguthaben jetzt **2 $ nur mit Geschäfts-E-Mail** (2026-10-12: rund 1.000 Bilder). API: `POST https://api.runware.ai/v1`, Liste von Aufgaben (`taskType: imageInference`, `model` als Kennung wie `xai:grok-imagine@image-2.0`, `positivePrompt`, `width`, `height`), Kosten nur mit `includeCost: true`, Bild-Adressen 7 Tage gültig (`ttl`). Offene Modelle (Z-Image, HiDream, FLUX dev) stehen nicht auf der Preisseite – Verfügbarkeit erst mit Schlüssel (Modellsuche) belegbar.
- **Replicate** (Preisseite): FLUX schnell 0,003 $, FLUX dev 0,025 $, FLUX 1.1 pro 0,04 $, Recraft V3 0,04 $, Ideogram V3 Quality 0,09 $ je Bild; übrige nach Rechenzeit.
- **fal.ai** (Preisseite): Z-Image Turbo 0,005 $ und FLUX 2 0,012 $ je Megapixel, FLUX.1 [dev] 0,025 $ je Megapixel, Seedream 4.5 0,04 $, Seedream 5.0 Pro 0,0675 $, Nano Banana Pro 0,15 $ je Bild; Vorab-Guthaben.
- **Filter nachgeprüft:** fal – Feldbeschreibung von `enable_safety_checker` bei `fal-ai/flux/dev`, `fal-ai/z-image/turbo`, `fal-ai/pony-v7` unverändert: „Disabling it requires account authorization; unauthorized requests are always checked, and images flagged as unsafe are returned as black images.“ Wie man die Freischaltung bekommt, nennt die Doku weiter nicht. Runware – Prüfung laut Integrationsdoku (Pipedream, `checkNSFW`) nur auf Anforderung in der Anfrage, sonst keine; kostet dann extra. Offizielle Seite zur Inhaltsprüfung nicht mehr erreichbar (404) – Voreinstellung damit nicht aus erster Hand belegt.
- **Erwachseneninhalte (Wunsch des Eigentümers 2026-11-07):** Runwares Bedingungen (abgerufen 2026-11-07, §10) verbieten sexuelle Darstellungen Minderjähriger und Material, das Minderjährige anspricht, und im selben Absatz Material, das „sexual material, graphic violence, obscenity, or other mature themes“ fördert – ob das auch für Inhalte zwischen fiktiven Erwachsenen gilt, lassen die Bedingungen offen. Erwachsenen- oder BDSM-Inhalte sind weder ausdrücklich erlaubt noch verboten; §2 verweist auf eigene Bedingungen je Modell, §11 verlangt Mindestalter 18. Geschlossene Modelle (Seedream, GPT Image, Nano Banana, FLUX pro) liefern so etwas nicht; in Frage kommen nur offene bzw. Community-Modelle. Kandidaten (aus Modellwissen, Verfügbarkeit bei Runware nicht belegt): fotorealistisch auf SDXL-Basis (z. B. Lustify, BigASP, epiCRealism XL), Anime/Comic (Pony Diffusion V6 XL, Illustrious XL bzw. NoobAI XL), auf FLUX-Basis Chroma; Z-Image Turbo und HiDream gelten als weniger beschränkt als FLUX dev. Pony- und Illustrious-Modelle erwarten Schlagwort-Prompts (Booru-Tags) statt Fließtext – Folge für die Vorbelegung aus dem Kanon.
- Unverändert seit 2026-10-12 (nicht neu geprüft): übrige Nutzungsbedingungen unten.

Quellen zum Nachtrag: <https://runware.ai/terms>, <https://offlinecreator.com/pony-diffusion-nsfw-models>, <https://reddit.sentinel-team.org/posts/1r1t8bj/snapshots/2026-02-11T20%3A12%3A00.051748Z>, <https://civarchive.com/seaart/models/ea32205921b9dde648f189932248d6fd/versions/98279f05714d6ebc08c3c56d8122f3b0> (abgerufen 2026-11-07).

Quellen: <https://openrouter.ai/api/v1/images/models>, <https://runware.ai/pricing>, <https://runware.ai/docs/image-inference/api-reference>, <https://runware.ai/models>, <https://replicate.com/pricing>, <https://fal.ai/pricing> (alle abgerufen 2026-11-07).

## Modellsuche mit Schlüssel (2026-11-07, Cloud-Session)

Nur lesend: `modelSearch` (kostenlos), `accountManagement`/`getDetails` (nur Guthaben und Verbrauch ausgewertet; die Antwort listet auch die Schlüssel des Kontos – nie ausgeben, im Adapter nicht aufrufen), öffentliche Modell-Schemata `https://runware.ai/docs/models/<id>/schema.json` (Preise in `info["x-pricing"]`). Kein Bild erzeugt.

- **Offene Modelle, von Runware betrieben (Preis je Bild laut Schema):**

| Modell | Kennung (AIR) | Beispielpreis |
|---|---|---|
| FLUX.2 [dev] | `runware:400@1` | 0,009 $ (1024², 20 Schritte); 0,0205 $ (50 Schritte) |
| FLUX.2 [klein] 4B / 9B | `runware:400@4` / `runware:400@2` | – (nicht ausgewertet) |
| FLUX.1 [dev] | `runware:101@1` | 0,0038 $ (1024², 28 Schritte) |
| FLUX.1 Krea [dev] | `runware:107@1` | 0,0098 $ |
| FLUX.1 [schnell] | `runware:100@1` | 0,0013 $ |
| Z-Image | `runware:z-image@0` | 0,0045 $ (1024², 20 Schritte) |
| Z-Image-Turbo | `runware:z-image@turbo` | 0,0032 $ (1024²), 0,0141 $ (2048²) |
| HiDream-I1 Dev / Fast / Full | `runware:97@2` / `@3` / `@1` | 0,0045 / 0,0038 / 0,009 $ (1024²) |
| Juggernaut Z (auf Z-Image) | `rundiffusion:200@100` | – |

- **Geschlossene Modelle zum Vergleich:** Seedream 5.0 Flash 0,0193 $, Qwen-Image-2.1-Turbo 0,0141 $, FLUX 1.1 [pro] 0,04 $ – deckungsgleich mit der Preisseite; OpenRouter führt diese Familien ohnehin.
- **Community-Modelle (aus Civitai, Kennung `civitai:<Modell>@<Version>`):** Pony-Basis 1.155 Treffer, Illustrious 167, NoobAI 43; gefunden u. a. LUSTIFY! (`civitai:573152@…`, mehrere Versionen), epiCRealismXL-Lightning, RealVisXL V5.0, CyberRealistic Pony, „Z Image Ultimate NSFW Unlock Turbo“. **Nicht gefunden:** BigASP, Chroma, Pony V7. Die Familien Pony, Illustrious, NoobAI und SDXL haben ein eigenes Schema ohne Preis: Abrechnung nach Rechenzeit, Kosten erst nach dem Lauf (`includeCost: true`). Pony und Illustrious: Schema nennt „tag-based prompting“.
- **Feld `nsfwLevel`** je Treffer (z. B. 31 bei LUSTIFY!, 1 bei den offiziellen Modellen). *Deutung, nicht belegt:* übernommen aus Civitai, dort Bitmaske der Altersstufen (1 PG … 16 XXX, 31 = alle Stufen).
- **Inhaltsprüfung:** 122 von 127 Text-zu-Bild-Schemata im offiziellen Verzeichnis haben `safety.checkContent` (an/aus, „Increases total generation time“); **keines nennt eine Voreinstellung**. Ohne Schalter nur 5 Vektor-Modelle (ohnehin ausgeschlossen, ADR-077). Die BFL-Pro-Modelle haben zusätzlich `safetyTolerance`. Folge: Der Adapter setzt `checkContent` ausdrücklich, statt sich auf eine Voreinstellung zu verlassen. Geschlossene Modelle filtern beim Hersteller weiter.
- **Kosten und Konto:** Guthaben 21,07 $; bisher 29 Anfragen für 3,99 $ (Probe im Playground, alle am 2026-11-07); die Aufschlüsselung je Modell (`getUsageActivity`) lieferte für den Zeitraum keine Zeilen. In der Doku keine Ausgabengrenze je Schlüssel gefunden – Bremse ist das Vorab-Guthaben ohne automatisches Nachladen. Kosten je Anfrage mit `includeCost: true` im Feld `cost`.
- **Ablauf:** Synchrone Anfragen, die nach 120 s noch laufen, kommen als `processing` zurück (dann Abfrage per `getResponse`); 429 mit `Retry-After` bei voller Warteschlange; 503/504 vorübergehend.
- **Daten:** Runware nutzt API-Daten nie zum Training; „Zero Data Retention“ nur für Unternehmenskonten. Erzeugte Bilder liegen bis zum Ablauf von `ttl` bereit.

- **Wunschmodelle des Eigentümers (2026-11-07, Abgleich Civitai-API ↔ Runware-Suche):**
  - *epiCRealism XL*, Version „VXVI – LastFAME DMD2 (Realism)“ (`civitai:277058@1552721`, Checkpoint, SDXL 1.0, März 2025): Das Modell führt Runware mit 20 Versionen (v1.0 bis VXIV, z. B. `civitai:277058@1405120` „VXIV-EyeCandy“, `civitai:277058@1346244` „VXIII-aB3AST“), dazu `beam:277058@1522905` „VXVI 0.1“ – **die verlinkte Version fehlt in der Suche**. Ob Runware nicht gelistete Civitai-Versionen beim ersten Aufruf nachlädt, zeigt nur eine Probe.
  - *Plastic Zip-Cuffs* (`civitai:2964163@3427755`, **LoRA**, Auslösewort `pla5ticz1pcuff5`, Oktober 2026): bei Runware nicht gefunden. Grundmodell „MOSS Image“ – bei Runware weder im Verzeichnis noch in der Suche; die LoRA ist dort damit nicht nutzbar. Ähnliche LoRAs für Pony/SDXL gibt es (z. B. Handschellen, `civitai:536201@596079`, `civitai:425173@473735`).
  - **Probe 2026-11-07 (Freigabe des Eigentümers):** `civitai:277058@1552721` → sofort `invalidModel` („valid AIR identifier“), ohne Kosten – Runware lädt nicht gelistete Civitai-Versionen **nicht** nach; nutzbar ist nur, was die Suche liefert. Ersatz `civitai:277058@1405120` (VXIV): 832 × 1216, 30 Schritte, CFG 5, `checkContent: false`, Fließtext-Prompt (Gelehrter in Burgbibliothek) → fotorealistisches, stimmiges Bild in 7 s für **0,0025 $** (`includeCost`).
  - **Plastic Zip-Cuffs für Krea 2 (Nachfrage 2026-11-07):** Civitai-Versionen `civitai:2964163@3386627` (V0.4 KREA, Auslösewort `pla5ticz1pcuff5`, 218 MB) und `@3358423` (V0.1 KREA, `plasticzipcuffs`) – beide bei Runware **nicht** gelistet. Runware führt Krea 2 mit offenen Gewichten: `krea:krea@2-raw` (Architektur `krea_oss_2`) und `krea:krea@2-turbo` (`krea_oss_2_turbo`), je ca. 0,015 $ je Bild, beide mit Feld `lora`; laut Schema laufen LoRAs für Turbo auch auf Raw. Krea 2 Medium/Large (`krea_2`) ohne LoRA. Weg zur Nutzung nur über **eigenen Upload** (`modelUpload`, Kategorie `lora`, Architektur `krea_oss_2` erlaubt, privat möglich; Beta kostenlos, danach 0,05 $ je GB und Monat); der Upload lädt von einer Adresse (`downloadURL`), Civitai liefert die Datei ohne Anmeldung nicht (HTTP 401). Lizenz der LoRA: Abwandlungen erlaubt, ohne Namensnennung, kommerziell nur „RentCivit“ – *Deutung, nicht belegt:* privater Upload für eigene, nicht verkaufte Bilder ist keine kommerzielle Nutzung. Offen: ob die Modellsuche private Modelle des eigenen Kontos findet; ob Runware-CLI oder Dashboard eine lokale Datei annehmen. Quellen: `https://civitai.com/api/v1/models/2964163`, Schemata `krea-2-raw`, `krea-2-turbo`, `krea-2-turbo-oss`, `krea-2-medium`, <https://runware.ai/docs/models-api/model-upload> (abgerufen 2026-11-07).
  - Folge für die Bauweise: LoRAs sind Zusätze zu einem Grundmodell (Feld `lora` mit Kennung und Gewicht in `imageInference`), kein eigenes Modell. Die Modell-Liste aus der zweiten Vorlage kennt bisher nur Grundmodelle.

Quellen (abgerufen 2026-11-07): API `https://api.runware.ai/v1` (`modelSearch`, `accountManagement`), <https://runware.ai/docs/models/index.json>, Schemata unter `https://runware.ai/docs/models/<id>/schema.json`, <https://runware.ai/docs/models-api/pricing>, <https://runware.ai/docs/models-api/account-management>, <https://runware.ai/docs/models-api/rate-limits>, <https://runware.ai/docs/models-api/zero-data-retention>, <https://runware.ai/llms.txt>, `https://civitai.com/api/v1/model-versions/<id>`.

## Vorgehen

- Öffentlicher Modellkatalog `https://api.fal.ai/v1/models?category=text-to-image&status=active` (ohne Schlüssel lesbar): **203 aktive Text-zu-Bild-Modelle**, alle per API aufrufbar.
- Je Modell das öffentliche OpenAPI-Schema (`https://fal.ai/api/openapi/queue/openapi.json?endpoint_id=…`) gelesen und nach Eingabefeldern gesucht, deren Name auf Filter hinweist (`safety`, `moderation`, `nsfw`, `filter`, `tolerance`). 3 Schemata waren nicht lesbar (PixArt-Σ, Stable Cascade, SoteDiffusion).
- Preise je Modell liefert die API nur mit Schlüssel (`/v1/models/pricing` → 401); sie stehen auf den Modellseiten bzw. `fal.ai/pricing`.

## Ergebnis

| Art des Schalters | Anzahl | Voreinstellung | Beispiele |
|---|---|---|---|
| `enable_safety_checker` (an/aus) | 165 | 158× an, 7× aus | FLUX.1 [dev]/[schnell]/Krea, FLUX.2 (dev, Flash, Turbo, klein), Seedream 4/4.5/5, Qwen Image, HiDream, Hunyuan Image, Z-Image, SDXL, SD 3.5, Juggernaut Flux, Krea 2, Grok Imagine, GPT Image 1/2 |
| `safety_tolerance` (Stufe, 1 = streng) | 18 | FLUX pro: 2 von 1–5/6; Nano Banana/Gemini: 4 von 1–6; Flux 3: 2 von 0–4 | FLUX1.1 [pro]/Ultra, FLUX.1 Kontext pro/max, FLUX.2 pro/max/flex, Nano Banana (alle Varianten), Gemini Flash/Pro Image, Flux 3 |
| standardmäßig aus | 7 | aus | Pony V7, Wan 2.2 (5B, A14B, mit LoRAs), Recraft V3 und 20B, Stable Diffusion mit LoRAs |
| kein Schalter im Schema | 20 | – | Ideogram V2/V3/V4.5, Bria, MiniMax Image-01, GPT Image 1.5, Microsoft MAI Image 2.5, Meta Muse Image, Vidu |

## Einschränkungen (wichtig für die Entscheidung)

- **Abschalten braucht eine Freischaltung durch fal (Nachtrag 2026-10-12).** Bei 138 der 165 Modelle mit An/Aus-Schalter steht in der Feldbeschreibung: „Disabling it requires account authorization; unauthorized requests are always checked.“ Ohne Freischaltung des Kontos prüft fal also immer – auch bei Pony V7, dessen Voreinstellung „aus“ ist. Wie man die Freischaltung bekommt, ist in der öffentlichen Doku nicht beschrieben; vermutlich über den Support von fal. Die Stufen-Regler (`safety_tolerance`) tragen diesen Hinweis nicht.
- **Ein Schalter im Schema heißt nicht „ungefiltert“.** Bei geschlossenen Modellen (GPT Image, Grok Imagine, Nano Banana/Gemini, Seedream, FLUX pro) steuert der Schalter nur zusätzliche Prüfungen; der Hersteller filtert dahinter weiter. Wirklich frei steuerbar ist es am ehesten bei offenen Modellen, die fal selbst betreibt (FLUX.1 [dev]/[schnell], FLUX.2 [dev]/klein, SDXL, SD 3.5, HiDream, Qwen Image, Z-Image, Wan 2.2, Pony V7).
- **Plattformregeln gelten immer:** fal verbietet Erwachseneninhalte nicht pauschal, untersagt aber u. a. Darstellungen Minderjähriger und sexuelle Darstellungen echter Personen ohne Einwilligung; fal prüft zusätzlich automatisch (Trust & Safety, Acceptable Use Policy).
- **Vektor-Modelle** (Recraft „text-to-vector“) liefern SVG – nach ADR-072 nicht übernehmen.
- Ob ein Modell bei den Figuren des Eigentümers tatsächlich liefert, zeigt nur eine echte Probe mit fal-Konto.

## Quellen

- fal Modellkatalog-API und OpenAPI-Schemata (selbst abgefragt 2026-10-12; Rohdaten nicht im Repo)
- fal Pricing-Doku: <https://fal.ai/docs/documentation/model-apis/pricing>
- fal Acceptable Use Policy: <https://fal.ai/legal/acceptable-use-policy>
- fal Trust & Safety: <https://fal.ai/legal/trust-and-safety>

## Pony V7 (Nachfrage des Eigentümers)

- Feinabstimmung auf der Grundlage AuraFlow (von fal entwickelt, Apache-2.0); Nachfolger von Pony Diffusion V6 XL; auf Figuren ausgerichtet, vor allem Anime-, Comic- und Furry-Stile, laut Drittquelle auch realistisch. Gesichter und kleine Details können je nach Stil leiden (Modellkarte), V7.1 ist angekündigt.
- Lizenz der Gewichte: „Pony License“ mit Einschränkungen für eigene Inferenzdienste und große Firmen; die Einschränkungen gelten nicht bei Nutzung über kommerzielle APIs der Anbieter wie fal.
- Bei fal: Sicherheitsprüfung standardmäßig aus, Abschalten aber nur mit Freischaltung des Kontos wirksam (siehe oben). Parameter u. a. 40 Schritte, Bildgröße `square_hd`, Ausgabe JPEG.
- Quellen: Modellkarte <https://huggingface.co/AriaVale2/pony-v7-base>, Civitai <https://civitai.com/models/1901521/pony-v7-base>, AuraFlow-Beschreibung <https://comfyui.nomadoor.net/en/basic-workflows/auraflow/>, fal-Schema `fal-ai/pony-v7` (selbst abgefragt).

## Anbieter im Überblick (Nachfrage des Eigentümers, 2026-10-12)

| Anbieter | Eignung | Filter (laut eigener Doku) | Kosten | Anmerkung |
|---|---|---|---|---|
| fal.ai | gut | Prüfung voreingestellt an; Abschalten bei vielen Modellen nur mit Freischaltung des Kontos, sonst schwarze Bilder; 18 Modelle mit Stufen-Regler | Vorab-Guthaben, je Bild/Megapixel | 203 Text-zu-Bild-Modelle |
| Replicate | gut | Prüfung für SDXL/FLUX und Abwandlungen nur im Web fest an; per API abschaltbar, keine Freischaltung erwähnt | je Bild bzw. Rechenzeit | größter Katalog; Inhaltsregeln in den Nutzungsbedingungen prüfen |
| Runware | möglich | Prüfung per `safety.checkContent` in der Anfrage; Regeln für Erwachseneninhalte nicht gefunden | laut Drittseiten sehr günstig | Regeln unklar |
| OpenRouter | einfach, eng | große Bildmodelle mit strengen Filtern | vorhandener Schlüssel | 12 Bildmodelle im Katalog |
| Hersteller direkt | eher nicht | eigene Filter, teils Stufen | je Bild | je Hersteller ein Konto |
| NovelAI | nicht geeignet | locker, Anime | Abo mit Anlas | keine öffentliche Bild-API gefunden |
| eigene Grafikkarte | nicht geeignet | keine | Miete | VPS ohne Grafikkarte, hoher Betriebsaufwand |

Empfehlung: fal.ai und Replicate per Probe vergleichen (Eigentümer im Playground, kleines festes Guthaben), bei fal zusätzlich die Freischaltung erfragen; 7.12 mit austauschbarem Anbieter bauen.

Quellen: <https://replicate.com/docs/topics/predictions/safety-checking>, <https://fal.ai/docs/documentation/model-apis/model-arguments>, <https://help.runware.ai/articles/5571280435-is-there-a-way-to-filter-out-nsfw-content>, <https://runware.ai/docs/models/content-safety.md>, <https://docs.novelai.net/en/subscription>, Vergleichsseiten <https://www.digitalapplied.com/blog/ai-image-generation-api-pricing-comparison-2026>, <https://www.teamday.ai/blog/ai-image-video-api-providers-comparison-2026>.

## Replicate im Detail (Auftrag des Eigentümers, 2026-10-12)

Vorgabe des Eigentümers: **pornografische Inhalte sind nicht geplant.** Die Filterfrage betrifft damit vor allem Fehlalarme bei düsteren, aber nicht expliziten Motiven (Horror, Gewalt angedeutet, Waffen, Blut, Figuren in Not).

- **Modelle:** Kollektion „text-to-image“ mit vielen offiziellen Modellen: FLUX (dev, schnell, pro, 1.1 pro/Ultra, Kontext, FLUX.2 pro/flex/max/klein), Seedream 3–5, Google Imagen 3/4 und Nano Banana, OpenAI GPT Image 1.5/2, Grok Imagine, Qwen Image, HiDream, Z-Image, Wan, Hunyuan Image 3, Ideogram V2/V3, Recraft V3/V4 (davon SVG-Varianten ausschließen), Stable Diffusion 3.5, Leonardo Lucid Origin, Luma Photon, MiniMax. Die Modell-API braucht einen Schlüssel (401 ohne).
- **Filter-Schalter je Modell** (aus den öffentlichen Schema-Seiten, selbst gelesen):

| Art | Voreinstellung | Modelle |
|---|---|---|
| `disable_safety_checker` (an/aus), kein Hinweis auf Freischaltung | Prüfung an | FLUX dev/schnell/dev-lora, FLUX.2 klein, Seedream 4.5, Qwen Image, Hunyuan Image 3, SDXL |
| `safety_tolerance` (Stufe) | 2 | FLUX pro, 1.1 pro, 1.1 Ultra (1–6), Kontext pro (0–6), FLUX.2 pro/flex/max (1–5) |
| `safety_filter_level` | „block_only_high“ (lockerste Stufe) | Nano Banana Pro, Imagen 4, Imagen 4 Ultra |
| `moderation` | „auto“, wahlweise „low“ | GPT Image 1.5 und 2 |
| kein Schalter | – | Seedream 4 und 5 lite, Nano Banana, Nano Banana 2, Grok Imagine, SD 3.5, HiDream, Wan 2.2, Ideogram, Recraft, Leonardo, Luma, MiniMax |

- **Kosten:** nach Rechenzeit bzw. je Bild; Beispiele von der Preisseite: FLUX schnell 0,003 $, FLUX dev 0,025 $, FLUX 1.1 pro 0,04 $, Recraft V3 0,04 $, Ideogram V3 Quality 0,09 $ je Bild. **Vorab-Guthaben** möglich, automatisches Nachladen abschaltbar; bei leerem Guthaben startet keine neue Arbeit (selten überzieht eine laufende Anfrage, der Rest wird am Monatsende belastet). Guthaben gilt ein Jahr, nicht erstattbar. Fehlgeschlagene Läufe kosten meist nichts.
- **Nutzungsbedingungen (Abschnitt 2.7):** verboten u. a. nicht einvernehmliche Nacktheit und illegale Pornografie, jede Ausbeutung Minderjähriger, Verherrlichung von Gewalt und Terror, **„extreme gore“ wie Zerstückelung, Verstümmelung, Folter**, Belästigung und Nachahmung echter Personen ohne Einwilligung. Replicate überwacht erzeugte Inhalte nicht (8.6); Verantwortung beim Kunden.
- **Daten:** Eingaben und Ausgaben gehören dem Kunden (5.1); Replicate erhält eine Lizenz zum Verarbeiten, auch für vom Kunden gewünschte abgeleitete Modelle (5.2); anonymisierte Nutzungsdaten gehören Replicate (5.3). Aufbewahrungsfristen nennt die Bedingung nicht (Verweis auf die Datenschutzerklärung). Sitz San Francisco, kalifornisches Recht, Schiedsverfahren.
- **Einschätzung:** Ohne pornografische Absicht genügen die Filter-Regler meist; Replicate erlaubt das Abschalten bei offenen Modellen ohne Freischaltung (fal: mit Freischaltung). Grenze für die Geschichten des Eigentümers: Folter- und Verstümmelungsmotive sind laut Bedingungen verboten, unabhängig vom Filter.

Quellen: <https://replicate.com/collections/text-to-image>, Schema-Seiten `https://replicate.com/<modell>/api/schema` (selbst gelesen), <https://replicate.com/pricing>, <https://replicate.com/docs/topics/billing>, <https://replicate.com/docs/topics/billing/prepaid-credit>, <https://replicate.com/docs/topics/predictions/safety-checking>, <https://replicate.com/terms>.

## Runware im Detail (Auftrag des Eigentümers, 2026-10-12)

- **Firma und Betrieb:** Runware Ltd, Harrow (England); Recht von England und Wales, Schiedsverfahren in London; EU-Verbraucher behalten zwingende Rechte ihres Landes. Rechenzentren laut Bedingungen in den USA, Deutschland und Rumänien.
- **Modelle:** FLUX (u. a. FLUX.2 [dev], FLUX.1 Kontext), Seedream, Ideogram, Recraft, GPT Image, Nano Banana, Qwen Image, Z-Image, HiDream, Stable Diffusion 3, Krea, ERNIE Image, Kandinsky, dazu „tausende Community-Modelle“; Imagen nicht genannt. Zugang über eine API (`POST https://api.runware.ai/v1` mit Schlüssel) sowie SDKs.
- **Filter:** Inhaltsprüfung als Objekt `safety` in der Anfrage (`checkContent`; in einer älteren Doku-Fassung `checkNSFW` – uneinheitlich). Hilfe-Artikel: Filter „konfigurieren“, um Inhalte zu reduzieren oder zu blockieren – die Prüfung wirkt also wie ein Einschalt-Schutz; ob sie voreingestellt an ist, sagt die öffentliche Doku nicht ausdrücklich. Geschlossene Modelle (GPT Image, Nano Banana, Seedream) filtern beim Hersteller weiter.
- **Nutzungsbedingungen:** verboten u. a. jede sexuelle Darstellung Minderjähriger (auch KI-erzeugt), auf Minderjährige zielende Inhalte mit Sexualität, drastischer Gewalt oder reifen Themen, Belästigung von Minderjährigen, das Trainieren von Modellen auf echte Personen ohne Einwilligung; laut Hilfe außerdem illegale Inhalte, Deepfakes ohne Kennzeichnung, Täuschung und Urheberrechtsverletzungen. **Kein allgemeines Verbot von Gore/Gewalt** für Erwachsene (nur im Zusammenhang mit Minderjährigen). Erwachseneninhalte weder ausdrücklich erlaubt noch verboten.
- **Daten:** Ausgaben gehören dem Kunden; Runware beansprucht keine Rechte, veröffentlicht nichts und **speichert Ausgaben nicht langfristig**; Trainingsdaten und eigene Modelle werden **nicht zum Training** fremder oder eigener Modelle genutzt; nach Kontoschließung Löschung binnen 30 Tagen. Umgang mit Prompts: Verweis auf die Datenschutzerklärung.
- **Kosten:** Vorab-Guthaben, verfällt nicht; keine Mindestabnahme; Preis je Anfrage nach Modell und Größe bzw. Rechenzeit, **keine feste Preisliste** (Hilfe-Artikel); Beispiele der Preisseite nur für Nebenfunktionen (Hintergrund entfernen 0,0006 $). Laut Vergleichsseiten sehr günstig. **Probe: rund 1.000 Bilder kostenlos.** Bei leerem Guthaben wird der Zugang eingeschränkt.
- **Einschätzung:** Für das Skriptorium attraktiv: europäische Firma mit Rechenzentrum in Deutschland, keine Langzeitspeicherung der Bilder, kein Gore-Verbot für Erwachsene, Vorab-Guthaben ohne Verfall, kostenlose Probe. Schwächen: Doku teils uneinheitlich, keine feste Preisliste (Kosten erst je Anfrage sichtbar), Filterverhalten der offenen Modelle nur per Probe belegbar.

Quellen: <https://runware.ai/terms>, <https://runware.ai/docs/image-inference/introduction>, <https://runware.ai/docs/en/image-inference/introduction>, <https://help.runware.ai/articles/5571280435-is-there-a-way-to-filter-out-nsfw-content>, <https://help.runware.ai/articles/6569725725-are-there-any-restrictions-on-how-i-can-use-runware>, <https://help.runware.ai/articles/2514257143-am-i-responsible-for-the-content-generated-through-my-account>, <https://help.runware.ai/articles/3397550557-how-does-pricing-work>, <https://runware.ai/pricing>, <https://runware.ai/abuse>; Drittquelle zum Safety-Objekt: <https://comfyai.run/documentation/Runware%20Safety%20Inputs>.
