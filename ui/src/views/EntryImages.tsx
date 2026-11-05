import { useRef, useState, type ChangeEvent } from "react";
import { api, describeError, type CanonEntry } from "../api";
import { base64, shrinkImage } from "../files";
import { ErrorText } from "./Common";
import { entryPrompt, lacksAppearance } from "../imagePrompts";
import { APPEARANCE } from "../sections";
import { ImageDescription } from "./ImageDescription";
import { ImageGenerate } from "./ImageGenerate";
import {
  ImageOriginPanel,
  seedOf,
  type GenerateSeed,
} from "./ImageOriginPanel";
import { ImageViewer } from "./ImageViewer";
import { LooksHint } from "./LooksHint";
import { SectionConflict } from "./SectionConflict";
import { useSectionChoice } from "./useSectionChoice";

/** As many images as the server keeps per entry (`MAX_IMAGES_PER_ENTRY`). */
const MAX_IMAGES = 12;

/**
 * The images of a canon entry (step 7.6, ADR-072): the first is the main image, large above the
 * text; the others follow as small previews, "＋" adds one. A tap shows an image large, with
 * browsing, "Zum Hauptbild machen", "Entfernen" and "Von der KI beschreiben lassen" (step 7.13);
 * a generated image shows its origin there (step 9.6, ADR-095).
 * Without `editable` (guests, the compact bar) the images are only shown.
 */
export function EntryImages({
  entry,
  editable,
  onChanged,
  onEdit,
}: {
  entry: CanonEntry;
  editable: boolean;
  onChanged: (entry: CanonEntry) => void;
  /** Opens the entry for editing, offered when an image lacks the looks (step 9.5, ADR-094). */
  onEdit?: () => void;
}) {
  const [shown, setShown] = useState<number | null>(null);
  const [generating, setGenerating] = useState(false);
  // Set when an image is generated anew from another (origin or basis, steps 9.6 and 9.8).
  const [seed, setSeed] = useState<GenerateSeed | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { place, asking } = useSectionChoice();
  const images = entry.images;
  const source = (image: string) => api.imagePath(entry.world, entry.id, image);
  const canAdd = editable && images.length < MAX_IMAGES;

  if (images.length === 0 && !editable) {
    return null;
  }

  async function change(work: () => Promise<CanonEntry>) {
    setBusy(true);
    setError(null);
    try {
      onChanged(await work());
      return true;
    } catch (reason: unknown) {
      setError(describeError(reason));
      return false;
    } finally {
      setBusy(false);
    }
  }

  function generateFrom(from: GenerateSeed) {
    setSeed(from);
    setGenerating(true);
    setShown(null);
  }

  return (
    <div className="entry-images">
      <EntryImageStrip
        entry={entry}
        source={source}
        editable={editable}
        canAdd={canAdd}
        busy={busy}
        onShow={setShown}
        onUpload={(file) =>
          void change(async () =>
            api.addImage(
              entry.world,
              entry.id,
              await base64(await shrinkImage(file)),
            ),
          )
        }
        onGenerate={() => {
          setGenerating(true);
        }}
      />
      <ErrorText message={error} />
      {generating && (
        <ImageGenerate
          target={{ world: entry.world }}
          title={
            seed?.basis === undefined
              ? `Bild erzeugen – ${entry.name}`
              : `Neues Bild aus ${seed.basis.label}`
          }
          initialPrompt={seed?.prompt ?? entryPrompt(entry)}
          hint={
            seed === null && lacksAppearance(entry) ? (
              <LooksHint entry={entry} onEdit={onEdit} onChanged={onChanged} />
            ) : null
          }
          initialFormat={seed?.format ?? defaultFormat(entry)}
          initialModel={seed?.model ?? null}
          basis={seed?.basis ?? null}
          onTakeOver={async (image, origin) => {
            onChanged(
              await api.addImage(
                entry.world,
                entry.id,
                await base64(await shrinkImage(image)),
                origin,
              ),
            );
          }}
          onClose={() => {
            setGenerating(false);
            setSeed(null);
          }}
        />
      )}
      {shown !== null && images[shown] !== undefined && (
        <EntryImageView
          entry={entry}
          at={shown}
          image={images[shown]}
          source={source}
          editable={editable}
          canAdd={canAdd}
          busy={busy}
          place={place}
          onMove={setShown}
          onClose={() => {
            setShown(null);
          }}
          onGenerate={generateFrom}
          onChanged={onChanged}
          onMain={(image) =>
            change(() => api.setMainImage(entry.world, entry.id, image)).then(
              (done) => {
                if (done) {
                  setShown(0);
                }
                return done;
              },
            )
          }
          onRemove={(image) =>
            change(() => api.removeImage(entry.world, entry.id, image)).then(
              (done) => {
                if (done) {
                  setShown(images.length > 1 ? Math.max(0, shown - 1) : null);
                }
                return done;
              },
            )
          }
        />
      )}
      <SectionConflict asking={asking} />
    </div>
  );
}

/** Portrait for figures, landscape for everything else. */
function defaultFormat(entry: CanonEntry): "2:3" | "3:2" {
  return entry.category === "figur" ? "2:3" : "3:2";
}

