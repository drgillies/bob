# Bob Phase 0 Scrumboard Implementation Plan for a Lightweight Offline Voice Assistant in Python

## Project framing and working architecture

This plan turns the Phase 0 scope into a scrumboard-ready backlog that is organised around measurable milestones, with explicit “definition of done” and acceptance criteria for each ticket. It assumes a Windows-first deployment on older hardware (dual-core CPU, 4+ GB RAM, mic + speakers), with offline-first behaviour and low steady-state CPU while always listening.

The practical, low-CPU architecture that best matches your goals is a gated pipeline with a small always-on “front end” and a heavier “on demand” back end:

**Always-on front end (idle loop, low CPU):** continuous microphone capture → lightweight noise gate/VAD (optional) → wake phrase detector. This stage must do *no full ASR* and should avoid large models.

**Back end (only after wake):** record a short utterance (with VAD end-of-speech) → speech-to-text → intent router → skill handler → response text → text-to-speech playback → return to idle.

This gate-first approach is also the main way to hit the latency target (“response starts within ~1–3s after user stops speaking”) without burning CPU continuously.

Key engineering decisions that should be made early (and therefore appear as “spike” tickets) are the **wake-word engine**, **offline STT engine**, and **offline TTS engine**, because these choices drive performance, packaging complexity, and licensing.

## Library research and recommended stacks with fallback routes

The following choices are optimised for: (a) low CPU in idle, (b) offline-first, (c) Windows compatibility, and (d) minimal “native build pain” on older machines.

### Audio capture and playback

**Primary recommendation: `sounddevice` (PortAudio bindings).**  
`sounddevice` provides cross-platform audio capture/playback as bindings around PortAudio, and it works on Windows, macOS, and Linux. citeturn1search1turn5search10  
It also supports “raw” streams (buffer objects) and callback-based capture, which is important to keep latency low and avoid heavy work on the audio thread. citeturn1search30  
Licensing is MIT. citeturn5search10  

**Fallbacks / roadblock options:**
- `PyAudio` (PortAudio bindings) is an alternative, but historically can have more installation friction (especially on Windows if wheels don’t match your Python version). citeturn1search2turn1search23  
- `PvRecorder` (from entity["company","Picovoice","voice ai company"]) is a cross‑platform recorder designed for real-time speech audio processing and exposes buffered frames and device enumeration, which can simplify capture (especially if you use Porcupine later). citeturn9search5turn9search11turn9search20  
  The trade-off is a tighter coupling to a vendor ecosystem.

**Typical roadblocks and mitigations:**
- PortAudio / device errors → implement device selection and recovery (“re-open stream on failure”), and keep a “push-to-talk” fallback mode.
- Buffer overruns → keep the callback minimal and queue frames; tune internal ring buffer size (both `sounddevice` and `PvRecorder` support buffering strategies). citeturn1search30turn9search5  

### Voice activity detection and end-of-utterance

**Primary recommendation: WebRTC VAD via `py-webrtcvad` / `webrtcvad`.**  
`py-webrtcvad` is a Python interface to the WebRTC Voice Activity Detector, designed to classify audio as voiced/unvoiced, and it is widely used because it is fast and suitable for real-time gating. citeturn1search0turn1search21  

**Fallbacks / roadblock options:**
- Simple energy-based gate (pure Python + NumPy) as a last resort if installing VAD wheels is hard.
- Use the VAD integrated into openWakeWord as a “second-stage filter” for wake-word (not exactly the same as end-of-utterance VAD, but can reduce false triggers). citeturn11view0  

### Wake phrase detection

Because “always-on” is the core constraint, wake-word choice matters more than almost any other component.

**Option A (offline-first, open-source): `openWakeWord`**
- openWakeWord is an open-source wake word / phrase detection framework focused on performance and simplicity, includes pre-trained models, and is Apache-2.0 licensed for code. citeturn11view0  
- On Windows, it installs `onnxruntime` (and not `tflite-runtime`), which is relevant to packaging and runtime size. citeturn11view0  
- It provides guidance on efficient frame sizes (multiples of ~80 ms) to balance latency vs efficiency. citeturn11view0  
- Important licensing nuance: while code is Apache 2.0, the included pre-trained models are CC BY‑NC‑SA 4.0 (non‑commercial), which can block commercial distribution unless you train/ship properly licensed models. citeturn11view0  

