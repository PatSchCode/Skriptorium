/**
 * Generating images with the AI (steps 7.12, 9.8, 10.5, ADR-077, ADR-097, ADR-109); a preview
 * only, nothing is stored.
 */

import { request } from "./core";

export interface ImageModelList {
  default: string;
  /**
   * `references`: how many images the model takes as a basis (step 9.8); `resolutions` and
   * `qualities`: the levels it offers, empty or missing for none (step 10.5, ADR-109).
   */
  models: {
    id: string;
    name: string;
    references: number;
    resolutions?: string[];
    qualities?: string[];
  }[];
  available: boolean;
  /** False without a key; generating then answers 503. */
  ready: boolean;
  /** The owner's base models at Runware (step 10.8, ADR-115). */
  runware?: RunwareModel[];
  /** The owner's LoRAs at Runware (ADR-115). */
  loras?: RunwareLora[];
  /** False without the Runware key. */
  runware_ready?: boolean;
}

/**
 * A base model at Runware (ADR-115): `addition` is appended to every prompt, `loras` are the
 * LoRAs of the list that fit it.
 */
export interface RunwareModel {
  id: string;
  name: string;
  architecture: string;
  addition: string;
  loras: string[];
}

/** A LoRA at Runware: trigger words appended to the prompt, the weight it starts with. */
export interface RunwareLora {
  id: string;
  name: string;
  architecture: string;
  trigger: string;
  weight: number;
}

/** A LoRA chosen for one image, with its weight (ADR-115). */
export interface LoraChoice {
  id: string;
  weight: number;
}

export interface ImagePrice {
  cost_usd: number | null;
  unit: string | null;
  /** What an image given as the basis costs, if the provider names it (step 9.8). */
  input_cost_usd?: number | null;
  input_unit?: string | null;
}

/** A stored image as the basis of a new one: an entry image, a map or a cover (ADR-097). */
export interface ImageReference {
  world: string;
  entry?: string;
  image?: string;
  map_file?: string;
  story?: string;
}

export type AspectRatio = "2:3" | "1:1" | "3:2";

/**
 * How a taken-over image was generated (step 9.6, ADR-095); sent along with the upload and
 * kept by the server next to the image.
 */
export interface ImageOrigin {
  model: string;
  prompt: string;
  aspect_ratio: AspectRatio;
  cost_usd: number | null;
  /** The image it was made from, e.g. "Bild 1 von Kael" (step 9.8, ADR-097). */
  basis?: string;
  /** The levels chosen, if the model offered any (step 10.5, ADR-109). */
  resolution?: string;
  quality?: string;
}

/** The levels of one image, `null` where the model offers none (step 10.5, ADR-109). */
export interface ImageLevels {
  resolution: string | null;
  quality: string | null;
}

/** The stored origin with the date it was taken over; `null` for an uploaded image. */
export interface StoredImageOrigin {
  model: string;
  prompt: string;
  aspect_ratio: string;
  cost_usd: number | null;
  date: string;
  basis: string | null;
  /** Missing or `null` for older origins and models without levels (step 10.5). */
  resolution?: string | null;
  quality?: string | null;
}

export interface GeneratedImage {
  content: string;
  media_type: string;
  cost_usd: number | null;
  model: string;
}

/** Where a generated image goes: a world, and a story for a cover (step 9.11, ADR-100). */
export interface ImageTarget {
  world: string;
  story?: string;
}

export const imagesApi = {
  imageModels: () =>
    request("GET", "/api/images/models") as Promise<ImageModelList>,
  /** The price of one image, at `levels` where given (step 10.5, ADR-109). */
  imagePrice: (model: string, levels?: ImageLevels) => {
    const query = [
      `model=${encodeURIComponent(model)}`,
      ...(levels?.resolution == null
        ? []
        : [`resolution=${encodeURIComponent(levels.resolution)}`]),
      ...(levels?.quality == null
        ? []
        : [`quality=${encodeURIComponent(levels.quality)}`]),
    ];
    return request(
      "GET",
      `/api/images/price?${query.join("&")}`,
    ) as Promise<ImagePrice>;
  },
  generateImage: (
    order: {
      model: string;
      prompt: string;
      aspect_ratio: AspectRatio;
      reference?: ImageReference;
      resolution?: string;
      quality?: string;
      /** Only for a Runware model (ADR-115). */
      loras?: LoraChoice[];
    } & ImageTarget,
  ) =>
    request("POST", "/api/images/generate", order) as Promise<GeneratedImage>,
  /** Look up a model or LoRA at Runware and add it to the list (ADR-115). */
  addRunwareModel: (reference: string) =>
    request("POST", "/api/images/runware", {
      reference,
    }) as Promise<ImageModelList>,
  /** Save the edited list; what is left out is removed (ADR-115). */
  setRunwareModels: (list: {
    models: { id: string; name: string; addition: string }[];
    loras: { id: string; name: string; trigger: string; weight: number }[];
  }) => request("PUT", "/api/images/runware", list) as Promise<ImageModelList>,
};
