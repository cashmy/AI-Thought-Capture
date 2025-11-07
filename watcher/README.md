# Watcher (AI Thought Capture)

Minimal Python watcher that monitors an `Ideas/Inbox` folder for new audio files and produces a Markdown artifact into `Ideas/Processed`.

Purpose: provide a local-first ingestion component for the AI Thought Capture prototype. This scaffold contains a small, testable implementation and a stubbed STT adapter so you can swap real transcription engines later.

Contents
- `watcher.py` — CLI entrypoint and optional long-running watcher using `watchdog`.
- `watcher_core.py` — core processing primitives (stability checks, processing, markdown emission).
- `stt_stub.py` — stubbed transcription adapter (replace with Whisper/OpenAI/etc.).
- `requirements.txt` — minimal dependencies.
- `tests/test_watcher.py` — basic pytest-based tests.
- `run_watcher.ps1` — convenience PowerShell script to run the watcher on Windows.

Quick start (PowerShell)

1. Create a Python venv and activate it.
2. Install dependencies:

```powershell
python -m pip install -r watcher/requirements.txt
```

3. Create folders:

```powershell
mkdir "Ideas/Inbox"; mkdir "Ideas/Processed"; mkdir "Ideas/Processed/originals"
```

4. Run once to process existing files:

```powershell
python watcher/watcher.py --inbox "Ideas/Inbox" --processed-dir "Ideas/Processed" --once
```

5. Or run continuously:

```powershell
python watcher/watcher.py --inbox "Ideas/Inbox" --processed-dir "Ideas/Processed"
```

Replace `stt_stub` with real STT adapter in `stt_stub.py` when ready.