**Option B (very lightweight and production‑maintained, but requires vendor access key): Porcupine**
- Porcupine is positioned as a lightweight, on-device wake word engine. citeturn0search3turn0search8  
- It processes audio on-device, but the vendor states internet connectivity is required to validate the AccessKey and check plan limits (“call home” for usage validation), which is a real operational dependency that can conflict with strict offline-first expectations. citeturn0search21turn0search11  

**Option C (open-source, older/legacy path): PocketSphinx keyword spotting**
- PocketSphinx from entity["organization","Carnegie Mellon University","pittsburgh pa, us"] is explicitly described as compact and efficient, though its algorithms/models are older relative to modern neural approaches. citeturn3search6turn5search13  
- It supports keyword spotting mode with configurable thresholds. citeturn3search8  
- Useful as a fallback on extremely constrained hardware or if neural wake-word options become too heavy.

**Option D (wake-word engine family): Precise / Precise-lite**
- Precise-lite is a wake word listener used in Mycroft/OpenVoiceOS ecosystems. citeturn3search7turn3search9  
- Recent work indicates ONNX conversions can reduce CPU usage compared to tflite on some devices (evidence shown on Raspberry Pi testing), suggesting it can be viable where openWakeWord is too heavy. citeturn3search20  

**Plan recommendation:** start with openWakeWord as the default offline-first choice *but* run an early spike to validate CPU and false-trigger rate on the target machine; keep Porcupine as the “it just works and is tiny” fallback; keep PocketSphinx as the “works even on very old CPUs” fallback.

### Speech-to-text for short commands

**Primary recommendation: Vosk**
- Vosk is an offline speech recognition toolkit that installs via pip and is designed to work on lightweight devices, with a streaming API and small per-language models (~50 MB typical). citeturn9search3turn0search12  
- Vosk small models are described as suitable for desktop apps; a typical small model is ~50 MB and ~300 MB runtime memory (per the project’s own model guidance). citeturn0search23  
- Vosk is Apache-2.0 licensed. citeturn5search0  
- Vosk and its Python package have not had a new PyPI release since December 2022 (v0.3.45), so you should treat maintenance risk as real and mitigate with isolation and fallbacks. citeturn10view0  
- Vosk is produced by entity["company","Alpha Cephei","speech recognition company"] and is explicitly intended for assistants/chatbots. citeturn5search0turn9search3  

**Fallbacks / roadblock options:**
- `whisper.cpp` (C/C++ implementation of entity["company","OpenAI","ai research company"] Whisper) supports Windows and offline inference. citeturn3search0turn3search25  
  This gives higher accuracy potential than Vosk, but on older dual-core CPUs you may need tiny/base models and quantized builds; benchmark before committing.
- `faster-whisper` (CTranslate2-based) is reported as faster and lower memory than the original Python Whisper implementation; it supports CPU execution and quantisation. citeturn3search1turn3search34  
  It can still be heavy relative to Vosk on old machines, so treat as “optional performance tier.”

### Text-to-speech with a friendly, slower, lower-pitch style

**Primary recommendation for MVP simplicity: `pyttsx3`**
- `pyttsx3` is an offline TTS library and uses the OS built-in engine on each platform (SAPI5 on Windows). citeturn1search12turn1search32  
- Benefits: minimal CPU load, no model downloads, easy installation, and it will run well on old hardware.

**Higher-quality offline option: Piper (`piper-tts`)**
- The original `rhasspy/piper` repository was archived (Oct 2025) and development moved to a new repo (`piper1-gpl`). citeturn2search4turn2search0  
- `piper-tts` on PyPI is active with a recent release (Feb 5, 2026) and is GPL-3.0-or-later, Python ≥3.9. citeturn10view1  
- Licensing: GPL can be a *distribution* blocker depending on how you ship Bob (especially if you distribute a bundled executable). This must be an explicit decision in your plan.

