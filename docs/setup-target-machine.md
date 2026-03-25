# Setup Target Machine (Old Hardware)

## Goal

Install and run Bob reliably on older Windows hardware.

## Minimum Assumptions

- Windows desktop/laptop
- 4+ GB RAM
- Dual-core CPU
- Working microphone and speakers/headset

## Installation Steps (PowerShell)

1. Install Python 3.10+.
2. Clone repository.
3. Install `uv`:
   - `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
4. Create local config files:
   - `Copy-Item config/settings.example.json config/settings.local.json`
   - `Copy-Item .env.example .env`
5. Set import path for `src/` layout:
   - `$env:PYTHONPATH = "src"`
6. Validate baseline with `uv`:
   - `uv run --with-requirements requirements.txt -- python -m bob --version`
   - `uv run --with-requirements requirements.txt -- python -m bob --list-audio-devices`

## Startup Mode Decision

- Preferred MVP startup mode: user-session startup via Windows Task Scheduler at logon
- Preferred MVP packaging mode: run from source with `uv`

Why:
- microphone access is more reliable in a logged-in user session than in a true Windows service context
- current repo workflow already supports source-run cleanly

See [service-mode.md](service-mode.md) for the full decision and install/uninstall guidance.

## Suggested Startup Wrapper

Create and use `scripts/start-bob.ps1`.

Contents:

```powershell
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

$env:PYTHONPATH = "src"

uv run --with-requirements requirements.txt -- python -m bob
```

Then use this as the scheduled action command:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\repos\bob\scripts\start-bob.ps1"
```

Current expected behavior at this project stage:
- the wrapper starts successfully
- Bob launches through the current bootstrap CLI
- the process exits after bootstrap because there is not yet a long-running runtime entrypoint

## Local Configuration

- Set non-sensitive values in `config/settings.local.json`:
  - assistant name
  - timeout settings
  - audio device settings
- Set secrets in `.env`:
  - API keys/tokens if required by chosen providers

## Validation Checklist

- Microphone input can be captured.
- Speaker output works.
- Wake phrase detection starts without errors.
- Logs are written with no secret values.

## Operations Notes

- Prefer local/offline processing where possible.
- Keep runtime defaults conservative for low CPU usage.
- Validate Bob manually before enabling automatic startup.
