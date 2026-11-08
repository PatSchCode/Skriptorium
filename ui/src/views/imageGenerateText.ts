import {
  formatCost,
  type AspectRatio,
  type GeneratedImage,
  type ImagePrice,
} from "../api";

/** The formats "Bild erzeugen" offers (step 7.12). */
export const FORMATS: readonly { id: AspectRatio; label: string }[] = [
  { id: "2:3", label: "Hochformat" },
  { id: "1:1", label: "Quadrat" },
  { id: "3:2", label: "Quer" },
];

/** Names of the quality levels the catalog uses; others are shown as they come. */
export const QUALITIES: Readonly<Record<string, string>> = {
  auto: "automatisch",
  low: "niedrig",
  medium: "mittel",
  high: "hoch",
  xhigh: "sehr hoch",
  max: "höchste",
};

/** The price shown before generating, at the chosen `resolution` if any (step 10.5). */
export function describePrice(
  price: ImagePrice | null,
  resolution: string | null = null,
): string {
  if (price === null) {
    return "Preis wird geladen …";
  }
  if (price.cost_usd === null || price.unit === null) {
    return resolution === null
      ? "Preis unbekannt"
      : `Preis für ${resolution} nicht ausgewiesen – die Kosten stehen nach dem Erzeugen da`;
  }
  if (price.unit === "image") {
    return `ca. ${formatCost(price.cost_usd)} je Bild${resolution === null ? "" : ` (${resolution})`}`;
  }
  if (price.unit === "megapixel") {
    return `ca. ${formatCost(price.cost_usd)} je Bild (1 Megapixel)`;
  }
  return "Abrechnung nach Verbrauch – die Kosten stehen nach dem Erzeugen da";
}

/** The server keeps at most this many characters of the basis's description (ADR-097). */
const MAX_BASIS_LABEL = 200;

/**
 * The description of the basis as the origin keeps it: a long entry name is cut with "…", so
 * taking over a paid image never fails on its length.
 */
export function shortLabel(label: string): string {
  return label.length <= MAX_BASIS_LABEL
    ? label
    : `${label.slice(0, MAX_BASIS_LABEL - 1)}…`;
}

/** What the basis costs, shown after the price of the new image (step 9.8). */
export function describeBasisPrice(price: ImagePrice): string {
  const cost = price.input_cost_usd ?? null;
  if (cost === null || price.input_unit == null) {
    return "Grundlage: Preis vom Anbieter nicht ausgewiesen";
  }
  if (cost === 0) {
    return "Grundlage ohne Aufpreis";
  }
  if (price.input_unit === "image") {
    return `Grundlage ${formatCost(cost)}`;
  }
  if (price.input_unit === "megapixel") {
    return `Grundlage ${formatCost(cost)} je Megapixel`;
  }
  return "Grundlage nach Verbrauch";
}

/** The offered format closest to the proportions `ratio` (width / height) of an image. */
export function nearestFormat(ratio: number): AspectRatio {
  const distance = (id: AspectRatio) => {
    const [width = 1, height = 1] = id.split(":").map(Number);
    return Math.abs(Math.log(ratio / (width / height)));
  };
  return FORMATS.map((entry) => entry.id).reduce((best, id) =>
    distance(id) < distance(best) ? id : best,
  );
}

/** The generated image as a file for the caller's upload. */
export function blobOf(image: GeneratedImage): Blob {
  const binary = atob(image.content);
  const bytes = new Uint8Array(binary.length);
  for (let at = 0; at < binary.length; at++) {
    bytes[at] = binary.charCodeAt(at);
  }
  return new Blob([bytes], { type: image.media_type });
}
