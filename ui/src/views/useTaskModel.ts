import { useEffect, useState } from "react";
import { api, describeError, type ModelTask } from "../api";
import { taskModel } from "../models";

/**
 * The text models a task offers – the favorites, with the saved model of the task in front if it
 * is not among them – and the chosen one: the saved model, else the preset if it is a favorite,
 * else the first favorite (ADR-055, ADR-096). A failed list ends up in `onError` and offers
 * nothing. Used by the figure assistant (step 11.5, ADR-123).
 */
export function useTaskModel(
  task: ModelTask,
  onError: (message: string) => void,
) {
  const [models, setModels] = useState<{ id: string; name: string }[] | null>(
    null,
  );
  const [model, setModel] = useState("");

  useEffect(() => {
    let current = true;
    api
      .models()
      .then((list) => {
        if (!current) {
          return;
        }
        const names = new Map(list.catalog.map((m) => [m.id, m.name]));
        const saved = taskModel(list, task);
        const offered =
          saved === null || list.favorites.includes(saved)
            ? list.favorites
            : [saved, ...list.favorites];
        setModels(offered.map((id) => ({ id, name: names.get(id) ?? id })));
        setModel(
          saved ??
            (list.favorites.includes(list.default)
              ? list.default
              : (list.favorites[0] ?? "")),
        );
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
  }, [task, onError]);

  return { models, model, setModel };
}
