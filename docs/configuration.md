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
  - `bob.config.load_wakeword_settings()`

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
- `wakeword.engine`
- `wakeword.keyword`
- `wakeword.threshold`
- `wakeword.model_path`
- `wakeword.inference_framework`
- `observability.logs_directory`
- `observability.log_filename`
- `observability.log_max_bytes`
- `observability.log_backup_count`
- `observability.health_summary_interval_seconds`
- `privacy.allow_debug_audio_capture`
- `tts.volume`
- `tts.sentence_pause_ms`
- `tts.preferred_gender`

## Wake-Word Model Path

- Bob's default local-first wake-word direction is `openWakeWord`
- shared config now includes a `wakeword` section for custom model loading
- expected local custom model path is `models/wakeword/openwakeword/hey_bob.onnx`
- that model file is not assumed to exist on every machine; until it exists, real spoken validation remains blocked

See:
- `docs/openwakeword-custom-model.md`

## Privacy Default

- `privacy.allow_debug_audio_capture` should remain `false` by default
- raw debug audio should only be written when there is explicit operator opt-in
- manual helper commands that save microphone audio should refuse to write unless explicitly enabled

## Suggested Secret Keys

- `OPENAI_API_KEY`
- `AZURE_OPENAI_API_KEY`
- `ELEVENLABS_API_KEY`
