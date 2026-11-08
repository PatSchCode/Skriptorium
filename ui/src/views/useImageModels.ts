import { useEffect, useState } from "react";
import {
  api,
  describeError,
  type ImageModelList,
  type RunwareLora,
  type RunwareModel,
} from "../api";

/**
 * One model of "Bild erzeugen": a model of OpenRouter, or a base model of the owner's list at
 * Runware (step 10.8, ADR-115), which carries its entry of that list.
 */
export type OfferedModel = ImageModelList["models"][number] & {
  runware?: RunwareModel;
};

/**
 * The image models "Bild erzeugen" offers (step 7.12, ADR-077) and the chosen one: with a basis
 * only models that take one (step 9.8, ADR-097), so no Runware model (ADR-115); preselected is
 * `initialModel`, else the default from the settings, else the first. A failed list ends up in
 * `onError` and offers nothing. `ready` tells whether the provider of the chosen model is set up.
 */
export function useImageModels(
  initialModel: string | null,
  withBasis: boolean,
  onError: (message: string) => void,
) {
  // With their levels (step 10.5, ADR-109).
  const [models, setModels] = useState<OfferedModel[] | null>(null);
  const [loras, setLoras] = useState<RunwareLora[]>([]);
  const [model, setModel] = useState("");
  const [readiness, setReadiness] = useState({
    openRouter: true,
    runware: true,
  });

  useEffect(() => {
    let current = true;
    api
      .imageModels()
      .then((list) => {
        if (!current) {
          return;
        }
        const offered: OfferedModel[] = withBasis
          ? list.models.filter((m) => m.references > 0)
          : [
              ...list.models,
              ...(list.runware ?? []).map((entry) => ({
                id: entry.id,
                name: entry.name,
                references: 0,
                // Every Runware model takes a start value (step 11.4, ADR-121).
                seed: true,
                runware: entry,
              })),
            ];
        setModels(offered);
        setLoras(list.loras ?? []);
        setReadiness({
          openRouter: list.ready,
          runware: list.runware_ready ?? false,
        });
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

  const chosen = models?.find((m) => m.id === model);
  const ready =
    chosen?.runware === undefined ? readiness.openRouter : readiness.runware;
  return { models, model, setModel, ready, chosen, loras };
}
