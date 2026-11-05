import { useEffect, useState } from "react";
import { api, type ImagePrice } from "../api";

const UNKNOWN: ImagePrice = { cost_usd: null, unit: null };

/**
 * The price of one image with `model` at each of its `resolutions` (or once without, for a model
 * that offers none) and the chosen `quality` (steps 7.12 and 10.5, ADR-109). The prices are kept
 * with what they belong to, so a stale one is never shown after a change; a failed request counts
 * as an unknown price. `priceOf` answers `null` while loading.
 */
export function useImagePrices(
  model: string,
  resolutions: readonly string[],
  quality: string | null,
) {
  // One string for the effect: the list as it is, without depending on its identity.
  const levels = resolutions.join("\n");
  const key = `${model}\n${quality ?? ""}\n${levels}`;
  const [priced, setPriced] = useState<{
    key: string;
    prices: ReadonlyMap<string, ImagePrice>;
  } | null>(null);

  useEffect(() => {
    if (model === "") {
      return;
    }
    let current = true;
    const asked = levels === "" ? [null] : levels.split("\n");
    void Promise.all(
      asked.map((resolution) =>
        api.imagePrice(model, { resolution, quality }).catch(() => UNKNOWN),
      ),
    ).then((found) => {
      if (current) {
        setPriced({
          key: `${model}\n${quality ?? ""}\n${levels}`,
          prices: new Map(
            asked.map((resolution, at) => [
              resolution ?? "",
              found[at] ?? UNKNOWN,
            ]),
          ),
        });
      }
    });
    return () => {
      current = false;
    };
  }, [model, quality, levels]);

  return {
    priceOf: (resolution: string | null): ImagePrice | null =>
      priced?.key === key
        ? (priced.prices.get(resolution ?? "") ?? null)
        : null,
  };
}
