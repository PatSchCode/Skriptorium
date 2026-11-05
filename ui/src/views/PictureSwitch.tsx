import { api, type CanonEntry, type CatalogModel } from "../api";
import { formatCents, pictureSurcharge, shortName } from "../models";

/** Images per request at most (owner, ADR-111); same value as on the server. */
export const MAX_PICTURES = 4;

/**
 * The named entries whose main image would go along: those with images, in the order they are
 * named, at most four (step 10.7, ADR-111).
 */
export function picturedEntries(named: readonly CanonEntry[]): CanonEntry[] {
  return named
    .filter((entry) => entry.images.length > 0)
    .slice(0, MAX_PICTURES);
}

/**
 * "Bilder mitschicken" under the named entries (step 10.7, ADR-111): small previews of the main
 * images and the estimated extra cost. Shown only when a named entry has an image; locked for a
 * model that does not read images. Whether it is ticked is the caller's state, cleared after
 * every request.
 */
export function PictureSwitch({
  named,
  model,
  modelId,
  checked,
  disabled,
  onChange,
}: {
  named: readonly CanonEntry[];
  model: CatalogModel | undefined;
  modelId: string;
  checked: boolean;
  disabled: boolean;
  onChange: (checked: boolean) => void;
}) {
  const withImage = named.filter((entry) => entry.images.length > 0);
  if (withImage.length === 0) {
    return null;
  }
  const pictured = withImage.slice(0, MAX_PICTURES);
  const reads = model?.reads_images ?? false;
  const count =
    pictured.length === withImage.length
      ? `${String(pictured.length)} ${pictured.length === 1 ? "Bild" : "Bilder"}`
      : `${String(pictured.length)} von ${String(withImage.length)} Bildern`;
  const surcharge = formatCents(pictureSurcharge(model, pictured.length));
  const without = named.filter((entry) => entry.images.length === 0);
  return (
    <p className="note picture-switch">
      <label className="check">
        <input
          type="checkbox"
          checked={checked && reads}
          disabled={disabled || !reads}
          onChange={(event) => {
            onChange(event.target.checked);
          }}
        />
        Bilder mitschicken
      </label>
      {reads ? (
        <>
          <span className="picture-thumbs">
            {pictured.map((entry) => (
              <img
                key={`${entry.world}/${entry.id}`}
                src={api.imagePath(
                  entry.world,
                  entry.id,
                  entry.images[0] ?? "",
                )}
                alt={entry.name}
                title={entry.name}
              />
            ))}
          </span>
          <span>
            {count}
            {surcharge === null ? ", Preis unbekannt" : `, ca. +${surcharge}`}
            {without.length > 0 &&
              ` · ohne Bild: ${without.map((entry) => entry.name).join(", ")}`}
          </span>
        </>
      ) : (
        <span>– {shortName(model, modelId)} kann keine Bilder lesen.</span>
      )}
    </p>
  );
}
