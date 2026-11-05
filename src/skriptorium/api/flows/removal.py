"""Flows "Welt endgültig löschen" (step 9.9, ADR-098, FR-036) and "Kanon-Eintrag löschen"
(step 10.1, ADR-106).

A world lies with all its stories in its own folder; from outside, only guest links in stories
of other worlds point into it, together with the facts and led characters about those guests.
``canon`` and ``manuscript`` do not know each other, so the flow across the world border lives
here:

1. ``canon`` checks that the world is archived and that the typed name is exactly its name.
2. In every story of another world, ``manuscript`` removes the guest links into the world and the
   facts and led characters that name one of those guests - unless the identifier also names an
   entry of the story's own world or another guest, which the fact may mean as well.
3. ``canon`` deletes the world's folder with its stories and their rows of the search index.

The usage files (``system/verbrauch/``) carry no reference to worlds and stay as they are.

Deleting a canon entry takes its traces in stories with it the same way: in stories of its own
world the led character and the facts with its identifier, in stories of other worlds the guest
link (with its relation) and there, too, led character and facts - each time unless the
identifier also names another entry the story may mean (a guest with the same identifier, or an
entry of the story's own world).
"""

from collections.abc import Iterator
from dataclasses import dataclass

from skriptorium.canon import CanonService
from skriptorium.manuscript import ManuscriptService, Story
from skriptorium.storage import NotFound


@dataclass(frozen=True)
class GuestUse:
    """A story of another world with guest links into the world to be deleted."""

    world: str
    world_name: str
    story: str
    story_title: str
    guests: tuple[str, ...]
    """Names of the guest entries, in the order of the links."""
    facts: int
    """Story facts that go with the guests."""


@dataclass(frozen=True)
class WorldDeletion:
    """What deleting a world for good takes with it (shown before the author confirms)."""

    name: str
    entries: int
    images: int
    maps: int
    stories: int
    guest_uses: tuple[GuestUse, ...]


@dataclass(frozen=True)
class _Use:
    story: Story
    entries: frozenset[str]
    """Identifiers whose facts and led characters go with the links."""


def world_deletion(
    canon: CanonService, manuscripts: ManuscriptService, world_id: str
) -> WorldDeletion:
    """The consequences of deleting ``world_id`` for good; changes nothing.

    Raises:
        NotFound: The world does not exist.
    """
    world = canon.get_world(world_id)
    contents = canon.world_contents(world_id)
    names = {w.id: w.name for w in canon.list_worlds()}
    uses = tuple(
        GuestUse(
            world=use.story.world,
            world_name=names.get(use.story.world, use.story.world),
            story=use.story.id,
            story_title=use.story.title,
            guests=tuple(
                _entry_name(canon, world_id, link.entry)
                for link in use.story.guest_links
                if link.world == world_id
            ),
            facts=sum(1 for fact in use.story.facts if fact.entry in use.entries),
        )
        for use in _guest_uses(canon, manuscripts, world_id)
    )
    return WorldDeletion(
        name=world.name,
        entries=contents.entries,
        images=contents.images,
        maps=contents.maps,
        stories=len(manuscripts.list_stories(world_id)),
        guest_uses=uses,
    )


def delete_world(
    canon: CanonService, manuscripts: ManuscriptService, world_id: str, name: str
) -> None:
    """Delete an archived world for good, with its guests in stories of other worlds.

    Raises:
        NotFound: The world does not exist.
        InvalidInput: The world is not archived, or ``name`` is not exactly its name; nothing
            is changed.
    """
    canon.check_world_deletion(world_id, name)
    for use in list(_guest_uses(canon, manuscripts, world_id)):
        manuscripts.remove_guest_world(use.story.world, use.story.id, world_id, use.entries)
    canon.delete_world(world_id, name)


def _guest_uses(
    canon: CanonService, manuscripts: ManuscriptService, world_id: str
) -> Iterator[_Use]:
    """The stories of other worlds with guest links into ``world_id``."""
    for other in canon.list_worlds():
        if other.id == world_id:
            continue
        own: set[str] | None = None
        for story in manuscripts.list_stories(other.id):
            guests = {link.entry for link in story.guest_links if link.world == world_id}
            if not guests:
                continue
            if own is None:
                own = {entry.id for entry in canon.list_entries(other.id)}
            elsewhere = {link.entry for link in story.guest_links if link.world != world_id}
            yield _Use(story, frozenset(guests - own - elsewhere))


