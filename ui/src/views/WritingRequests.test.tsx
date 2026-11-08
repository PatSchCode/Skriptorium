import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { useState } from "react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { fail, fakeApi, ok } from "../../fake-api";
import type { RequestSummary, WritingRequest } from "../api";
import { WritingRequests } from "./WritingRequests";

const REQUESTS = "/api/worlds/salzmark/stories/ueberfahrt/requests";

afterEach(() => {
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});

const SUMMARY: RequestSummary = {
  id: "20261108-140205",
  at: "2026-11-08T14:02:05Z",
  chapter: 4,
  model: "x-ai/grok-4.6",
  estimated_tokens: 23410,
  input_tokens: 23000,
  output_tokens: 512,
  cost_usd: 0.05,
  outcome: "ok",
  instruction: "Mara betritt den Turm.",
  taken_over: false,
};

const REQUEST: WritingRequest = {
  ...SUMMARY,
  length: "mittel",
  instruction: "Mara betritt den Turm.",
  blocks: [
    { kind: "rahmen", label: "Rahmen", tokens: 812 },
    { kind: "kapiteltext", label: "Kapiteltext", tokens: 21000 },
  ],
  pictures: ["Mara", "Turm"],
  messages: [
    { role: "system", content: "# Rahmen\n\nDu schreibst mit." },
    { role: "user", content: "# Anweisung\n\nMara betritt den Turm." },
  ],
  answer: "HINWEIS: Der Turm ist eingestürzt.\nMara stand vor Trümmern.",
};

/** The time of SUMMARY as the list shows it, in the time zone of the machine. */
const SHOWN = new Intl.DateTimeFormat("de-DE", {
  day: "2-digit",
  month: "2-digit",
  hour: "2-digit",
  minute: "2-digit",
}).format(new Date(SUMMARY.at));

/** The tab as the chapter view holds it: the open request lives above it. */
function Tab() {
  const [shown, setShown] = useState<string | null>(null);
  return (
    <WritingRequests
      world="salzmark"
      story="ueberfahrt"
      shown={shown}
      onShow={setShown}
    />
  );
}

