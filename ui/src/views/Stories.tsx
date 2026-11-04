import { useCallback, useState, type SyntheticEvent } from "react";
import {
  api,
  describeError,
  FORMS,
  type Form,
  type Story,
  type StoryDeletion,
} from "../api";
import { useNavigation } from "../paths";
import { useLoad } from "../useLoad";
import { ArchiveArea, counted, MoreActions } from "./Archive";
import { ErrorText, Field } from "./Common";
import { DeleteDialog } from "./DeleteDialog";

/**
 * Stories of a world; open one or create a new one. Archived stories stand only in the area
 * "Archiv" below the list, from where they come back or are deleted for good (step 9.9).
 */
export function Stories({
  world,
  onOpen,
}: {
  world: string;
  onOpen: (story: Story) => void;
}) {
  const { revision, refresh } = useNavigation();
  const load = useCallback(() => api.stories(world), [world]);
  const { data, error, reload } = useLoad(load, revision);
  const [title, setTitle] = useState("");
  const [form, setForm] = useState<Form>("roman");
  const [perspective, setPerspective] = useState("");
  const [createError, setCreateError] = useState<string | null>(null);
  const [deleting, setDeleting] = useState<{
    id: string;
    preview: StoryDeletion;
  } | null>(null);
  const [deleteError, setDeleteError] = useState<string | null>(null);
  const active = (data ?? []).filter((story) => !story.archived);
  const archived = (data ?? []).filter((story) => story.archived);

  function changed() {
    reload();
    refresh();
  }

  async function askDelete(id: string) {
    setDeleteError(null);
    try {
      setDeleting({ id, preview: await api.storyDeletion(world, id) });
    } catch (reason: unknown) {
      setDeleteError(describeError(reason));
    }
  }

  async function create(event: SyntheticEvent) {
    event.preventDefault();
    setCreateError(null);
    try {
      const clean = perspective.trim();
      onOpen(
        await api.createStory(world, title, form, clean === "" ? null : clean),
      );
    } catch (reason: unknown) {
      setCreateError(describeError(reason));
    }
  }

  return (
    <div className="stack">
      <section className="card">
        <h2>Geschichten</h2>
        <ErrorText message={error} />
        {data !== undefined && active.length === 0 && (
          <p>Noch keine Geschichte.</p>
        )}
        <ul className="list">
          {active.map((story) => (
            <li key={story.id}>
              <span>
                <button
                  type="button"
                  className="link"
                  onClick={() => {
                    onOpen(story);
                  }}
                >
                  {story.title}
                </button>
                <small>
                  {" "}
                  ({FORMS.find((f) => f.id === story.form)?.label})
                </small>
              </span>
              <MoreActions
                name={story.title}
                onArchive={async () => {
                  await api.archiveStory(world, story.id);
                  changed();
                }}
              />
            </li>
          ))}
        </ul>
        <ArchiveArea
          items={archived.map((story) => ({
            id: story.id,
            label: story.title,
          }))}
          onRestore={async (id) => {
            await api.restoreStory(world, id);
            changed();
          }}
          onDelete={(id) => void askDelete(id)}
        />
        <ErrorText message={deleteError} />
      </section>
      {deleting !== null && (
        <DeleteDialog
          heading={`„${deleting.preview.title}“ endgültig löschen?`}
          name={deleting.preview.title}
          nameLabel="Zum Bestätigen den Titel eintippen"
          onCancel={() => {
            setDeleting(null);
          }}
          onConfirm={async () => {
            await api.deleteStory(world, deleting.id, deleting.preview.title);
            setDeleting(null);
            changed();
          }}
        >
          <StoryConsequences preview={deleting.preview} />
        </DeleteDialog>
      )}
      <form className="card" onSubmit={(event) => void create(event)}>
        <h2>Neue Geschichte</h2>
        <Field label="Titel">
          <input
            value={title}
            onChange={(event) => {
              setTitle(event.target.value);
            }}
            required
          />
        </Field>
        <Field label="Form">
          <select
            value={form}
            onChange={(event) => {
              setForm(event.target.value as Form);
            }}
          >
            {FORMS.map(({ id, label }) => (
              <option key={id} value={id}>
                {label}
              </option>
            ))}
          </select>
        </Field>
        <Field label="Erzählperspektive (optional)">
          <input
            value={perspective}
            onChange={(event) => {
              setPerspective(event.target.value);
            }}
          />
        </Field>
        <ErrorText message={createError} />
        <button type="submit">Geschichte anlegen</button>
      </form>
    </div>
  );
}

/** What deleting a story for good takes with it, as the server counted it. */
function StoryConsequences({ preview }: { preview: StoryDeletion }) {
  const parts = [
    `${counted(preview.chapters, "Kapitel", "Kapitel")} mit Kurzfassungen und Anweisungsverlauf`,
  ];
  if (preview.facts > 0) {
    parts.push(counted(preview.facts, "Fakt", "Fakten"));
  }
  if (preview.cover) {
    parts.push("Titelbild");
  }
  return (
    <>
      <p>Wird gelöscht: {parts.join(", ")}.</p>
      <p className="note">
        Bleibt: die Kosten im Verbrauch (ohne Bezug zur Geschichte).
      </p>
    </>
  );
}
