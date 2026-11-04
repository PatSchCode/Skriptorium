"""Flow "Welt endgültig löschen" (step 9.9, ADR-098, FR-036).

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