/** The main image, the previews and "＋" with its choice: upload or generate (step 9.5). */
function EntryImageStrip({
  entry,
  source,
  editable,
  canAdd,
  busy,
  onShow,
  onUpload,
  onGenerate,
}: {
  entry: CanonEntry;
  source: (image: string) => string;
  editable: boolean;
  canAdd: boolean;
  busy: boolean;
  onShow: (at: number) => void;
  onUpload: (file: File) => void;
  onGenerate: () => void;
}) {
  const [choosing, setChoosing] = useState(false);
  const picker = useRef<HTMLInputElement>(null);
  const images = entry.images;

  function add(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    event.target.value = "";
    if (file !== undefined) {
      onUpload(file);
    }
  }

  return (
    <>
      {images[0] !== undefined && (
        <button
          type="button"
          className="entry-image-main"
          onClick={() => {
            onShow(0);
          }}
        >
          <img src={source(images[0])} alt={`${entry.name}, Hauptbild`} />
        </button>
      )}
      {(images.length > 1 || editable) && (
        <div className="entry-image-thumbs">
          {images.map((image, at) => (
            <button
              key={image}
              type="button"
              className={at === 0 ? "chosen" : undefined}
              aria-label={`Bild ${String(at + 1)} groß zeigen`}
              onClick={() => {
                onShow(at);
              }}
            >
              <img src={source(image)} alt="" />
            </button>
          ))}
          {canAdd && (
            <button
              type="button"
              className="entry-image-add"
              aria-label="Bild hinzufügen"
              title="Bild hinzufügen"
              aria-expanded={choosing}
              disabled={busy}
              onClick={() => {
                setChoosing((open) => !open);
              }}
            >
              ＋
            </button>
          )}
          {choosing && (
            <div className="add-choice" role="menu">
              <button
                type="button"
                role="menuitem"
                onClick={() => {
                  setChoosing(false);
                  picker.current?.click();
                }}
              >
                Bild hochladen
              </button>
              <button
                type="button"
                role="menuitem"
                onClick={() => {
                  setChoosing(false);
                  onGenerate();
                }}
              >
                ✨ Bild erzeugen
              </button>
            </div>
          )}
        </div>
      )}
      {editable && (
        <input
          ref={picker}
          type="file"
          accept="image/*"
          hidden
          onChange={add}
        />
      )}
      <p className="note entry-image-note">
        {busy
          ? "Bild wird verkleinert und gespeichert …"
          : images.length === 0
            ? "Noch kein Bild – „＋“ fügt eins hinzu"
            : `${String(images.length)} ${images.length === 1 ? "Bild" : "Bilder"} · Tipp auf ein Bild zeigt es groß`}
      </p>
    </>
  );
}

/**
 * One image of the entry large (`ImageViewer`) with its origin (step 9.6) and, on request, its
 * description by the AI taken over as "Aussehen" (step 7.13); "Als Grundlage" and "Neu erzeugen"
 * open "Bild erzeugen" with a seed (steps 9.6 and 9.8). `onMain` and `onRemove` resolve to
 * whether the change went through.
 */
function EntryImageView({
  entry,
  at,
  image: shownImage,
  source,
  editable,
  canAdd,
  busy,
  place,
  onMove,
  onClose,
  onGenerate,
  onChanged,
  onMain,
  onRemove,
}: {
  entry: CanonEntry;
  at: number;
  /** The image at `at`. */
  image: string;
  source: (image: string) => string;
  editable: boolean;
  canAdd: boolean;
  busy: boolean;
  place: ReturnType<typeof useSectionChoice>["place"];
  onMove: (at: number) => void;
  onClose: () => void;
  onGenerate: (seed: GenerateSeed) => void;
  onChanged: (entry: CanonEntry) => void;
  onMain: (image: string) => Promise<boolean>;
  onRemove: (image: string) => Promise<boolean>;
}) {
  const [describing, setDescribing] = useState<string | null>(null);
  const images = entry.images;

  return (
    <ImageViewer
      name={entry.name}
      images={images}
      at={at}
      source={source}
      editable={editable}
      busy={busy}
      onMove={(to) => {
        onMove(to);
        setDescribing(null);
      }}
      onClose={onClose}
      onDescribe={setDescribing}
      onBuildOn={
        canAdd
          ? (image) => {
              onGenerate({
                prompt: "",
                format: defaultFormat(entry),
                model: null,
                basis: {
                  reference: { world: entry.world, entry: entry.id, image },
                  label: `Bild ${String(images.indexOf(image) + 1)} von ${entry.name}`,
                  src: source(image),
                },
              });
            }
          : undefined
      }
      onMain={(image) => void onMain(image)}
      onRemove={(image) => {
        if (!window.confirm("Dieses Bild wirklich entfernen?")) {
          return;
        }
        void onRemove(image).then((done) => {
          if (done) {
            setDescribing(null);
          }
        });
      }}
    >
      <ImageOriginPanel
        key={shownImage}
        load={() => api.imageOrigin(entry.world, entry.id, shownImage)}
        onRegenerate={
          canAdd
            ? (origin) => {
                onGenerate(seedOf(origin, defaultFormat(entry)));
              }
            : undefined
        }
      />
      {describing !== null && (
        <ImageDescription
          key={describing}
          title={`Aussehen von ${entry.name}`}
          path={api.describeImagePath(entry.world, entry.id, describing)}
          takeOverLabel="Übernehmen als „Aussehen“"
          onTakeOver={async (text) => {
            // The current text, in case it changed elsewhere meanwhile.
            const fresh = await api.entry(entry.world, entry.id);
            const body = await place(fresh.body, APPEARANCE, text);
            if (body === null) {
              return false;
            }
            onChanged(await api.updateEntry(entry.world, entry.id, { body }));
            return true;
          }}
          onClose={() => {
            setDescribing(null);
          }}
        />
      )}
    </ImageViewer>
  );
}
