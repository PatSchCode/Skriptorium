"""``ManuscriptService``: stories, chapters, summaries, guest links and story facts.

Layout below the data directory (docs/architecture.md section 7)::

    worlds/<world>/stories/<story>/story.md              titel, form, perspektive,
                                                         gefuehrte_figuren, gast_verbindungen,
                                                         modell (ADR-023), genre and schreibweise
                                                         (ADR-053), optional archiviert
                                                         (ADR-098); body: overall summary
    worlds/<world>/stories/<story>/chapters/NN-<t>.md    kapitel, titel, status, kurzfassung,
                                                         kurzfassung_status, schreibweise
                                                         (optional, ADR-053); body: text
    worlds/<world>/stories/<story>/facts.md              fakten: list of eintrag and fakt
    worlds/<world>/stories/<story>/titelbild-<r>.<e>     cover (story header titelbild, ADR-075)
    worlds/<world>/stories/<story>/verlauf/NN.md         kapitel, anweisungen (ADR-056)

A novel (``roman``) has any number of chapters; a short story or fragment has exactly one,
created with the story, because the data model keeps all manuscript text in chapter files.
References to canon entries are stored as given; checking that they exist is the task of
the flow control in ``api`` (``manuscript`` does not depend on ``canon``). The same holds
for the existence of the world.

The service is a facade: the work is done by ``StoryStore`` (``stories``), ``ChapterStore``
(``chapters``) and ``StoryExtras`` (``extras``); the header handling of the files lives in
``headers``, the checks of caller input in ``validation``.
"""

import contextlib
from collections.abc import Sequence, Set
from datetime import datetime

from skriptorium.manuscript.chapters import ChapterStore
from skriptorium.manuscript.epub import epub_for
from skriptorium.manuscript.extras import StoryExtras
from skriptorium.manuscript.models import (
    ATMOSPHERES,
    CHAPTER_STATUSES,
    EXPLICITNESSES,
    FORMS,
    FREE_TEXT_MAX,
    GENRES,
    KEEP,
    STYLES,
    SUMMARY_STATUSES,
    TEMPOS,
    TONES,
    Chapter,
    ChapterStatus,
    Form,
    GuestLink,
    InstructionNote,
    Keep,
    Story,
    StoryContents,
    StoryFact,
    SummaryStatus,
    WritingStyle,
)
from skriptorium.manuscript.stories import StoryStore
from skriptorium.manuscript.validation import checked_chapter_style
from skriptorium.storage import DocumentStore, ImageOrigin, InvalidInput, NotFound

__all__ = [
    "ATMOSPHERES",
    "CHAPTER_STATUSES",
    "EXPLICITNESSES",
    "FORMS",
    "FREE_TEXT_MAX",
    "GENRES",
    "KEEP",
    "STYLES",
    "SUMMARY_STATUSES",
    "TEMPOS",
    "TONES",
    "Chapter",
    "ChapterStatus",
    "Form",
    "GuestLink",
    "InstructionNote",
    "Keep",
    "ManuscriptService",
    "Story",
    "StoryContents",
    "StoryFact",
    "SummaryStatus",
    "WritingStyle",
]


