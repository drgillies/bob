# Configuration

## Files

- `config/settings.example.json`: committed baseline template for shared defaults.
- `config/settings.local.json`: local machine/project settings (ignored by git).
- `.env.example`: committed template for sensitive secrets only (keys/tokens).
- `.env`: local secrets file (ignored by git).

## Usage

1. Create your local file from the template:
   - PowerShell: `Copy-Item config/settings.example.json config/settings.local.json`
2. Create your local environment file:
   - PowerShell: `Copy-Item .env.example .env`
3. Edit:
   - `config/settings.local.json` for non-sensitive runtime/config values
   - `.env` for sensitive values only (API keys, tokens, credentials)
4. Keep non-sensitive shared defaults in `config/settings.example.json`; keep only secret key names/placeholders in `.env.example`.

## Runtime Loader

- Runtime config should be loaded through `bob.config.load_app_config()`.
- Merge order is:
  1. `config/settings.example.json`
  2. `config/settings.local.json` if present
  3. `.env` plus process environment for supported secret keys only
- Existing callers that only need a slice can use:
  - `bob.config.load_open_app_settings()`
  - `bob.config.load_stt_settings()`

Validation goals:

- required sections must exist
- required values must have the expected type
- invalid JSON or malformed `.env` input fails fast with actionable errors
- secrets are loaded, but should not be printed or logged verbatim

## Split of Responsibility

- Put in `config/settings.local.json`:
  - names
  - timeout values
  - audio/device options
  - behavior toggles
- Put in `.env`:
  - API keys
  - access tokens
  - credentials/secrets

## Suggested Fields

- `project.name`
- `assistant.name`
- `assistant.wake_phrase`
- `timeouts.listen_seconds`
- `timeouts.response_start_seconds`
- `timeouts.network_fallback_seconds`
- `audio.input_device`
- `audio.output_device`
- `audio.sample_rate_hz`
- `audio.watchdog_timeout_seconds`
- `observability.logs_directory`
- `observability.log_filename`
- `observability.log_max_bytes`
- `observability.log_backup_count`
- `observability.health_summary_interval_seconds`

## Suggested Secret Keys

- `OPENAI_API_KEY`
- `AZURE_OPENAI_API_KEY`
- `ELEVENLABS_API_KEY`
