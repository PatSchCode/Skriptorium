"""Flow "Weiterschreiben im Wechsel" (docs/architecture.md section 5, roadmap step 3.3).

1. The chapter as saved is the basis: ``context`` builds the request under the token budget.
2. ``ai_gateway`` streams the answer; text chunks go to the caller as Server-Sent Events.
3. Nothing is saved here. The author takes over, changes or discards the proposal, and the
   interface saves taken-over text at the end of the chapter through the chapter endpoint
   (FR-009). An abort or an error therefore leaves the manuscript unchanged.

A new scene (FR-008) is a request like any other: place and characters become ``@``-references,
the goal becomes part of the instruction.

References, place and characters are entries of the story's world or guests the story binds in
from other worlds (FR-017, step 3.7); a guest wins over an entry of the world with the same
identifier, as in the checks of the story endpoints.

On request the main images of the named entries go along as image parts (step 10.7, ADR-111):
at most :data:`MAX_PICTURES`, in the order the entries are named, only for models that read
images. ``context`` words which image belongs to which entry; the images do not count against
the text budget.

Every request is counted through ``record`` when the stream ends: finished, failed or aborted
(ADR-023, step 3.9). At the same place a :class:`RequestKeeper` keeps the request as it went to
the AI, with the raw answer, in the story (step 10.9, ADR-116); the ``start`` event names its
identifier so that taking the proposal over can note it in the history. Keeping is never read
back for a request to the AI, and a storage failure never breaks the stream.

If the instruction contradicts the canon, the AI writes in line with the canon and starts its
answer with one line beginning with ``CONFLICT_MARKER``. That line goes to the interface as a
separate ``hinweis`` event, so taking over the proposal never puts it into the manuscript
(step 4.14).
"""

import json
import logging
from collections.abc import AsyncIterator, Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from typing import Final

from skriptorium.ai_gateway import (
    DEFAULT_MODELS,
    Completed,
    CompletionRequest,
    GatewayError,
    ImagePart,
    InvalidRequest,
    Message,
    ModelCatalog,
    ModelConfig,
    ModelProvider,
    ModelRefused,
    RateLimited,
    Usage,
)
from skriptorium.api.usage import Kind
from skriptorium.canon import CanonEntry, CanonService, Category
from skriptorium.context import (
    CONFLICT_MARKER,
    DEFAULT_LENGTH,
    ContextBlock,
    ContextBuilder,
    ContextTooLarge,
    Length,
)
from skriptorium.manuscript import (
    ManuscriptService,
    RequestBlock,
    RequestMessage,
    WritingRequest,
)
from skriptorium.storage import AlreadyExists, InvalidInput, NotFound, StorageError

# First model of the model order grok-4.6 → grok-4.7 → qwen3.8-max (ADR-011, ADR-044).
DEFAULT_MODEL: Final = next(iter(DEFAULT_MODELS))
# Values of the acceptance runs in steps 1.1 and 3.2.
MAX_OUTPUT_TOKENS: Final = 8000
TEMPERATURE: Final = 0.8
# "Weiter" without instruction: a small step, then the author's turn (owner, step 5.15).
CONTINUE: Final = (
    "Setze das Manuskript an seinem Ende fort: nur den unmittelbar nächsten Moment der Szene, "
    "ohne Zeitsprung."
)
# Images per request at most (owner, ADR-111).
MAX_PICTURES: Final = 4
# Input tokens of one image: a description with grok-4.6 took 2,788 tokens, about 200 of them
# text (2026-11-05, ADR-111); checked again against the consumption after the first requests.
PICTURE_TOKENS: Final = 2500

# Counts one AI request: kind, model, usage reported by the provider, outcome (ADR-023).
UsageRecorder = Callable[[Kind, str, Usage | None, str], None]

_log = logging.getLogger("skriptorium.api.flows.writing")


@dataclass(frozen=True)
class Scene:
    """Start of a new scene: place, characters (canon entry identifiers) and goal."""

    place: str | None = None
    characters: tuple[str, ...] = ()
    goal: str = ""


