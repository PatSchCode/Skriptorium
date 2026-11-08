import { useState } from "react";

/** The largest start value the server and every provider take (ADR-121). */
export const MAX_SEED = 2_147_483_647;

/**
 * The start value of "Bild erzeugen" (step 11.4, ADR-121): random (the server draws one) or
 * fixed. `initial` presets a fixed one, e.g. when generating anew from an origin. `seed` is what
 * goes along: the fixed value, or `undefined` for random; `valid` is false for a fixed value out
 * of range.
 */
export function useSeedChoice(initial: number | null) {
  const [fixed, setFixed] = useState(initial !== null);
  const [text, setText] = useState(initial === null ? "" : String(initial));
  const value = Number(text);
  const valid =
    !fixed ||
    (/^\d{1,10}$/.test(text) &&
      Number.isInteger(value) &&
      value >= 1 &&
      value <= MAX_SEED);
  return {
    fixed,
    text,
    valid,
    seed: fixed && valid ? value : undefined,
    setFixed,
    setText,
    /** "Startwert behalten": fixed from now on with the value of the preview. */
    keep: (seed: number) => {
      setFixed(true);
      setText(String(seed));
    },
  };
}

/** "Startwert [zufällig | fest]" with the number for a fixed one. */
export function SeedField({
  choice,
  busy,
}: {
  choice: ReturnType<typeof useSeedChoice>;
  busy: boolean;
}) {
  return (
    <div className="image-generate-field">
      Startwert
      <div className="row">
        <div
          className="image-generate-formats"
          role="radiogroup"
          aria-label="Startwert"
        >
          {[false, true].map((fixed) => (
            <button
              key={String(fixed)}
              type="button"
              role="radio"
              aria-checked={choice.fixed === fixed}
              className={choice.fixed === fixed ? "chosen" : undefined}
              disabled={busy}
              onClick={() => {
                choice.setFixed(fixed);
              }}
            >
              {fixed ? "fest" : "zufällig"}
            </button>
          ))}
        </div>
        <input
          type="text"
          inputMode="numeric"
          aria-label="Fester Startwert"
          value={choice.fixed ? choice.text : ""}
          placeholder="—"
          disabled={busy || !choice.fixed}
          size={11}
          onChange={(event) => {
            choice.setText(event.target.value.trim());
          }}
        />
      </div>
      {!choice.valid && (
        <p className="note">
          Ein fester Startwert ist eine ganze Zahl von 1 bis 2.147.483.647.
        </p>
      )}
    </div>
  );
}
