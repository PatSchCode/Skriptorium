/** Letting the AI describe an image or a map once (step 7.13, ADR-074). */

import { WRITE_EVENTS, streamEvents } from "./stream";
import type { WorldbuilderEvent } from "./worldbuilder";
import { enc, worldPath } from "./paths";

/**
 * Events of a description: start, text pieces, then done or error. The server streams them like
 * the world builder's answer (its "start" names the web search, which is always off here).
 */
export type DescribeEvent = Extract<
  WorldbuilderEvent,
  { type: "start" | "text" | "done" | "error" }
>;

/**
 * Ask a model that reads images to describe the image behind `path`; each event goes to
 * `onEvent`. Errors and aborting behave as in `streamWrite`. Nothing is saved.
 */
export function streamDescription(
  path: string,
  model: string,
  onEvent: (event: DescribeEvent) => void,
  signal?: AbortSignal,
): Promise<void> {
  return streamEvents(
    path,
    { model },
    WRITE_EVENTS,
    { type: "error", kind: "verbindung" },
    onEvent,
    signal,
  );
}

/**
 * Ask the world builder how a guest fits the world of the story (step 9.13, ADR-102); events as
 * for a description. `wish` may be empty. Nothing is saved.
 */
export function streamGuestFit(
  path: string,
  model: string,
  wish: string,
  onEvent: (event: DescribeEvent) => void,
  signal?: AbortSignal,
): Promise<void> {
  return streamEvents(
    path,
    { model, wish },
    WRITE_EVENTS,
    { type: "error", kind: "verbindung" },
    onEvent,
    signal,
  );
}

/**
 * Ask the figure assistant for an English image description from the answers about a figure's
 * looks (step 11.5, ADR-123), or – with the suggestions path – for three suggestions per question
 * from the entry and the world (ADR-124, answers may be partial); events as for a description.
 * Nothing is saved.
 */
export function streamFigureLooks(
  path: string,
  model: string,
  answers: Readonly<Record<string, string>>,
  onEvent: (event: DescribeEvent) => void,
  signal?: AbortSignal,
): Promise<void> {
  return streamEvents(
    path,
    { model, answers },
    WRITE_EVENTS,
    { type: "error", kind: "verbindung" },
    onEvent,
    signal,
  );
}

export const describeApi = {
  describeImagePath: (world: string, entry: string, image: string) =>
    `${worldPath(world)}/entries/${enc(entry)}/images/${enc(image)}/describe`,
  describeMapPath: (world: string, file: string) =>
    `${worldPath(world)}/maps/${enc(file)}/describe`,
  /** Stream of "Aussehen herauslösen" (step 7.16); takes `{model}` like a description. */
  appearancePath: (world: string, entry: string) =>
    `${worldPath(world)}/entries/${enc(entry)}/appearance`,
  /** Stream of the figure assistant (step 11.5, ADR-123); takes `{model, answers}`. */
  figureLooksPath: (world: string, entry: string) =>
    `${worldPath(world)}/entries/${enc(entry)}/figure-looks`,
  /** Stream of the suggestions for the questions (step 11.5, ADR-124); takes `{model, answers}`. */
  figureLooksSuggestionsPath: (world: string, entry: string) =>
    `${worldPath(world)}/entries/${enc(entry)}/figure-looks/suggestions`,
};
