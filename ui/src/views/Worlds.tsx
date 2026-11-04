import { useCallback, useState, type SyntheticEvent } from "react";
import { api, describeError, type World, type WorldDeletion } from "../api";
import { useNavigation } from "../paths";
import { useLoad } from "../useLoad";
import { ArchiveArea, counted, MoreActions } from "./Archive";
import { ErrorText, Field } from "./Common";
import { DeleteDialog } from "./DeleteDialog";

/**
 * List of worlds; choose one or create a new one. Archived worlds stand only in the area
 * "Archiv" below the list, from where they come back or are deleted for good (step 9.9).
 */
export function Worlds({ onOpen }: { onOpen: (world: World) => void }) {
  const { revision, refresh } = useNavigation();
  const load = useCallback(() => api.worlds(), []);
  const { data, error, reload } = useLoad(load, revision);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [createError, setCreateError] = useState<string | null>(null);
  const [deleting, setDeleting] = useState<{
    id: string;
    preview: WorldDeletion;
  } | null>(null);
  const [deleteError, setDeleteError] = useState<string | null>(null);
  const active = (data ?? []).filter((world) => !world.archived);
  const archived = (data ?? []).filter((world) => world.archived);

  function changed() {
    reload();
    refresh();
  }

  async function askDelete(id: string) {
    setDeleteError(null);
    try {
      setDeleting({ id, preview: await api.worldDeletion(id) });
    } catch (reason: unknown) {
      setDeleteError(describeError(reason));
    }
  }

  async function create(event: SyntheticEvent) {
    event.preventDefault();
    setCreateError(null);
    try {
      onOpen(await api.createWorld(name, description));
    } catch (reason: unknown) {
      setCreateError(describeError(reason));
    }
  }

  return (
    <div className="stack">
      <section className="card">
        <h2>Welten</h2>
        <ErrorText message={error} />
        {data !== undefined && active.length === 0 && (
          <p>Noch keine Welt angelegt.</p>
        )}
        <ul className="list">
          {active.map((world) => (
            <li key={world.id}>
              <button
                type="button"
                className="link"
                onClick={() => {
                  onOpen(world);
                }}
              >
                {world.name}
              </button>
              <MoreActions
                name={world.name}
                onArchive={async () => {
                  await api.archiveWorld(world.id);
                  changed();
                }}
              />
            </li>
          ))}
        </ul>
        <ArchiveArea
          items={archived.map((world) => ({ id: world.id, label: world.name }))}
          onRestore={async (id) => {
            await api.restoreWorld(id);
            changed();
          }}
          onDelete={(id) => void askDelete(id)}
        />
        <ErrorText message={deleteError} />
      </section>
      {deleting !== null && (
        <DeleteDialog
          heading={`Welt „${deleting.preview.name}“ endgültig löschen?`}
          name={deleting.preview.name}
          nameLabel="Zum Bestätigen den Namen der Welt eintippen"
          onCancel={() => {
            setDeleting(null);
          }}
          onConfirm={async () => {
            await api.deleteWorld(deleting.id, deleting.preview.name);
            setDeleting(null);
            changed();
          }}
        >
          <WorldConsequences preview={deleting.preview} />
        </DeleteDialog>
      )}
      <form className="card" onSubmit={(event) => void create(event)}>
        <h2>Neue Welt</h2>
        <Field label="Name">
          <input
            value={name}
            onChange={(event) => {
              setName(event.target.value);
            }}
            required
          />
        </Field>
        <Field label="Beschreibung und Grundregeln">
          <textarea
            rows={4}
            value={description}
            onChange={(event) => {
              setDescription(event.target.value);
            }}
          />
        </Field>
        <ErrorText message={createError} />
        <button type="submit">Welt anlegen</button>
      </form>
    </div>
  );
}

/** What deleting a world for good takes with it, as the server counted it. */
function WorldConsequences({ preview }: { preview: WorldDeletion }) {
  return (
    <>
      <p>
        Mit ihr:{" "}
        {[
          counted(preview.entries, "Kanon-Eintrag", "Kanon-Einträge"),
          counted(preview.maps, "Karte", "Karten"),
          counted(preview.images, "Bild", "Bilder"),
          counted(preview.stories, "Geschichte", "Geschichten"),
        ].join(", ")}
        .
      </p>
      {preview.guest_uses.length > 0 && (
        <>
          <p>Auch betroffen:</p>
          <ul>
            {preview.guest_uses.map((use) => (
              <li key={`${use.world}/${use.story}`}>
                {counted(
                  use.guests.length,
                  "Gast-Verbindung",
                  "Gast-Verbindungen",
                )}{" "}
                in „{use.story_title}“ (Welt „{use.world_name}“:{" "}
                {use.guests.join(", ")}) – werden dort
                {use.facts > 0
                  ? ` samt ${counted(use.facts, "Fakt", "Fakten")}`
                  : ""}{" "}
                entfernt.
              </li>
            ))}
          </ul>
        </>
      )}
      <p className="note">
        Bleibt: die Kosten im Verbrauch (ohne Bezug zur Welt).
      </p>
    </>
  );
}