@dataclass(frozen=True)
class WriteOrder:
    """What the author asks for: an instruction, ``@``-references, optionally a new scene.

    ``length`` is the length of the proposal the author chose (step 5.15).
    """

    world: str
    story: str
    chapter: int
    instruction: str = ""
    references: tuple[str, ...] = ()
    scene: Scene | None = None
    model: str = DEFAULT_MODEL
    length: Length = DEFAULT_LENGTH
    # The main images of the named entries go along (step 10.7, ADR-111).
    images: bool = False


@dataclass(frozen=True)
class SentRequest:
    """What a writing request is kept with besides its messages (step 10.9, ADR-116).

    ``instruction`` is the instruction as it went into the request; ``pictures`` names the
    entries whose main image went along.
    """

    world: str
    story: str
    chapter: int
    length: Length
    instruction: str
    blocks: tuple[ContextBlock, ...]
    pictures: tuple[str, ...] = ()


@dataclass(frozen=True)
class PreparedRequest:
    """The request for ``ai_gateway``, the estimated size of its context and its image count.

    ``sent`` is set for writing requests, which are kept (ADR-116); other flows leave it out.
    """

    completion: CompletionRequest
    estimated_tokens: int
    pictures: int = 0
    sent: SentRequest | None = None


def prepare_request(
    canon: CanonService,
    manuscripts: ManuscriptService,
    builder: ContextBuilder,
    order: WriteOrder,
    models: Mapping[str, ModelConfig] = DEFAULT_MODELS,
) -> PreparedRequest:
    """Check the order and build the request; runs before anything is streamed.

    Raises:
        InvalidInput: Unknown model, unknown or unsuitable canon entry, empty scene, images for
            a model that does not read them, or the context does not fit the budget (message
            names the largest blocks).
        NotFound: World, story or chapter does not exist.
    """
    if order.model not in models:
        raise InvalidInput(f"Unbekanntes Modell: {order.model}")
    if order.images and not (isinstance(models, ModelCatalog) and models.reads_images(order.model)):
        raise InvalidInput("Dieses Modell kann keine Bilder lesen - bitte ohne Bilder senden")
    canon.get_world(order.world)
    story = manuscripts.get_story(order.world, order.story)
    homes = {link.entry: link.world for link in story.guest_links}

    def entry(entry_id: str, category: Category | None = None) -> CanonEntry:
        return _entry(canon, homes.get(entry_id, order.world), entry_id, category)

    instruction = order.instruction.strip()
    references = [entry(reference).id for reference in order.references]
    if order.scene is not None:
        scene_refs, instruction = _scene(entry, order.scene, instruction)
        references += scene_refs
    elif not instruction:
        instruction = CONTINUE
    named = list(dict.fromkeys(references))
    pictured = _pictured([entry(reference) for reference in named]) if order.images else []
    try:
        built = builder.build(
            order.world,
            order.story,
            order.chapter,
            instruction,
            named,
            length=order.length,
            pictured=[found.name for found in pictured],
        )
    except ContextTooLarge as error:
        raise InvalidInput(str(error)) from error
    messages = [Message(message.role, message.content) for message in built.messages]
    if pictured:
        images = tuple(
            ImagePart(media_type, data)
            for data, media_type in (
                canon.entry_image(found.world, found.id, found.images[0]) for found in pictured
            )
        )
        last = messages[-1]
        messages[-1] = Message(last.role, last.content, images=images)
    return PreparedRequest(
        CompletionRequest(order.model, tuple(messages), MAX_OUTPUT_TOKENS, TEMPERATURE),
        built.estimated_tokens + PICTURE_TOKENS * len(pictured),
        len(pictured),
        SentRequest(
            order.world,
            order.story,
            order.chapter,
            order.length,
            instruction,
            built.blocks,
            tuple(found.name for found in pictured),
        ),
    )


def _pictured(named: Sequence[CanonEntry]) -> list[CanonEntry]:
    """The named entries whose main image goes along: those with images, at most four."""
    return [found for found in named if found.images][:MAX_PICTURES]


def _entry(
    canon: CanonService, world: str, entry_id: str, category: Category | None = None
) -> CanonEntry:
    try:
        entry = canon.get_entry(world, entry_id)
    except NotFound as error:
        raise InvalidInput(f"Unbekannter Kanon-Eintrag {entry_id}") from error
    if category is not None and entry.category != category:
        raise InvalidInput(f"{entry.name} ist kein Eintrag der Kategorie {category}")
    return entry


