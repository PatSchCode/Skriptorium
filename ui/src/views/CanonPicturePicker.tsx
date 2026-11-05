import { useEffect, useState } from "react";
import {
  api,
  describeError,
  type CanonEntry,
  type StoredImageOrigin,
} from "../api";
import { ErrorText } from "./Common";

/**
 * "Aus dem Kanon …" (step 10.6, ADR-110): an entry of the world with images, one of its images
 * and a caption (preset: the entry's name). "Einfügen" loads the image and hands it to `onPick`
 * with its origin, which stores a copy with the story.
 */
export function CanonPicturePicker({
  world,
  onPick,
  onClose,
}: {
  world: string;
  onPick: (
    image: Blob,
    caption: string,
    origin: StoredImageOrigin | null,
  ) => Promise<void>;
  onClose: () => void;
}) {
  const [entries, setEntries] = useState<CanonEntry[] | null>(null);
  const [entryId, setEntryId] = useState("");
  const [image, setImage] = useState<string | null>(null);
  const [caption, setCaption] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let current = true;
    api
      .entries(world)
      .then((found) => {
        if (current) {
          const pictured = found.filter((entry) => entry.images.length > 0);
          setEntries(pictured);
          const first = pictured[0];
          if (first !== undefined) {
            setEntryId(first.id);
            setImage(first.images[0] ?? null);
            setCaption(first.name);
          }
        }
      })
      .catch((reason: unknown) => {
        if (current) {
          setError(describeError(reason));
          setEntries([]);
        }
      });
    return () => {
      current = false;
    };
  }, [world]);

  const entry = entries?.find((one) => one.id === entryId);

  async function insert() {
    if (entry === undefined || image === null) {
      return;
    }
    setBusy(true);
    setError(null);
    try {
      const path = api.imagePath(world, entry.id, image);
      const response = await fetch(path);
      if (!response.ok) {
        setError("Das Bild des Eintrags ließ sich nicht laden.");
        setBusy(false);
        return;
      }
      const origin = await api.imageOrigin(world, entry.id, image);
      await onPick(await response.blob(), caption, origin);
      onClose();
    } catch (reason: unknown) {
      setError(describeError(reason));
      setBusy(false);
    }
  }

  return (
    <div className="canon-picture" role="group" aria-label="Bild aus dem Kanon">
      <h3>Bild aus dem Kanon</h3>
      {entries !== null && entries.length === 0 && error === null && (
        <p className="note">In dieser Welt hat noch kein Eintrag ein Bild.</p>
      )}
      {entries !== null && entries.length > 0 && (
        <>
          <label className="image-generate-field">
            Eintrag
            <select
              value={entryId}
              disabled={busy}
              onChange={(event) => {
                const chosen = entries.find(
                  (one) => one.id === event.target.value,
                );
                setEntryId(event.target.value);
                setImage(chosen?.images[0] ?? null);
                setCaption(chosen?.name ?? "");
              }}
            >
              {entries.map((one) => (
                <option key={one.id} value={one.id}>
                  {one.name}
                </option>
              ))}
            </select>
          </label>
          {entry !== undefined && (
            <div
              className="entry-image-thumbs"
              role="radiogroup"
              aria-label="Bild"
            >
              {entry.images.map((one, at) => (
                <button
                  key={one}
                  type="button"
                  role="radio"
                  aria-checked={image === one}
                  aria-label={`Bild ${String(at + 1)} von ${entry.name}`}
                  className={image === one ? "chosen" : undefined}
                  disabled={busy}
                  onClick={() => {
                    setImage(one);
                  }}
                >
                  <img src={api.imagePath(world, entry.id, one)} alt="" />
                </button>
              ))}
            </div>
          )}
          <label className="image-generate-field">
            Beschriftung
            <input
              value={caption}
              maxLength={200}
              disabled={busy}
              onChange={(event) => {
                setCaption(event.target.value);
              }}
            />
          </label>
          <p className="note">
            Das Bild wird in die Geschichte kopiert; es bleibt, auch wenn du es
            am Eintrag löschst.
          </p>
        </>
      )}
      <ErrorText message={error} />
      <div className="row">
        <button
          type="button"
          className="primary"
          disabled={busy || entry === undefined || image === null}
          onClick={() => void insert()}
        >
          Einfügen
        </button>
        <button
          type="button"
          className="ghost"
          disabled={busy}
          onClick={onClose}
        >
          Abbrechen
        </button>
      </div>
    </div>
  );
}
