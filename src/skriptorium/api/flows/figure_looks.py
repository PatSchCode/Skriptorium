"""Flow "Figuren-Assistent" (roadmap step 11.5, ADR-123).

1. ``context`` checks the author's answers about a figure's looks and builds the request.
2. ``ai_gateway`` streams the English image description; nothing is stored. The interface
   writes the German lines of "Aussehen" from the answers itself and takes both over into the
   entry when the author says so.

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
