"""Audio capture service with queue-based callback and recovery support."""

from __future__ import annotations

from dataclasses import dataclass
from queue import Empty, Full, Queue
from threading import Lock
from time import sleep
from typing import Callable


class AudioCaptureError(RuntimeError):
    """Raised when audio capture cannot be started or recovered."""


@dataclass(frozen=True)
class AudioCaptureConfig:
    """Settings for audio capture stream behavior."""

    sample_rate_hz: int = 16000
    channels: int = 1
    dtype: str = "int16"
    frame_duration_ms: int = 80
    max_queue_size: int = 256
    input_device: str | None = None
    recovery_wait_seconds: float = 1.0
    max_recovery_attempts: int = 30

    @property
    def block_size(self) -> int:
        """Compute callback frame block size in samples."""
        return int(self.sample_rate_hz * (self.frame_duration_ms / 1000.0))

    @property
    def frame_duration_seconds(self) -> float:
        """Return the callback frame duration in seconds."""
        return self.frame_duration_ms / 1000.0

    @property
    def sample_width_bytes(self) -> int:
        """Return the sample width for the configured dtype."""
        if self.dtype == "int16":
            return 2
        raise ValueError(f"Unsupported audio dtype for sample width lookup: {self.dtype}")


class AudioCaptureService:
    """Capture microphone frames through a non-blocking callback queue."""

    def __init__(
        self,
        config: AudioCaptureConfig | None = None,
        stream_factory: Callable[..., object] | None = None,
    ) -> None:
        self.config = config or AudioCaptureConfig()
        self._stream_factory = stream_factory or self._default_stream_factory
        self._frame_queue: Queue[bytes] = Queue(maxsize=self.config.max_queue_size)
        self._stream: object | None = None
        self._lock = Lock()

    @staticmethod
    def _default_stream_factory(**kwargs: object) -> object:
        try:
            import sounddevice as sd
        except ImportError as exc:
            raise AudioCaptureError(
                "sounddevice is not installed. Install dependencies before audio capture."
            ) from exc

        return sd.RawInputStream(**kwargs)

    def _audio_callback(
        self,
        indata: bytes | bytearray | memoryview,
        frames: int,  # noqa: ARG002
        time_info: object,  # noqa: ARG002
        status: object,  # noqa: ARG002
    ) -> None:
        # Callback must stay non-blocking; drop oldest frame if queue is full.
        frame_bytes = bytes(indata)
        try:
            self._frame_queue.put_nowait(frame_bytes)
        except Full:
            try:
                self._frame_queue.get_nowait()
            except Empty:
                pass
            try:
                self._frame_queue.put_nowait(frame_bytes)
            except Full:
                # If still full, drop frame to keep callback realtime-safe.
                pass

    def start(self) -> None:
        """Open and start the audio stream."""
        with self._lock:
            if self.is_running():
                return

            try:
                self._stream = self._stream_factory(
                    samplerate=self.config.sample_rate_hz,
                    channels=self.config.channels,
                    dtype=self.config.dtype,
                    blocksize=self.config.block_size,
                    device=self.config.input_device,
                    callback=self._audio_callback,
                )
                self._stream.start()
            except Exception as exc:  # pragma: no cover - exercised via tests
                self._stream = None
                raise AudioCaptureError(f"Failed to start audio capture: {exc}") from exc

    def stop(self) -> None:
        """Stop and close the audio stream if active."""
        with self._lock:
            if self._stream is None:
                return
            try:
                if hasattr(self._stream, "stop"):
                    self._stream.stop()
            finally:
                if hasattr(self._stream, "close"):
                    self._stream.close()
                self._stream = None

    def is_running(self) -> bool:
        """Return True if stream is currently active."""
        return self._stream is not None

    def read_frame(self, timeout_seconds: float | None = None) -> bytes | None:
        """Read one frame from the callback queue."""
        try:
            return self._frame_queue.get(timeout=timeout_seconds)
        except Empty:
            return None

    def recover_stream(self) -> bool:
        """Attempt to recover stream by restart loop."""
        for _ in range(self.config.max_recovery_attempts):
            self.stop()
            try:
                self.start()
                return True
            except AudioCaptureError:
                sleep(self.config.recovery_wait_seconds)
        return False
