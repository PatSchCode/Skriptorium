"""Consumption of the AI requests, one file per month (ADR-023, roadmap step 3.9).

``system/verbrauch/JJJJ-MM.md`` holds a header field ``anfragen``: one item per AI request with
``zeit`` (ISO 8601, UTC), ``art`` (schreiben, kurzfassung, gesamtzusammenfassung, weltenbau),
``modell``, ``ergebnis`` (``ok``, an error kind of the writing flow, ``leer`` or ``abgebrochen``),
``token_ein``, ``token_aus``, ``kosten_usd`` and, since step 9.10 (ADR-099), ``cache_gelesen``
and ``cache_geschrieben``: input tokens read from or written to the provider's prompt cache
(``null`` if the provider reported nothing; older items lack the two fields) and, since step 9.11
(ADR-100), ``welt`` and ``geschichte``: the identifiers the request belonged to (``geschichte``
``null`` for work on the world itself; older items lack both and count as unassigned).
No text, only metadata and identifiers, as in the log (ADR-021). The monthly sums leave the cache
counts out; the statistics (:meth:`UsageLog.stats`) group by world, story, kind and model.
"""

import logging
import re
import threading
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from datetime import datetime
from typing import Final, Literal

from skriptorium.ai_gateway import Usage
from skriptorium.storage import (
    DocumentStore,
    HeaderValue,
    InvalidInput,
    NotFound,
    StorageError,
    checked_identifier,
)

DIRECTORY: Final = "system/verbrauch"
_MONTH: Final = re.compile(r"\d{4}-(0[1-9]|1[0-2])")
_log = logging.getLogger("skriptorium.api.usage")

Kind = Literal[
    "schreiben",
    "kurzfassung",
    "gesamtzusammenfassung",
    "weltenbau",
    "bildbeschreibung",
    "bilderzeugung",
    "aussehen",
]


Recorder = Callable[[Kind, str, Usage | None, str], None]
"""Records one request: kind, model, usage (``None`` if unknown) and outcome."""


@dataclass
class Totals:
    """Sums over a set of requests.

    ``cache_read_tokens`` and ``cache_input_tokens`` only count requests whose provider reported
    the cache: the tokens read from it and all input tokens of those requests (ADR-099).
    """

    requests: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0
    without_cost: int = 0
    cache_read_tokens: int = 0
    cache_input_tokens: int = 0

    @property
    def cache_share(self) -> float | None:
        """Part of the input read from the provider's cache; ``None`` if nothing was reported."""
        if self.cache_input_tokens == 0:
            return None
        return min(1.0, self.cache_read_tokens / self.cache_input_tokens)

    def add(self, item: dict[str, HeaderValue]) -> None:
        """Count one item of a month file."""
        cost = item.get("kosten_usd")
        self.requests += 1
        self.input_tokens += _count(item.get("token_ein"))
        self.output_tokens += _count(item.get("token_aus"))
        self.cost_usd = round(self.cost_usd + _number(cost), 6)
        self.without_cost += 0 if _is_number(cost) else 1
        cached = item.get("cache_gelesen")
        if _is_count(cached):
            self.cache_read_tokens += _count(cached)
            self.cache_input_tokens += _count(item.get("token_ein"))


@dataclass
class Group:
    """Sums of a set of requests, also by kind and by model."""

    totals: Totals = field(default_factory=Totals)
    kinds: dict[str, Totals] = field(default_factory=dict)
    models: dict[str, Totals] = field(default_factory=dict)

    def add(self, item: dict[str, HeaderValue]) -> None:
        """Count one item of a month file."""
        self.totals.add(item)
        self.kinds.setdefault(_text(item.get("art")), Totals()).add(item)
        self.models.setdefault(_text(item.get("modell")), Totals()).add(item)


@dataclass
class WorldGroup:
    """The requests of one world: all, those on the world itself, and those of each story."""

    all: Group = field(default_factory=Group)
    own: Group = field(default_factory=Group)
    stories: dict[str, Group] = field(default_factory=dict)


@dataclass
class UsageStats:
    """Statistics of one month or, with ``month`` ``None``, of all months (ADR-100).

    ``months`` lists every month with a file, newest first. Requests without a world (older than
    step 9.11, or an image generated without a target) count in ``unassigned``; ``worlds`` and
    ``unassigned`` together make up ``total``.
    """

    month: str | None
    months: list[str]
    total: Group = field(default_factory=Group)
    worlds: dict[str, WorldGroup] = field(default_factory=dict)
    unassigned: Group = field(default_factory=Group)

    def add(self, item: dict[str, HeaderValue]) -> None:
        """Count one item of a month file under its world and story."""
        self.total.add(item)
        world = item.get("welt")
        if not isinstance(world, str) or not world:
            self.unassigned.add(item)
            return
        group = self.worlds.setdefault(world, WorldGroup())
        group.all.add(item)
        story = item.get("geschichte")
        if isinstance(story, str) and story:
            group.stories.setdefault(story, Group()).add(item)
        else:
            group.own.add(item)


@dataclass(frozen=True)
class MonthUsage:
    """Sums of one month; ``without_cost`` counts requests the provider reported no cost for."""

    month: str
    requests: int
    input_tokens: int
    output_tokens: int
    cost_usd: float
    without_cost: int


