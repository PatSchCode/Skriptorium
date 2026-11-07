import { useState } from "react";

/** The bounds of a LoRA's weight, as the server takes them (ADR-115). */
const MIN_WEIGHT = -2;
const MAX_WEIGHT = 2;

/**
 * The weight of a LoRA (step 10.8, ADR-115). The text may be empty or unfinished while typing
 * ("", "-", "0."); only a number within the bounds reaches `onChange`. Leaving the field shows the
 * weight in force again.
 */
export function WeightInput({
  value,
  label,
  disabled,
  onChange,
}: {
  value: number;
  label: string;
  disabled: boolean;
  onChange: (weight: number) => void;
}) {
  const [text, setText] = useState<string | null>(null);
  return (
    <input
      type="number"
      min={MIN_WEIGHT}
      max={MAX_WEIGHT}
      step={0.05}
      aria-label={label}
      value={text ?? String(value)}
      disabled={disabled}
      onChange={(event) => {
        const typed = event.target.value;
        setText(typed);
        const weight = Number(typed);
        if (
          typed.trim() !== "" &&
          Number.isFinite(weight) &&
          weight >= MIN_WEIGHT &&
          weight <= MAX_WEIGHT
        ) {
          onChange(weight);
        }
      }}
      onBlur={() => {
        setText(null);
      }}
    />
  );
}
