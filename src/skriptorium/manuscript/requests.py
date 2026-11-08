"""Writing requests as they went to the AI, kept per story (step 10.9, ADR-116).

One file per request ``worlds/<world>/stories/<story>/anfragen/<id>.md``. The header holds
``zeit`` (ISO 8601, UTC), ``kapitel``, ``modell``, ``laenge``, ``anweisung``, ``bausteine``
(``art``, ``bezeichnung``, ``token``), ``geschaetzte_token``, ``bilder`` (names of the entries
whose main image went along, no image data), ``ergebnis`` (``ok``, ``abgebrochen`` or an error
kind) and ``token_ein``, ``token_aus``, ``kosten_usd`` as the provider reported them (``null`` if
it reported nothing), named as in the consumption files (ADR-023). The body holds each message
verbatim behind a marker line, then the AI's raw answer behind its own marker line.

The identifier is the time the request was sent, ``JJJJMMTT-HHMMSS``; a second request in the
same second gets ``-2``, ``-3`` and so on. An identifier is reserved before the request is
sent, so the start of the stream can name it, and the file is written when the stream ends.
At most :data:`MAX_REQUESTS` stay per story; the oldest goes first. Nothing here is ever read
for a request to the AI.
"""

import re
import threading
from datetime import UTC, datetime
from pathlib import PurePosixPath
from typing import Final

from skriptorium.manuscript.headers import notes_from
from skriptorium.manuscript.layout import HISTORY, request_dir, request_path, story_dir, story_path
from skriptorium.manuscript.models import (
    INSTRUCTION_START,
    MAX_REQUESTS,
    RequestBlock,
    RequestMessage,
    RequestSummary,
    WritingRequest,
)
from skriptorium.storage import (
    Document,
    DocumentStore,
    HeaderValue,
    InvalidInput,
    NotFound,
)

REQUEST_ID: Final = re.compile(r"\d{8}-\d{6}(?:-[1-9]\d{0,3})?")
"""Form of a request identifier: the time of sending, a number for a second one in a second."""

# Marker lines of the body: one before each message (with its role), one before the answer.
_MARKER: Final = re.compile(
    r"^<!-- (?:nachricht: (system|user|assistant)|antwort der ki) -->$", re.MULTILINE
)


def checked_request_id(request_id: str) -> str:
    """``request_id`` if it has the form of a request identifier.

    Raises:
        InvalidInput: Any other text.
    """
    if not REQUEST_ID.fullmatch(request_id):
        raise InvalidInput(f"Ungültige Kennung einer Anfrage: {request_id!r}")
    return request_id