def _entry_name(canon: CanonService, world_id: str, entry_id: str) -> str:
    """The name of a guest entry; its identifier if the entry is gone (deleted by hand)."""
    try:
        return canon.get_entry(world_id, entry_id).name
    except NotFound:
        return entry_id


@dataclass(frozen=True)
class EntryUse:
    """A story that holds traces of the canon entry to be deleted."""

    world: str
    world_name: str
    story: str
    story_title: str
    guest: bool
    """The entry is bound into this story of another world as a guest."""
    relation: bool
    """The guest has a relation to that world (step 9.13)."""
    led: bool
    """The author leads the entry in this story; goes with it."""
    facts: int
    """Story facts about the entry that go with it."""


@dataclass(frozen=True)
class EntryDeletion:
    """What deleting a canon entry takes with it (shown before the author confirms)."""

    name: str
    images: int
    markers: int
    """Markers on the maps of the world."""
    uses: tuple[EntryUse, ...]


@dataclass(frozen=True)
class _EntryTrace:
    story: Story
    guest_world: str | None
    with_facts: bool


def entry_deletion(
    canon: CanonService, manuscripts: ManuscriptService, world_id: str, entry_id: str
) -> EntryDeletion:
    """The consequences of deleting a canon entry; changes nothing.

    Raises:
        NotFound: The world or the entry does not exist.
    """
    entry = canon.get_entry(world_id, entry_id)
    world = canon.get_world(world_id)
    names = {w.id: w.name for w in canon.list_worlds()}
    uses = []
    for trace in _entry_traces(canon, manuscripts, world_id, entry_id):
        story = trace.story
        link = next(
            (
                g
                for g in story.guest_links
                if trace.guest_world is not None and (g.world, g.entry) == (world_id, entry_id)
            ),
            None,
        )
        uses.append(
            EntryUse(
                world=story.world,
                world_name=names.get(story.world, story.world),
                story=story.id,
                story_title=story.title,
                guest=link is not None,
                relation=link is not None and link.relation != "",
                led=trace.with_facts and entry_id in story.controlled_characters,
                facts=sum(1 for f in story.facts if f.entry == entry_id) if trace.with_facts else 0,
            )
        )
    markers = sum(1 for m in world.maps for marker in m.markers if marker.entry == entry_id)
    return EntryDeletion(entry.name, len(entry.images), markers, tuple(uses))


def delete_entry_with_traces(
    canon: CanonService, manuscripts: ManuscriptService, world_id: str, entry_id: str
) -> None:
    """Delete a canon entry with its images, markers and its traces in stories.

    Raises:
        NotFound: The world or the entry does not exist; nothing is changed.
    """
    canon.get_entry(world_id, entry_id)
    for trace in list(_entry_traces(canon, manuscripts, world_id, entry_id)):
        manuscripts.remove_entry_uses(
            trace.story.world, trace.story.id, entry_id, trace.guest_world, trace.with_facts
        )
    canon.delete_entry(world_id, entry_id)


def _entry_traces(
    canon: CanonService, manuscripts: ManuscriptService, world_id: str, entry_id: str
) -> Iterator[_EntryTrace]:
    """The stories that hold traces of the entry, with what goes from each."""
    for world in canon.list_worlds():
        own: set[str] | None = None
        for story in manuscripts.list_stories(world.id):
            if world.id == world_id:
                if any(link.entry == entry_id for link in story.guest_links):
                    continue
                if entry_id in story.controlled_characters or any(
                    f.entry == entry_id for f in story.facts
                ):
                    yield _EntryTrace(story, None, with_facts=True)
                continue
            if not any((g.world, g.entry) == (world_id, entry_id) for g in story.guest_links):
                continue
            if own is None:
                own = {entry.id for entry in canon.list_entries(world.id)}
            elsewhere = any(g.entry == entry_id and g.world != world_id for g in story.guest_links)
            yield _EntryTrace(story, world_id, with_facts=entry_id not in own and not elsewhere)
