import { useEffect, useState } from "react";
import { api, describeError, type ImageModelList } from "../api";

/**
 * The image models "Bild erzeugen" offers (step 7.12, ADR-077) and the chosen one: with a basis
 * only models that take one (step 9.8, ADR-097); preselected is `initialModel`, else the default
 * from the settings, else the first. A failed list ends up in `onError` and offers nothing.
 */
export function useImageModels(
  initialModel: string | null,
  withBasis: boolean,
  onError: (message: string) => void,
) {
  // With their levels (step 10.5, ADR-109).
  const [models, setModels] = useState<ImageModelList["models"] | null>(null);
  const [model, setModel] = useState("");
  const [ready, setReady] = useState(true);

  useEffect(() => {
    let current = true;
    api
      .imageModels()
      .then((list) => {
        if (!current) {
          return;
        }
        const offered = withBasis
          ? list.models.filter((m) => m.references > 0)
          : list.models;
        setModels(offered);
        setReady(list.ready);
        const wanted = [initialModel, list.default];
        const preset =
          wanted.find((id) => offered.some((m) => m.id === id)) ??
          offered[0]?.id ??
          "";
        setModel(preset);
      })
      .catch((reason: unknown) => {
        if (current) {
          onError(describeError(reason));
          setModels([]);
        }
      });
    return () => {
      current = false;
    };
  }, [initialModel, withBasis, onError]);

  return { models, model, setModel, ready };
}
