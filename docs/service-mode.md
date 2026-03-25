# Service Mode And Packaging Strategy

## Decision Summary

Chosen MVP startup mode:
- run Bob in the logged-in user session with Windows Task Scheduler at user logon

Chosen MVP packaging strategy:
- run from source with `uv` and the repository checkout

Not chosen for MVP:
- true Windows service via NSSM
- native Windows service via `pywin32`
- bundled executable via PyInstaller

## Why This Is The Right MVP Choice

Bob depends on live microphone access and interactive desktop audio behavior.
For this project stage, that is more reliable in a normal user session than in a background Windows service context.

Practical reasons:

1. User-session startup is simpler to debug.
2. Audio device access is less fragile than service-session capture.
3. The current repo already runs cleanly from source with `uv`.
4. Packaging into an executable would add distribution complexity before the runtime loop is fully mature.

## Alternatives Considered

### NSSM-managed service

Pros:
- simple service wrapper
- automatic restart behavior
- no need to write native service code

Cons:
- microphone/device access can be fragile in service context
- harder to debug interactive audio issues
- adds service-manager operational steps before Bob is fully stabilized

Decision:
- keep as a later operational option, not the MVP default

### Native `pywin32` service

Pros:
- first-class Windows service implementation
- more control over service lifecycle

Cons:
- more implementation complexity
- higher maintenance cost
- same service-context audio risks still apply

Decision:
- not justified at current project maturity

### PyInstaller bundle

Pros:
- easier handoff to a non-developer machine later
- one-folder or one-file distribution path exists

Cons:
- extra packaging/debugging work
- more friction when iterating on config and models
- one-file startup can be slower

Decision:
- defer until the runtime loop and deployment story stabilize

## Chosen Operational Model

MVP recommendation:

1. Keep a local repo checkout on the target machine.
2. Use `uv` to run Bob from source.
3. Start Bob automatically with Task Scheduler at user logon.
4. Keep logs and config local to that machine.

This gives a dependable startup path without pretending Bob is ready for fully packaged distribution.

## Current Limitation

At the current project stage, the startup wrapper and Task Scheduler task can launch Bob successfully, but Bob does not yet stay resident as an always-on assistant.

Why:

1. `python -m bob` currently runs the bootstrap CLI entrypoint
2. the default CLI path prints a bootstrap message and exits
3. a true long-running runtime command has not been added yet

Practical meaning:

- the startup method is chosen and documented
- the automation path is valid
- full always-on startup behavior depends on a later runtime entrypoint task

## Install Steps

From an elevated or normal PowerShell session on the target machine:

1. Clone the repo to a stable path, for example `C:\repos\bob`
2. Install Python and `uv`
3. Create:
   - `config/settings.local.json`
   - `.env`
4. Verify Bob runs manually before adding startup automation:

```powershell
$env:PYTHONPATH = "src"
uv run --with-requirements requirements.txt -- python -m bob --version
uv run --with-requirements requirements.txt -- python -m bob
```

## Task Scheduler Startup Recommendation

Recommended trigger:
- `At log on` for the intended user account

Recommended action:
- start `powershell.exe`
- point it to the wrapper script at `scripts/start-bob.ps1`

Recommended action command:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\repos\bob\scripts\start-bob.ps1"
```

Wrapper script contents:

```powershell
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

$env:PYTHONPATH = "src"

uv run --with-requirements requirements.txt -- python -m bob
```

Current expected behavior when run today:
- Bob starts
- the current bootstrap CLI runs
- the process exits because there is not yet a persistent assistant runtime command

Recommended Task Scheduler settings:

1. Run only when the user is logged on
2. Restart on failure if desired
3. Start in: `C:\repos\bob\scripts`

## Uninstall / Disable Steps

1. Remove or disable the scheduled task
2. Keep config and logs if you want diagnostics
3. Delete the repo checkout only after logs/config are no longer needed
4. Remove `scripts/start-bob.ps1` only if the repo checkout is being removed entirely

## Packaging Decision

Current default:
- source-run from the repo using `uv`

Why:
- fastest iteration path
- easiest to debug
- aligns with the current developer/operator workflow
- avoids premature installer/executable complexity

Revisit packaging when:

1. startup/service mode is proven stable on the target machine
2. config and model assets are settled
3. Bob is ready to be handed to a non-developer operator

## Future Upgrade Path

When the project is ready, reevaluate:

1. NSSM + source-run if service-style restart supervision is needed
2. PyInstaller one-folder build if distribution convenience becomes important
3. native service implementation only if there is a clear operational benefit
