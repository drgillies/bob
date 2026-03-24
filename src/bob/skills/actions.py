"""Local action dispatch for Bob skills."""

from __future__ import annotations

from dataclasses import dataclass, field
from subprocess import Popen
from typing import Callable, Mapping

from bob.data.model import ActionResult


class LocalActionError(RuntimeError):
    """Raised when a configured local action cannot be executed."""


@dataclass(frozen=True)
class OpenAppActionConfig:
    """Config for app alias resolution and launch behavior."""

    enabled: bool = True
    aliases: dict[str, str] = field(default_factory=dict)


def normalize_app_name(app_name: str) -> str:
    """Normalize an app alias for config lookup."""
    return " ".join(app_name.lower().strip().split())


class OpenAppAction:
    """Resolve configured app aliases and launch them."""

    def __init__(
        self,
        config: OpenAppActionConfig | None = None,
        *,
        launcher: Callable[[str], object] | None = None,
    ) -> None:
        self._config = config or OpenAppActionConfig()
        self._launcher = launcher or self._default_launcher

    @staticmethod
    def _default_launcher(command: str) -> object:
        return Popen([command])

    def execute(self, app_name: str) -> ActionResult:
        """Launch a configured app alias if enabled and known."""
        normalized_app_name = normalize_app_name(app_name)
        if not self._config.enabled:
            return ActionResult(
                succeeded=False,
                message="App launching is disabled right now.",
                metadata={"app_name": normalized_app_name},
            )

        command = self._config.aliases.get(normalized_app_name)
        if not command:
            return ActionResult(
                succeeded=False,
                message=f"I don't know how to open {normalized_app_name} yet.",
                metadata={"app_name": normalized_app_name},
            )

        try:
            self._launcher(command)
        except Exception as exc:
            raise LocalActionError(
                f"Failed to launch app '{normalized_app_name}' with command '{command}': {exc}"
            ) from exc

        return ActionResult(
            succeeded=True,
            message=f"Opening {normalized_app_name}.",
            metadata={"app_name": normalized_app_name, "command": command},
        )


def build_open_app_action(
    settings: Mapping[str, object] | None = None,
    *,
    launcher: Callable[[str], object] | None = None,
) -> OpenAppAction:
    """Build open-app action from settings-like mapping."""
    config = settings or {}
    enabled = bool(config.get("enabled", True))
    aliases_value = config.get("aliases", {})
    aliases: dict[str, str] = {}
    if isinstance(aliases_value, Mapping):
        for key, value in aliases_value.items():
            aliases[normalize_app_name(str(key))] = str(value)

    return OpenAppAction(
        OpenAppActionConfig(
            enabled=enabled,
            aliases=aliases,
        ),
        launcher=launcher,
    )