class RequestStore:
    """Reserves, writes, lists, reads and trims the kept writing requests of the stories."""

    def __init__(self, store: DocumentStore) -> None:
        """Use ``store`` for all files."""
        self._store = store
        # Identifiers handed out whose file is not written yet, per story folder.
        self._reserved: set[tuple[str, str]] = set()
        self._lock = threading.Lock()

    def reserve(self, world_id: str, story_id: str, at: datetime) -> str:
        """A new identifier for a request sent at ``at``, unique among the story's requests."""
        folder = request_dir(world_id, story_id)
        base = at.astimezone(UTC).strftime("%Y%m%d-%H%M%S")
        with self._lock:
            taken = set(self._ids(world_id, story_id)) | {
                reserved for owner, reserved in self._reserved if owner == folder
            }
            request_id, number = base, 1
            while request_id in taken:
                number += 1
                request_id = f"{base}-{number}"
            self._reserved.add((folder, request_id))
        return request_id

    def release(self, world_id: str, story_id: str, request_id: str) -> None:
        """Give back a reserved identifier whose request was never sent."""
        with self._lock:
            self._reserved.discard((request_dir(world_id, story_id), request_id))

    def save(self, world_id: str, story_id: str, request: WritingRequest) -> None:
        """Write the file of a reserved request and drop the oldest beyond the limit.

        The reservation ends either way.

        Raises:
            NotFound: The story does not exist (any more).
            InvalidInput: Bad identifier.
            AlreadyExists: A file with the identifier exists.
            StorageError: Writing or deleting failed.
        """
        try:
            checked_request_id(request.id)
            self._store.read(story_path(world_id, story_id))
            with self._lock:
                self._store.write(
                    request_path(world_id, story_id, request.id),
                    _header(request),
                    _body(request),
                    create=True,
                )
                for old in self._ids(world_id, story_id)[:-MAX_REQUESTS]:
                    self._store.delete(request_path(world_id, story_id, old))
        finally:
            self.release(world_id, story_id, request.id)

    def list_requests(self, world_id: str, story_id: str) -> list[RequestSummary]:
        """The kept requests of a story, newest first, without their texts.

        Raises:
            NotFound: The story does not exist.
            InvalidInput: A file is broken.
        """
        self._store.read(story_path(world_id, story_id))
        taken = self._taken_over(world_id, story_id)
        summaries = []
        for request_id in reversed(self._ids(world_id, story_id)):
            request = _request_from(self._store.read(request_path(world_id, story_id, request_id)))
            summaries.append(
                RequestSummary(
                    id=request.id,
                    at=request.at,
                    chapter=request.chapter,
                    model=request.model,
                    estimated_tokens=request.estimated_tokens,
                    input_tokens=request.input_tokens,
                    output_tokens=request.output_tokens,
                    cost_usd=request.cost_usd,
                    outcome=request.outcome,
                    instruction=request.instruction[:INSTRUCTION_START],
                    taken_over=request.id in taken,
                )
            )
        return summaries

    def get_request(self, world_id: str, story_id: str, request_id: str) -> WritingRequest:
        """One kept request with its messages and answer.

        Raises:
            NotFound: The story or the request does not exist (an identifier of another form
                never does).
            InvalidInput: The file is broken.
        """
        self._store.read(story_path(world_id, story_id))
        if not REQUEST_ID.fullmatch(request_id):
            raise NotFound(f"{world_id}/{story_id}/Anfrage {request_id}")
        return _request_from(self._store.read(request_path(world_id, story_id, request_id)))

    def drop_chapter(self, world_id: str, story_id: str, number: int) -> None:
        """Delete the requests of chapter ``number``; those of later chapters move up by one."""
        with self._lock:
            for request_id in self._ids(world_id, story_id):
                path = request_path(world_id, story_id, request_id)
                document = self._store.read(path)
                chapter = _count(document, "kapitel")
                if chapter == number:
                    self._store.delete(path)
                elif chapter > number:
                    header = dict(document.header)
                    header["kapitel"] = chapter - 1
                    self._store.write(path, header, document.body)

    def _ids(self, world_id: str, story_id: str) -> list[str]:
        """Identifiers of the request files of a story, oldest first."""
        stems = (
            PurePosixPath(path).stem
            for path in self._store.list_paths(request_dir(world_id, story_id))
        )
        return sorted((stem for stem in stems if REQUEST_ID.fullmatch(stem)), key=_order)

    def _taken_over(self, world_id: str, story_id: str) -> set[str]:
        """Identifiers of the requests a note of the history names."""
        paths = self._store.list_paths(f"{story_dir(world_id, story_id)}/{HISTORY}")
        return {
            note.request
            for path in paths
            for note in notes_from(self._store.read(path))
            if note.request is not None
        }


def _order(request_id: str) -> tuple[str, int]:
    """Sort key: the time, then the number of a further request in the same second."""
    return request_id[:15], int(request_id[16:] or 1)


def _header(request: WritingRequest) -> dict[str, HeaderValue]:
    return {
        "zeit": request.at.astimezone(UTC).isoformat(timespec="seconds"),
        "kapitel": request.chapter,
        "modell": request.model,
        "laenge": request.length,
        "anweisung": request.instruction,
        "bausteine": [
            {"art": block.kind, "bezeichnung": block.label, "token": block.tokens}
            for block in request.blocks
        ],
        "geschaetzte_token": request.estimated_tokens,
        "bilder": list[HeaderValue](request.pictures),
        "ergebnis": request.outcome,
        "token_ein": request.input_tokens,
        "token_aus": request.output_tokens,
        "kosten_usd": request.cost_usd,
    }


