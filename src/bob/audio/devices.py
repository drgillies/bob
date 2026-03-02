"""Audio device discovery helpers."""

from __future__ import annotations

from collections.abc import Mapping


def format_audio_devices(devices: list[Mapping[str, object]]) -> list[str]:
    """Format discovered audio device entries for human-readable output.

    Testing:
        - Verify output includes index, name, input channels, and output channels.
        - Verify empty input returns the no-devices message.
    """
    if not devices:
        return ["No audio devices found."]

    lines = ["Detected audio devices:"]
    for index, device in enumerate(devices):
        name = str(device.get("name", f"device-{index}"))
        max_input = int(device.get("max_input_channels", 0))
        max_output = int(device.get("max_output_channels", 0))
        lines.append(
            f"[{index}] {name} | inputs={max_input} | outputs={max_output}"
        )
    return lines


def print_audio_devices() -> int:
    """Discover and print audio devices.

    Testing:
        - Verify return code is 0 when discovery succeeds.
        - Verify the command exits non-zero with actionable message if dependency is missing.
    """
    try:
        import sounddevice as sd
    except ImportError:
        print(
            "sounddevice is not installed. Install dependencies with "
            "`uv run --with-requirements requirements.txt -- python -m bob --version`."
        )
        return 1

    devices = sd.query_devices()
    lines = format_audio_devices(list(devices))
    for line in lines:
        print(line)
    return 0
