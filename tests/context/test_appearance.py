"""Taking the looks of a figure, a place or an item out of its entry (7.16, 10.3)."""

from pathlib import Path

import pytest

from skriptorium.canon import CanonService, Category, InvalidInput, NotFound
from skriptorium.context import NO_APPEARANCE, ContextBuilder
from skriptorium.manuscript import ManuscriptService
from skriptorium.storage import DocumentStore

W = "die-salzmark"


@pytest.fixture
def builder(tmp_path: Path) -> ContextBuilder:
    store = DocumentStore(tmp_path / "data")
    canon = CanonService(store)
    canon.create_world("Die Salzmark")
    canon.create_entry(
        W, "figur", "Tomas Rehl", body="- **Wesen:** geduldig\n- **Aussehen:** breit"
    )
    return ContextBuilder(canon, ManuscriptService(store))


def test_the_request_asks_only_for_the_visible(builder: ContextBuilder) -> None:
    system, user = builder.build_appearance(W, "tomas-rehl").messages
    assert "nur ihr äußeres Erscheinungsbild" in system.content
    assert "Lass Wesen" in system.content
    assert "erfinde nichts" in system.content
    assert NO_APPEARANCE in system.content
    assert user.content.startswith("# Tomas Rehl")
    assert "geduldig" in user.content


def test_unknown_entries(builder: ContextBuilder) -> None:
    with pytest.raises(NotFound):
        builder.build_appearance(W, "niemand")


def test_only_figures_places_and_items_can_be_taken_apart(
    builder: ContextBuilder, tmp_path: Path
) -> None:
    """Steps 8.4 and 10.3 (ADR-083, ADR-108): the server checks the category too."""
    canon = CanonService(DocumentStore(tmp_path / "data"))
    for category in ("kultur", "regel", "zeitlinie"):
        canon.create_entry(W, category, f"Probe {category}", body="Text.")
        with pytest.raises(InvalidInput, match="Figuren, Orten und Gegenständen"):
            builder.build_appearance(W, f"probe-{category}")


@pytest.mark.parametrize(
    ("category", "subject", "kept", "left_out"),
    [
        ("ort", "eines Ortes", "Bauweise", "Lass Lage und Weg dorthin, Bewohner"),
        ("gegenstand", "eines Gegenstands", "Inschriften", "Lass Zweck, Verwendung, Wirkung"),
    ],
)
def test_places_and_items_get_their_own_frame(
    builder: ContextBuilder,
    tmp_path: Path,
    category: Category,
    subject: str,
    kept: str,
    left_out: str,
) -> None:
    """Step 10.3 (ADR-108): same rules as for a figure, own list of what is visible."""
    canon = CanonService(DocumentStore(tmp_path / "data"))
    canon.create_entry(W, category, "Probe", body="Aus grauem Stein.")

    system, user = builder.build_appearance(W, "probe").messages

    assert f"Kanon-Eintrag {subject}" in system.content
    assert kept in system.content
    assert left_out in system.content
    assert "erfinde nichts" in system.content
    assert system.content.endswith(NO_APPEARANCE)
    assert "Erscheinungsbild" not in system.content
    assert user.content == "# Probe\n\nAus grauem Stein."


def test_a_place_goes_without_its_location(builder: ContextBuilder, tmp_path: Path) -> None:
    """Step 10.3 (ADR-108): the image gets "Lage" anyway; any level, with its subsections."""
    canon = CanonService(DocumentStore(tmp_path / "data"))
    canon.create_entry(
        W,
        "ort",
        "Leuchtturm",
        body=(
            "Ein schlanker Turm.\n\n### Lage\n\nAuf der Klippe.\n\n#### Weg\n\nZwei Stunden."
            "\n\n### Aussehen\n\n\n### Bewohner\n\nDer Wärter."
        ),
    )

    _, user = builder.build_appearance(W, "leuchtturm").messages

    assert user.content == (
        "# Leuchtturm\n\nEin schlanker Turm.\n\n### Aussehen\n\n\n### Bewohner\n\nDer Wärter."
    )


def test_an_unstructured_place_and_an_empty_location_go_in_whole(
    builder: ContextBuilder, tmp_path: Path
) -> None:
    canon = CanonService(DocumentStore(tmp_path / "data"))
    canon.create_entry(W, "ort", "Karst", body="Hafenstadt auf der Klippe.\n\n## Lage\n")
    canon.create_entry(W, "figur", "Wache", body="## Lage\n\nSteht am Tor.")

    assert builder.build_appearance(W, "karst").messages[1].content == (
        "# Karst\n\nHafenstadt auf der Klippe.\n\n## Lage"
    )
    assert "Steht am Tor." in builder.build_appearance(W, "wache").messages[1].content
