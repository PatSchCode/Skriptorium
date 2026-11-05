import {
  RangeSetBuilder,
  StateField,
  type EditorState,
} from "@codemirror/state";
import {
  Decoration,
  EditorView,
  WidgetType,
  type DecorationSet,
} from "@codemirror/view";
import { pictureOf } from "../pictures";

/** A small preview of a picture below its line (step 10.6, ADR-110). */
class PictureWidget extends WidgetType {
  constructor(
    readonly src: string,
    readonly caption: string,
  ) {
    super();
  }

  override eq(other: PictureWidget): boolean {
    return other.src === this.src && other.caption === this.caption;
  }

  toDOM(): HTMLElement {
    const image = document.createElement("img");
    image.className = "manuscript-picture";
    image.src = this.src;
    image.alt = this.caption;
    image.loading = "lazy";
    return image;
  }
}

function previews(
  state: EditorState,
  source: (file: string) => string,
): DecorationSet {
  const builder = new RangeSetBuilder<Decoration>();
  for (let number = 1; number <= state.doc.lines; number++) {
    const line = state.doc.line(number);
    const picture = line.text.includes("](bild:") ? pictureOf(line.text) : null;
    if (picture !== null) {
      builder.add(
        line.to,
        line.to,
        Decoration.widget({
          widget: new PictureWidget(source(picture.file), picture.caption),
          side: 1,
          block: true,
        }),
      );
    }
  }
  return builder.finish();
}

/**
 * Previews of the pictures a chapter names, each below its line. The text itself stays
 * Markdown; only the picture of the story is shown, never anything the text points to elsewhere.
 */
export function picturePreviews(source: (file: string) => string) {
  return StateField.define<DecorationSet>({
    create: (state) => previews(state, source),
    update: (value, transaction) =>
      transaction.docChanged ? previews(transaction.state, source) : value,
    provide: (field) => EditorView.decorations.from(field),
  });
}
