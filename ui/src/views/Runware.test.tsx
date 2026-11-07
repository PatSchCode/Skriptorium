import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import { fail, fakeApi, ok } from "../../fake-api";
import type { ImageModelList, RunwareLora, RunwareModel } from "../api";
import { ImageGenerate } from "./ImageGenerate";
import { RunwareSettings } from "./RunwareSettings";

const EPIC = "civitai:277058@1405120";
const FLUX = "runware:400@1";
const CUFFS = "civitai:536201@596079";

const PLAIN: ImageModelList = {
  default: "black-forest-labs/flux.2-pro",
  models: [
    { id: "black-forest-labs/flux.2-pro", name: "FLUX.2 Pro", references: 1 },
  ],
  available: true,
  ready: true,
};
const EPIC_ENTRY: RunwareModel = {
  id: EPIC,
  name: "epiCRealism XL VXIV",
  architecture: "sdxl",
  addition: "raw photo",
  loras: [CUFFS],
};
const CUFFS_ENTRY: RunwareLora = {
  id: CUFFS,
  name: "Handcuffs",
  architecture: "pony",
  trigger: "handcuffs",
  weight: 0.8,
};
const LIST: ImageModelList = {
  ...PLAIN,
  runware: [
    EPIC_ENTRY,
    {
      id: FLUX,
      name: "FLUX.2 [dev]",
      architecture: "flux_2_dev",
      addition: "",
      loras: [],
    },
  ],
  loras: [CUFFS_ENTRY],
  runware_ready: true,
};

const IMAGE = ok({
  content: "iVBORw0KGgo=",
  media_type: "image/png",
  cost_usd: 0.0025,
  model: EPIC,
});

afterEach(() => {
  vi.restoreAllMocks();
});

function dialog(initialModel: string | null = null) {
  return render(
    <ImageGenerate
      target={{ world: "die-salzmark" }}
      title="Bild erzeugen"
      initialPrompt="Kael am Fluss"
      initialFormat="2:3"
      initialModel={initialModel}
      onTakeOver={() => Promise.resolve()}
      onClose={() => undefined}
    />,
  );
}

