import { useEffect, useRef, type ReactNode } from "react";

/** One image large over the page; arrow keys browse, Escape closes. */
export function ImageViewer({
  name,
  images,
  at,
  source,
  editable,
  busy,
  onMove,
  onClose,
  onMain,
  onRemove,
  onDescribe,
  onBuildOn,
  children,
}: {
  name: string;
  images: readonly string[];
  at: number;
  source: (image: string) => string;
  editable: boolean;
  busy: boolean;
  onMove: (at: number) => void;
  onClose: () => void;
  onMain: (image: string) => void;
  onRemove: (image: string) => void;
  onDescribe: (image: string) => void;
  /** Opens "Bild erzeugen" with the image as basis (step 9.8); missing: no button. */
  onBuildOn?: (image: string) => void;
  /** Shown under the bar: the description of the image (step 7.13). */
  children?: ReactNode;
}) {
  const close = useRef<HTMLButtonElement>(null);
  const image = images[at] ?? "";
  const count = images.length;
  const label = `${name}, Bild ${String(at + 1)} von ${String(count)}`;

  useEffect(() => {
    close.current?.focus();
  }, []);

  useEffect(() => {
    function key(event: KeyboardEvent) {
      const target = event.target;
      const typing =
        target instanceof HTMLTextAreaElement ||
        target instanceof HTMLInputElement ||
        target instanceof HTMLSelectElement;
      // Keys in a field (the description) stay in the field.
      if (typing) {
        return;
      }
      if (event.key === "Escape") {
        onClose();
      } else if (event.key === "ArrowLeft" && count > 1) {
        onMove((at - 1 + count) % count);
      } else if (event.key === "ArrowRight" && count > 1) {
        onMove((at + 1) % count);
      }
    }
    window.addEventListener("keydown", key);
    return () => {
      window.removeEventListener("keydown", key);
    };
  }, [at, count, onClose, onMove]);

  return (
    <div
      className="overlay image-viewer-veil"
      onClick={(event) => {
        if (event.target === event.currentTarget) {
          onClose();
        }
      }}
    >
      <div
        className={
          children === undefined || children === false || children === null
            ? "image-viewer"
            : "image-viewer describing"
        }
        role="dialog"
        aria-modal="true"
        aria-label={label}
      >
        <img src={source(image)} alt={label} />
        <div className="image-viewer-bar">
          {count > 1 && (
            <>
              <button
                type="button"
                className="ghost"
                onClick={() => {
                  onMove((at - 1 + count) % count);
                }}
              >
                ‹ voriges
              </button>
              <button
                type="button"
                className="ghost"
                onClick={() => {
                  onMove((at + 1) % count);
                }}
              >
                nächstes ›
              </button>
            </>
          )}
          {editable && (
            <button
              type="button"
              className="ghost"
              disabled={busy}
              onClick={() => {
                onDescribe(image);
              }}
            >
              ✨ Von der KI beschreiben lassen
            </button>
          )}
          {onBuildOn !== undefined && (
            <button
              type="button"
              className="ghost"
              disabled={busy}
              onClick={() => {
                onBuildOn(image);
              }}
            >
              ✨ Als Grundlage für ein neues Bild
            </button>
          )}
          <span className="image-viewer-gap" />
          {editable && at > 0 && (
            <button
              type="button"
              className="ghost"
              disabled={busy}
              onClick={() => {
                onMain(image);
              }}
            >
              Zum Hauptbild machen
            </button>
          )}
          {editable && (
            <button
              type="button"
              className="ghost"
              disabled={busy}
              onClick={() => {
                onRemove(image);
              }}
            >
              Entfernen
            </button>
          )}
          <button ref={close} type="button" className="ghost" onClick={onClose}>
            Schließen
          </button>
        </div>
        {children}
      </div>
    </div>
  );
}