**Plan recommendation:** use `pyttsx3` for Milestone 1 & 2 to keep the core loop stable on old machines; add Piper as Milestone 4 (personality pass) or as an optional “enhanced voice pack” if licensing and packaging work for your distribution.

### Intent handling and “skills” plumbing

For a small command set, heavy NLP frameworks are unnecessary. The simplest reliable path is deterministic intent matching plus a small fuzzy matching library.

- `RapidFuzz` is a fast string similarity/matching library suitable for fuzzy phrase matching (“open chrome” vs “open google chrome”). citeturn4search0  
- `dateparser` can parse human-readable date/time strings if you later expand beyond “what time is it” into “remind me tomorrow at 3”. citeturn4search1turn4search9  

### Observability, config, and secrets

- `psutil` is cross-platform for CPU/memory/process metrics and is suitable for local health stats reporting and leak detection. citeturn4search2  
- Python standard `logging` supports rotating file logs (`RotatingFileHandler` / `TimedRotatingFileHandler`). citeturn8search1  
- `python-dotenv` loads env vars from `.env` files (secrets baseline aligns to your `.env` rule). citeturn4search3  
- If you want schema validation for settings, Pydantic Settings supports loading typed configuration from environment variables and secrets files. citeturn7search0  
- If you want config layering across file formats and env vars, Dynaconf supports env vars and settings files (including JSON), and can optionally support `.env`. citeturn7search1turn7search5  

### Windows “local actions” tooling

- For volume/session control, `pycaw` is a Windows Core Audio library enabling programmatic control over audio sessions and devices. citeturn6search0  
- For simulating key presses (e.g., play/pause media), `keyboard` exists but is explicitly marked unmaintained by its author, so it should be treated as a risky dependency. citeturn6search13  
- `pynput` can control and monitor keyboard/mouse inputs and supports global hotkeys. citeturn6search10turn6search18  

**Plan recommendation:** implement “open app” using Windows-native process launching (no extra library), and implement “media control” as an optional skill behind a feature flag, with `pynput` as the first attempt and a “not supported” graceful fallback if permissions/OS limitations block it.

### Deployment and service mode

- `nssm` (Non‑Sucking Service Manager) can run an executable/script as a Windows service and explicitly monitors/restarts the process if it dies. citeturn2search3turn2search6  
- Alternative: implement a native Windows service using `pywin32`, which provides access to Windows APIs including service management. citeturn2search26turn2search16  
- Packaging option: PyInstaller can bundle scripts and deps into a single Windows executable; the one-file bundle is convenient but may start slower than one-folder builds. citeturn6search35turn6search15  

## Milestones and scrumboard backlog with ticket-level acceptance criteria

This section is written so you can directly convert it into Epics → Stories/Tasks on a scrumboard. Tickets are grouped by Milestone, and each includes acceptance criteria and the “deliverable artefact” that proves completion.

### Shared definition of done for all tickets

A ticket is “Done” when:
- Code merged into main (or your trunk branch), builds/runs on the target Windows machine.
- Unit tests (where applicable) pass locally.
- Any new config fields are documented in `config/settings.example.json`.
- Any user-facing behaviour change is recorded in `docs/` (or `planning/` when appropriate).
- Logs are emitted for major state transitions and errors.

### Milestone target

Milestones align to your Phase 0 definition:
- Milestone 1: skeleton (audio loop + wake phrase + deterministic reply)
- Milestone 2: core MVP (STT + intents + error handling)
- Milestone 3: reliability (config/logging/health/service mode/long-run stability)
- Milestone 4: personality pass (voice tuning + response style consistency)

#### Milestone 1 tickets

**M1-01 Repository skeleton aligned to baseline structure**  
Acceptance:
- `src/`, `tests/`, `docs/`, `standards/`, `planning/`, and `config/` exist per baseline.
- A minimal runnable entrypoint exists (e.g., `python -m bob` or `bob` console script).
- A smoke test confirms the entrypoint prints version and exits 0.

