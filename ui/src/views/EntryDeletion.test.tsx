import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import { ENTRY, fail, fakeApi, noContent, ok } from "../../fake-api";
import type { EntryDeletion } from "../api";
import { EntryForm } from "./EntryForm";

const PREVIEW = "GET /api/worlds/salzmark/entries/kael/deletion-preview";
const MIRA = {
  ...ENTRY,
  id: "mira",
  name: "Mira",
  aliases: [],
  body: "## Beziehungen\n\n- Schwester von @Kael",
};
const HAFEN = {
  ...ENTRY,
  id: "hafen",
  category: "ort" as const,
  name: "Hafen",
  aliases: [],
  body: "Hier wartet @Kael.",
};
const FULL: EntryDeletion = {
  name: "Kael",
  images: 2,
  markers: 1,
  uses: [
    {
      world: "salzmark",
      world_name: "Die Salzmark",
      story: "ueberfahrt",
      story_title: "Die Überfahrt",
      guest: false,
      relation: false,
      led: true,
      facts: 2,
    },
    {
      world: "nordland",
      world_name: "Nordland",
      story: "eisgang",
      story_title: "Eisgang",
      guest: true,
      relation: true,
      led: false,
      facts: 1,
    },
    {
      world: "nordland",
      world_name: "Nordland",
      story: "schnee",
      story_title: "Schnee",
      guest: true,
      relation: false,
      led: false,
      facts: 0,
    },
  ],
};

afterEach(() => {
  vi.restoreAllMocks();
});

function form(onClose = vi.fn()) {
  render(
    <EntryForm
      world="salzmark"
      entry={ENTRY}
      entries={[ENTRY, MIRA, HAFEN]}
      onClose={onClose}
    />,
  );
  return onClose;
}

describe("deleting a canon entry with its traces (step 10.1, ADR-106)", () => {
  it("names what goes, what stays, and deletes on one click", async () => {
    const { calls } = fakeApi({
      [PREVIEW]: ok(FULL),
      "DELETE /api/worlds/salzmark/entries/kael": noContent(),
    });
    const user = userEvent.setup();
    const onClose = form();

    await user.click(screen.getByRole("button", { name: "Löschen" }));
    const dialog = await screen.findByRole("dialog", {
      name: "„Kael“ löschen?",
    });

    expect(
      within(dialog).getByRole("list", { name: "Dateien" }).textContent,
    ).toBe("2 Bilder und 1 Markierung auf Karten");
    expect(
      within(dialog).getByRole("list", { name: "Geschichten dieser Welt" })
        .textContent,
    ).toBe("„Die Überfahrt“: geführte Figur, 2 Fakten „nur diese Geschichte“");
    const others = within(dialog).getByRole("list", {
      name: "Geschichten anderer Welten",
    });
    expect(
      within(others)
        .getAllByRole("listitem")
        .map((item) => item.textContent),
    ).toEqual([
      "„Eisgang“ (Nordland): Gast-Verbindung mit Weltbezug, 1 Fakt „nur diese Geschichte“",
      "„Schnee“ (Nordland): Gast-Verbindung",
    ]);
    expect(
      within(dialog).getByText(/Erwähnungen mit @ in „Mira“, „Hafen“/),
    ).toBeDefined();
    expect(within(dialog).getByRole("button", { name: "Abbrechen" })).toBe(
      document.activeElement,
    );

    await user.click(
      within(dialog).getByRole("button", { name: "Endgültig löschen" }),
    );
    await waitFor(() => {
      expect(onClose).toHaveBeenCalledWith(null);
    });
    expect(calls.at(-1)?.method).toBe("DELETE");
  });

  it("says so when only the entry goes, and shows a failed preview", async () => {
    fakeApi({
      [PREVIEW]: ok({ name: "Kael", images: 1, markers: 0, uses: [] }),
    });
    const user = userEvent.setup();
    render(<EntryForm world="salzmark" entry={ENTRY} onClose={vi.fn()} />);
    await user.click(screen.getByRole("button", { name: "Löschen" }));
    const dialog = await screen.findByRole("dialog");
    expect(
      within(dialog).getByRole("list", { name: "Dateien" }).textContent,
    ).toBe("1 Bild");
    expect(within(dialog).queryByText(/Erwähnungen/)).toBeNull();
    expect(
      within(dialog).queryByRole("list", { name: "Geschichten dieser Welt" }),
    ).toBeNull();

    fakeApi({ [PREVIEW]: fail(404, "Eintrag fehlt") });
    await user.click(within(dialog).getByRole("button", { name: "Abbrechen" }));
    await user.click(screen.getByRole("button", { name: "Löschen" }));
    expect(await screen.findByText("Eintrag fehlt")).toBeDefined();
    expect(screen.queryByRole("dialog")).toBeNull();
  });

  it("names markers alone and a single fact", async () => {
    fakeApi({
      [PREVIEW]: ok({
        name: "Kael",
        images: 0,
        markers: 3,
        uses: [{ ...FULL.uses[0], led: false, facts: 1 }],
      }),
    });
    const user = userEvent.setup();
    form();
    await user.click(screen.getByRole("button", { name: "Löschen" }));
    const dialog = await screen.findByRole("dialog");
    expect(
      within(dialog).getByRole("list", { name: "Dateien" }).textContent,
    ).toBe("3 Markierungen auf Karten");
    expect(
      within(dialog).getByRole("list", { name: "Geschichten dieser Welt" })
        .textContent,
    ).toBe("„Die Überfahrt“: 1 Fakt „nur diese Geschichte“");
  });
});
