import { useRef, useState, type ChangeEvent } from "react";
import {
  api,
  describeError,
  type AspectRatio,
  type ImageOrigin,
  type StoredImageOrigin,
} from "../api";
import { base64, GENERATED_SIDE, IMAGE_SIDE, shrinkImage } from "../files";
import { pictureLine } from "../pictures";
import { CanonPicturePicker } from "./CanonPicturePicker";
import { ErrorText } from "./Common";
import { ImageGenerate } from "./ImageGenerate";

const FORMATS: readonly string[] = ["2:3", "1:1", "3:2"];

/** The stored origin of a canon image as the origin of its copy; `null` without one. */
function originOf(found: StoredImageOrigin | null): ImageOrigin | null {
  if (found === null || !FORMATS.includes(found.aspect_ratio)) {
    return null;
  }
  return {
    model: found.model,
    prompt: found.prompt,
    aspect_ratio: found.aspect_ratio as AspectRatio,
    cost_usd: found.cost_usd,
    ...(found.basis === null ? {} : { basis: found.basis }),
    ...(found.resolution == null ? {} : { resolution: found.resolution }),
    ...(found.quality == null ? {} : { quality: found.quality }),
  };
}

/** Store a picture with the story as JPEG – every e-book reader shows it (ADR-075). */
async function storePicture(
  world: string,
  story: string,
  image: Blob,
  side: number,
  caption: string,
  origin: ImageOrigin | null,
): Promise<string> {
  const content = await base64(await shrinkImage(image, side, true));
  const { file } = await api.addStoryPicture(world, story, content, origin);
  return pictureLine(caption, file);
}

/** The ways of "＋ Bild" that open a dialog. */
export type PictureWay = "erzeugen" | "kanon";

/**
 * "＋ Bild" in the tools of a chapter (step 10.6, ADR-110): "Bild hochladen" stores the chosen
 * file right away; "✨ Bild erzeugen" and "Aus dem Kanon …" ask `onWay` to open their dialog
 * (`StoryPictureDialog`). `onInsert` receives the line of a stored picture.
 */
export function StoryPictureButton({
  world,
  story,
  onWay,
  onInsert,
}: {
  world: string;
  story: string;
  onWay: (way: PictureWay) => void;
  onInsert: (line: string) => void;
}) {
  const [choosing, setChoosing] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const picker = useRef<HTMLInputElement>(null);

  async function upload(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    event.target.value = "";
    if (file === undefined) {
      return;
    }
    setBusy(true);
    setError(null);
    try {
      onInsert(await storePicture(world, story, file, IMAGE_SIDE, "", null));
    } catch (reason: unknown) {
      setError(describeError(reason));
    } finally {
      setBusy(false);
    }
  }

  return (
    <span className="story-picture">
      <button
        type="button"
        className="ghost"
        aria-expanded={choosing}
        disabled={busy}
        onClick={() => {
          setChoosing((open) => !open);
        }}
      >
        ＋ Bild
      </button>
      {choosing && (
        <span className="add-choice" role="menu">
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
              onWay("erzeugen");
            }}
          >
            ✨ Bild erzeugen
          </button>
          <button
            type="button"
            role="menuitem"
            onClick={() => {
              setChoosing(false);
              onWay("kanon");
            }}
          >
            Aus dem Kanon …
          </button>
        </span>
      )}
      <input
        ref={picker}
        type="file"
        accept="image/*"
        hidden
        aria-label="Bild für das Kapitel"
        onChange={(event) => void upload(event)}
      />
      {busy && <span className="note">Bild wird gespeichert …</span>}
      <ErrorText message={error} />
    </span>
  );
}

/**
 * The dialog of "＋ Bild" (step 10.6, ADR-110): "Bild erzeugen" with the marked passage as the
 * starting text, or the choice from the canon; a picture taken over is stored with the story
 * up to 4,096 pixels (ADR-109) and its line goes to `onInsert`.
 */
export function StoryPictureDialog({
  world,
  story,
  way,
  marked,
  onInsert,
  onClose,
}: {
  world: string;
  story: string;
  way: PictureWay;
  /** The marked passage of the chapter, the starting text for generating. */
  marked: string;
  onInsert: (line: string) => void;
  onClose: () => void;
}) {
  return way === "erzeugen" ? (
    <ImageGenerate
      target={{ world, story }}
      title="Bild für das Kapitel"
      initialPrompt={marked.trim()}
      initialFormat="3:2"
      takeOverLabel="Ins Kapitel einfügen"
      onTakeOver={async (image, origin) => {
        onInsert(
          await storePicture(world, story, image, GENERATED_SIDE, "", origin),
        );
      }}
      onClose={onClose}
    />
  ) : (
    <CanonPicturePicker
      world={world}
      onPick={async (image, caption, origin) => {
        onInsert(
          await storePicture(
            world,
            story,
            image,
            GENERATED_SIDE,
            caption,
            originOf(origin),
          ),
        );
      }}
      onClose={onClose}
    />
  );
}