class ManuscriptService:
    """Creates and changes stories and chapters."""

    def __init__(self, store: DocumentStore) -> None:
        """Use ``store`` for all files."""
        self._chapters = ChapterStore(store)
        self._stories = StoryStore(store, self._chapters)
        self._extras = StoryExtras(store, self._stories, self._chapters)

    # --- stories --------------------------------------------------------------------------

    def list_stories(self, world_id: str) -> list[Story]:
        """The stories of a world, sorted by title."""
        return self._stories.list_stories(world_id)

    def get_story(self, world_id: str, story_id: str) -> Story:
        """One story with guest links and story facts.

        Raises:
            NotFound: The story does not exist.
            InvalidInput: Bad identifier or inconsistent file.
        """
        return self._stories.get_story(world_id, story_id)

    def create_story(
        self,
        world_id: str,
        title: str,
        form: Form,
        *,
        perspective: str | None = None,
        controlled_characters: Sequence[str] = (),
    ) -> Story:
        """Create a story; a short story or fragment gets its single chapter at once.

        Raises:
            AlreadyExists: A story with the same identifier exists in the world.
            InvalidInput: Empty title, unknown form or bad character reference.
        """
        return self._stories.create_story(
            world_id,
            title,
            form,
            perspective=perspective,
            controlled_characters=controlled_characters,
        )

    def update_story(
        self,
        world_id: str,
        story_id: str,
        *,
        title: str | Keep = KEEP,
        form: Form | Keep = KEEP,
        perspective: str | Keep | None = KEEP,
        controlled_characters: Sequence[str] | Keep = KEEP,
        model: str | Keep | None = KEEP,
        genres: Sequence[str] | Keep = KEEP,
        writing_style: WritingStyle | Keep = KEEP,
    ) -> Story:
        """Change title, form, the settings of the character mode (FR-012), the model, the
        genres or the default writing style (step 5.6).

        Which models exist is known to ``api``, not here; ``model`` is stored as given
        (blank or ``None`` clears it). A new default style applies to every chapter
        without a style of its own; chapters whose style equals the old default follow from
        then on, chapters changed on their own keep theirs (ADR-070).

        Raises:
            NotFound: The story does not exist.
            InvalidInput: Empty title, unknown form, bad reference, a value outside the lists
                of genre or writing style, or a form other than ``roman`` for a story with
                more than one chapter.
        """
        return self._stories.update_story(
            world_id,
            story_id,
            title=title,
            form=form,
            perspective=perspective,
            controlled_characters=controlled_characters,
            model=model,
            genres=genres,
            writing_style=writing_style,
        )

    def set_story_summary(self, world_id: str, story_id: str, summary: str) -> Story:
        """Set the overall summary of a story.

        Raises:
            NotFound: The story does not exist.
        """
        return self._stories.set_story_summary(world_id, story_id, summary)

    # --- archive and deleting for good (step 9.9, ADR-098) ---------------------------------

    def archive_story(self, world_id: str, story_id: str) -> Story:
        """Put a story into the archive (header ``archiviert: true``).

        Raises:
            NotFound: The story does not exist.
        """
        return self._stories.set_archived(world_id, story_id, True)

    def restore_story(self, world_id: str, story_id: str) -> Story:
        """Take a story back from the archive; the header field goes away.

        Raises:
            NotFound: The story does not exist.
        """
        return self._stories.set_archived(world_id, story_id, False)

    def story_contents(self, world_id: str, story_id: str) -> StoryContents:
        """What goes with the story when it is deleted for good.

        Raises:
            NotFound: The story does not exist.
        """
        return self._stories.story_contents(world_id, story_id)

    def delete_story(self, world_id: str, story_id: str, title: str) -> None:
        """Delete an archived story for good: its folder with chapters, summaries, history,
        facts and cover, and their rows of the search index.

        Raises:
            NotFound: The story does not exist.
            InvalidInput: The story is not archived, or ``title`` is not exactly its title.
            StorageError: The folder could not be moved aside; nothing is changed.
        """
        self._stories.delete_story(world_id, story_id, title)

    def remove_guest_world(
        self, world_id: str, story_id: str, guest_world: str, entries: Set[str]
    ) -> Story:
        """Remove every guest link of the story into ``guest_world``, with the story facts and
        led characters that name one of ``entries`` (step 9.9, ADR-098).

        Which identifiers belong to the guests only, and not also to the story's own world or
        another guest, is known to the flow in ``api``; it passes them as ``entries``.

        Raises:
            NotFound: The story does not exist.
        """
        return self._extras.remove_guest_world(world_id, story_id, guest_world, entries)

    # --- guest links and story facts ------------------------------------------------------

    def add_guest_link(self, world_id: str, story_id: str, guest_world: str, entry: str) -> Story:
        """Bind a canon entry of another world into this story only (FR-017).

        Raises:
            NotFound: The story does not exist.
            AlreadyExists: The link exists.
            InvalidInput: ``guest_world`` is the story's own world or a bad identifier.
        """
        return self._extras.add_guest_link(world_id, story_id, guest_world, entry)

    def remove_guest_link(
        self, world_id: str, story_id: str, guest_world: str, entry: str
    ) -> Story:
        """Remove a guest link.

        Raises:
            NotFound: The story or the link does not exist.
        """
        return self._extras.remove_guest_link(world_id, story_id, guest_world, entry)

    def add_fact(self, world_id: str, story_id: str, entry: str, fact: str) -> Story:
        """Add a fact about ``entry`` that holds only in this story (FR-024).

        Raises:
            NotFound: The story does not exist.
            AlreadyExists: The same fact exists.
            InvalidInput: Empty fact or bad entry reference.
        """
        return self._extras.add_fact(world_id, story_id, entry, fact)

    def remove_fact(self, world_id: str, story_id: str, entry: str, fact: str) -> Story:
        """Remove a story fact.

        Raises:
            NotFound: The story or the fact does not exist.
        """
        return self._extras.remove_fact(world_id, story_id, entry, fact)

    # --- chapters -------------------------------------------------------------------------

    def list_chapters(self, world_id: str, story_id: str) -> list[Chapter]:
        """The chapters of a story in order.

        Raises:
            NotFound: The story does not exist.
        """
        return self._chapters.list_chapters(world_id, story_id)

    def epub(
        self,
        world_id: str,
        story_id: str,
        *,
        author: str | None,
        only_completed: bool,
        modified: datetime,
    ) -> bytes:
        """The story as an EPUB file (step 7.4, ADR-071); ``author`` goes on the title page.

        Raises:
            NotFound: The story does not exist.
            InvalidInput: There is no chapter to put in (or none completed).
        """
        story = self._stories.get_story(world_id, story_id)
        chapters = [
            chapter
            for chapter in self._chapters.list_chapters(world_id, story_id)
            if not only_completed or chapter.status == "abgeschlossen"
        ]
        if not chapters:
            raise InvalidInput(
                "Kein abgeschlossenes Kapitel"
                if only_completed
                else "Die Geschichte hat keine Kapitel"
            )
        cover = None
        if story.cover is not None:
            # A cover file gone missing (deleted by hand) must not stop the book.
            with contextlib.suppress(NotFound):
                cover = self._stories.story_cover(world_id, story_id)
        return epub_for(story, chapters, author, modified, cover=cover)

    def set_story_cover(
        self, world_id: str, story_id: str, data: bytes, origin: ImageOrigin | None = None
    ) -> Story:
        """Store a cover for the story (step 7.11, ADR-075); it replaces the previous one.

        A generated cover keeps its ``origin`` next to the file (step 9.6, ADR-095).

        Raises:
            NotFound: The story does not exist.
            InvalidInput: Not a PNG, JPEG or WebP image, or too large.
        """
        return self._stories.set_story_cover(world_id, story_id, data, origin)

    def story_cover(self, world_id: str, story_id: str) -> tuple[bytes, str]:
        """The bytes and media type of the story's cover.

        Raises:
            NotFound: The story does not exist or has no cover.
        """
        return self._stories.story_cover(world_id, story_id)

    def story_cover_origin(self, world_id: str, story_id: str) -> ImageOrigin | None:
        """The origin of the story's cover, ``None`` if it has none (ADR-095).

        Raises:
            NotFound: The story does not exist or has no cover.
            InvalidInput: The origin file is unreadable.
        """
        return self._stories.story_cover_origin(world_id, story_id)

    def remove_story_cover(self, world_id: str, story_id: str) -> Story:
        """Remove the story's cover and delete its file.

        Raises:
            NotFound: The story does not exist or has no cover.
        """
        return self._stories.remove_story_cover(world_id, story_id)

    def get_chapter(self, world_id: str, story_id: str, number: int) -> Chapter:
        """One chapter.

        Raises:
            NotFound: The story or the chapter does not exist.
        """
        return self._chapters.get_chapter(world_id, story_id, number)

    def save_chapter(
        self,
        world_id: str,
        story_id: str,
        number: int,
        *,
        title: str | Keep = KEEP,
        text: str | Keep = KEEP,
        writing_style: WritingStyle | Keep | None = KEEP,
    ) -> Chapter:
        """Save a chapter; the next free number creates a new chapter (novels only).

        A new chapter follows the default writing style of the story (steps 5.6, 7.3;
        ADR-053, ADR-070). ``writing_style=None`` takes an existing chapter back to the
        default of the story; a style sets one of its own.

        Raises:
            NotFound: The story does not exist.
            InvalidInput: Number is neither existing nor the next one, a new chapter has no
                title, a new chapter is added to a story that is not a novel, or the style
                has a value outside the lists.
        """
        checked = checked_chapter_style(writing_style)
        return self._chapters.save_chapter(
            self._stories.get_story(world_id, story_id),
            number,
            title=title,
            text=text,
            writing_style=checked,
        )

    def delete_chapter(self, world_id: str, story_id: str, number: int) -> list[Chapter]:
        """Delete a chapter (step 9.9, ADR-098); the chapters after it move up by one.

        Number and file name of each following chapter go down by one, its history
        ``verlauf/NN.md`` moves along; the history of the deleted chapter is deleted. The
        overall summary is left as it is. Returns the remaining chapters in order.

        Raises:
            NotFound: The story or the chapter does not exist.
        """
        return self._chapters.delete_chapter(world_id, story_id, number)

    def complete_chapter(self, world_id: str, story_id: str, number: int) -> Chapter:
        """Mark a chapter as completed; its summary is created by the flow in ``api`` (3.6).

        Raises:
            NotFound: The story or the chapter does not exist.
        """
        return self._chapters.complete_chapter(world_id, story_id, number)

    def set_chapter_summary(
        self,
        world_id: str,
        story_id: str,
        number: int,
        summary: str,
        status: SummaryStatus,
    ) -> Chapter:
        """Set the short summary of a chapter and its review status.

        Raises:
            NotFound: The story or the chapter does not exist.
            InvalidInput: Unknown status.
        """
        return self._chapters.set_chapter_summary(world_id, story_id, number, summary, status)

    # --- history of instructions (step 5.13, ADR-056) --------------------------------------

    def list_instructions(self, world_id: str, story_id: str, number: int) -> list[InstructionNote]:
        """The taken-over instructions of a chapter, oldest first; never sent to the AI.

        Raises:
            NotFound: The story or the chapter does not exist.
        """
        return self._extras.list_instructions(world_id, story_id, number)

    def add_instruction(
        self,
        world_id: str,
        story_id: str,
        number: int,
        note: InstructionNote,
    ) -> list[InstructionNote]:
        """Note a taken-over exchange; the chapter file stays as it is.

        Raises:
            NotFound: The story or the chapter does not exist.
            InvalidInput: Empty instruction or text.
        """
        return self._extras.add_instruction(world_id, story_id, number, note)
