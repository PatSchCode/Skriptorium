import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router";
import { afterEach, describe, expect, it, vi } from "vitest";
import { catalogModel, fail, fakeApi, modelList, ok } from "../../fake-api";
import type { UsageGroup, UsageStats, UsageTotals } from "../api";
import { Account } from "./Account";
import { Usage } from "./Usage";

function totals(
  requests: number,
  cost: number,
  changes: Partial<UsageTotals> = {},
): UsageTotals {
  return {
    requests,
    input_tokens: requests * 1000,
    output_tokens: requests * 100,
    cost_usd: cost,
    without_cost: 0,
    cache_read_tokens: 0,
    cache_share: null,
    ...changes,
  };
}

function group(
  sums: UsageTotals,
  models: UsageGroup["models"] = [],
): UsageGroup {
  return {
    totals: sums,
    kinds: [
      { kind: "schreiben", ...sums },
      { kind: "weltenbau", ...totals(1, 0.1) },
    ],
    models,
  };
}

const MONTH = new Date().toISOString().slice(0, 7);

const STATS: UsageStats = {
  month: MONTH,
  months: [MONTH, "2026-09"],
  total: group(totals(7, 6.42, { without_cost: 2, cache_share: 0.58 })),
  worlds: [
    {
      id: "die-salzmark",
      name: "Die Salzmark",
      archived: false,
      deleted: false,
      usage: group(totals(4, 4.61, { cache_share: 0.61 }), [
        { model: "x-ai/grok-4.6", ...totals(2, 3) },
        { model: "x-ai/grok-4.7", ...totals(1, 1, { input_tokens: 90000 }) },
        {
          model: "black-forest-labs/flux.2-pro",
          ...totals(1, 0.49, { input_tokens: 0, output_tokens: 0 }),
        },
      ]),
      own: group(totals(1, 1.03)),
      stories: [
        {
          id: "das-salz-der-toten",
          title: "Das Salz der Toten",
          form: "roman",
          archived: true,
          deleted: false,
          usage: group(totals(2, 3.58)),
        },
        {
          id: "weg",
          title: null,
          form: null,
          archived: false,
          deleted: true,
          usage: group(totals(1, 0.01)),
        },
      ],
    },
    {
      id: "verschwunden",
      name: null,
      archived: false,
      deleted: true,
      usage: group(totals(1, 1.22)),
      own: group(totals(1, 1.22)),
      stories: [],
    },
  ],
  unassigned: group(totals(2, 0.59)),
};

const EMPTY: UsageStats = {
  month: MONTH,
  months: [],
  total: group(totals(0, 0)),
  worlds: [],
  unassigned: group(totals(0, 0)),
};

