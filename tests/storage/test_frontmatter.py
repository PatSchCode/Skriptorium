"""Tests for reading and writing the YAML header (ADR-016).

Every case runs with the pure Python classes and with libyaml (ADR-100).
"""

from collections.abc import Iterator

import pytest

from skriptorium.storage import HeaderValue, InvalidInput, frontmatter
from skriptorium.storage.frontmatter import parse, render

_BOTH = [pytest.param(frontmatter.PURE, id="python")]
if frontmatter.FAST is not None:
    _BOTH.append(pytest.param(frontmatter.FAST, id="libyaml"))


@pytest.fixture(autouse=True, params=_BOTH)
def classes(request: pytest.FixtureRequest, monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    """Run the test with one pair of loader and dumper."""
    monkeypatch.setattr(frontmatter, "_classes", request.param)
    yield


def test_libyaml_is_used_when_present() -> None:
    assert frontmatter.FAST is not None, "PyYAML ohne libyaml: Lesen wäre langsam (ADR-100)"
    assert frontmatter.FAST[1].__name__ == "CSafeDumper"


def test_both_write_the_same_text(monkeypatch: pytest.MonkeyPatch) -> None:
    header: dict[str, HeaderValue] = {
        "name": "Anselm Drach",
        "lang": "Ein sehr langer Wert, " * 12,
        "zeichen": "„Zitat“ \u2013 äöüß: #1 ' \" ` @Kael",
        "leer": "",
        "nichts": None,
        "zahlen": [0, -3, 1.5, 0.0123, True, False],
        "anfragen": [{"zeit": "2026-11-04T19:00:00+00:00", "welt": "die-salzmark"}],
    }
    texts = set()
    for pair in (frontmatter.PURE, frontmatter.FAST or frontmatter.PURE):
        monkeypatch.setattr(frontmatter, "_classes", pair)
        texts.add(render(header, "Text\n"))
        assert parse(render(header, "Text\n")) == (header, "Text\n")
    assert len(texts) == 1


def test_round_trip_keeps_header_and_body() -> None:
    header: dict[str, HeaderValue] = {
        "name": "Kael",
        "aliasse": ["No", "On", "012"],
        "kategorie": "figur",
        "kapitel": 3,
        "gast_verbindungen": [{"welt": "salzmark", "eintrag": "ilka"}],
    }
    body = "Kael kam aus dem Norden.\n\nZweiter Absatz: „Zitat“ \u2013 äöüß.\n"
    assert parse(render(header, body)) == (header, body)


def test_written_ambiguous_strings_are_quoted() -> None:
    text = render({"name": "No", "aliasse": ["On", "012"]}, "")
    assert "'No'" in text
    assert "'On'" in text
    assert "'012'" in text


def test_document_without_header_has_empty_header() -> None:
    assert parse("Nur Text.\n") == ({}, "Nur Text.\n")
    assert render({}, "Nur Text.\n") == "Nur Text.\n"


def test_body_starting_with_delimiter_survives_round_trip() -> None:
    body = "---\nkein Kopf, sondern Text\n"
    assert parse(render({}, body)) == ({}, body)


def test_empty_header_block_is_empty_header() -> None:
    assert parse("---\n---\nText") == ({}, "Text")


def test_windows_line_endings_are_accepted() -> None:
    header, body = parse("---\r\nname: Kael\r\n---\r\nText")
    assert header == {"name": "Kael"}
    assert body == "Text"


@pytest.mark.parametrize(
    "value",
    ["No", "yes", "On", "off", "012", "0x1F", "0b101", "1_000", "190:20:30", "1_0.5", ".inf"],
)
def test_ambiguous_hand_written_values_are_rejected(value: str) -> None:
    with pytest.raises(InvalidInput, match="Anführungszeichen"):
        parse(f"---\nwert: {value}\n---\n")


@pytest.mark.parametrize(
    ("value", "expected"),
    [("true", True), ("False", False), ("12", 12), ("-3", -3), ("1.5", 1.5), ("~", None)],
)
def test_plain_values_are_read(value: str, expected: object) -> None:
    assert parse(f"---\nwert: {value}\n---\n")[0] == {"wert": expected}


def test_dates_stay_text() -> None:
    assert parse("---\ndatum: 2026-09-26\n---\n")[0] == {"datum": "2026-09-26"}


@pytest.mark.parametrize(
    "header",
    [
        "name: [nicht geschlossen",
        "- nur\n- eine Liste",
        "1: zahl als Feldname",
        "daten: !!binary aGFsbG8=",
        "menge: !!set {a: null}",
        "objekt: !!python/object:os.system {}",
    ],
)
def test_invalid_headers_are_rejected(header: str) -> None:
    with pytest.raises(InvalidInput):
        parse(f"---\n{header}\n---\n")


def test_unclosed_header_is_rejected() -> None:
    with pytest.raises(InvalidInput, match="nicht mit --- abgeschlossen"):
        parse("---\nname: Kael\nText ohne Ende des Kopfs")
