"""Pictures between the paragraphs of a chapter (step 10.6, ADR-110).

A picture is a paragraph of its own in the chapter's Markdown, ``![caption](bild:<file>)``,
where ``<file>`` names a picture of the story (``bild-<12 hex>.<png|jpg|webp>`` in its folder
``bilder/``). Any other target is plain text. The pictures stay out of every request to the AI;
the e-book shows them as figures with their caption.
"""

import re
from typing import Final, NamedTuple

PICTURE_FILE: Final = re.compile(r"bild-[0-9a-f]{12}\.(?:png|jpg|webp)")
"""Names of picture files as this module creates them; nothing else is ever read or served."""

_LINE: Final = re.compile(
    r"^[ \t]*!\[(?P<caption>[^\]\n]*)\]\(bild:(?P<file>bild-[0-9a-f]{12}\.(?:png|jpg|webp))\)"
    r"[ \t]*$"
)


class Picture(NamedTuple):
    """A picture line: its caption (may be empty) and the file it names."""

    caption: str
    file: str


def picture_of(line: str) -> Picture | None:
    """The picture a line of Markdown stands for, ``None`` for any other line."""
    found = _LINE.match(line.rstrip("\r"))
    return None if found is None else Picture(found["caption"].strip(), found["file"])


def pictures_in(markdown: str) -> list[Picture]:
    """The pictures of a chapter, in order; a file named twice appears twice."""
    return [p for line in markdown.split("\n") if (p := picture_of(line)) is not None]


def without_pictures(markdown: str) -> str:
    """The chapter without its picture lines, for the AI (ADR-110); other text unchanged."""
    if "](bild:" not in markdown:
        return markdown
    kept = [line for line in markdown.split("\n") if picture_of(line) is None]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(kept))
