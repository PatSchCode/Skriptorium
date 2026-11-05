"""The text of a chapter as the AI reads it (step 10.6, ADR-110): without picture lines."""

from dataclasses import replace

from skriptorium.manuscript import Chapter, without_pictures


def readable(chapter: Chapter) -> Chapter:
    """The chapter with its picture lines (``![…](bild:…)``) left out of the text."""
    text = without_pictures(chapter.text)
    return chapter if text == chapter.text else replace(chapter, text=text)