describe("WritingRequests (step 10.9, ADR-116)", () => {
  it("lists the requests newest first with chapter, model, tokens, cost and status", async () => {
    fakeApi({
      [`GET ${REQUESTS}`]: ok([
        { ...SUMMARY, taken_over: true, id: "a" },
        { ...SUMMARY, id: "b" },
        {
          ...SUMMARY,
          id: "c",
          outcome: "abgebrochen",
          input_tokens: null,
          output_tokens: null,
          cost_usd: null,
        },
        {
          ...SUMMARY,
          id: "d",
          outcome: "zu_viele_anfragen",
          instruction: "x".repeat(100),
        },
      ]),
    });
    render(<Tab />);

    const rows = (await screen.findAllByRole("row")).slice(1);
    const cells = rows.map((row) =>
      within(row)
        .getAllByRole("cell")
        .map((cell) => cell.textContent),
    );
    expect(cells[0]).toEqual([
      SHOWN,
      "Kap. 4",
      "grok-4.6",
      "23.410 Token",
      "0,05 $",
      "übernommen",
      "„Mara betritt den Turm.“",
    ]);
    expect(cells.map((row) => row[5])).toEqual([
      "übernommen",
      "verworfen",
      "abgebrochen",
      "Fehler",
    ]);
    expect(cells[2]?.[4]).toBe("–");
    expect(cells[3]?.[6]).toBe(`„${"x".repeat(60)} …“`);
    expect(screen.getByTitle(/zu viele Anfragen/)).toBeDefined();
  });

  it("shows a request with its blocks and, to open, its messages and the answer", async () => {
    const { calls } = fakeApi({
      [`GET ${REQUESTS}`]: ok([SUMMARY]),
      [`GET ${REQUESTS}/20261108-140205`]: ok(REQUEST),
    });
    const user = userEvent.setup();
    render(<Tab />);

    await user.click(await screen.findByRole("button", { name: SHOWN }));

    const shown = await screen.findByRole("article", {
      name: `Anfrage vom ${SHOWN}`,
    });
    expect(
      within(shown).getByText(
        "Modell grok-4.6 · Länge mittel · 2 Bilder (Mara, Turm) · geschätzt 23.410 / 30.000 Token",
      ),
    ).toBeDefined();
    expect(
      within(shown).getByText(
        "Gemeldet: 23.000 Token ein, 512 aus · Kosten 0,05 $",
      ),
    ).toBeDefined();
    const blocks = within(shown)
      .getAllByRole("row")
      .slice(1)
      .map((row) => row.textContent);
    expect(blocks).toEqual(["Rahmen812", "Kapiteltext21.000"]);
    const summaries = shown.querySelectorAll("summary");
    expect([...summaries].map((summary) => summary.textContent)).toEqual([
      "Wortlaut: Systemnachricht",
      "Wortlaut: Nutzernachricht",
      "Antwort der KI",
    ]);
    const answer = within(shown).getByText(/Mara stand vor Trümmern/);
    expect(answer.textContent).toBe(REQUEST.answer);
    expect(answer.closest("details")?.open).toBe(false);
    await user.click(within(shown).getByText("Antwort der KI"));
    expect(answer.closest("details")?.open).toBe(true);
    expect(
      screen.getByRole("button", { name: SHOWN, pressed: true }),
    ).toBeDefined();
    expect(calls.map((call) => call.path)).toEqual([
      REQUESTS,
      `${REQUESTS}/20261108-140205`,
    ]);
  });

  it("names a request without images, usage or answer", async () => {
    fakeApi({
      [`GET ${REQUESTS}`]: ok([SUMMARY]),
      [`GET ${REQUESTS}/20261108-140205`]: ok({
        ...REQUEST,
        pictures: ["Mara"],
        input_tokens: null,
        output_tokens: null,
        cost_usd: null,
        outcome: "abgebrochen",
        messages: [{ role: "assistant", content: "Früher." }],
        answer: "",
      }),
    });
    const user = userEvent.setup();
    render(<Tab />);
    await user.click(await screen.findByRole("button", { name: SHOWN }));

    expect(await screen.findByText(/· 1 Bild \(Mara\) ·/)).toBeDefined();
    expect(
      screen.getByText("Gemeldet: keine Token · Kosten nicht gemeldet"),
    ).toBeDefined();
    expect(screen.getByText("Wortlaut: Antwort im Gespräch")).toBeDefined();
    expect(screen.getByText("(keine Antwort)")).toBeDefined();
  });

  it("says when there are none, when a request is gone and when loading fails", async () => {
    fakeApi({
      [`GET ${REQUESTS}`]: ok([]),
    });
    const { unmount } = render(<Tab />);
    expect(
      await screen.findByText("Noch keine Anfragen in dieser Geschichte."),
    ).toBeDefined();
    unmount();

    fakeApi({
      [`GET ${REQUESTS}`]: ok([{ ...SUMMARY, pictures: [] }]),
      [`GET ${REQUESTS}/20261108-140205`]: fail(404, "Nicht gefunden"),
    });
    const user = userEvent.setup();
    render(<Tab />);
    await user.click(await screen.findByRole("button", { name: SHOWN }));
    expect((await screen.findByRole("alert")).textContent).toContain(
      "Nicht gefunden",
    );
  });

  it("names a request without images as such", async () => {
    fakeApi({
      [`GET ${REQUESTS}`]: ok([SUMMARY]),
      [`GET ${REQUESTS}/20261108-140205`]: ok({ ...REQUEST, pictures: [] }),
    });
    const user = userEvent.setup();
    render(<Tab />);
    await user.click(await screen.findByRole("button", { name: SHOWN }));
    expect(await screen.findByText(/· ohne Bilder ·/)).toBeDefined();
  });
});
