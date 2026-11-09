# Runware-Liste für die App (Schritt 11.17)

Stand 2026-11-09. Entscheidungen des Eigentümers (Auswahlfragen in der Session zu 11.17): Grundmodell nur Krea 2 Turbo, 26 LoRAs (8 von ihm bestätigte und 18 im Test vom 2026-11-07 stimmige), keine LoRAs von „sarahpeterson“, Probe am Server als Stichprobe. Alle Kennungen am 2026-11-09 bei Runware nachgeschlagen (`modelSearch`, wie die App beim Hinzufügen): vorhanden, Architektur `krea_oss_2_turbo` (Grundmodell), `krea_oss_2` (LoRAs, passen zu Turbo) bzw. `z_image_turbo` (Large Ball Gag). Gewichte und Auslösewörter aus `docs/research/bildanbieter.md`.

**Eingetragen am 2026-11-09** von der KI in einer Mac-Session (Weg nach ADR-125): alle Einträge dieser Tabelle mit Gewicht und Auslösewort, Kennungen unmittelbar vorher erneut nachgeschlagen; die vier Modelle der Startliste stehen mit in der Datei. Die Anleitung unten gilt für künftige Einträge.

## So trägst du ein

1. In der App **Einstellungen** öffnen, Abschnitt **„Bildmodelle bei Runware“**.
2. Unten bei **„Hinzufügen“** die Kennung aus der Tabelle einfügen, **„Prüfen und hinzufügen“** tippen.
3. Beim neuen Eintrag **Gewicht** und **Auslösewort** wie in der Tabelle setzen. Die App übernimmt sonst Runwares Wert – meist Gewicht 1,0 und kein Auslösewort.
4. Nach ein paar Einträgen **„Änderungen speichern“** tippen.

## Grundmodell

| Kennung | Name |
|---|---|
| `krea:krea@2-turbo` | Krea 2 Turbo |

## LoRAs – von dir bestätigt (8)

| # | Kennung | Name | Gewicht | Auslösewort |
|---|---|---|---|---|
| 1 | `skriptorium:2861561@3232520` | German Handcuffs | 0,6 | `clejuso` |
| 2 | `skriptorium:2767766@3119356` | Armbinder | 1,0 | `BDSMArmbinder, arms behind the back in one single black leather armbinder sleeve for both arms, not two separate sleeves, laced, with shoulder straps, centered on the back` (seit 2026-11-09; mit `BDSMArmbinder` allein entsteht kein Armbinder, ADR-125 Nachtrag) |
| 3 | `skriptorium:2767605@3115420` | Bondage & Gags Megapack | 0,8 | – |
| 4 | `skriptorium:999177@2731175` | Large Ball Gag (nur bei Z-Image-Turbo) | 0,6 | `gagged with a ball gag` |
| 5 | `skriptorium:2742699@3142259` | Rope Bondage | 0,6 | – |
| 6 | `skriptorium:2728181@3066750` | Metal Bondage | 0,6 | – |
| 7 | `skriptorium:2351806@3096239` | Tape Bondage | 0,6 | – |
| 8 | `skriptorium:2964163@3386627` | Plastic Zip-Cuffs | 0,6 | `pla5ticz1pcuff5` |

## LoRAs – im Test stimmig (18)

| # | Kennung | Name | Gewicht | Auslösewort |
|---|---|---|---|---|
| 9 | `skriptorium:2727310@3096554` | Ball Gags | 0,6 | `ball gag` |
| 10 | `skriptorium:2771325@3120207` | Leather Cuffs | 0,6 | – |
| 11 | `skriptorium:2729799@3068740` | Hogtied | 0,6 | `hogtied` |
| 12 | `skriptorium:2736971@3077605` | Harness Gag | 0,6 | `ball gag with head harness` |
| 13 | `skriptorium:2745959@3088665` | Yoke | 1,0 | – |
| 14 | `skriptorium:2750440@3094170` | Metalstocks | 0,6 | – |
| 15 | `skriptorium:2737161@3077841` | Bolero Straitjacket | 0,6 | `bolero straitjacket` |
| 16 | `skriptorium:2729323@3068160` | Shiny Latex Bodysuits | 0,6 | `latex bodysuit` |
| 17 | `skriptorium:2780723@3131719` | Spider Gag | 0,6 | `metal gag` |
| 18 | `skriptorium:2750568@3094331` | Panel Gag | 1,0 | – |
| 19 | `skriptorium:2743032@3085106` | Getting Gagged | 1,0 | `putting a ball gag in their mouth` |
| 20 | `skriptorium:2735794@3076147` | Nipple Clamps | 0,6 | `nipple clamps` |
| 21 | `skriptorium:2741407@3127168` | Female Chastity Harness | 1,0 | – |
| 22 | `skriptorium:2734524@3074651` | Ballet Ankle Heels | 0,6 | `ankle boots with extremely high heels` |
| 23 | `skriptorium:2780496@3131454` | Gimp (am besten mit Latex Bodysuits 0,5) | 0,6 | – |
| 24 | `skriptorium:2728644@3116175` | Mystic XXX (Fotowirkung) | 0,6 | – |
| 25 | `skriptorium:2935877@3323262` | Lingerie Construction | 0,8 | `lngcon` |
| 26 | `skriptorium:2815591@3222067` | Cinzia Lingerie | 0,8 | `C1nz14L1ng` |

Gewicht bei Runware schon richtig: Leather Cuffs (0,6), Mystic XXX (0,6), Lingerie Construction und Cinzia (0,8); bei Armbinder, Yoke, Panel Gag, Getting Gagged und Female Chastity Harness bleibt 1,0. Bei den übrigen 17 von 1,0 auf den Wert der Tabelle ändern.

## Nicht aufgenommen

- Von „sarahpeterson“ (aussortiert 2026-11-07), u. a. `skriptorium:1756180@2568521` (cuffed behind back).
- Im Test schwach oder nicht überzeugend: Spreader Gag, Sidesuspension, Touch, Lip Biting, Bowing Down, Laced Lingerie, Waist slider, Hands (Z-Image-Turbo); Kneeling Hands on Thighs wird bei Runware nicht verarbeitet.
- Grundmodell Krea 2 Raw (im Test fleckig und zu jung wirkend, Einstellungen unerprobt).

## Stichprobe am Server (nach dem Eintragen)

Im Dialog „Bild erzeugen“ mit dem Testavatar: Krea 2 Turbo ohne LoRA, dann je eine Fessel (Leather Cuffs), ein Knebel (Harness Gag) und eine Kleidung (Shiny Latex Bodysuits). Kosten zusammen rund 0,02 $.
