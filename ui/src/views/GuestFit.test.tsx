import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import {
  catalogModel,
  fail,
  fakeApi,
  modelList,
  ok,
  sseFeed,
  STORY,
} from "../../fake-api";
import { GuestFit } from "./GuestFit";

const FIT =
  "POST /api/worlds/salzmark/stories/ueberfahrt/guests/nebelreich/nebelkoenig/fit";
const LINK = { world: "nebelreich", entry: "nebelkoenig" };

afterEach(() => {
  vi.restoreAllMocks();
});

function fit(onTake = vi.fn(), onClose = vi.fn()) {
  render(
    <GuestFit
      story={STORY}
      link={LINK}
      name="Nebelkönig"
      onTake={onTake}
      onClose={onClose}
    />,
  );
  return { onTake, onClose };
}

describe("the world builder's proposal for a guest (step 9.13)", () => {
  it("starts with the model of the world builder and lets the author change it", async () => {
    const feed = sseFeed();
    const { calls } = fakeApi({
      "GET /api/models": ok(
        modelList(
          ["x-ai/grok-4.6"],
          [
            catalogModel("x-ai/grok-4.6", { name: "Grok 4.6" }),
            catalogModel("qwen/qwen3.8-max-0902", { name: "Qwen" }),
          ],
          { weltenbau: "qwen/qwen3.8-max-0902" },
        ),
      ),
      [FIT]: () => ({ status: 200, stream: feed.stream }),
    });
    const user = userEvent.setup();
    const { onTake } = fit();

    const model = await screen.findByLabelText("Modell");
    expect((model as HTMLSelectElement).value).toBe("qwen/qwen3.8-max-0902");
    await user.selectOptions(model, "x-ai/grok-4.6");
    await user.click(screen.getByRole("button", { name: "Vorschlagen" }));
    expect(calls.at(-1)?.body).toEqual({ model: "x-ai/grok-4.6", wish: "" });
    expect(screen.getByText("Der Weltenbauer liest …")).toBeDefined();
    feed.send("text", { text: "Erster." });
    feed.send("done", {
      input_tokens: 1,
      output_tokens: 1,
      cost_usd: null,
      finish_reason: "stop",
    });
    feed.close();

    const proposal = await screen.findByLabelText("Vorschlag");
    await user.type(proposal, " Mehr. ");
    await user.click(
      screen.getByRole("button", { name: "In das Feld übernehmen" }),
    );
    expect(onTake).toHaveBeenCalledWith("Erster. Mehr.");
  });

  it("asks again, can be stopped while it runs and closes", async () => {
    const first = sseFeed();
    const second = sseFeed();
    const feeds = [first, second];
    fakeApi({
      "GET /api/models": ok(modelList(["x-ai/grok-4.6"])),
      [FIT]: () => ({ status: 200, stream: feeds.shift()?.stream }),
    });
    const user = userEvent.setup();
    const { onClose } = fit();

    await user.click(
      await screen.findByRole("button", { name: "Vorschlagen" }),
    );
    first.send("text", { text: "Eins." });
    first.close();
    await user.click(
      await screen.findByRole("button", { name: "Neuer Vorschlag" }),
    );
    expect(screen.getByRole("button", { name: "Abbrechen" })).toBeDefined();
    await user.click(screen.getByRole("button", { name: "Abbrechen" }));
    expect(onClose).toHaveBeenCalled();
  });

  it("says when the models or the request fail", async () => {
    fakeApi({
      "GET /api/models": fail(500, "Modelle nicht ladbar"),
      [FIT]: fail(404, "Gast fehlt"),
    });
    fit();

    expect(await screen.findByText("Modelle nicht ladbar")).toBeDefined();
    expect(screen.queryByLabelText("Modell")).toBeNull();
    expect(screen.getByRole("button", { name: "Vorschlagen" })).toHaveProperty(
      "disabled",
      true,
    );
  });

  it("shows a failed stream", async () => {
    fakeApi({
      "GET /api/models": ok(modelList(["x-ai/grok-4.6"])),
      [FIT]: fail(404, "Gast fehlt"),
    });
    const user = userEvent.setup();
    fit();

    await user.click(
      await screen.findByRole("button", { name: "Vorschlagen" }),
    );
    await waitFor(() => {
      expect(screen.getByText("Gast fehlt")).toBeDefined();
    });
  });
});
