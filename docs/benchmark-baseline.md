# Benchmark Baseline

## Purpose

Record the wake-word spike decision and the benchmark procedure Bob should use on the target machine before wake-word integration.

Evaluation date:
- 2026-03-23

Evaluation context:
- Windows-first
- Python `3.10.3`
- Offline-first where practical
- Low idle CPU on older hardware

## Decision Summary

Primary recommendation:
- `openWakeWord`, but only with a pinned and verified Windows model-asset setup.

Fallback recommendation:
- `PocketSphinx` for the first account-free, fully local fallback path.

Operational alternative:
- `Porcupine` if lower implementation friction or lower idle CPU matters more than strict offline-first behavior.

Rationale:
- `openWakeWord` is still the best fit for Bob's intended direction: local wake-word detection, open-source code, and a modern model approach.
- `PocketSphinx` is the safest fallback because it installed and initialized cleanly on this Windows/Python 3.10 setup without vendor dependencies.
- `Porcupine` looks operationally simple, but the AccessKey requirement makes it a weaker default for a project that is trying to stay local-first and avoid cloud-tied core behavior.

## Candidate Comparison

| Candidate | Strengths | Weaknesses | Local feasibility on 2026-03-23 | Recommendation |
| --- | --- | --- | --- | --- |
| `openWakeWord` | Open-source, wake-word focused, Windows ONNX path, strong architectural fit for Bob | Current plain `pip`/`uv` install was not turnkey on this machine; bundled pre-trained models have non-commercial licensing constraints | Import passed, but default model init failed and ONNX model init also failed because expected model assets were not present in the installed package | Primary direction, but pin setup before integration |
| `Porcupine` | Lightweight, mature SDK, simple package install, strong always-on wake-word focus | Requires Picovoice AccessKey and related vendor validation path | Import passed cleanly | Operational alternative, not default |
| `PocketSphinx` | Fully local, BSD license, keyword spotting support, Windows wheel available, low setup friction | Older decoder and likely weaker accuracy than newer neural wake-word options | Import passed and `Decoder()` initialized successfully | Fallback engine |

## Local Feasibility Checks

Commands executed:

```powershell
uv run --with openwakeword -- python -c "import openwakeword; print('openwakeword import ok')"
uv run --with openwakeword -- python -c "from openwakeword.model import Model; Model()"
uv run --with openwakeword -- python -c "from openwakeword.model import Model; Model(inference_framework='onnx')"
uv run --with pvporcupine -- python -c "import pvporcupine; print('pvporcupine import ok')"
uv run --with pocketsphinx -- python -c "import pocketsphinx; print('pocketsphinx import ok')"
uv run --with pocketsphinx -- python -c "from pocketsphinx import Decoder; Decoder(); print('pocketsphinx decoder init ok')"
```

Observed results:
- `openwakeword` imported successfully.
- `openwakeword` default `Model()` failed because `tflite_runtime` was unavailable.
- `openwakeword` ONNX initialization also failed because the expected ONNX model files were not present in the installed package.
- `pvporcupine` imported successfully.
- `pocketsphinx` imported successfully.
- `pocketsphinx.Decoder()` initialized successfully.

Interpretation:
- `openWakeWord` remains viable, but Bob should not depend on an unpinned default install path for `TASK-006`.
- `PocketSphinx` is the lowest-friction local contingency.
- `Porcupine` is a reasonable practical option if the project accepts an AccessKey dependency.

## Reproducible Benchmark Procedure

Use this process on the target machine before finalizing wake-word integration.

Shared assumptions:
- 16 kHz mono audio
- 16-bit PCM
- `AudioCaptureService` frame handoff
- No STT or TTS running during idle CPU measurement

### 1. Verify install and startup

Run the smoke commands above for each candidate and record:
- install success/failure
- extra files required
- model download or asset setup steps
- vendor/account requirements

### 2. Measure idle CPU and memory

For each candidate:
- run only audio capture plus wake-word detection for 10 minutes
- capture CPU percent and RSS memory every 30 seconds
- note any startup failures or drift

Record:
- average CPU
- peak CPU
- average RSS memory
- startup time

### 3. Measure trigger quality

For each candidate:
- perform 20 intended wake-phrase attempts
- record false rejects
- run 1 hour of room-noise/background-audio observation
- record false accepts

Record:
- threshold/sensitivity used
- false rejects out of 20
- false accepts per hour
- comments about noise sensitivity

### 4. Measure operational friction

Record:
- whether it runs fully offline after setup
- whether an account or key is required
- Windows-specific issues
- licensing notes for code and model assets

### 5. Acceptance rule

Keep `openWakeWord` as primary if:
- its setup is made deterministic on Windows
- idle CPU is acceptable on the target machine
- trigger quality is acceptable in normal room use

Use `PocketSphinx` as the fallback if:
- `openWakeWord` blocks Milestone 1 progress
- a fully local account-free path is required immediately

Use `Porcupine` only if:
- the target machine needs a lower-friction path
- the team accepts AccessKey and vendor-validation constraints

## Guidance For TASK-006

Before integrating wake detection:
- add a small `src/bob/wakeword/` adapter layer
- keep engine selection behind config
- avoid hard-coding a single vendor or model format

Suggested config fields:
- `wakeword.engine`
- `wakeword.model_path`
- `wakeword.threshold`
- `wakeword.access_key_env_var`

## Sources

- openWakeWord GitHub README: https://github.com/dscripka/openWakeWord
- Porcupine Python quick start: https://picovoice.ai/docs/quick-start/porcupine-python/
- Porcupine overview: https://picovoice.ai/platform/porcupine/
- Picovoice pricing and AccessKey validation note: https://picovoice.ai/pricing/
- PocketSphinx PyPI: https://pypi.org/project/pocketsphinx/
- CMUSphinx documentation: https://cmusphinx.github.io/wiki/
