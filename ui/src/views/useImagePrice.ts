import { useEffect, useState } from "react";
import { api, type ImagePrice } from "../api";

/**
 * The price of one image with `model` (step 7.12), `null` while it loads. The price is kept with
 * the model it belongs to, so a stale one is never shown after a change of model; a failed request
 * counts as an unknown price.
 */
export function useImagePrice(model: string): ImagePrice | null {
  const [priced, setPriced] = useState<{
    model: string;
    price: ImagePrice;
  } | null>(null);

  useEffect(() => {
    if (model === "") {
      return;
    }
    let current = true;
    api
      .imagePrice(model)
      .then((found) => {
        if (current) {
          setPriced({ model, price: found });
        }
      })
      .catch(() => {
        if (current) {
          setPriced({ model, price: { cost_usd: null, unit: null } });
        }
      });
    return () => {
      current = false;
    };
  }, [model]);

  return priced?.model === model ? priced.price : null;
}