function usageApi(stats: UsageStats = STATS) {
  return fakeApi({
    "GET /api/usage/stats": ok(stats),
    "GET /api/models": ok(
      modelList(
        ["x-ai/grok-4.6"],
        [catalogModel("x-ai/grok-4.6", { name: "SpaceXAI: Grok 4.6" })],
      ),
    ),
    "GET /api/images/models": ok({
      default: "black-forest-labs/flux.2-pro",
      models: [
        {
          id: "black-forest-labs/flux.2-pro",
          name: "FLUX.2 Pro",
          references: 1,
        },
      ],
      available: true,
      ready: true,
    }),
  });
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe("Verbrauch (step 9.11, ADR-100)", () => {
  it("shows the month by world with the requests before the change and the sum", async () => {
    const { calls } = usageApi();
    render(<Usage />);

    const table = await screen.findByRole("table");
    expect(calls[0]?.path).toBe(`/api/usage/stats?month=${MONTH}`);
    expect(
      screen.getByText(/6,42 \$ für 7 Anfragen · 7\.000 Token ein, 700 aus/),
    ).toBeDefined();
    expect(screen.getAllByText("58 %")).toHaveLength(2);
    expect(screen.getByText(/2 Anfragen ohne gemeldete Kosten/)).toBeDefined();
    const rows = within(table).getAllByRole("row");
    expect(rows.map((row) => row.textContent)).toEqual([
      expect.stringContaining("Welt") as string,
      expect.stringContaining("▸ Die Salzmark") as string,
      expect.stringContaining("▸ gelöschte Welt (verschwunden)") as string,
      expect.stringContaining("ohne Zuordnung") as string,
      expect.stringContaining("Summe") as string,
    ]);
    expect(rows[1]?.textContent).toContain("4,61 $");
    expect(rows[1]?.textContent).toContain("61 %");
    expect(rows[4]?.textContent).toContain("7.700");
  });

  it("opens a world to its stories and shows it by kind and by model", async () => {
    usageApi();
    const user = userEvent.setup();
    render(<Usage />);

    await user.click(
      await screen.findByRole("button", { name: /Die Salzmark/ }),
    );

    const table = screen.getAllByRole("table")[0] as HTMLTableElement;
    expect(within(table).getByText("Das Salz der Toten")).toBeDefined();
    expect(within(table).getByText("Roman (archiviert)")).toBeDefined();
    expect(within(table).getByText("gelöschte Geschichte (weg)")).toBeDefined();
    expect(within(table).getByText("Welt selbst")).toBeDefined();
    expect(
      screen.getByRole("heading", { name: "Die Salzmark – nach Art" }),
    ).toBeDefined();
    expect(screen.getByText("Weltenbauer")).toBeDefined();
    const models = screen.getAllByRole("table")[1];
    if (models === undefined) {
      throw new Error("keine Modell-Tabelle");
    }
    const names = () =>
      within(models)
        .getAllByRole("row")
        .slice(1)
        .map((row) => (row as HTMLTableRowElement).cells[0]?.textContent);
    expect(names()).toEqual(["Grok 4.6", "x-ai/grok-4.7", "FLUX.2 Pro"]);
    const flux = within(models)
      .getByText("FLUX.2 Pro")
      .closest<HTMLTableRowElement>("tr");
    expect(flux?.cells[2]?.textContent).toBe("–");

    await user.click(screen.getByRole("button", { name: "nach Token" }));
    expect(names()).toEqual(["x-ai/grok-4.7", "Grok 4.6", "FLUX.2 Pro"]);
    await user.click(screen.getByRole("button", { name: "nach Anzahl" }));
    expect(names()[0]).toBe("Grok 4.6");

    await user.click(
      screen.getByRole("button", { name: "Das Salz der Toten" }),
    );
    expect(
      screen.getByRole("heading", { name: "Das Salz der Toten – nach Art" }),
    ).toBeDefined();
    await user.click(
      screen.getByRole("button", { name: "gelöschte Geschichte (weg)" }),
    );
    expect(
      screen.getByRole("heading", {
        name: "gelöschte Geschichte (weg) – Modelle",
      }),
    ).toBeDefined();

    // Back to the world, then closed.
    await user.click(screen.getByRole("button", { name: /Die Salzmark/ }));
    expect(
      screen.getByRole("heading", { name: "Die Salzmark – Modelle" }),
    ).toBeDefined();
    await user.click(screen.getByRole("button", { name: /Die Salzmark/ }));
    expect(screen.queryByText("Welt selbst")).toBeNull();
    expect(screen.queryByRole("heading", { name: /nach Art/ })).toBeNull();
  });

  it("loads all months and names the months", async () => {
    const { calls } = usageApi();
    const user = userEvent.setup();
    render(<Usage />);

    const period = await screen.findByRole("combobox", { name: "Zeitraum" });
    expect(
      [...(period as HTMLSelectElement).options].map((option) => option.text),
    ).toEqual([expect.any(String) as string, "September 2026", "Alle Monate"]);
    await user.selectOptions(period, "Alle Monate");
    expect(calls.at(-1)?.path).toBe("/api/usage/stats");
    await user.selectOptions(period, "September 2026");
    expect(calls.at(-1)?.path).toBe("/api/usage/stats?month=2026-09");
  });

  it("says when there were no requests and offers this month anyway", async () => {
    usageApi(EMPTY);
    render(<Usage />);

    expect(
      await screen.findByText("Keine Anfragen in diesem Zeitraum."),
    ).toBeDefined();
    const period = screen.getByRole("combobox", { name: "Zeitraum" });
    expect((period as HTMLSelectElement).options).toHaveLength(2);
    expect(
      screen.queryByText(/der Eingabe aus dem Zwischenspeicher/),
    ).toBeNull();
  });

  it("shows model ids while the model lists fail, and a failed load", async () => {
    fakeApi({
      "GET /api/usage/stats": ok(STATS),
      "GET /api/models": fail(503, "OpenRouter nicht erreichbar"),
      "GET /api/images/models": fail(503, "OpenRouter nicht erreichbar"),
    });
    const user = userEvent.setup();
    const { unmount } = render(<Usage />);
    await user.click(
      await screen.findByRole("button", { name: /Die Salzmark/ }),
    );
    expect(screen.getByText("x-ai/grok-4.6")).toBeDefined();
    unmount();

    fakeApi({
      "GET /api/usage/stats": fail(422, "Monat muss die Form JJJJ-MM haben"),
    });
    render(<Usage />);
    expect(await screen.findByText(/Monat muss die Form/)).toBeDefined();
  });

  it("is linked from the costs of the month in the account", async () => {
    fakeApi({
      "GET /api/usage": ok({
        month: MONTH,
        requests: 1,
        input_tokens: 10,
        output_tokens: 1,
        cost_usd: 0.01,
        without_cost: 0,
      }),
      "GET /api/auth/sessions": ok([]),
    });
    render(
      <MemoryRouter>
        <Account />
      </MemoryRouter>,
    );
    const link = await screen.findByRole("link", {
      name: "Aufteilung nach Welt, Geschichte und Modell",
    });
    expect(link.getAttribute("href")).toBe("/verbrauch");
  });
});