def _scene(
    entry: Callable[[str, Category], CanonEntry], scene: Scene, extra: str
) -> tuple[list[str], str]:
    """References and instruction for the first paragraph of a new scene (FR-008)."""
    goal = scene.goal.strip()
    if scene.place is None and not scene.characters and not goal:
        raise InvalidInput("Die Szene braucht einen Ort, Figuren oder ein Ziel")
    place = entry(scene.place, "ort") if scene.place is not None else None
    characters = [entry(c, "figur") for c in scene.characters]
    lines = ["Beginne hier eine neue Szene und schreibe ihren ersten Absatz."]
    if place is not None:
        lines.append(f"Ort: {place.name}")
    if characters:
        lines.append(f"Figuren: {', '.join(c.name for c in characters)}")
    if goal:
        lines.append(f"Ziel der Szene: {goal}")
    if extra:
        lines.append(extra)
    references = [e.id for e in ([place] if place is not None else []) + characters]
    return references, "\n".join(lines)


_ERROR_KINDS: Final[Sequence[tuple[type[GatewayError], str]]] = (
    (ModelRefused, "abgelehnt"),
    (RateLimited, "zu_viele_anfragen"),
    (InvalidRequest, "ungueltig"),
)


@dataclass(frozen=True)
class OpenRequest:
    """A writing request about to be sent: its reserved identifier, the time of sending and
    what it is kept with."""

    id: str
    at: datetime
    sent: SentRequest


@dataclass(frozen=True)
class RequestKeeper:
    """Keeps every writing request with the AI's raw answer in its story (ADR-116).

    A storage failure is logged by its kind and swallowed: keeping must never break writing,
    and no text of the request ever goes into the log.
    """

    manuscripts: ManuscriptService
    clock: Callable[[], datetime]

    def open(self, prepared: PreparedRequest) -> OpenRequest | None:
        """Reserve the identifier of the request; ``None`` for a request that is not kept."""
        sent = prepared.sent
        if sent is None:
            return None
        at = self.clock()
        return OpenRequest(self.manuscripts.reserve_request(sent.world, sent.story, at), at, sent)

    def release(self, opened: OpenRequest) -> None:
        """Give the identifier back: the request was never sent."""
        self.manuscripts.release_request(opened.sent.world, opened.sent.story, opened.id)

    def keep(
        self,
        prepared: PreparedRequest,
        opened: OpenRequest,
        answer: str,
        outcome: str,
        usage: Usage | None,
    ) -> None:
        """Keep the request as sent, with ``answer`` as the AI streamed it."""
        sent = opened.sent
        request = WritingRequest(
            id=opened.id,
            at=opened.at,
            chapter=sent.chapter,
            model=prepared.completion.model,
            length=sent.length,
            instruction=sent.instruction,
            blocks=tuple(RequestBlock(b.kind, b.label, b.tokens) for b in sent.blocks),
            estimated_tokens=prepared.estimated_tokens,
            pictures=sent.pictures,
            outcome=outcome,
            input_tokens=usage.input_tokens if usage else None,
            output_tokens=usage.output_tokens if usage else None,
            cost_usd=usage.cost_usd if usage else None,
            messages=tuple(
                RequestMessage(message.role, message.content)
                for message in prepared.completion.messages
            ),
            answer=answer,
        )
        try:
            self.manuscripts.save_request(sent.world, sent.story, request)
        except (StorageError, InvalidInput, NotFound, AlreadyExists) as error:
            _log.warning("Anfrage nicht gespeichert: %s", type(error).__name__)


