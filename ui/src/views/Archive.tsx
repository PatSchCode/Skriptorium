import { useState } from "react";
import { describeError } from "../api";
import { ErrorText } from "./Common";

/** One archived world or story in the area "Archiv". */
export interface ArchivedItem {
  id: string;
  label: string;
}

/** "1 Kapitel", "3 Kanon-Einträge". */
export function counted(count: number, one: string, many: string): string {
  return `${String(count)} ${count === 1 ? one : many}`;
}

/**
 * The folded area "Archiv" under a list (step 9.9, ADR-098): archived worlds or stories, each
 * with "Zurückholen" and "Endgültig löschen …". Nothing is shown while the archive is empty.
 */
export function ArchiveArea({
  items,
  onRestore,
  onDelete,
}: {
  items: ArchivedItem[];
  onRestore: (id: string) => Promise<void>;
  /** Opens the question before deleting for good. */
  onDelete: (id: string) => void;
}) {
  const [error, setError] = useState<string | null>(null);
  if (items.length === 0) {
    return null;
  }

  async function restore(id: string) {
    setError(null);
    try {
      await onRestore(id);
    } catch (reason: unknown) {
      setError(describeError(reason));
    }
  }

  return (
    <details className="archive">
      <summary>Archiv ({items.length})</summary>
      <ul className="list">
        {items.map((item) => (
          <li key={item.id}>
            <span className="note">{item.label}</span>
            <span className="row">
              <button
                type="button"
                className="ghost"
                onClick={() => void restore(item.id)}
              >
                Zurückholen
              </button>
              <button
                type="button"
                className="danger"
                onClick={() => {
                  onDelete(item.id);
                }}
              >
                Endgültig löschen …
              </button>
            </span>
          </li>
        ))}
      </ul>
      <ErrorText message={error} />
    </details>
  );
}

/**
 * The "⋯" next to a world or story in a list, with "Archivieren" (step 9.9, ADR-098). Archiving
 * changes nothing but the mark; the item then stands in the area "Archiv".
 */
export function MoreActions({
  name,
  onArchive,
}: {
  name: string;
  onArchive: () => Promise<void>;
}) {
  const [error, setError] = useState<string | null>(null);

  async function archive() {
    setError(null);
    try {
      await onArchive();
    } catch (reason: unknown) {
      setError(describeError(reason));
    }
  }

  return (
    <details className="more-actions">
      <summary aria-label={`Weitere Aktionen für ${name}`}>⋯</summary>
      <button type="button" className="ghost" onClick={() => void archive()}>
        Archivieren
      </button>
      <ErrorText message={error} />
    </details>
  );
}
