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

## Suggested Secret Keys

- `OPENAI_API_KEY`
- `AZURE_OPENAI_API_KEY`
- `ELEVENLABS_API_KEY`