async def stream_events(
    provider: ModelProvider,
    prepared: PreparedRequest,
    record: UsageRecorder | None = None,
    keeper: RequestKeeper | None = None,
) -> AsyncIterator[str]:
    """Stream the answer as Server-Sent Events.

    Events: ``start`` (model, estimated tokens, images, the identifier of the kept request or
    ``None``), then at most one ``hinweis`` (the AI's note on a contradiction with the canon,
    step 4.14) and ``text`` per chunk, then either ``done`` (usage) or ``error`` (kind only;
    texts for the author live in the interface). Closing the connection closes the provider
    stream, which ends the request at the provider. At the end the request is passed to
    ``record`` with outcome ``ok``, the error kind or ``abgebrochen``, and to ``keeper`` with the
    same outcome and the raw answer (ADR-116). A connection closed before the request was sent
    counts nothing and keeps nothing.
    """
    completion = prepared.completion
    opened = keeper.open(prepared) if keeper is not None else None
    usage: Usage | None = None
    outcome = "abgebrochen"
    sent = False
    answer: list[str] = []
    events = provider.stream(completion)
    split = NoteSplitter()
    try:
        yield _event(
            "start",
            {
                "model": completion.model,
                "estimated_tokens": prepared.estimated_tokens,
                "images": prepared.pictures,
                "request": opened.id if opened is not None else None,
            },
        )
        sent = True
        async for event in events:
            if isinstance(event, Completed):
                usage, outcome = event.usage, "ok"
                for name, text in split.finish():
                    yield _event(name, {"text": text})
                yield _event(
                    "done",
                    {
                        "input_tokens": event.usage.input_tokens,
                        "output_tokens": event.usage.output_tokens,
                        "cost_usd": event.usage.cost_usd,
                        "finish_reason": event.finish_reason,
                    },
                )
            elif event.text:
                answer.append(event.text)
                for name, text in split.feed(event.text):
                    yield _event(name, {"text": text})
    except GatewayError as error:
        outcome = error_kind(error)
        for name, text in split.finish():
            yield _event(name, {"text": text})
        yield _event("error", {"kind": outcome})
    finally:
        close = getattr(events, "aclose", None)
        if close is not None:
            await close()
        if sent and record is not None:
            record("schreiben", completion.model, usage, outcome)
        if keeper is not None and opened is not None:
            if sent:
                keeper.keep(prepared, opened, "".join(answer), outcome, usage)
            else:
                keeper.release(opened)


class NoteSplitter:
    """Separates the AI's conflict note from the text while the answer streams (step 4.14).

    The note is the first line if it starts with ``CONFLICT_MARKER`` (ignoring case and leading
    whitespace). Until that is decided, chunks are held back; afterwards they pass unchanged.
    Each call returns ``(event, text)`` pairs with event ``hinweis`` or ``text``.
    """

    def __init__(self) -> None:
        """Start undecided with nothing held back."""
        self._held = ""
        self._decided = False
        # After a note, blank lines up to the first text are dropped, even in later chunks.
        self._skip_blank = False

    def feed(self, chunk: str) -> list[tuple[str, str]]:
        """Pass on ``chunk`` or hold it back until the first line is decided."""
        if self._decided:
            if self._skip_blank:
                chunk = chunk.lstrip("\r\n")
                self._skip_blank = not chunk
            return [("text", chunk)] if chunk else []
        self._held += chunk
        start = self._held.lstrip()
        marker = CONFLICT_MARKER.casefold()
        if len(start) < len(marker) and marker.startswith(start.casefold()):
            return []
        if not start.casefold().startswith(marker):
            return self._release(self._held, "")
        line_end = start.find("\n")
        if line_end == -1:
            return []
        return self._release(start[line_end:].lstrip("\r\n"), start[len(marker) : line_end])

    def finish(self) -> list[tuple[str, str]]:
        """Pass on what is held back when the answer ends, completely or not."""
        if self._decided:
            return []
        start = self._held.lstrip()
        if start.casefold().startswith(CONFLICT_MARKER.casefold()):
            return self._release("", start[len(CONFLICT_MARKER) :])
        return self._release(self._held, "")

    def _release(self, text: str, note: str) -> list[tuple[str, str]]:
        self._decided = True
        self._held = ""
        self._skip_blank = bool(note.strip()) and not text
        pairs = [("hinweis", note.strip())] if note.strip() else []
        return pairs + ([("text", text)] if text else [])


def error_kind(error: GatewayError) -> str:
    """Kind of a provider error as sent to the interface."""
    for error_type, kind in _ERROR_KINDS:
        if isinstance(error, error_type):
            return kind
    return "nicht_erreichbar"


def _event(name: str, data: Mapping[str, object]) -> str:
    return f"event: {name}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"