**M1-02 Dependency management and reproducible environment**  
Acceptance:
- A pinned dependency file exists (e.g., `requirements.txt` or `pyproject.toml` + lock strategy).
- A one-command install on a clean Windows machine is documented in `docs/setup-target-machine.md` (you already have this doc; update as needed).
- A “hello audio device list” script runs and prints available microphones.

**M1-03 Audio capture MVP using `sounddevice`**  
Acceptance:
- Microphone frames are captured continuously at a fixed sample rate and frame size.
- Frames are queued without blocking the audio callback (no heavy work in callback).
- If the device disappears (USB mic unplug), the system retries and recovers without reboot within 30 seconds.

**M1-04 Wake-word spike decision ticket**  
Acceptance:
- A short spike write-up (1–2 pages in `docs/benchmark-baseline.md` or `planning/phase0-wakeword-spike.md`) compares at least:
  - openWakeWord feasibility on Windows (dependency install, CPU at idle, basic accuracy)
  - Porcupine feasibility (AccessKey requirements + offline caveat) citeturn0search21
  - One fallback (PocketSphinx or Precise-lite)
- Decision recorded: “Primary wake-word engine” + “fallback engine”.

**M1-05 Wake phrase detection integrated in idle loop**  
Acceptance:
- Saying the wake phrase (e.g., “Hey Bob”) triggers a state transition from IDLE → TRIGGERED.
- False triggers are logged (manual observation session of 15 minutes, with count recorded).
- Wake trigger event is debounced (no multiple triggers from one phrase).

**M1-06 Deterministic response via TTS**  
Acceptance:
- On wake trigger, Bob speaks a deterministic reply (e.g., “Hello, I’m here.”).
- Speech rate is configurable and slower than default.
- The system returns to IDLE after speaking.

**M1-07 Listening/processing indicator MVP**  
Acceptance:
- Console logs clearly indicate state: IDLE / LISTENING / PROCESSING / SPEAKING.
- A “mute” flag exists in config that disables wake-word processing (but keeps app running).
- When muted, state is visible in logs.

**Milestone 1 exit check**  
Acceptance:
- End-to-end: audio capture + wake phrase + TTS reply works on the target machine for 30 minutes without manual restart.

#### Milestone 2 tickets

**M2-01 STT spike decision ticket**  
Acceptance:
- Evaluate Vosk vs whisper.cpp (and optionally faster-whisper) on target hardware:
  - CPU and latency for a 2–5 second utterance
  - memory footprint
  - install complexity
- Decision recorded: default STT engine + fallback STT engine.
- If Vosk is selected, document model choice and expected runtime memory (~300 MB for a typical small model per Vosk guidance). citeturn0search23  

**M2-02 Utterance recording with end-of-speech detection**  
Acceptance:
- After wake, Bob records audio until VAD indicates end-of-speech (plus a short trailing buffer).
- Recording stops within 0.5–1.0 seconds after the user finishes speaking in typical conditions.
- A timeout exists (e.g., stop listening after N seconds of silence).

**M2-03 STT adapter interface and Vosk implementation**  
Acceptance:
- A clean interface exists: `transcribe(audio_bytes) -> text + confidence/meta`.
- Vosk implementation runs fully offline and returns a transcript for short commands. citeturn9search3turn5search0  
- Errors are captured and reported as typed exceptions to the orchestrator (no crash).

**M2-04 STT fallback implementation stub**  
Acceptance:
- A second STT engine can be selected via config (even if not fully optimised).
- If fallback engine is unavailable at runtime, Bob logs and reverts to default without crashing.

**M2-05 Intent router framework**  
Acceptance:
- Define an intent schema (intent name + slots + confidence + matched phrase).
- Router supports:
  - exact phrase matching (fast path)
  - fuzzy match path using RapidFuzz citeturn4search0  
- Router returns either a known intent or an “unknown” intent.

**M2-06 Implement core intents set**  
Acceptance:
- At minimum implement:
  - Time/date
  - “Are you there?”
  - “What can you do?”
  - “Stop / cancel”
- Each intent has:
  - unit tests for parsing
  - deterministic response templates
- All intents listed in your existing `docs/mvp-command-list.md` are implemented (treat that doc as source of truth).

