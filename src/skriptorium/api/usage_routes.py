"""Usage statistics by world, story, kind and model (step 9.11, ADR-100).

The month files hold identifiers only; names, forms and the archive mark come from ``canon`` and
``manuscript`` when the statistics are asked for. A world or story that no longer exists is shown
as deleted with its identifier.
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from skriptorium.api.context import Services, ServicesDep, current_session
from skriptorium.api.usage import Group, Totals, UsageStats, WorldGroup
from skriptorium.canon import World
from skriptorium.manuscript import Story

router = APIRouter(prefix="/api", dependencies=[Depends(current_session)])


class UsageTotalsOut(BaseModel):
    """Sums over a set of requests; ``cache_share`` is ``None`` if no provider reported a cache."""

    requests: int
    input_tokens: int
    output_tokens: int
    cost_usd: float
    without_cost: int
    cache_read_tokens: int
    cache_share: float | None


class KindUsageOut(UsageTotalsOut):
    """Sums of one kind of request (``schreiben``, ``weltenbau`` …)."""

    kind: str


class ModelUsageOut(UsageTotalsOut):
    """Sums of one model."""

    model: str


class UsageGroupOut(BaseModel):
    """Sums of a set of requests, by kind and by model; both lists by number of requests."""

    totals: UsageTotalsOut
    kinds: list[KindUsageOut]
    models: list[ModelUsageOut]


class StoryUsageOut(BaseModel):
    """The requests of one story; ``title`` and ``form`` are ``None`` if it was deleted."""

    id: str
    title: str | None
    form: str | None
    archived: bool
    deleted: bool
    usage: UsageGroupOut


class WorldUsageOut(BaseModel):
    """The requests of one world: all, on the world itself (``own``) and per story."""

    id: str
    name: str | None
    archived: bool
    deleted: bool
    usage: UsageGroupOut
    own: UsageGroupOut
    stories: list[StoryUsageOut]


class UsageStatsOut(BaseModel):
    """Statistics of ``month`` or, if ``None``, of all months; ``months`` newest first.

    ``worlds`` (by cost, highest first) and ``unassigned`` together make up ``total``.
    """

    month: str | None
    months: list[str]
    total: UsageGroupOut
    worlds: list[WorldUsageOut]
    unassigned: UsageGroupOut


@router.get("/usage/stats")
def usage_stats(found: ServicesDep, month: str | None = None) -> UsageStatsOut:
    """Usage of ``month`` (``JJJJ-MM``) or of all months by world, story, kind and model."""
    stats: UsageStats = found.usage.stats(month)
    worlds = {world.id: world for world in found.canon.list_worlds()}
    out = [
        _world(world_id, group, worlds.get(world_id), found)
        for world_id, group in stats.worlds.items()
    ]
    out.sort(key=lambda world: (-world.usage.totals.cost_usd, world.name or world.id))
    return UsageStatsOut(
        month=stats.month,
        months=stats.months,
        total=_group(stats.total),
        worlds=out,
        unassigned=_group(stats.unassigned),
    )


def _world(world_id: str, group: WorldGroup, world: World | None, found: Services) -> WorldUsageOut:
    stories: dict[str, Story] = {}
    if world is not None:
        stories = {story.id: story for story in found.manuscript.list_stories(world.id)}
    listed = [
        _story(story_id, usage, stories.get(story_id)) for story_id, usage in group.stories.items()
    ]
    listed.sort(key=lambda story: (-story.usage.totals.cost_usd, story.title or story.id))
    return WorldUsageOut(
        id=world_id,
        name=world.name if world else None,
        archived=world.archived if world else False,
        deleted=world is None,
        usage=_group(group.all),
        own=_group(group.own),
        stories=listed,
    )


def _story(story_id: str, group: Group, story: Story | None) -> StoryUsageOut:
    return StoryUsageOut(
        id=story_id,
        title=story.title if story else None,
        form=story.form if story else None,
        archived=story.archived if story else False,
        deleted=story is None,
        usage=_group(group),
    )


def _group(group: Group) -> UsageGroupOut:
    kinds = [
        KindUsageOut(kind=kind, **_totals(totals).model_dump())
        for kind, totals in group.kinds.items()
    ]
    models = [
        ModelUsageOut(model=model, **_totals(totals).model_dump())
        for model, totals in group.models.items()
    ]
    kinds.sort(key=lambda kind: (-kind.requests, kind.kind))
    models.sort(key=lambda model: (-model.requests, model.model))
    return UsageGroupOut(totals=_totals(group.totals), kinds=kinds, models=models)


def _totals(totals: Totals) -> UsageTotalsOut:
    return UsageTotalsOut(
        requests=totals.requests,
        input_tokens=totals.input_tokens,
        output_tokens=totals.output_tokens,
        cost_usd=totals.cost_usd,
        without_cost=totals.without_cost,
        cache_read_tokens=totals.cache_read_tokens,
        cache_share=totals.cache_share,
    )
