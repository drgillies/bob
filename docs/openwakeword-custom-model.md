# openWakeWord Custom Model Path

## Purpose

Define Bob's expected local-first path for a custom `Hey Bob` wake-word model using `openWakeWord`.

This document does not claim that a production-ready `Hey Bob` model already exists in the repository.
It defines the integration contract Bob will use once that model is sourced or trained.

## Current State

- `openWakeWord` runs on Windows with downloaded ONNX assets.
- `hey_bob` is not available as a built-in model.
- Real spoken validation for `Hey Bob` remains blocked until a compatible custom model file exists locally.

## Expected Local Model Layout

Recommended local path:

```text
models/
  wakeword/
    openwakeword/
      hey_bob.onnx
```

Notes:

- The model file is local machine state, not a committed repository artifact by default.
- The file stem should match Bob's configured wake keyword:
  - file: `hey_bob.onnx`
  - config keyword: `hey_bob`
- If a later workflow uses a different filename, Bob can still load it, but the configured keyword should match the model's prediction label.

## Config Contract

Bob's shared config now expects a `wakeword` section:

```json
{
  "wakeword": {
    "engine": "openwakeword",
    "keyword": "hey_bob",
    "threshold": 0.5,
    "model_path": "models/wakeword/openwakeword/hey_bob.onnx",
    "inference_framework": "onnx"
  }
}
```

Meaning:

- `engine`: current expected wake-word engine
- `keyword`: prediction label Bob treats as a wake event
- `threshold`: minimum score required for a trigger
- `model_path`: local custom model file path
- `inference_framework`: preferred runtime on this Windows setup

## Current Integration Support

Bob's `openWakeWord` adapter now supports:

- loading a custom model by explicit file path
- loading with explicit inference framework
- listing available keywords from the loaded model
- failing fast with a clear error if the configured model file does not exist

## Manual Validation Flow

Once a compatible model file exists locally:

```powershell
$env:PYTHONPATH="src"
uv run --with openwakeword --with-requirements requirements.txt -- python _testing.py wake-openwakeword-live --seconds 15
```

Expected success condition:

- the command initializes the detector using the configured custom model
- `available keywords` includes `hey_bob`
- speaking `Hey Bob` produces one detection event

Expected honest blocker condition:

- if the model file is missing or incompatible, the command should fail with a concrete setup/model error

## Non-Goals

- This document does not define the full training pipeline for creating the model.
- This document does not claim that Bob has already passed real spoken `Hey Bob` validation.
- This document does not introduce vendor-key wake-word services into the default path.
