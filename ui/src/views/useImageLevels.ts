import { useState } from "react";
import type { ImageLevels } from "../api";

/** What a model offers (step 10.5, ADR-109); missing lists count as none. */
export interface OfferedLevels {
  resolutions?: readonly string[];
  qualities?: readonly string[];
}

/** The resolution preset where offered (ADR-109). */
const PRESET_RESOLUTION = "2K";
/** The quality preset where offered: what the model picks on its own. */
const PRESET_QUALITY = "auto";

function preset(
  offered: readonly string[],
  wanted: string | null,
  fallback: string,
): string | null {
  if (wanted !== null && offered.includes(wanted)) {
    return wanted;
  }
  return offered.includes(fallback) ? fallback : (offered[0] ?? null);
}

/**
 * Resolution and quality of the image to generate (step 10.5, ADR-109): for each model its own
 * levels; preset are `initial` (generating anew from an origin) where the model offers them, else
 * "2K" and "auto", else its first level. A model without levels has `null`. Changing the model
 * starts from the preset again.
 */
export function useImageLevels(
  model: string,
  offered: OfferedLevels | undefined,
  initial: ImageLevels,
) {
  const resolutions = offered?.resolutions ?? [];
  const qualities = offered?.qualities ?? [];
  const [chosen, setChosen] = useState<
    ({ model: string } & ImageLevels) | null
  >(null);
  const levels: ImageLevels =
    chosen?.model === model
      ? chosen
      : {
          resolution: preset(
            resolutions,
            initial.resolution,
            PRESET_RESOLUTION,
          ),
          quality: preset(qualities, initial.quality, PRESET_QUALITY),
        };

  return {
    resolutions,
    qualities,
    resolution: levels.resolution,
    quality: levels.quality,
    pickResolution: (resolution: string) => {
      setChosen({ model, resolution, quality: levels.quality });
    },
    pickQuality: (quality: string) => {
      setChosen({ model, resolution: levels.resolution, quality });
    },
  };
}
