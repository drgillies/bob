# Architecture (MVP)

## Purpose

Define module boundaries, data flow, and integration points for Bob's MVP.

## High-Level Modules

- `src/audio/`: microphone capture, buffering, and VAD/noise gating
- `src/wakeword/`: wake phrase detection
- `src/stt/`: speech-to-text adapters
- `src/orchestrator/`: request routing and state coordination
- `src/skills/`: intent handlers/command execution
- `src/tts/`: text-to-speech output
- `src/observability/`: logging and health metrics
- `src/data/model/`: shared models and validation
- `src/config/`: config loading and normalization

## Primary Data Flow

1. Audio input captures stream.
2. Wake word layer detects activation.
3. STT converts utterance to text.
4. Orchestrator selects skill/intent.
5. Skill returns response/action result.
6. TTS produces spoken output.
7. Observability records key events/errors.

## Core Interfaces (Draft)

- Audio frame event
- Wake detection event
- Transcription result
- Intent request/response
- TTS request
- Health/status event

## Error Handling Strategy

- Recover from transient audio/STT/TTS failures without process restart.
- Centralize exception handling at orchestrator boundaries.
- Log actionable context with stable identifiers.

## Open Decisions

- Final library stack for wakeword/STT/TTS.
- Event transport approach (callbacks vs queue/message bus).
- Session memory implementation details for MVP.
