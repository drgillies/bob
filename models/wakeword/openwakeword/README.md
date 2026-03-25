# Custom Wake-Word Artifact Placeholder

Expected local artifact for Bob:

- temporary engineering artifact: `yo_homie.onnx`
- target product artifact later: `hey_bob.onnx`

Expected directory:

```text
models/wakeword/openwakeword/
```

Notes:

- This directory exists so the expected local model path is explicit.
- `yo_homie.onnx` is currently present as a temporary engineering/testing artifact sourced from the Home Assistant wakeword community collection.
- The actual product-aligned `hey_bob.onnx` artifact is not included yet.
- Bob can now use `yo_homie.onnx` to unblock wake-word testing while `hey_bob.onnx` remains future work.

Validation command once the artifact exists:

```powershell
$env:PYTHONPATH="src"
uv run --with openwakeword --with-requirements requirements.txt -- python _testing.py wake-openwakeword-live --seconds 15
```
