"""Intent routing and skills support for Bob."""

from bob.skills.handlers import CoreIntentHandler, CoreIntentHandlerConfig
from bob.skills.router import IntentRouter, IntentRouterConfig, normalize_text

__all__ = [
    "CoreIntentHandler",
    "CoreIntentHandlerConfig",
    "IntentRouter",
    "IntentRouterConfig",
    "normalize_text",
]
