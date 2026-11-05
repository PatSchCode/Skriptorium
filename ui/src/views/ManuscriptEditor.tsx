import { defaultKeymap, history, historyKeymap } from "@codemirror/commands";
import { markdown } from "@codemirror/lang-markdown";
import { EditorSelection, EditorState } from "@codemirror/state";
import { EditorView, keymap } from "@codemirror/view";
import { useEffect, useRef } from "react";
import { placePicture } from "../pictures";
import { picturePreviews } from "./picturePreviews";

/**
 * Markdown editor for the manuscript (CodeMirror 6). Shows the Markdown source only; it never
 * renders HTML from the text, so nothing in a manuscript can run as script. `onSelect` receives
 * the marked text whenever the selection changes (empty without a selection, step 3.8).
 * The editor grows with the text and scrolls with the page around it (step 5.11); `onEnd` asks
 * the page to show the end of the text, where writing goes on: when the editor opens and when
 * new text arrives from outside, e.g. a taken-over proposal (step 5.9). With `pictureSrc` a
 * picture line shows a small preview below it, and `insertion` puts a picture line after the
 * line of the cursor (step 10.6, ADR-110).
 */
export function ManuscriptEditor({
  value,
  onChange,
  onSelect,
  onEnd,
  label,
  pictureSrc,
  insertion,
}: {
  value: string;
  onChange: (text: string) => void;
  onSelect?: (marked: string) => void;
  /** Called when the end of the text should come into view (step 5.9). */
  onEnd?: () => void;
  label: string;
  /** Address of a picture of the story; without it no previews. */
  pictureSrc?: (file: string) => string;
  /** A picture line to put in; a new `id` puts it in once. */
  insertion?: { id: number; line: string } | null;
}) {
  const host = useRef<HTMLDivElement>(null);
  const view = useRef<EditorView | null>(null);
  const onChangeRef = useRef(onChange);
  const onSelectRef = useRef(onSelect);
  const onEndRef = useRef(onEnd);
  const initialValue = useRef(value);
  const initialSource = useRef(pictureSrc);

  useEffect(() => {
    onChangeRef.current = onChange;
    onSelectRef.current = onSelect;
    onEndRef.current = onEnd;
  }, [onChange, onSelect, onEnd]);

  useEffect(() => {
    if (host.current === null) {
      return;
    }
    const editor = new EditorView({
      parent: host.current,
      state: EditorState.create({
        doc: initialValue.current,
        selection: EditorSelection.cursor(initialValue.current.length),
        extensions: [
          history(),
          keymap.of([...defaultKeymap, ...historyKeymap]),
          markdown(),
          EditorView.lineWrapping,
          ...(initialSource.current === undefined
            ? []
            : [picturePreviews(initialSource.current)]),
          EditorView.contentAttributes.of({ "aria-label": label }),
          EditorView.updateListener.of((update) => {
            if (update.docChanged) {
              onChangeRef.current(update.state.doc.toString());
            }
            if (update.selectionSet || update.docChanged) {
              const { from, to } = update.state.selection.main;
              onSelectRef.current?.(update.state.sliceDoc(from, to));
            }
          }),
        ],
      }),
    });
    view.current = editor;
    onEndRef.current?.();
    return () => {
      editor.destroy();
      view.current = null;
    };
  }, [label]);

  useEffect(() => {
    const editor = view.current;
    if (editor !== null && editor.state.doc.toString() !== value) {
      editor.dispatch({
        changes: { from: 0, to: editor.state.doc.length, insert: value },
        selection: EditorSelection.cursor(value.length),
      });
      onEndRef.current?.();
    }
  }, [value]);

  useEffect(() => {
    const editor = view.current;
    if (editor === null || insertion == null) {
      return;
    }
    const placed = placePicture(
      editor.state.doc.toString(),
      editor.state.selection.main.head,
      insertion.line,
    );
    editor.dispatch({
      changes: { from: placed.from, to: placed.to, insert: placed.insert },
      selection: EditorSelection.cursor(placed.cursor),
      scrollIntoView: true,
    });
    editor.focus();
  }, [insertion]);

  return <div className="editor manuscript" ref={host} />;
}