describe("generating through Runware (step 10.8, ADR-115)", () => {
  it("groups the models and sends the ticked LoRAs with their weight", async () => {
    const { calls } = fakeApi({
      "GET /api/images/models": ok(LIST),
      "GET /api/images/price": ok({ cost_usd: null, unit: null }),
      "POST /api/images/generate": IMAGE,
    });
    const user = userEvent.setup();
    dialog(EPIC);
    const select = await screen.findByLabelText("Modell");
    expect(
      within(select)
        .getAllByRole("group")
        .map((g) => g.getAttribute("label")),
    ).toEqual(["OpenRouter", "Runware"]);
    expect(
      screen.getByText(
        "Abrechnung nach Rechenzeit – die Kosten stehen nach dem Erzeugen da",
      ),
    ).toBeDefined();
    expect(
      screen.getByText("Angehängt an die Beschreibung: raw photo"),
    ).toBeDefined();
    const weight = screen.getByLabelText("Gewicht Handcuffs");
    expect(weight).toHaveProperty("disabled", true);
    await user.click(screen.getByRole("checkbox", { name: "Handcuffs" }));
    expect(
      screen.getByText("Angehängt an die Beschreibung: raw photo, handcuffs"),
    ).toBeDefined();
    await user.clear(weight);
    await user.type(weight, "0.5");
    await user.clear(weight);
    await user.type(weight, "9");
    await user.click(screen.getByRole("button", { name: "✨ Erzeugen" }));
    expect(
      await screen.findByAltText("Vorschau des erzeugten Bildes"),
    ).toBeDefined();
    expect(calls.find((c) => c.method === "POST")?.body).toEqual({
      model: EPIC,
      prompt: "Kael am Fluss",
      aspect_ratio: "2:3",
      world: "die-salzmark",
      loras: [{ id: CUFFS, weight: 0.5 }],
    });
  });

  it("drops a LoRA that is unticked or does not fit the model", async () => {
    const { calls } = fakeApi({
      "GET /api/images/models": ok(LIST),
      "GET /api/images/price": ok({ cost_usd: null, unit: null }),
      "POST /api/images/generate": IMAGE,
    });
    const user = userEvent.setup();
    dialog(EPIC);
    const box = await screen.findByRole("checkbox", { name: "Handcuffs" });
    await user.click(box);
    await user.click(box);
    await user.click(box);
    await user.selectOptions(screen.getByLabelText("Modell"), FLUX);
    expect(screen.queryByRole("checkbox", { name: "Handcuffs" })).toBeNull();
    await user.click(screen.getByRole("button", { name: "✨ Erzeugen" }));
    await screen.findByAltText("Vorschau des erzeugten Bildes");
    expect(calls.find((c) => c.method === "POST")?.body).toEqual({
      model: FLUX,
      prompt: "Kael am Fluss",
      aspect_ratio: "2:3",
      world: "die-salzmark",
    });
  });

  it("says so when Runware is not set up", async () => {
    fakeApi({
      "GET /api/images/models": ok({ ...LIST, runware_ready: false }),
      "GET /api/images/price": ok({ cost_usd: null, unit: null }),
    });
    dialog(FLUX);
    expect(
      await screen.findByText(
        "Runware ist nicht eingerichtet – mit diesem Modell geht es gerade nicht.",
      ),
    ).toBeDefined();
    expect(screen.getByRole("button", { name: "✨ Erzeugen" })).toHaveProperty(
      "disabled",
      true,
    );
  });

  it("offers no Runware model for an image with a basis", async () => {
    fakeApi({
      "GET /api/images/models": ok(LIST),
      "GET /api/images/price": ok({ cost_usd: 0.03, unit: "image" }),
    });
    render(
      <ImageGenerate
        target={{ world: "w" }}
        title="Bild"
        initialPrompt="x"
        initialFormat="1:1"
        basis={{
          src: "data:image/png;base64,iVBORw0KGgo=",
          label: "Bild 1 von Kael",
          reference: { world: "w", entry: "kael", image: "a.png" },
        }}
        onTakeOver={() => Promise.resolve()}
        onClose={() => undefined}
      />,
    );
    const select = await screen.findByLabelText("Modell");
    expect(within(select).queryAllByRole("group")).toEqual([]);
    expect(within(select).getAllByRole("option")).toHaveLength(1);
  });

  it("works with a server that names no Runware lists", async () => {
    fakeApi({
      "GET /api/images/models": ok(PLAIN),
      "GET /api/images/price": ok({ cost_usd: 0.03, unit: "image" }),
    });
    dialog();
    const select = await screen.findByLabelText("Modell");
    expect(within(select).getAllByRole("option")).toHaveLength(1);
  });
});