class UsageLog:
    """Records every AI request of a month and sums them up."""

    def __init__(self, store: DocumentStore, clock: Callable[[], datetime]) -> None:
        """Use ``store`` for the files below ``system/verbrauch`` and ``clock`` (UTC)."""
        self._store = store
        self._clock = clock
        # Each record is a read-modify-write of the month's file.
        self._lock = threading.Lock()

    def recorder(self, world: str | None, story: str | None = None) -> Recorder:
        """A recorder that files each request under ``world`` and ``story`` (ADR-100).

        Raises:
            InvalidInput: ``world`` or ``story`` is no valid identifier, or a story has no world.
        """
        if story is not None and world is None:
            raise InvalidInput("Eine Geschichte braucht ihre Welt")
        for identifier in (world, story):
            if identifier is not None:
                checked_identifier(identifier)

        def record(kind: Kind, model: str, usage: Usage | None, outcome: str) -> None:
            self.record(kind, model, usage, outcome, world=world, story=story)

        return record

    def record(
        self,
        kind: Kind,
        model: str,
        usage: Usage | None,
        outcome: str,
        *,
        world: str | None = None,
        story: str | None = None,
    ) -> None:
        """Add one request to the file of the current month, filed under ``world`` and ``story``.

        A write error is logged and swallowed: counting must never break writing.
        """
        now = self._clock()
        item: dict[str, HeaderValue] = {
            "zeit": now.isoformat(),
            "art": kind,
            "modell": model,
            "ergebnis": outcome,
            "token_ein": usage.input_tokens if usage else None,
            "token_aus": usage.output_tokens if usage else None,
            "kosten_usd": usage.cost_usd if usage else None,
            "cache_gelesen": usage.cache_read_tokens if usage else None,
            "cache_geschrieben": usage.cache_write_tokens if usage else None,
            "welt": world,
            "geschichte": story,
        }
        path = _path(now.strftime("%Y-%m"))
        try:
            with self._lock:
                self._store.write(path, {"anfragen": [*self._items(path), item]}, "")
        except (StorageError, InvalidInput) as error:
            _log.warning("Verbrauch nicht gespeichert: %s", type(error).__name__)

    def month(self, month: str | None = None) -> MonthUsage:
        """Sums of ``month`` (``JJJJ-MM``), by default the current one.

        Raises:
            InvalidInput: ``month`` is not of the form ``JJJJ-MM`` or the file is broken.
        """
        wanted = month if month is not None else self._clock().strftime("%Y-%m")
        if not _MONTH.fullmatch(wanted):
            raise InvalidInput(f"Monat muss die Form JJJJ-MM haben: {wanted}")
        items = self._items(_path(wanted))
        costs = [item.get("kosten_usd") for item in items]
        return MonthUsage(
            month=wanted,
            requests=len(items),
            input_tokens=sum(_count(item.get("token_ein")) for item in items),
            output_tokens=sum(_count(item.get("token_aus")) for item in items),
            cost_usd=round(sum(_number(cost) for cost in costs), 6),
            without_cost=sum(1 for cost in costs if not _is_number(cost)),
        )

    def months(self) -> list[str]:
        """Every month with a file, newest first."""
        names = (path.rsplit("/", 1)[-1].removesuffix(".md") for path in self._paths())
        return sorted((name for name in names if _MONTH.fullmatch(name)), reverse=True)

    def stats(self, month: str | None = None) -> UsageStats:
        """Statistics of ``month`` (``JJJJ-MM``) or, if ``None``, of all months (ADR-100).

        Raises:
            InvalidInput: ``month`` is not of the form ``JJJJ-MM`` or a file is broken.
        """
        if month is not None and not _MONTH.fullmatch(month):
            raise InvalidInput(f"Monat muss die Form JJJJ-MM haben: {month}")
        months = self.months()
        stats = UsageStats(month=month, months=months)
        for name in [month] if month is not None else months:
            _add_all(stats, self._items(_path(name)))
        return stats

    def _paths(self) -> list[str]:
        return self._store.list_paths(DIRECTORY)

    def _items(self, path: str) -> list[dict[str, HeaderValue]]:
        try:
            header = self._store.read(path).header
        except NotFound:
            return []
        items = header.get("anfragen", [])
        if not isinstance(items, list) or not all(isinstance(item, dict) for item in items):
            raise InvalidInput(f"{path}: Feld 'anfragen' muss eine Liste sein")
        return [item for item in items if isinstance(item, dict)]


def _add_all(stats: UsageStats, items: Iterable[dict[str, HeaderValue]]) -> None:
    for item in items:
        stats.add(item)


def _path(month: str) -> str:
    return f"{DIRECTORY}/{month}.md"


def _is_number(value: HeaderValue) -> bool:
    return isinstance(value, int | float) and not isinstance(value, bool)


def _number(value: HeaderValue) -> float:
    if isinstance(value, bool) or not isinstance(value, int | float):
        return 0.0
    return float(value)


def _count(value: HeaderValue) -> int:
    return value if isinstance(value, int) and not isinstance(value, bool) else 0


def _is_count(value: HeaderValue) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _text(value: HeaderValue) -> str:
    return value if isinstance(value, str) else "unbekannt"
