/**
 * Pictures between the paragraphs of a chapter (step 10.6, ADR-110): a paragraph of its own
 * `![caption](bild:<file>)`, where `<file>` is a picture of the story. The same form as the
 * server reads (`manuscript/pictures.py`); any other target stays text.
 */

const LINE =
  /^[ \t]*!\[([^\]\n]*)\]\(bild:(bild-[0-9a-f]{12}\.(?:png|jpg|webp))\)[ \t]*$/;

export interface Picture {
  caption: string;
  file: string;
}

/** The picture a line of Markdown stands for, `null` for any other line. */
export function pictureOf(line: string): Picture | null {
  const found = LINE.exec(line.replace(/\r$/, ""));
  return found === null
    ? null
    : { caption: (found[1] ?? "").trim(), file: found[2] ?? "" };
}

/** The line for a picture; brackets and line breaks in the caption would end it early. */
export function pictureLine(caption: string, file: string): string {
  const clean = caption
    .replace(/[[\]\r\n]+/g, " ")
    .replace(/\s+/g, " ")
    .trim();
  return `![${clean}](bild:${file})`;
}

/**
 * Where a picture line goes when the cursor stands at `head`: after the line of the cursor, as
 * a paragraph of its own – one blank line before and after, never inside a sentence. Returns
 * the change (`from`, `to`, `insert`) and the cursor after it.
 */
export function placePicture(
  text: string,
  head: number,
  line: string,
): { from: number; to: number; insert: string; cursor: number } {
  const end = text.indexOf("\n", head);
  const lineEnd = end === -1 ? text.length : end;
  const before = text.slice(0, lineEnd).replace(/\s+$/, "");
  const rest = text.slice(lineEnd);
  const after = rest.replace(/^\s+/, "");
  const insert =
    (before === "" ? "" : "\n\n") + line + (after === "" ? "\n" : "\n\n");
  const from = before.length;
  return {
    from,
    to: lineEnd + (rest.length - after.length),
    insert,
    cursor: from + insert.length,
  };
}
