import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import { ENTRY, fakeApi, ok } from "../../fake-api";
import { shrinkImage } from "../files";
import { pictureLine, pictureOf, placePicture } from "../pictures";
import { CanonPicturePicker } from "./CanonPicturePicker";
import { ManuscriptEditor } from "./ManuscriptEditor";
import { StoryPictureButton, StoryPictureDialog } from "./StoryPictureButton";

vi.mock("../files", () => ({
  GENERATED_SIDE: 4096,
  IMAGE_SIDE: 2000,
  shrinkImage: vi.fn(() => Promise.resolve(new Blob(["klein"]))),
  base64: vi.fn(() => Promise.resolve("a2xlaW4=")),
}));

const FILE = "bild-0123456789ab.jpg";
const STORY_IMAGES = "POST /api/worlds/salzmark/stories/der-hafen/images";

afterEach(() => {
  vi.restoreAllMocks();
});

describe("picture lines (step 10.6, ADR-110)", () => {
  it("knows its own form only", () => {
    expect(pictureOf(`![Hafen](bild:${FILE})`)).toEqual({
      caption: "Hafen",
      file: FILE,
    });
    expect(pictureOf(`  ![ ](bild:${FILE}) \r`)).toEqual({
      caption: "",
      file: FILE,
    });
    expect(pictureOf("![x](https://example.org/a.png)")).toBeNull();
    expect(pictureOf(`Text ![x](bild:${FILE})`)).toBeNull();
    expect(pictureLine("Der [alte]\nHafen", FILE)).toBe(
      `![Der alte Hafen](bild:${FILE})`,
    );
  });

  it("goes after the line of the cursor, as a paragraph of its own", () => {
    const line = `![](bild:${FILE})`;
    const text = "Erster Satz. Zweiter Satz.\n\nNächster Absatz.";
    const placed = placePicture(text, 5, line);
    const result =
      text.slice(0, placed.from) + placed.insert + text.slice(placed.to);
    expect(result).toBe(
      `Erster Satz. Zweiter Satz.\n\n${line}\n\nNächster Absatz.`,
    );
    expect(result.slice(0, placed.cursor).endsWith(`${line}\n\n`)).toBe(true);
    const atEnd = placePicture("Nur ein Absatz.\n\n", 17, line);
    expect(atEnd.insert).toBe(`\n\n${line}\n`);
    expect(atEnd.from).toBe(15);
    expect(placePicture("", 0, line).insert).toBe(`${line}\n`);
  });
});

describe("pictures in the editor", () => {
  it("shows a preview below a picture line and puts new lines in at the cursor", async () => {
    const onChange = vi.fn();
    const source = (file: string) => `/bilder/${file}`;
    const { rerender, container } = render(
      <ManuscriptEditor
        label="Manuskript"
        value={`Am Kai.\n\n![Hafen](bild:${FILE})\n\n![x](https://fremd/a.png)`}
        onChange={onChange}
        pictureSrc={source}
      />,
    );
    await screen.findByLabelText("Manuskript");
    const previews = container.querySelectorAll("img.manuscript-picture");
    expect(previews).toHaveLength(1);
    expect(previews[0]?.getAttribute("src")).toBe(`/bilder/${FILE}`);
    expect(previews[0]?.getAttribute("alt")).toBe("Hafen");

    const content = await screen.findByLabelText("Manuskript");
    const view = (await import("@codemirror/view")).EditorView.findFromDOM(
      content,
    );
    view?.dispatch({ selection: { anchor: 2 } });
    rerender(
      <ManuscriptEditor
        label="Manuskript"
        value={`Am Kai.\n\n![Hafen](bild:${FILE})\n\n![x](https://fremd/a.png)`}
        onChange={onChange}
        pictureSrc={source}
        insertion={{ id: 1, line: "![Neu](bild:bild-ffffffffffff.png)" }}
      />,
    );
    expect(onChange).toHaveBeenLastCalledWith(
      `Am Kai.\n\n![Neu](bild:bild-ffffffffffff.png)\n\n![Hafen](bild:${FILE})\n\n![x](https://fremd/a.png)`,
    );
    expect(container.querySelectorAll("img.manuscript-picture")).toHaveLength(
      2,
    );
  });
});

