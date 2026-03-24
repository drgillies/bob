"""Intent routing and skills support for Bob."""

from bob.skills.actions import (
    LocalActionError,
    OpenAppAction,
    OpenAppActionConfig,
    build_open_app_action,
    normalize_app_name,
)
from bob.skills.handlers import CoreIntentHandler, CoreIntentHandlerConfig
from bob.skills.router import IntentRouter, IntentRouterConfig, normalize_text

__all__ = [
    "CoreIntentHandler",
    "CoreIntentHandlerConfig",
    "IntentRouter",
    "IntentRouterConfig",
    "LocalActionError",
    "OpenAppAction",
    "OpenAppActionConfig",
    "build_open_app_action",
    "normalize_app_name",
    "normalize_text",
]
