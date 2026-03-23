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

---

## STT Spike

## Purpose

Record the current speech-to-text engine decision and the benchmark procedure Bob should use before STT implementation work begins.

Evaluation date:
- 2026-03-23

Evaluation context:
- Windows-first
- Python `3.10.3`
- Offline-first
- Older hardware target: dual-core CPU, 4+ GB RAM

## STT Decision Summary

Primary recommendation:
- `Vosk`

Fallback recommendation:
- `faster-whisper`

Native-build alternative:
- `whisper.cpp`

Rationale:
- `Vosk` best matches Bob's current constraints: offline operation, small desktop-suitable models, streaming API, and relatively low install friction on Windows.
- `faster-whisper` is the best fallback when better accuracy is needed and the machine can tolerate a heavier dependency stack and larger runtime footprint.
- `whisper.cpp` remains a viable option, but it introduces more native-build and model-management friction for a Python-first Windows workflow.

## Candidate Comparison

| Candidate | Strengths | Weaknesses | Local feasibility on 2026-03-23 | Recommendation |
| --- | --- | --- | --- | --- |
| `Vosk` | Offline, streaming API, small models, Apache 2.0, Windows wheel available | Older PyPI release cadence; accuracy ceiling may be lower than Whisper-family models | Installed and imported cleanly with `uv`; lightweight package install | Primary STT engine |
| `faster-whisper` | Better accuracy potential, faster and lower memory than `openai/whisper`, 8-bit CPU/GPU quantization support | Heavier dependency footprint, Python 3.9+ requirement, still likely heavier than Vosk on old CPUs | Installed and imported cleanly with `uv`, but pulled a much larger dependency set | Fallback STT engine |
| `whisper.cpp` | Native C/C++ implementation, quantized models, Windows support, strong offline path | More operational friction: model download/build workflow, Python binding is not the main project path | `whispercpp` Python binding installed and imported, but required building during install | Native-build alternative, not default |

## Local Feasibility Checks

Commands executed:

```powershell
uv run --with vosk -- python -c "import vosk; print('vosk import ok')"
uv run --with faster-whisper -- python -c "from faster_whisper import WhisperModel; print('faster-whisper import ok')"
uv run --with whispercpp -- python -c "import whispercpp; print('whispercpp import ok')"
uv run --with vosk -- python -c "import importlib.metadata; print(importlib.metadata.version('vosk'))"
uv run --with faster-whisper -- python -c "import importlib.metadata; print(importlib.metadata.version('faster-whisper'))"
uv run --with whispercpp -- python -c "import importlib.metadata; print(importlib.metadata.version('whispercpp'))"
```

Observed results:
- `vosk` installed and imported successfully.
- `faster-whisper` installed and imported successfully.
- `whispercpp` installed and imported successfully.
- Local resolved versions during this spike:
  - `vosk`: `0.3.45`
  - `faster-whisper`: `1.2.1`
  - `whispercpp`: `0.0.17`

Interpretation:
- `Vosk` is the lowest-friction fit for the MVP default path.
- `faster-whisper` is technically accessible, but its dependency stack is substantially heavier than Vosk.
- `whisper.cpp` is viable, though it is better treated as a deliberate native-tooling choice than the default Python path.

## Reproducible STT Benchmark Procedure

Use this process on the target machine before finalizing `TASK-011`.

Shared assumptions:
- 16 kHz mono audio
- short utterances in the 2-5 second range
- one consistent test phrase set across all engines
- local/offline inference only

### 1. Verify install and startup

Run a minimal import/startup command for each engine and record:
- install success/failure
- whether build tooling is required
- extra model downloads or conversion steps
- Python/runtime constraints

### 2. Measure transcription latency

For each engine:
- transcribe the same 2-5 second utterances at least 20 times
- measure elapsed time from transcription start to transcript result
- record median and worst-case latency

Record:
- model used
- median latency
- p95 or worst-case latency
- whether the result feels acceptable for Bob's response target

### 3. Measure memory and CPU

For each engine:
- record idle RSS after model load
- record peak RSS during transcription
- record CPU usage during repeated transcription runs

Record:
- model size on disk
- memory after load
- peak memory during run
- rough CPU behavior on the target machine

### 4. Measure transcript quality for MVP phrases

For each engine:
- run the same command-like phrase set
- note obvious misses or substitutions
- include short status phrases and local-action phrases from the MVP list

Record:
- phrase
- transcript
- whether the intent would still route correctly

### 5. Acceptance rule

Keep `Vosk` as default if:
- latency stays within Bob's response target on the target machine
- memory stays acceptable for 4+ GB systems
- transcript quality is sufficient for command-style phrases

Use `faster-whisper` as fallback if:
- more accuracy is needed
- the target machine can tolerate the heavier model/runtime cost

Consider `whisper.cpp` if:
- native executable deployment becomes preferable
- benchmark results on the target hardware beat the Python-based fallback path

## Guidance For TASK-011

Before implementing STT adapters:
- keep engine selection behind `src/bob/stt/`
- treat model path and model size as explicit config
- preserve a default/fallback switch in config

Suggested config fields:
- `stt.engine`
- `stt.model`
- `stt.model_path`
- `stt.compute_type`
- `stt.language`
- `stt.fallback_engine`

## Sources

- openWakeWord GitHub README: https://github.com/dscripka/openWakeWord
- Porcupine Python quick start: https://picovoice.ai/docs/quick-start/porcupine-python/
- Porcupine overview: https://picovoice.ai/platform/porcupine/
- Picovoice pricing and AccessKey validation note: https://picovoice.ai/pricing/
- PocketSphinx PyPI: https://pypi.org/project/pocketsphinx/
- CMUSphinx documentation: https://cmusphinx.github.io/wiki/
- Vosk PyPI: https://pypi.org/project/vosk/
- Vosk website: https://alphacephei.com/vosk/
- Vosk models: https://alphacephei.com/vosk/models
- faster-whisper GitHub README: https://github.com/SYSTRAN/faster-whisper
- whisper.cpp GitHub README: https://github.com/ggml-org/whisper.cpp