describe("＋ Bild", () => {
  it("uploads a picture as JPEG and hands over its line; the other ways open a dialog", async () => {
    const { calls } = fakeApi({
      [STORY_IMAGES]: () => ({ status: 201, body: { file: FILE } }),
    });
    const inserted = vi.fn();
    const way = vi.fn();
    const user = userEvent.setup();
    render(
      <StoryPictureButton
        world="salzmark"
        story="der-hafen"
        onWay={way}
        onInsert={inserted}
      />,
    );
    await user.click(screen.getByRole("button", { name: "＋ Bild" }));
    await user.click(
      screen.getByRole("menuitem", { name: "✨ Bild erzeugen" }),
    );
    expect(way).toHaveBeenLastCalledWith("erzeugen");
    await user.click(screen.getByRole("button", { name: "＋ Bild" }));
    await user.click(screen.getByRole("menuitem", { name: "Aus dem Kanon …" }));
    expect(way).toHaveBeenLastCalledWith("kanon");
    await user.click(screen.getByRole("button", { name: "＋ Bild" }));
    expect(
      screen.getByRole("menuitem", { name: "Bild hochladen" }),
    ).toBeDefined();

    await user.upload(
      screen.getByLabelText("Bild für das Kapitel"),
      new File(["x"], "foto.png", { type: "image/png" }),
    );
    await waitFor(() => {
      expect(inserted).toHaveBeenCalledWith(`![](bild:${FILE})`);
    });
    expect(vi.mocked(shrinkImage).mock.calls.at(-1)?.slice(1)).toEqual([
      2000,
      true,
    ]);
    expect(calls.at(-1)?.body).toEqual({ content: "a2xlaW4=" });
  });

  it("shows why an upload failed", async () => {
    fakeApi({
      [STORY_IMAGES]: () => ({ status: 422, body: { detail: "Kein Bild" } }),
    });
    const user = userEvent.setup();
    render(
      <StoryPictureButton
        world="salzmark"
        story="der-hafen"
        onWay={vi.fn()}
        onInsert={vi.fn()}
      />,
    );
    await user.upload(
      screen.getByLabelText("Bild für das Kapitel"),
      new File(["x"], "foto.png", { type: "image/png" }),
    );
    expect(await screen.findByText("Kein Bild")).toBeDefined();
  });

  it("generates a picture from the marked passage and keeps it up to 4096 pixels", async () => {
    const { calls } = fakeApi({
      "GET /api/images/models": ok({
        default: "x/y",
        models: [{ id: "x/y", name: "Y", references: 0 }],
        available: true,
        ready: true,
      }),
      "GET /api/images/price": ok({ cost_usd: 0.04, unit: "image" }),
      "POST /api/images/generate": ok({
        content: "iVBORw0KGgo=",
        media_type: "image/png",
        cost_usd: 0.04,
        model: "x/y",
      }),
      [STORY_IMAGES]: () => ({ status: 201, body: { file: FILE } }),
    });
    const inserted = vi.fn();
    const closed = vi.fn();
    const user = userEvent.setup();
    render(
      <StoryPictureDialog
        world="salzmark"
        story="der-hafen"
        way="erzeugen"
        marked="  Nebel über dem Hafen  "
        onInsert={inserted}
        onClose={closed}
      />,
    );
    expect(screen.getByLabelText("Bildbeschreibung (änderbar)")).toHaveProperty(
      "value",
      "Nebel über dem Hafen",
    );
    await user.click(
      await screen.findByRole("button", { name: "✨ Erzeugen" }),
    );
    await user.click(
      await screen.findByRole("button", { name: "Ins Kapitel einfügen" }),
    );
    await waitFor(() => {
      expect(inserted).toHaveBeenCalledWith(`![](bild:${FILE})`);
    });
    expect(closed).toHaveBeenCalled();
    expect(vi.mocked(shrinkImage).mock.calls.at(-1)?.slice(1)).toEqual([
      4096,
      true,
    ]);
    expect(calls.find((c) => c.path.endsWith("/generate"))?.body).toMatchObject(
      {
        world: "salzmark",
        story: "der-hafen",
      },
    );
    expect(calls.at(-1)?.body).toMatchObject({
      herkunft: { model: "x/y", prompt: "Nebel über dem Hafen" },
    });
  });
});

