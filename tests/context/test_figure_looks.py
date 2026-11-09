"""Request of the figure assistant for an English image description (11.5, ADR-123)."""

from pathlib import Path

import pytest

from skriptorium.canon import LOOKS_LABELS, CanonService, InvalidInput, NotFound
from skriptorium.context import MIN_AGE, ContextBuilder, ContextTooLarge, check_answers
from skriptorium.manuscript import ManuscriptService
from skriptorium.storage import DocumentStore

W = "die-salzmark"
ANSWERS = {"Alter": "26", "Haar": "kupferrot,  glatt", "Augen": "grün"}


@pytest.fixture
def builder(tmp_path: Path) -> ContextBuilder:
    store = DocumentStore(tmp_path / "data")
    canon = CanonService(store)
    canon.create_world("Die Salzmark", "Rauer Norden, Salzpfannen und Fährleute.")
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


def test_the_suggestions_request_holds_frame_world_entry_and_answers(
    builder: ContextBuilder,
) -> None:
    system, user = builder.build_looks_suggestions(W, "liv", ANSWERS).messages
    assert "genau 3 Vorschläge" in system.content
    assert "„ [Eintrag]“" in system.content
    assert "kein Volk, Land oder Ort" in system.content
    assert f"ganze Zahlen ab {MIN_AGE}" in system.content
    assert "keine Fesseln, Ketten oder Halsbänder" in system.content
    assert "Kein Vorschlag darf dem Eintrag widersprechen" in system.content
    assert system.content.endswith("Besondere Merkmale: … | … | …")
    assert "Herkunft: … | … | …\nAlter: … | … | …" in system.content
    assert user.content.startswith("# Welt: Die Salzmark\n\nRauer Norden")
    assert "Kanon-Eintrag der Figur:\n\n# Liv" in user.content
    assert "Sommersprossen" in user.content
    assert "laut" in user.content
    assert "- Haar: kupferrot, glatt" in user.content
    assert "- Herkunft: (noch keine Angabe)" in user.content
    assert user.content.index("- Herkunft") < user.content.index("- Alter")
    assert user.content.index("Rauer Norden") < user.content.index("# Liv")
    assert user.content.index("# Liv") < user.content.index("Angaben des Autors bisher")


def test_the_suggestions_request_leaves_the_former_image_description_out(
    builder: ContextBuilder,
) -> None:
    _, user = builder.build_looks_suggestions(W, "liv", ANSWERS).messages
    assert "Bildbeschreibung" not in user.content
    assert "30-year-old" not in user.content


@pytest.mark.parametrize("answers", [{}, {"Alter": ""}, {"Alter": "17"}, {"Haar": "rot"}])
def test_suggestions_need_neither_an_age_nor_any_answer(
    builder: ContextBuilder, answers: dict[str, str]
) -> None:
    _, user = builder.build_looks_suggestions(W, "liv", answers).messages
    assert "Angaben des Autors bisher" in user.content


def test_suggestions_only_for_figures(builder: ContextBuilder) -> None:
    with pytest.raises(InvalidInput, match="nur für Figuren"):
        builder.build_looks_suggestions(W, "kerrow", {})
    with pytest.raises(NotFound):
        builder.build_looks_suggestions(W, "niemand", {})
    with pytest.raises(NotFound):
        builder.build_looks_suggestions("gibt-es-nicht", "liv", {})


def test_suggestions_refuse_unknown_questions_and_long_answers(builder: ContextBuilder) -> None:
    with pytest.raises(InvalidInput, match="Unbekannte Frage zum Aussehen: Kleidung"):
        builder.build_looks_suggestions(W, "liv", {"Kleidung": "Mantel"})
    with pytest.raises(InvalidInput, match=r"Antwort zu lang .*: Haar"):
        builder.build_looks_suggestions(W, "liv", {"Haar": "x" * 301})


def test_suggestions_refuse_a_world_too_large_for_the_budget(builder: ContextBuilder) -> None:
    with pytest.raises(InvalidInput):
        builder.build_looks_suggestions(W, "liv", {}, budget=0)
    with pytest.raises(ContextTooLarge):
        builder.build_looks_suggestions(W, "liv", {}, budget=200)
