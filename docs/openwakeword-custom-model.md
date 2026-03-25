# openWakeWord Custom Model Path

## Purpose

Define Bob's expected local-first path for a custom `Hey Bob` wake-word model using `openWakeWord`.

This document does not claim that a production-ready `Hey Bob` model already exists in the repository.
It defines the integration contract Bob will use once that model is sourced or trained.

## Current State

- `openWakeWord` runs on Windows with downloaded ONNX assets.
- `hey_bob` is not available as a built-in model.
- Real spoken validation for `Hey Bob` remains blocked until a compatible custom model file exists locally.

## Temporary Engineering Override

To unblock wake-word testing without changing the product decision, Bob currently supports a temporary engineering phrase:

- product phrase: `Hey Bob`
- temporary engineering phrase: `Yo homie`
- temporary engineering keyword/model: `yo_homie`

Meaning:

- `Hey Bob` remains the intended user-facing wake phrase.
- `Yo homie` is only the current engineering/testing substitute because a community `openWakeWord` model exists for it.
- This is a temporary unblocker, not a final product naming decision.

## TASK-027 Sourcing Outcome

What was checked:

- the official `openWakeWord` training guidance
- the official automated training notebook
- the upstream synthetic dataset generation repository referenced by `openWakeWord`
- the Home Assistant community wakeword collection referenced from the `openWakeWord` README

Observed result:

- the official automated training notebook says automated custom-model training is currently supported on Linux only because the sample-generation path depends on Piper tooling
- the upstream synthetic dataset generation repository also describes GPU-friendly synthetic generation tooling rather than a lightweight Windows-local path
- the referenced Home Assistant community wakeword collection did not contain a `Bob` or `hey_bob` model artifact when checked on 2026-03-25

Current conclusion:

- Bob's integration path is ready
- Bob does not currently have a sourced `hey_bob.onnx` artifact
- Bob also does not currently have a supported Windows-local official training path for producing that artifact
- Bob does now have a temporary engineering artifact, `yo_homie.onnx`, that can be used to unblock live wake-word testing without changing the product phrase decision

Next practical path:

1. run the official automated training flow in Linux or Google Colab to produce a baseline `hey_bob.onnx`
2. place the resulting file at `models/wakeword/openwakeword/hey_bob.onnx`
3. rerun Bob's live wake validation on Windows

## Current Temporary Engineering Validation

Current engineering test path:

- phrase: `Yo homie`
- keyword: `yo_homie`
- model path: `models/wakeword/openwakeword/yo_homie.onnx`

Observed result on 2026-03-25:

- the community `yo_homie.onnx` model downloaded successfully
- Bob initialized `openWakeWord` successfully with that model
- available keywords included `yo_homie`
- after fixing Bob's live frame conversion to `int16`, real spoken `Yo homie` triggered successfully on the target machine

This means wake-word testing is now unblocked at the runtime and real spoken validation level, even though it does not yet validate the final product phrase `Hey Bob`.

## Expected Local Model Layout

Recommended local path:

```text
models/
  wakeword/
    openwakeword/
      yo_homie.onnx
```

Notes:

- The model file is local machine state, not a committed repository artifact by default.
- The current temporary engineering file stem matches the configured wake keyword:
  - file: `yo_homie.onnx`
  - config keyword: `yo_homie`
- If a later workflow uses a different filename, Bob can still load it, but the configured keyword should match the model's prediction label.

## Config Contract

Bob's shared config now expects a `wakeword` section:

```json
{
  "wakeword": {
    "engine": "openwakeword",
    "phrase": "Yo homie",
    "keyword": "yo_homie",
    "threshold": 0.5,
    "model_path": "models/wakeword/openwakeword/yo_homie.onnx",
    "inference_framework": "onnx"
  }
}
```

Meaning:

- `engine`: current expected wake-word engine
- `phrase`: the currently spoken engineering/runtime phrase for the loaded model
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
- `available keywords` includes `yo_homie`
- speaking `Yo homie` produces one detection event
- Bob reports `IDLE -> TRIGGERED -> IDLE`

Expected honest blocker condition:

- if the model file is missing or incompatible, the command should fail with a concrete setup/model error

## Non-Goals

- This document does not define the full training pipeline for creating the model.
- This document does not claim that Bob has already passed real spoken `Hey Bob` validation.
- This document does not introduce vendor-key wake-word services into the default path.
