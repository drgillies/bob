# MVP Command List (Draft)

## Purpose

Define initial intents Bob supports in MVP and expected behavior.

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
