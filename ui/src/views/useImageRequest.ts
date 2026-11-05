import { useState } from "react";
import type { AspectRatio } from "../api";

/**
 * What the author asks for in "Bild erzeugen" (step 7.12): the description and the format. A new
 * starting text (places chosen, looks added; step 9.5) replaces the description. Until the author
 * picks a format, it may follow the proportions of a basis (step 9.8).
 */
export function useImageRequest(
  initialPrompt: string,
  initialFormat: AspectRatio,
) {
  const [prompt, setPrompt] = useState(initialPrompt);
  const [shownInitial, setShownInitial] = useState(initialPrompt);
  if (initialPrompt !== shownInitial) {
    setShownInitial(initialPrompt);
    setPrompt(initialPrompt);
  }
  const [format, setFormat] = useState<AspectRatio>(initialFormat);
  const [formatPicked, setFormatPicked] = useState(false);

  return {
    prompt,
    setPrompt,
    format,
    /** The author's choice; from now on the basis no longer decides. */
    pickFormat: (chosen: AspectRatio) => {
      setFormat(chosen);
      setFormatPicked(true);
    },
    /** The format of the basis, as long as the author has not picked one. */
    followBasis: (proportions: AspectRatio) => {
      if (!formatPicked) {
        setFormat(proportions);
      }
    },
  };
}
