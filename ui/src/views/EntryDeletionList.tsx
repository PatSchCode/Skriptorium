import type { CanonEntry, EntryDeletion, EntryUse } from "../api";
import { incomingOf } from "../relations";

function counted(count: number, one: string, many: string): string {
  return `${count.toString()} ${count === 1 ? one : many}`;
}

/** What goes from one story: led character, facts and, for a guest, the link. */
function traces(use: EntryUse): string {
  const parts: string[] = [];
  if (use.guest) {
    parts.push(
      use.relation ? "Gast-Verbindung mit Weltbezug" : "Gast-Verbindung",
    );
  }
  if (use.led) {
    parts.push("geführte Figur");
  }
  if (use.facts > 0) {
    parts.push(
      `${counted(use.facts, "Fakt", "Fakten")} „nur diese Geschichte“`,
    );
  }
  return parts.join(", ");
}

/**
 * The consequences of deleting a canon entry (step 10.1, ADR-106), as the server counted them:
 * images, markers and the traces in stories of its world and, as a guest, of other worlds. The
 * entries that mention it with `@` are named too; their text stays.
 */
export function EntryDeletionList({
  entry,
  deletion,
  entries,
}: {
  entry: CanonEntry;
  deletion: EntryDeletion;
  entries: readonly CanonEntry[];
}) {
  const own = deletion.uses.filter((use) => !use.guest);
  const guests = deletion.uses.filter((use) => use.guest);
  const incoming = incomingOf(entry, entries);
  const mentioning = [
    ...new Set([
      ...incoming.relations.map((relation) => relation.from.name),
      ...incoming.mentions.map((mention) => mention.name),
    ]),
  ];
  const files: string[] = [];
  if (deletion.images > 0) {
    files.push(counted(deletion.images, "Bild", "Bilder"));
  }
  if (deletion.markers > 0) {
    files.push(
      `${counted(deletion.markers, "Markierung", "Markierungen")} auf Karten`,
    );
  }
  const nothing = files.length === 0 && deletion.uses.length === 0;
  return (
    <>
      {nothing ? (
        <p>
          Keine Bilder, Markierungen oder Verweise in Geschichten – nur der
          Eintrag selbst verschwindet.
        </p>
      ) : (
        <>
          <p>Das verschwindet mit dem Eintrag:</p>
          {files.length > 0 && (
            <ul aria-label="Dateien">
              <li>{files.join(" und ")}</li>
            </ul>
          )}
          {own.length > 0 && (
            <>
              <p className="delete-group">In Geschichten dieser Welt</p>
              <ul aria-label="Geschichten dieser Welt">
                {own.map((use) => (
                  <li key={use.story}>
                    „{use.story_title}“: {traces(use)}
                  </li>
                ))}
              </ul>
            </>
          )}
          {guests.length > 0 && (
            <>
              <p className="delete-group">
                In Geschichten anderer Welten (als Gast)
              </p>
              <ul aria-label="Geschichten anderer Welten">
                {guests.map((use) => (
                  <li key={`${use.world}/${use.story}`}>
                    „{use.story_title}“ ({use.world_name}): {traces(use)}
                  </li>
                ))}
              </ul>
            </>
          )}
        </>
      )}
      {mentioning.length > 0 && (
        <p className="note">
          Bleibt stehen: Erwähnungen mit @ in{" "}
          {mentioning.map((name) => `„${name}“`).join(", ")} – sie bleiben als
          Text und verweisen dann auf nichts mehr.
        </p>
      )}
    </>
  );
}
