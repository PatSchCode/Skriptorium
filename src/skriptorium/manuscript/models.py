"""Data types and fixed lists of the module ``manuscript`` (re-exported by ``service``)."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Final, Literal, get_args

Form = Literal["roman", "kurzgeschichte", "fragment"]
FORMS: Final[tuple[Form, ...]] = get_args(Form)
ChapterStatus = Literal["in-arbeit", "abgeschlossen"]
CHAPTER_STATUSES: Final[tuple[ChapterStatus, ...]] = get_args(ChapterStatus)
# ``veraltet``: the chapter moved up after a chapter before it was deleted (step 9.9, ADR-098);
# its short summary still stands but is to be created again.
SummaryStatus = Literal["fehlt", "erzeugt", "geprüft", "veraltet"]
SUMMARY_STATUSES: Final[tuple[SummaryStatus, ...]] = get_args(SummaryStatus)

# Fixed lists of the atmospheric writing style (step 5.6, ADR-053); the order is the one in
# which the owner chose them. ``ui/src/views/WritingStyle.tsx`` keeps a copy that must match.
GENRES: Final[tuple[str, ...]] = (
    "Dark Romance",
    "Dark Erotic",
    "CNC",
    "Thriller",
    "Psychothriller",
    "düstere Geschichte",
    "Horror",
    "Dark Fantasy",
    "Krimi",
)
TONES: Final[tuple[str, ...]] = (
    "düster",
    "bedrückend",
    "kalt",
    "roh",
    "sinnlich",
    "zärtlich",
    "leidenschaftlich",
    "melancholisch",
    "bedrohlich",
    "nüchtern",
    "ironisch",
)
ATMOSPHERES: Final[tuple[str, ...]] = (
    "beklemmend",
    "angespannt",
    "unheimlich",
    "gefährlich",
    "schwül",
    "intim",
    "eisig",
    "hoffnungslos",
    "still",
    "fiebrig",
)
TEMPOS: Final[tuple[str, ...]] = ("langsam", "gemessen", "zügig", "atemlos")
STYLES: Final[tuple[str, ...]] = (
    "knapp",
    "schlicht",
    "bildhaft",
    "poetisch",
    "ausführlich",
    "dialogreich",
)
EXPLICITNESSES: Final[tuple[str, ...]] = ("angedeutet", "sinnlich", "explizit")
# Longest free text of a writing style. Other texts of the module have no limit; the request
# budget bounds this block, so the limit follows the owner's decision (ADR-053).
FREE_TEXT_MAX: Final = 1000
# Longest relation of a guest to the world of the story (step 9.13, ADR-102); several paragraphs,
# far below the request budget.
RELATION_MAX: Final = 4000
# Kept writing requests per story; beyond that the oldest goes (step 10.9, ADR-116).
MAX_REQUESTS: Final = 50
# Characters of the instruction in the list of kept requests.
INSTRUCTION_START: Final = 120


class Keep(Enum):
    """Marker for "leave this field unchanged" in updates."""

    KEEP = "keep"


KEEP: Final = Keep.KEEP


@dataclass(frozen=True)
class GuestLink:
    """A canon entry of another world bound into one story (FR-017).

    ``relation`` tells how the guest fits the world of the story: origin, relations, belongings,
    role there (step 9.13, ADR-102); ``""`` means none. It is not part of equality: a link is the
    pair of world and entry.
    """

    world: str
    entry: str
    relation: str = field(default="", compare=False)


@dataclass(frozen=True)
class StoryFact:
    """A fact that holds only in one story (FR-024)."""

    entry: str
    fact: str


@dataclass(frozen=True)
class InstructionNote:
    """One taken-over exchange (step 5.13, FR-027, ADR-056): the author's instruction and the
    AI's text as it went into the manuscript, with the model that wrote it."""

    at: datetime
    instruction: str
    text: str
    model: str | None = None
    # Identifier of the writing request the text came from (step 10.9, ADR-116); older notes
    # and notes of texts taken over before the request was kept have none.
    request: str | None = None


@dataclass(frozen=True)
class RequestBlock:
    """One building block of a writing request: its kind, its label and its estimated tokens."""

    kind: str
    label: str
    tokens: int


@dataclass(frozen=True)
class RequestMessage:
    """One message of a writing request as it went to the AI (text only, no image data)."""

    role: str
    content: str


@dataclass(frozen=True)
class WritingRequest:
    """A writing request as it went to the AI, with the AI's raw answer (step 10.9, ADR-116).

    ``instruction`` is the instruction as it went into the request (the text for "Weiter" or
    the lines of a new scene included); ``pictures`` names the entries whose main image went
    along. ``outcome`` is ``ok``, ``abgebrochen`` or the error kind of the writing flow; tokens
    and cost are those the provider reported, ``None`` if it reported none. ``answer`` is the
    streamed text as the AI wrote it, with the line of a conflict note if there was one.
    """

    id: str
    at: datetime
    chapter: int
    model: str
    length: str
    instruction: str
    blocks: tuple[RequestBlock, ...]
    estimated_tokens: int
    pictures: tuple[str, ...]
    outcome: str
    input_tokens: int | None
    output_tokens: int | None
    cost_usd: float | None
    messages: tuple[RequestMessage, ...]
    answer: str


@dataclass(frozen=True)
class RequestSummary:
    """A kept writing request in the list (step 10.9, ADR-116), without its texts.

    ``instruction`` is the start of the instruction, at most :data:`INSTRUCTION_START`
    characters; ``taken_over`` is true when a note of the history names the request.
    """

    id: str
    at: datetime
    chapter: int
    model: str
    estimated_tokens: int
    input_tokens: int | None
    output_tokens: int | None
    cost_usd: float | None
    outcome: str
    instruction: str
    taken_over: bool


@dataclass(frozen=True)
class WritingStyle:
    """Atmospheric writing style (step 5.6, ADR-053); the empty style has nothing set."""

    tone: tuple[str, ...] = ()
    atmosphere: tuple[str, ...] = ()
    style: tuple[str, ...] = ()
    tempo: str | None = None
    explicitness: str | None = None
    free: str = ""


@dataclass(frozen=True)
class Story:
    """A story with its settings and overall summary."""

    world: str
    id: str
    title: str
    form: Form
    perspective: str | None
    controlled_characters: tuple[str, ...]
    guest_links: tuple[GuestLink, ...]
    facts: tuple[StoryFact, ...]
    summary: str
    # Model chosen for this story (step 3.9, ADR-023); ``None`` means the preset model.
    model: str | None = None
    # Genres and the default writing style that new chapters copy (step 5.6, ADR-053).
    genres: tuple[str, ...] = ()
    writing_style: WritingStyle = WritingStyle()
    # File name of the cover in the story's folder (step 7.11, ADR-075); ``None`` without one.
    cover: str | None = None
    # In the archive (step 9.9, ADR-098): listed only there, deleted for good only from there.
    archived: bool = False


@dataclass(frozen=True)
class StoryContents:
    """What goes with a story when it is deleted for good (step 9.9, ADR-098)."""

    chapters: int
    facts: int
    cover: bool


@dataclass(frozen=True)
class Chapter:
    """One chapter: its text and its short summary."""

    world: str
    story: str
    number: int
    title: str
    status: ChapterStatus
    summary: str
    summary_status: SummaryStatus
    text: str
    # ``None``: the chapter has no style of its own, the default of the story applies.
    writing_style: WritingStyle | None = None
