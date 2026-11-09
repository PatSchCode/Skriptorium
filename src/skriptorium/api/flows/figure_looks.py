"""Flow "Figuren-Assistent" (roadmap step 11.5, ADR-123, ADR-124).

1. ``context`` checks the author's answers about a figure's looks and builds the request.
2. ``ai_gateway`` streams the English image description; nothing is stored. The interface
   writes the German lines of "Aussehen" from the answers itself and takes both over into the
   entry when the author says so.

The same flow serves the suggestions (ADR-124): ``context`` builds a request for three answers
per question from the entry and the world, ``ai_gateway`` streams them as lines, the interface
parses them.

Every request is counted through ``record`` as ``figurenassistent`` when the stream ends.
"""

from collections.abc import Mapping
from typing import Final

from skriptorium.ai_gateway import CompletionRequest, Message, ModelConfig
from skriptorium.api.flows.writing import PreparedRequest
from skriptorium.context import ContextBuilder, ContextTooLarge
from skriptorium.storage import InvalidInput

# About 70 words, with room to spare.
MAX_OUTPUT_TOKENS: Final = 600
# Close to the answers; the probe ran at the same value (spikes/figuren-assistent-11.5).
TEMPERATURE: Final = 0.4
# Ten lines of three short phrases, plus room for the model's own thinking: the probe of
# 2026-11-09 needed up to about 2,300 output tokens, a limit of 1,200 cut qwen3.8-max off.
SUGGESTIONS_MAX_OUTPUT_TOKENS: Final = 4_000
# Varied proposals; the probe ran at the same value (spikes/figuren-assistent-11.5).
SUGGESTIONS_TEMPERATURE: Final = 0.8


def prepare_figure_looks(
    builder: ContextBuilder,
    world_id: str,
    entry_id: str,
    answers: Mapping[str, str],
    model: str,
    models: Mapping[str, ModelConfig],
) -> PreparedRequest:
    """Check the order and build the request; runs before anything streams.

    Raises:
        InvalidInput: Unknown model, answers that do not pass the check (age under 18 and
            others), the entry is not a figure, or it is too large for the budget.
        NotFound: The world or the entry does not exist.
    """
    if model not in models:
        raise InvalidInput(f"Unbekanntes Modell: {model}")
    try:
        built = builder.build_figure_looks(world_id, entry_id, answers)
    except ContextTooLarge as error:
        raise InvalidInput(str(error)) from error
    messages = tuple(Message(m.role, m.content) for m in built.messages)
    return PreparedRequest(
        CompletionRequest(model, messages, MAX_OUTPUT_TOKENS, TEMPERATURE),
        built.estimated_tokens,
    )


def prepare_looks_suggestions(
    builder: ContextBuilder,
    world_id: str,
    entry_id: str,
    answers: Mapping[str, str],
    model: str,
    models: Mapping[str, ModelConfig],
) -> PreparedRequest:
    """Check the order and build the request for suggestions; runs before anything streams.

    Raises:
        InvalidInput: Unknown model, answers for unknown questions or too long, the entry is not
            a figure, or world and entry are too large for the budget.
        NotFound: The world or the entry does not exist.
    """
    if model not in models:
        raise InvalidInput(f"Unbekanntes Modell: {model}")
    try:
        built = builder.build_looks_suggestions(world_id, entry_id, answers)
    except ContextTooLarge as error:
        raise InvalidInput(str(error)) from error
    messages = tuple(Message(m.role, m.content) for m in built.messages)
    return PreparedRequest(
        CompletionRequest(model, messages, SUGGESTIONS_MAX_OUTPUT_TOKENS, SUGGESTIONS_TEMPERATURE),
        built.estimated_tokens,
    )