**M2-07 Local action skills framework**  
Acceptance:
- Skills are pluggable: each skill declares triggers + handler.
- Skills can be disabled individually via config.
- Unknown intent routes to a safe fallback answer (“Sorry, I didn’t catch that. Try asking…”) without throwing.

**M2-08 Windows “open app” skill**  
Acceptance:
- A config mapping exists (friendly name → executable path or app id).
- “Open <app>” launches the configured application.
- If app is missing, Bob speaks a helpful error and logs details.

**M2-09 Optional “media play/pause” skill behind feature flag**  
Acceptance:
- If enabled and supported, “play/pause” triggers a media action.
- If unsupported (permissions/API limitations), Bob responds “I can’t control media on this setup” and logs the reason.
- No global keylogging behaviour is introduced by default (avoid dependencies that require privileged hooks unless explicitly enabled). citeturn6search13turn6search2  

**M2-10 Session-only conversation memory**  
Acceptance:
- Bob maintains an in-memory session context (last intent, last response, last N user texts).
- Memory clears on restart.
- Privacy note is documented: “session memory only; no raw audio stored by default.”

**M2-11 Error-handling policy draft and implementation**  
Acceptance:
- `docs/error-handling-policy.md` is created and defines component-level retry/reset behaviour.
- In code: transient audio failures, STT failures, and TTS failures do not crash the process; Bob returns to IDLE.

**Milestone 2 exit check**  
Acceptance:
- End-to-end: wake → record → transcribe → intent → speak response works for the full MVP command list, with unknown-intent fallback, on the target machine.

#### Milestone 3 tickets

**M3-01 Centralised config loader aligned to baseline**  
Acceptance:
- `config/settings.local.json` overrides defaults from `config/settings.example.json`.
- Secrets only loaded from `.env` using python-dotenv. citeturn4search3  
- Config schema validation exists (either lightweight custom validation or Pydantic Settings). citeturn7search0  

**M3-02 Logging framework with rotation**  
Acceptance:
- Logs written to local files with rotation (size-based or time-based). citeturn8search1  
- Log events include:
  - state transitions
  - wake triggers
  - transcription duration
  - intent decisions
  - errors with stack traces
- A log level setting exists in config.

**M3-03 Health stats and watchdog**  
Acceptance:
- Health metrics gathered at runtime using psutil (CPU %, RSS memory, uptime). citeturn4search2  
- A periodic health summary is emitted to logs every N minutes.
- A watchdog detects “no audio frames received for >X seconds” and resets the audio stream.

**M3-04 Long-session stability validation harness**  
Acceptance:
- `docs/benchmark-baseline.md` contains the repeatable long-run test procedure (4+ hours).
- A script exists to run Bob in “test mode” (no TTS, or pre-recorded input) to validate memory growth.
- Pass criteria: no crash, no unbounded memory growth beyond an agreed threshold.

**M3-05 Service mode decision and implementation plan**  
Acceptance:
- `docs/service-mode.md` documents the chosen Windows startup mode:
  - NSSM-managed service, or
  - pywin32 native service
- Decision includes pros/cons: NSSM restarts on failure as designed. citeturn2search3turn2search6  
- A reproducible install/uninstall walkthrough is included.

**M3-06 Packaging strategy**  
Acceptance:
- Decide distribution method:
  - “run from source with venv” or
  - “bundle exe”
- If bundling: PyInstaller build instructions in docs, including one-folder vs one-file tradeoffs. citeturn6search35turn6search15  

**M3-07 Privacy mode hardening**  
Acceptance:
- Default: no raw audio saved.
- Optional debug setting: store last N seconds of audio only when explicitly enabled, with clear log warnings.
- A visible “mute” state is always available and persisted in config.

**Milestone 3 exit check**  
Acceptance:
- Config centralised, logging usable for debugging, health signals present, and a successful long-session test run is documented and repeatable.

#### Milestone 4 tickets

**M4-01 Voice tuning configuration**  
Acceptance:
- Voice settings are configurable and documented:
  - speech rate
  - voice selection (where supported)
  - optional “lower pitch” effect setting (if using an engine that supports it)
- Default delivery matches the “friendly, slow, simple” target.

