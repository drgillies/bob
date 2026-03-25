# MVP Command List (Draft)

## Purpose

Define initial intents Bob supports in MVP and expected behavior.

## Wake Phrase

- Final MVP wake phrase: `Hey Bob`

Rationale:

- short and easy to remember
- aligned with the current assistant name and existing docs/config
- distinct enough for MVP testing, while still natural to say out loud

Operational note:

- `Hey Bob` is the phrase Bob should respond to in user-facing docs and config.
- Wake-engine support is still constrained by the chosen detector and available model assets.
- If `openWakeWord` remains the primary engine, production-quality support for `Hey Bob` may require custom model work rather than assuming a built-in phrase model exists.

## Time and Date

- "What time is it?"
- "What is today's date?"

Expected behavior:
- Return local system time/date clearly and briefly.

## Basic Status

- "Are you there?"
- "What can you do?"
- "Are you listening?"

Expected behavior:
- Confirm active status and summarize supported command categories.

## Local Actions (If Enabled)

- "Open <app>"
- "Play music"
- "Pause music"

Expected behavior:
- Execute configured local action or return safe fallback if unavailable.

## Fallback Behavior

- If intent is unknown, respond with:
  - a short clarification prompt, or
  - a capability summary.

## Notes

- Command coverage is intentionally small for MVP.
- Expand only after reliability baseline is stable.
- Wake-phrase false-trigger and custom-model caveats are tracked in `docs/benchmark-baseline.md`.
