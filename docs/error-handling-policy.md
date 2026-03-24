# Error Handling Policy

## Purpose

This document defines how Bob handles transient runtime failures during the current MVP phase.

Goals:

1. Keep the process running for recoverable failures.
2. Return Bob to a safe `IDLE` state after handled errors.
3. Record enough in-memory context to understand what happened in the current session.
4. Avoid storing raw audio by default.

## Session Memory Policy

Session memory is runtime-only.

It may store:

1. Last intent
2. Last response text
3. Last N user texts
4. Recovered error summaries for the current run

It must not store by default:

1. Raw microphone audio
2. Persistent transcripts across restart
3. Secrets or tokens

Session memory is cleared when Bob restarts.

## Recovery Rules By Component

### Audio Capture

Failure examples:

1. Audio frame read raises unexpectedly
2. Temporary device/stream instability

Recovery behavior:

1. Stop the current audio stream if it is running
2. Attempt one immediate restart of the audio stream
3. Reset wake detection state
4. Return runtime state to `IDLE`
5. Record an in-memory recovery event

If restart does not succeed, Bob should remain in a safe non-triggered state and surface the error through logs or operator visibility.

### Wake-Word Detection

Failure examples:

1. Detector processing raises on a frame
2. Detector internal state becomes invalid

Recovery behavior:

1. Reset detector state
2. Keep the audio stream running unless the failure clearly came from audio
3. Return runtime state to `IDLE`
4. Record an in-memory recovery event

### STT

Failure examples:

1. Model cannot load
2. Transcription fails for a captured utterance

Recovery behavior:

1. Treat the current turn as failed
2. Return runtime state to `IDLE`
3. Record an in-memory recovery event
4. Do not crash the process

Configuration errors should still be surfaced clearly for setup/debugging, but runtime orchestration should not leave Bob stuck in a triggered state.

### Intent Routing / Handler Execution

Failure examples:

1. Routing code raises unexpectedly
2. A local action fails during execution

Recovery behavior:

1. Abort the current turn
2. Return runtime state to `IDLE`
3. Record an in-memory recovery event
4. Prefer a safe fallback response in future work where appropriate

### TTS

Failure examples:

1. Speech engine fails to initialize
2. Speech playback raises during `speak`

Recovery behavior:

1. Stop processing the current spoken response
2. Return runtime state to `IDLE`
3. Record an in-memory recovery event
4. Keep the process alive for the next turn

## Current Implementation Notes

Current code guarantees:

1. Idle-loop audio and wake-word errors are handled in the orchestrator and recover back to `IDLE`
2. STT, action, and TTS failures can be caught by a top-level session-aware controller
3. Session memory is in-process only and capped to recent turns/errors

## Logging Expectations

For each handled error, logs should eventually include:

1. Component
2. Error message
3. Whether recovery completed
4. Relevant state transition back to `IDLE`

Detailed rotating logs and health summaries are tracked by later reliability tasks.

## Non-Goals For This Phase

This phase does not yet add:

1. Persistent memory across restarts
2. Automatic backoff/retry loops for every dependency
3. Debug audio capture by default
4. Full health metrics storage
