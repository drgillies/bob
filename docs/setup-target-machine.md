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
3. Create and activate virtual environment:
   - `python -m venv .venv`
   - `.venv\Scripts\Activate.ps1`
4. Install dependencies:
   - `python -m pip install --upgrade pip`
   - `pip install -r requirements.txt`
5. Create local config files:
   - `Copy-Item config/settings.example.json config/settings.local.json`
   - `Copy-Item .env.example .env`

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
