"""Pictures between the paragraphs of a chapter (step 10.6, ADR-110): lines, storage, e-book,
and the text the AI reads."""

import zipfile
from datetime import UTC, datetime
from io import BytesIO
from pathlib import Path

import pytest

from skriptorium.canon import CanonService
from skriptorium.context import ContextBuilder
from skriptorium.manuscript import ImageOrigin, ManuscriptService, without_pictures
from skriptorium.manuscript.pictures import Picture, picture_of, pictures_in
from skriptorium.storage import DocumentStore, InvalidInput, NotFound
from tests.image_samples import jpeg, png

W = "die-salzmark"
S = "der-hafen"
WHEN = datetime(2026, 11, 5, 12, 0, tzinfo=UTC)
FILE = "bild-0123456789ab.jpg"


@pytest.fixture
def ms(tmp_path: Path) -> ManuscriptService:
    store = DocumentStore(tmp_path / "data")
    CanonService(store).create_world("Die Salzmark")
    service = ManuscriptService(store)
    service.create_story(W, "Der Hafen", "kurzgeschichte")
    return service


@pytest.mark.parametrize(
    ("line", "picture"),
    [
        (f"![Der Hafen im Nebel](bild:{FILE})", Picture("Der Hafen im Nebel", FILE)),
        (f"  ![](bild:{FILE})  \r", Picture("", FILE)),
        ("![x](bild:bild-0123456789ab.webp)", Picture("x", "bild-0123456789ab.webp")),
        ("![x](https://example.org/a.png)", None),
        ("![x](bild:../story.md)", None),
        ("![x](bild:bild-0123456789ab.gif)", None),
        (f"Davor ![x](bild:{FILE})", None),
        (f"![x](bild:{FILE}) danach", None),
        ("![a]b](bild:bild-0123456789ab.png)", None),
    ],
)
def test_only_a_line_of_its_own_naming_a_story_picture_counts(
    line: str, picture: Picture | None
) -> None:
    assert picture_of(line) == picture


def test_the_text_for_the_ai_drops_picture_lines_and_nothing_else() -> None:
    text = f"Erster Absatz.\n\n![Hafen](bild:{FILE})\n\nZweiter Absatz.\n![Link](https://x)"
    assert pictures_in(text) == [Picture("Hafen", FILE)]
    assert without_pictures(text) == "Erster Absatz.\n\nZweiter Absatz.\n![Link](https://x)"
    plain = "Kein Bild hier.\n\n\n\nDrei Leerzeilen bleiben."
    assert without_pictures(plain) == plain


def test_stores_reads_and_keeps_the_origin_of_a_picture(ms: ManuscriptService) -> None:
    origin = ImageOrigin("m", "Hafen im Nebel", "3:2", 0.035, "2026-11-05T12:00:00+00:00")
    made = ms.add_story_picture(W, S, jpeg(), origin)
    uploaded = ms.add_story_picture(W, S, png())
    assert made.startswith("bild-") and made.endswith(".jpg")
    assert uploaded.endswith(".png")
    assert ms.story_picture(W, S, made) == (jpeg(), "image/jpeg")
    assert ms.story_picture_origin(W, S, made) == origin
    assert ms.story_picture_origin(W, S, uploaded) is None


def test_refuses_odd_names_missing_pictures_stories_and_files(ms: ManuscriptService) -> None:
    for name in ("../story.md", "titelbild-0123456789ab.jpg", FILE):
        with pytest.raises(NotFound):
            ms.story_picture(W, S, name)
        with pytest.raises(NotFound):
            ms.story_picture_origin(W, S, name)
    with pytest.raises(NotFound):
        ms.add_story_picture(W, "gibt-es-nicht", jpeg())
    with pytest.raises(InvalidInput):
        ms.add_story_picture(W, S, b"<svg/>")


def test_the_e_book_shows_named_pictures_as_figures(ms: ManuscriptService) -> None:
    shown = ms.add_story_picture(W, S, jpeg())
    unused = ms.add_story_picture(W, S, png())
    text = (
        "Der Nebel lag über dem Hafen.\n\n"
        f"![Der Hafen <im> Nebel](bild:{shown})\n\n"
        f"![](bild:{shown})\n"
        "Sie zählte die Laternen.\n\n"
        f"![Fehlt](bild:{FILE})"
    )
    ms.save_chapter(W, S, 1, title="Eins", text=text)
    book = zipfile.ZipFile(BytesIO(ms.epub(W, S, author=None, only_completed=False, modified=WHEN)))
    chapter = book.read("OEBPS/kapitel-01.xhtml").decode("utf-8")
    assert (
        f'<figure><img src="bilder/{shown}" alt="Der Hafen &lt;im&gt; Nebel"/>'
        "<figcaption>Der Hafen &lt;im&gt; Nebel</figcaption></figure>"
    ) in chapter
    assert f'<figure><img src="bilder/{shown}" alt=""/></figure>' in chapter
    assert "<p>Sie zählte die Laternen.</p>" in chapter
    assert "Fehlt" not in chapter and FILE not in chapter
    names = book.namelist()
    assert f"OEBPS/bilder/{shown}" in names
    assert f"OEBPS/bilder/{unused}" not in names
    assert book.read(f"OEBPS/bilder/{shown}") == jpeg()
    package = book.read("OEBPS/content.opf").decode("utf-8")
    assert f'<item id="b1" href="bilder/{shown}" media-type="image/jpeg"/>' in package
    assert package.count("bilder/") == 1


def test_a_picture_gone_missing_is_left_out_of_the_book(
    ms: ManuscriptService, tmp_path: Path
) -> None:
    gone = ms.add_story_picture(W, S, jpeg())
    ms.save_chapter(W, S, 1, title="Eins", text=f"Text.\n\n![Weg](bild:{gone})")
    (tmp_path / "data" / "worlds" / W / "stories" / S / "bilder" / gone).unlink()
    book = zipfile.ZipFile(BytesIO(ms.epub(W, S, author=None, only_completed=False, modified=WHEN)))
    assert "<figure" not in book.read("OEBPS/kapitel-01.xhtml").decode("utf-8")


def test_picture_lines_stay_out_of_the_requests_to_the_ai(tmp_path: Path) -> None:
    store = DocumentStore(tmp_path / "data")
    canon = CanonService(store)
    canon.create_world("Die Salzmark")
    ms = ManuscriptService(store)
    ms.create_story(W, "Der Hafen", "roman")
    ms.save_chapter(W, S, 1, title="Eins", text=f"Am Kai.\n\n![Hafenbild](bild:{FILE})\n\nNebel.")
    ms.save_chapter(W, S, 2, title="Zwei", text=f"![Nur ein Bild](bild:{FILE})")
    builder = ContextBuilder(canon, ms)

    writing = builder.build(W, S, 1, "Weiter.")
    summary = builder.build_chapter_summary(W, S, 1)
    for built in (writing, summary):
        sent = "\n".join(m.content for m in built.messages)
        assert "Am Kai." in sent and "Nebel." in sent
        assert "bild:" not in sent and "Hafenbild" not in sent
    with pytest.raises(InvalidInput, match="noch keinen Text"):
        builder.build_chapter_summary(W, S, 2)
