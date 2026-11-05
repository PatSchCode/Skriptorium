"""Leaving out the sections about a home world (step 9.13, ADR-102)."""

import pytest

from skriptorium.canon.sections import drop_world_sections

BODY = (
    "Groß, wortkarg.\n\n"
    "## Wesen\n\nHält Versprechen.\n\n"
    "## In Das Eisenmeer\n\nSchmied in Hargsund.\n\n"
    "### Familie\n\nBruder von Ysa.\n\n"
    "## Fähigkeiten\n\nSchmieden.\n"
)


def test_drops_the_section_with_its_subsections() -> None:
    assert drop_world_sections(BODY, "Das Eisenmeer") == (
        "Groß, wortkarg.\n\n## Wesen\n\nHält Versprechen.\n\n## Fähigkeiten\n\nSchmieden.\n"
    )


@pytest.mark.parametrize(
    "heading",
    ["In Das Eisenmeer", "Im Eisenmeer", "in der Stadt am eisenmeer", "IM EISENMEER"],
)
def test_names_the_world_without_its_article_in_any_case(heading: str) -> None:
    text = f"Kern.\n\n## {heading}\n\nAlt.\n"
    assert drop_world_sections(text, "Das Eisenmeer") == "Kern.\n\n"


@pytest.mark.parametrize(
    "heading",
    ["Eisenmeer", "Geschichte im Eisenmeer", "In der Salzmark", "Innen"],
)
def test_other_sections_stay(heading: str) -> None:
    text = f"Kern.\n\n## {heading}\n\nBleibt.\n"
    assert drop_world_sections(text, "Das Eisenmeer") == text


def test_headings_in_code_and_names_of_only_an_article_change_nothing() -> None:
    fenced = "```\n## In Das Eisenmeer\n```\n"
    assert drop_world_sections(fenced, "Das Eisenmeer") == fenced
    assert drop_world_sections(BODY, "Das") == BODY
    assert drop_world_sections(BODY, "  ") == BODY