describe("the Runware list in the settings (ADR-115)", () => {
  it("adds a model by a Civitai link and shows the new list", async () => {
    const added: ImageModelList = {
      ...LIST,
      runware: [
        ...(LIST.runware ?? []),
        {
          id: "civitai:548016@861939",
          name: "PonyXL MIX v2",
          architecture: "pony",
          addition: "",
          loras: [CUFFS],
        },
      ],
    };
    const { calls } = fakeApi({ "POST /api/images/runware": ok(added) });
    const changed = vi.fn();
    const user = userEvent.setup();
    const view = render(<RunwareSettings list={LIST} onChange={changed} />);
    const field = screen.getByLabelText("Kennung oder Civitai-Link");
    await user.type(
      field,
      " https://civitai.com/models/548016/x?modelVersionId=861939 ",
    );
    await user.click(
      screen.getByRole("button", { name: "Prüfen und hinzufügen" }),
    );
    await waitFor(() => {
      expect(changed).toHaveBeenCalledWith(added);
    });
    expect(calls[0]?.body).toEqual({
      reference: "https://civitai.com/models/548016/x?modelVersionId=861939",
    });
    expect(field).toHaveProperty("value", "");
    view.rerender(<RunwareSettings list={added} onChange={changed} />);
    expect(screen.getByDisplayValue("PonyXL MIX v2")).toBeDefined();
  });

  it("shows why Runware refused a model and keeps the input", async () => {
    fakeApi({
      "POST /api/images/runware": fail(
        422,
        "Runware führt civitai:277058@1552721 nicht.",
      ),
    });
    const user = userEvent.setup();
    render(<RunwareSettings list={LIST} onChange={vi.fn()} />);
    const field = screen.getByLabelText("Kennung oder Civitai-Link");
    await user.type(field, "civitai:277058@1552721");
    await user.click(
      screen.getByRole("button", { name: "Prüfen und hinzufügen" }),
    );
    expect(
      await screen.findByText("Runware führt civitai:277058@1552721 nicht."),
    ).toBeDefined();
    expect(field).toHaveProperty("value", "civitai:277058@1552721");
  });

  it("edits, removes and saves the list together", async () => {
    const { calls } = fakeApi({ "PUT /api/images/runware": ok(LIST) });
    const changed = vi.fn();
    const user = userEvent.setup();
    render(<RunwareSettings list={LIST} onChange={changed} />);
    expect(
      screen.queryByRole("button", { name: "Änderungen speichern" }),
    ).toBeNull();
    await user.type(
      screen.getByLabelText("Zusatz zur Beschreibung FLUX.2 [dev]"),
      "film grain",
    );
    await user.clear(screen.getByLabelText(`Name ${EPIC}`));
    await user.type(screen.getByLabelText(`Name ${EPIC}`), "Epic");
    await user.clear(screen.getByLabelText("Auslösewort Handcuffs"));
    await user.type(screen.getByLabelText("Auslösewort Handcuffs"), "cuffs");
    await user.clear(screen.getByLabelText(`Name ${CUFFS}`));
    await user.type(screen.getByLabelText(`Name ${CUFFS}`), "Fesseln");
    const weight = screen.getByLabelText("Gewicht Fesseln");
    await user.clear(weight);
    await user.type(weight, "1.2");
    await user.clear(weight);
    await user.type(weight, "3");
    await user.tab();
    expect(weight).toHaveProperty("value", "1.2");
    await user.click(screen.getByRole("button", { name: "Epic entfernen" }));
    await user.click(
      screen.getByRole("button", { name: "Änderungen speichern" }),
    );
    await waitFor(() => {
      expect(changed).toHaveBeenCalledWith(LIST);
    });
    expect(calls[0]?.body).toEqual({
      models: [{ id: FLUX, name: "FLUX.2 [dev]", addition: "film grain" }],
      loras: [{ id: CUFFS, name: "Fesseln", trigger: "cuffs", weight: 1.2 }],
    });
  });

  it("removes a LoRA and says when the list is empty", async () => {
    const { calls } = fakeApi({ "PUT /api/images/runware": ok(LIST) });
    const user = userEvent.setup();
    render(<RunwareSettings list={LIST} onChange={vi.fn()} />);
    await user.click(
      screen.getByRole("button", { name: "Handcuffs entfernen" }),
    );
    expect(screen.getByText("Keine LoRAs.")).toBeDefined();
    await user.click(
      screen.getByRole("button", { name: "Änderungen speichern" }),
    );
    await waitFor(() => {
      expect(calls).toHaveLength(1);
    });
    expect(calls[0]?.body).toMatchObject({ loras: [] });
  });

  it("can only show the list without the key", () => {
    render(
      <RunwareSettings
        list={{ ...LIST, runware: [], loras: [], runware_ready: false }}
        onChange={vi.fn()}
      />,
    );
    expect(screen.getByText(/Runware ist nicht eingerichtet/)).toBeDefined();
    expect(screen.getByText("Keine Grundmodelle.")).toBeDefined();
    expect(screen.getByLabelText("Kennung oder Civitai-Link")).toHaveProperty(
      "disabled",
      true,
    );
  });

  it("names an unknown base", () => {
    render(
      <RunwareSettings
        list={{
          ...LIST,
          runware: [{ ...EPIC_ENTRY, architecture: "" }],
          loras: [{ ...CUFFS_ENTRY, architecture: "" }],
        }}
        onChange={vi.fn()}
      />,
    );
    expect(screen.getAllByText(/Basis unbekannt/)).toHaveLength(2);
  });
});
