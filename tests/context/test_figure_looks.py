"""Request of the figure assistant for an English image description (11.5, ADR-123)."""

from pathlib import Path

import pytest

from skriptorium.canon import LOOKS_LABELS, CanonService, InvalidInput, NotFound
from skriptorium.context import MIN_AGE, ContextBuilder, check_answers
from skriptorium.manuscript import ManuscriptService
from skriptorium.storage import DocumentStore

W = "die-salzmark"
ANSWERS = {"Alter": "26", "Haar": "kupferrot,  glatt", "Augen": "grün"}


@pytest.fixture
def builder(tmp_path: Path) -> ContextBuilder:
    store = DocumentStore(tmp_path / "data")
    canon = CanonService(store)
    canon.create_world("Die Salzmark")
    canon.create_entry(
        W,
        "figur",
        "Liv",
        body=(
            "Fährfrau am Nordsund.\n\n### Aussehen\n\nSommersprossen.\n\n"
            "### Bildbeschreibung\n\na 30-year-old adult woman\n\n### Wesen\n\nlaut"
        ),
    )
    canon.create_entry(W, "ort", "Kerrow", body="Hafen.")
    return ContextBuilder(canon, ManuscriptService(store))


def test_the_request_holds_frame_answers_and_entry(builder: ContextBuilder) -> None:
    system, user = builder.build_figure_looks(W, "liv", ANSWERS).messages
    assert "a <Alter>-year-old adult" in system.content
    assert "keine Kleidung" in system.content
    assert "Fesseln" in system.content
    assert "Erfinde keine Merkmale" in system.content
    assert "- Alter: 26" in user.content
    assert "- Haar: kupferrot, glatt" in user.content
    assert "- Herkunft: (keine Angabe)" in user.content
    assert user.content.index("- Herkunft") < user.content.index("- Alter")
    assert "# Liv" in user.content
    assert "Sommersprossen" in user.content
    assert "laut" in user.content


def test_the_former_image_description_stays_out(builder: ContextBuilder) -> None:
    _, user = builder.build_figure_looks(W, "liv", ANSWERS).messages
    assert "Bildbeschreibung" not in user.content
    assert "30-year-old" not in user.content


def test_only_figures(builder: ContextBuilder) -> None:
    with pytest.raises(InvalidInput, match="nur für Figuren"):
        builder.build_figure_looks(W, "kerrow", ANSWERS)
    with pytest.raises(NotFound):
        builder.build_figure_looks(W, "niemand", ANSWERS)


@pytest.mark.parametrize("age", ["", "17", "0", "sechsundzwanzig", "26 Jahre", "1000", "-20"])
def test_only_adults(builder: ContextBuilder, age: str) -> None:
    with pytest.raises(InvalidInput, match=f"ab {MIN_AGE}"):
        builder.build_figure_looks(W, "liv", {**ANSWERS, "Alter": age})


def test_long_lived_beings_are_fine() -> None:
    assert check_answers({"Alter": "18"})["Alter"] == "18"
    assert check_answers({"Alter": " 340 "})["Alter"] == "340"


def test_unknown_questions_and_long_answers_are_refused() -> None:
    with pytest.raises(InvalidInput, match="Unbekannte Frage zum Aussehen: Kleidung"):
        check_answers({"Alter": "30", "Kleidung": "Mantel"})
    with pytest.raises(InvalidInput, match=r"Antwort zu lang .*: Haar"):
        check_answers({"Alter": "30", "Haar": "x" * 301})


def test_the_answers_come_back_in_the_order_of_the_questions() -> None:
    checked = check_answers({"Augen": "grün", "Alter": "30"})
    assert tuple(checked) == LOOKS_LABELS
    assert checked["Haut"] == ""


def test_a_too_small_budget_is_refused(builder: ContextBuilder) -> None:
    with pytest.raises(InvalidInput):
        builder.build_figure_looks(W, "liv", ANSWERS, budget=0)
