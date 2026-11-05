import { useState } from "react";
import type { CanonEntry } from "../api";
import { PURPOSE, readSection } from "../sections";
import { AppearanceExtract } from "./AppearanceExtract";

/**
 * What an image of an entry without "Aussehen" misses, with a way to add it (step 9.5,
 * ADR-094): "✨ Aussehen herauslösen" right here (ADR-078; places and items since step 10.3,
 * ADR-108), for a place or an item also "✎ Selbst ergänzen" (opens editing).
 */
export function LooksHint({
  entry,
  onEdit,
  onChanged,
}: {
  entry: CanonEntry;
  onEdit?: () => void;
  onChanged: (entry: CanonEntry) => void;
}) {
  const [extracting, setExtracting] = useState(false);
  if (extracting) {
    return (
      <AppearanceExtract
        entry={entry}
        onChanged={(changed) => {
          setExtracting(false);
          onChanged(changed);
        }}
        onClose={() => {
          setExtracting(false);
        }}
      />
    );
  }
  const figure = entry.category === "figur";
  return (
    <p className="row appearance-hint">
      <button
        type="button"
        className="ghost"
        onClick={() => {
          setExtracting(true);
        }}
      >
        ✨ Aussehen herauslösen
      </button>
      {!figure && onEdit !== undefined && (
        <button type="button" className="ghost" onClick={onEdit}>
          ✎ Selbst ergänzen
        </button>
      )}
      <span className="note">
        – {entry.name} hat noch kein „Aussehen“;{" "}
        {figure
          ? "ohne es kennt das Bild nur den Namen"
          : `das Bild nutzt nur ${
              entry.category !== "gegenstand"
                ? "den Anfang des Textes"
                : readSection(entry.body, PURPOSE) === null
                  ? "den ersten Satz des Textes"
                  : "den ersten Satz aus „Zweck“"
            }`}
        .
      </span>
    </p>
  );
}