def _body(request: WritingRequest) -> str:
    parts = [f"<!-- nachricht: {m.role} -->\n\n{m.content}\n\n" for m in request.messages]
    return "".join(parts) + f"<!-- antwort der ki -->\n\n{request.answer}"


def _request_from(document: Document) -> WritingRequest:
    at = _text(document, "zeit")
    try:
        moment = datetime.fromisoformat(at)
    except ValueError as error:
        raise InvalidInput(f"{document.path}: ungültige Zeit {at!r}") from error
    messages, answer = _parts(document)
    return WritingRequest(
        id=PurePosixPath(document.path).stem,
        at=moment,
        chapter=_count(document, "kapitel"),
        model=_text(document, "modell"),
        length=_text(document, "laenge"),
        instruction=_text(document, "anweisung"),
        blocks=_blocks(document),
        estimated_tokens=_count(document, "geschaetzte_token"),
        pictures=_names(document),
        outcome=_text(document, "ergebnis"),
        input_tokens=_optional_count(document, "token_ein"),
        output_tokens=_optional_count(document, "token_aus"),
        cost_usd=_cost(document),
        messages=messages,
        answer=answer,
    )


def _parts(document: Document) -> tuple[tuple[RequestMessage, ...], str]:
    """The messages and the answer of the body: the text between the marker lines.

    The answer runs to the end of the file, whatever it contains; the messages end at the next
    marker line.
    """
    body = document.body
    markers = list(_MARKER.finditer(body))
    messages: list[RequestMessage] = []
    for index, marker in enumerate(markers):
        if marker[1] is None:
            return tuple(messages), body[marker.end() + 2 :]
        end = markers[index + 1].start() if index + 1 < len(markers) else len(body)
        messages.append(RequestMessage(marker[1], body[marker.end() + 2 : end - 2]))
    raise InvalidInput(f"{document.path}: Antwort der KI fehlt")


def _text(document: Document, key: str) -> str:
    value = document.header.get(key)
    if not isinstance(value, str):
        raise InvalidInput(f"{document.path}: Feld {key!r} muss ein Text sein")
    return value


def _count(document: Document, key: str) -> int:
    value = document.header.get(key)
    if not isinstance(value, int) or isinstance(value, bool):
        raise InvalidInput(f"{document.path}: Feld {key!r} muss eine Zahl sein")
    return value


def _optional_count(document: Document, key: str) -> int | None:
    return None if document.header.get(key) is None else _count(document, key)


def _cost(document: Document) -> float | None:
    value = document.header.get("kosten_usd")
    if value is None:
        return None
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise InvalidInput(f"{document.path}: Feld 'kosten_usd' muss eine Zahl sein")
    return float(value)


def _names(document: Document) -> tuple[str, ...]:
    value = document.header.get("bilder", [])
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise InvalidInput(f"{document.path}: Feld 'bilder' muss eine Liste von Texten sein")
    return tuple(item for item in value if isinstance(item, str))


def _blocks(document: Document) -> tuple[RequestBlock, ...]:
    value = document.header.get("bausteine", [])
    if not isinstance(value, list):
        raise InvalidInput(f"{document.path}: Feld 'bausteine' muss eine Liste sein")
    blocks = []
    for item in value:
        kind = item.get("art") if isinstance(item, dict) else None
        label = item.get("bezeichnung") if isinstance(item, dict) else None
        tokens = item.get("token") if isinstance(item, dict) else None
        if (
            not isinstance(kind, str)
            or not isinstance(label, str)
            or not isinstance(tokens, int)
            or isinstance(tokens, bool)
        ):
            raise InvalidInput(
                f"{document.path}: bausteine braucht je Eintrag art, bezeichnung und token"
            )
        blocks.append(RequestBlock(kind, label, tokens))
    return tuple(blocks)
