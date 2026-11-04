"""Flows across module boundaries, kept out of the routes (ADR-020)."""

from skriptorium.api.flows.appearance import prepare_appearance
from skriptorium.api.flows.describe import DescribeOrder, prepare_description
from skriptorium.api.flows.removal import GuestUse, WorldDeletion, delete_world, world_deletion
from skriptorium.api.flows.summary import (
    SUMMARY_TEMPERATURE,
    SummaryFailure,
    SummaryOutcome,
    summarize_chapter,
)
from skriptorium.api.flows.worldbuilder import (
    Turn,
    WorldOrder,
    prepare_worldbuilder,
    stream_answer,
    stream_worldbuilder,
)
from skriptorium.api.flows.writing import (
    CONTINUE,
    DEFAULT_MODEL,
    MAX_OUTPUT_TOKENS,
    TEMPERATURE,
    PreparedRequest,
    Scene,
    WriteOrder,
    error_kind,
    prepare_request,
    stream_events,
)

__all__ = [
    "CONTINUE",
    "DEFAULT_MODEL",
    "MAX_OUTPUT_TOKENS",
    "SUMMARY_TEMPERATURE",
    "TEMPERATURE",
    "DescribeOrder",
    "GuestUse",
    "PreparedRequest",
    "Scene",
    "SummaryFailure",
    "SummaryOutcome",
    "Turn",
    "WorldDeletion",
    "WorldOrder",
    "WriteOrder",
    "delete_world",
    "error_kind",
    "prepare_appearance",
    "prepare_description",
    "prepare_request",
    "prepare_worldbuilder",
    "stream_answer",
    "stream_events",
    "stream_worldbuilder",
    "summarize_chapter",
    "world_deletion",
]