describe("Aus dem Kanon …", () => {
  const MIRA = {
    ...ENTRY,
    id: "mira",
    name: "Mira",
    images: ["mira-a.webp", "mira-b.webp"],
  };
  const PLAIN = { ...ENTRY, id: "ohne", name: "Ohne Bild", images: [] };
  const KAEL = { ...ENTRY, id: "kael", name: "Kael", images: ["kael-a.webp"] };

  it("copies a chosen image with caption and origin", async () => {
    fakeApi({
      "GET /api/worlds/salzmark/entries": ok([PLAIN, MIRA, KAEL]),
      "GET /api/worlds/salzmark/entries/kael/images/kael-a.webp": ok("bild"),
      "GET /api/worlds/salzmark/entries/kael/images/kael-a.webp/origin": ok({
        model: "m",
        prompt: "Kael",
        aspect_ratio: "2:3",
        cost_usd: 0.04,
        date: "2026-11-05T10:00:00+00:00",
        basis: null,
      }),
      [STORY_IMAGES]: () => ({ status: 201, body: { file: FILE } }),
    });
    const inserted = vi.fn();
    const closed = vi.fn();
    const user = userEvent.setup();
    render(
      <StoryPictureDialog
        world="salzmark"
        story="der-hafen"
        way="kanon"
        marked=""
        onInsert={inserted}
        onClose={closed}
      />,
    );
    const entry = await screen.findByLabelText("Eintrag");
    expect(
      [...entry.querySelectorAll("option")].map((o) => o.textContent),
    ).toEqual(["Mira", "Kael"]);
    expect(screen.getByLabelText("Beschriftung")).toHaveProperty(
      "value",
      "Mira",
    );
    expect(
      screen.getByRole("radio", { name: "Bild 1 von Mira" }),
    ).toHaveProperty("ariaChecked", "true");
    await user.click(screen.getByRole("radio", { name: "Bild 2 von Mira" }));
    await user.selectOptions(entry, "kael");
    expect(screen.getByLabelText("Beschriftung")).toHaveProperty(
      "value",
      "Kael",
    );
    await user.clear(screen.getByLabelText("Beschriftung"));
    await user.type(screen.getByLabelText("Beschriftung"), "Kael am Kai");
    await user.click(screen.getByRole("button", { name: "Einfügen" }));
    await waitFor(() => {
      expect(inserted).toHaveBeenCalledWith(`![Kael am Kai](bild:${FILE})`);
    });
    expect(closed).toHaveBeenCalled();
  });

  it("keeps the dialog and shows why storing the copy failed", async () => {
    fakeApi({
      "GET /api/worlds/salzmark/entries": ok([KAEL]),
      "GET /api/worlds/salzmark/entries/kael/images/kael-a.webp": ok("bild"),
      "GET /api/worlds/salzmark/entries/kael/images/kael-a.webp/origin": ok({
        model: "m",
        prompt: "Kael",
        aspect_ratio: "16:9",
        cost_usd: null,
        date: "2026-11-05T10:00:00+00:00",
        basis: "Bild 1 von Mira",
        resolution: "2K",
        quality: "high",
      }),
      [STORY_IMAGES]: () => ({ status: 422, body: { detail: "Zu groß" } }),
    });
    const closed = vi.fn();
    const user = userEvent.setup();
    render(
      <StoryPictureDialog
        world="salzmark"
        story="der-hafen"
        way="kanon"
        marked=""
        onInsert={vi.fn()}
        onClose={closed}
      />,
    );
    await screen.findByLabelText("Eintrag");
    await user.click(screen.getByRole("button", { name: "Einfügen" }));
    expect(await screen.findByText("Zu groß")).toBeDefined();
    expect(closed).not.toHaveBeenCalled();
    expect(screen.getByRole("button", { name: "Einfügen" })).toHaveProperty(
      "disabled",
      false,
    );
  });

  it("carries the whole origin of a canon image over to its copy", async () => {
    const { calls } = fakeApi({
      "GET /api/worlds/salzmark/entries": ok([KAEL]),
      "GET /api/worlds/salzmark/entries/kael/images/kael-a.webp": ok("bild"),
      "GET /api/worlds/salzmark/entries/kael/images/kael-a.webp/origin": ok({
        model: "m",
        prompt: "Kael",
        aspect_ratio: "2:3",
        cost_usd: 0.09,
        date: "2026-11-05T10:00:00+00:00",
        basis: "Bild 1 von Mira",
        resolution: "2K",
        quality: "high",
      }),
      [STORY_IMAGES]: () => ({ status: 201, body: { file: FILE } }),
    });
    const user = userEvent.setup();
    render(
      <StoryPictureDialog
        world="salzmark"
        story="der-hafen"
        way="kanon"
        marked=""
        onInsert={vi.fn()}
        onClose={vi.fn()}
      />,
    );
    await screen.findByLabelText("Eintrag");
    await user.click(screen.getByRole("button", { name: "Einfügen" }));
    await waitFor(() => {
      expect(calls.at(-1)?.body).toEqual({
        content: "a2xlaW4=",
        herkunft: {
          model: "m",
          prompt: "Kael",
          aspect_ratio: "2:3",
          cost_usd: 0.09,
          basis: "Bild 1 von Mira",
          resolution: "2K",
          quality: "high",
        },
      });
    });
  });

  it("says so when no entry has an image, and shows failures", async () => {
    fakeApi({ "GET /api/worlds/salzmark/entries": ok([PLAIN]) });
    const { unmount } = render(
      <CanonPicturePicker
        world="salzmark"
        onPick={vi.fn()}
        onClose={vi.fn()}
      />,
    );
    expect(
      await screen.findByText("In dieser Welt hat noch kein Eintrag ein Bild."),
    ).toBeDefined();
    expect(screen.getByRole("button", { name: "Einfügen" })).toHaveProperty(
      "disabled",
      true,
    );
    unmount();

    fakeApi({
      "GET /api/worlds/salzmark/entries": ok([KAEL]),
      "GET /api/worlds/salzmark/entries/kael/images/kael-a.webp": () => ({
        status: 404,
        body: { detail: "weg" },
      }),
    });
    const user = userEvent.setup();
    const picked = vi.fn();
    const { unmount: unmount2 } = render(
      <CanonPicturePicker world="salzmark" onPick={picked} onClose={vi.fn()} />,
    );
    await screen.findByLabelText("Eintrag");
    await user.click(screen.getByRole("button", { name: "Einfügen" }));
    expect(
      await screen.findByText("Das Bild des Eintrags ließ sich nicht laden."),
    ).toBeDefined();
    expect(picked).not.toHaveBeenCalled();
    unmount2();

    fakeApi({
      "GET /api/worlds/salzmark/entries": () => ({
        status: 500,
        body: { detail: "Liste kaputt" },
      }),
    });
    render(
      <CanonPicturePicker
        world="salzmark"
        onPick={vi.fn()}
        onClose={vi.fn()}
      />,
    );
    expect(await screen.findByText("Liste kaputt")).toBeDefined();
  });
});

