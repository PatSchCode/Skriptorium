"""Flow "Einpassen vorschlagen" for a guest (roadmap step 9.13, ADR-102).

1. ``context`` builds the request from the guest's entry and the world of the story.
2. ``ai_gateway`` streams the proposal; nothing is stored. The author changes the text and
   saves it as the guest's relation to the world of the story.

Every request is counted through ``record`` as ``weltenbau`` of the world and the story.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Final

from skriptorium.ai_gateway import CompletionRequest, Message, ModelConfig
from skriptorium.api.flows.writing import PreparedRequest
from skriptorium.context import ContextBuilder, ContextTooLarge
from skriptorium.storage import InvalidInput

# About 150 words, with room to spare.
MAX_OUTPUT_TOKENS: Final = 800
# Inventing within the world, a little more freedom than taking out the looks.
TEMPERATURE: Final = 0.7


@dataclass(frozen=True)
class FitOrder:
    """Which guest of which story to fit in, with which model and wish."""

    world: str
    story: str
    guest_world: str
    entry: str
    model: str
    wish: str = ""


def prepare_guest_fit(
    builder: ContextBuilder, order: FitOrder, models: Mapping[str, ModelConfig]
) -> PreparedRequest:
    """Check the order and build the request; runs before anything streams.

    Raises:
        InvalidInput: Unknown model or a request too large for the budget.
        NotFound: The world, the story, the guest link or the guest's entry does not exist.
    """
    if order.model not in models:
        raise InvalidInput(f"Unbekanntes Modell: {order.model}")
    try:
        built = builder.build_guest_fit(
            order.world, order.story, order.guest_world, order.entry, order.wish
        )
    except ContextTooLarge as error:
        raise InvalidInput(str(error)) from error
    messages = tuple(Message(m.role, m.content) for m in built.messages)
    return PreparedRequest(
        CompletionRequest(order.model, messages, MAX_OUTPUT_TOKENS, TEMPERATURE),
        built.estimated_tokens,
    )