**M4-02 TTS upgrade spike and decision**  
Acceptance:
- Evaluate:
  - staying with pyttsx3 (reliability + low CPU) citeturn1search12  
  - adding Piper (`piper-tts`) for more natural voice, noting GPL licensing and Python ≥3.9 requirement citeturn10view1  
- Decision recorded: keep pyttsx3 / add Piper / provide both as selectable engines.

**M4-03 Response style consistency pass**  
Acceptance:
- Responses follow a consistent persona:
  - short sentences
  - friendly phrasing
  - slower pacing (optionally with pauses)
- A “style guide” for responses is written in `docs/persona-style.md` (new file).

**M4-04 Wake phrasing finalisation**  
Acceptance:
- Final wake phrase chosen and documented, with rationale (phonetic distinctness, false trigger rate).
- If openWakeWord: a custom model training plan is written and tested, since pre-trained models may not include “Hey Bob.” citeturn11view0  
- If Porcupine: include AccessKey operational note and offline caveat. citeturn0search21  

**M4-05 “Patrick-like” constraint compliance check**  
Acceptance:
- Confirm no voice cloning of copyrighted character voices.
- Document how the style is achieved (pace, pitch, phrasing), not an imitation.
- Include a compliance note in README or docs.

**Milestone 4 exit check**  
Acceptance:
- Voice settings and response style documented and configurable; persona delivery is consistent with constraints.

## Benchmarks, quality gates, and acceptance measurements

To make the scrumboard actionable, define measurements that convert your quality targets into pass/fail gates.

**CPU usage (idle):**  
Acceptance gate: on the target machine, with Bob idle and listening, average CPU over 10 minutes remains below an agreed threshold (set initial target after first benchmark; store in `docs/benchmark-baseline.md`). The plan requires measuring this before you commit to wake-word and STT stack, because different engines change CPU dramatically.

**Response latency:**  
Acceptance gate: for typical commands, time from “user stops speaking” to “TTS audio starts” is within 1–3 seconds in the median case, recorded over at least 20 test runs.

**Stability:**  
Acceptance gate: continuous run for 4+ hours with no crash; memory does not continuously increase (define allowable drift and measure via psutil). citeturn4search2  

**Wake-word false triggers:**  
Acceptance gate: run a “normal room use” test (TV on low volume or background noise) for 1 hour and record false activations. openWakeWord explicitly discusses acceptable false accept rates on the order of <0.5/hour as a practical target, but you should tune based on your environment. citeturn11view0  

## Operational considerations, licensing flags, and risk register

**Licensing risks that must be tracked as explicit backlog items:**
- openWakeWord code is Apache 2.0, but bundled pre-trained models are CC BY‑NC‑SA (non-commercial). If you distribute Bob, determine whether you ship models, train your own, or require the user to download. citeturn11view0  
- Piper’s active distribution path (`piper-tts`) is GPL‑3.0‑or‑later. If you distribute a bundled executable, this can impose GPL obligations; this must be decided before Milestone 4 voice upgrades. citeturn10view1  
- Porcupine requires an AccessKey and vendor validation connectivity, which can be a blocker if Bob must work with no internet at all. citeturn0search21  

**Maintainability risks and mitigations:**
- Some packages in the voice stack ecosystem can lag releases; for example, Vosk’s PyPI release history shows no new release since late 2022. citeturn10view0  
  Mitigation: keep STT behind an adapter interface and preserve fallback engines.
- The `keyboard` library is marked unmaintained; avoid as a core dependency. citeturn6search13  

**Service reliability risks:**
- Running always-on audio capture as a Windows service can be fragile depending on session audio device access. Mitigation: treat “service mode” as Milestone 3 and validate device capture in the intended run context (service vs user session). NSSM’s restart monitoring can reduce operational pain if the process dies. citeturn2search3turn2search6  

**Roadmap guardrails (to preserve MVP focus):**
- Avoid heavy cloud features in the core loop (keep offline-first).
- If you later add cloud fallback for “hard queries,” isolate it behind a skill and require explicit opt-in via `.env` secrets, consistent with your secrets baseline. citeturn4search3