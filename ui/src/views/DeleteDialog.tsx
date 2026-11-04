import { useEffect, useRef, useState, type ReactNode } from "react";
import { describeError } from "../api";
import { ErrorText } from "./Common";

/**
 * The question before deleting a world or a story for good (step 9.9, ADR-098): what goes with
 * it, what stays, and the name to type. "Endgültig löschen" works only once the typed text is
 * exactly the name; the server checks it again. Escape cancels.
 */
export function DeleteDialog({
  heading,
  name,
  nameLabel,
  children,
  onConfirm,
  onCancel,
}: {
  heading: string;
  /** What the author types to confirm: the name of the world or the title of the story. */
  name: string;
  /** Label of the field, e.g. "Zum Bestätigen den Namen der Welt eintippen". */
  nameLabel: string;
  /** The consequences, as the server counted them. */
  children: ReactNode;
  onConfirm: () => Promise<void>;
  onCancel: () => void;
}) {
  const field = useRef<HTMLInputElement>(null);
  const [typed, setTyped] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    field.current?.focus();
  }, []);

  async function confirm() {
    setBusy(true);
    setError(null);
    try {
      await onConfirm();
    } catch (reason: unknown) {
      setError(describeError(reason));
      setBusy(false);
    }
  }

  return (
    <div
      className="overlay image-viewer-veil"
      onKeyDown={(event) => {
        if (event.key === "Escape") {
          event.stopPropagation();
          onCancel();
        }
      }}
    >
      <div
        className="section-conflict delete-dialog"
        role="dialog"
        aria-modal="true"
        aria-labelledby="delete-dialog-title"
      >
        <h3 id="delete-dialog-title">{heading}</h3>
        {children}
        <p className="note">
          Rückweg nur über die tägliche Sicherung (05:00 Uhr).
        </p>
        <label className="stack tight">
          <span>{nameLabel}:</span>
          <input
            ref={field}
            value={typed}
            placeholder={name}
            autoComplete="off"
            onChange={(event) => {
              setTyped(event.target.value);
            }}
          />
        </label>
        <ErrorText message={error} />
        <div className="row">
          <button type="button" className="ghost" onClick={onCancel}>
            Abbrechen
          </button>
          <button
            type="button"
            className="danger"
            disabled={typed !== name || busy}
            onClick={() => void confirm()}
          >
            Endgültig löschen
          </button>
        </div>
      </div>
    </div>
  );
}