describe("＋ Bild in a chapter (step 10.6)", () => {
  it("puts a picture from the canon in after the line of the cursor, with its preview", async () => {
    const { EditorView } = await import("@codemirror/view");
    const { StoryPage } = await import("./StoryPage");
    const { CHAPTER, STORY, WORLD, modelList } = await import("../../fake-api");
    const base = `/api/worlds/${STORY.world}/stories/${STORY.id}`;
    const kael = { ...ENTRY, images: ["kael-a.webp"] };
    fakeApi({
      "GET /api/models": ok(modelList(["x-ai/grok-4.7"])),
      "GET /api/worlds": ok([WORLD]),
      [`GET /api/worlds/${STORY.world}/entries`]: ok([kael]),
      [`GET /api/worlds/${STORY.world}/entries/kael/images/kael-a.webp`]:
        ok("bild"),
      [`GET /api/worlds/${STORY.world}/entries/kael/images/kael-a.webp/origin`]:
        ok(null),
      [`GET ${base}/chapters`]: ok([{ ...CHAPTER, text: "Am Kai.\n\nNebel." }]),
      [`POST ${base}/images`]: () => ({ status: 201, body: { file: FILE } }),
    });
    const user = userEvent.setup();
    const { container } = render(<StoryPage story={STORY} />);
    const content = await screen.findByLabelText("Manuskript");
    EditorView.findFromDOM(content)?.dispatch({ selection: { anchor: 2 } });

    await user.click(screen.getByRole("button", { name: "＋ Bild" }));
    await user.click(screen.getByRole("menuitem", { name: "Aus dem Kanon …" }));
    await screen.findByRole("group", { name: "Bild aus dem Kanon" });
    await user.click(await screen.findByRole("button", { name: "Einfügen" }));

    await waitFor(() => {
      expect(content.textContent).toContain(`![Kael](bild:${FILE})`);
    });
    expect(
      screen.queryByRole("group", { name: "Bild aus dem Kanon" }),
    ).toBeNull();
    const preview = container.querySelector("img.manuscript-picture");
    expect(preview?.getAttribute("src")).toBe(`${base}/images/${FILE}`);
  });
});
