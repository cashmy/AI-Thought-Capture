<!-- markdownlint-disable MD033 -->
<!-- markdownlint-disable MD025 -->

# Watcher: Purpose & Description

## Purpose

The Watcher is a lightweight, Windows-first service whose job is to reliably detect new voice recordings dropped into an "Ideas/Inbox" folder and hand them off to the processing pipeline. It is the single, minimal piece of infrastructure required to bridge physical/audio capture (hardware or phone) and the AI processing stages (STT → summarize → classify → task generation).

Core goals:

- Make audio ingestion idempotent and resilient (avoid double-processing, handle partial writes).
- Normalize inputs (naming, metadata, chunking) so downstream steps can be simple and deterministic.
- Provide clear artifact outputs (Markdown idea files + metadata) that are human-reviewable and easy to attach to Obsidian/Notion.
- Fail gracefully and surface low-confidence or problematic files to a review queue.

## High-level behavior (what it does)

1. Watch a configurable inbox directory (default: `Ideas/Inbox`).
2. Detect newly created or moved-in audio files (wav, mp3, m4a, flac).
3. Wait for file write completion (file locking/size-stability check) to avoid partial reads.
4. Optionally chunk long recordings into <N>-minute segments for STT.
5. Transcribe each chunk using the configured STT engine (local Whisper, whisper.cpp, or remote API).
6. Run a lightweight summarization/classification pass (can be stubbed or call the configured LM) to produce a short Title, Summary, Classification and Suggested Tasks.
7. Emit a Markdown artifact into `Ideas/Processed` with a standard template and metadata (timestamps, confidence, original filename). Also move or mark the original file to `Ideas/Processed/originals` or `Ideas/Processed/failed` as appropriate.
8. Optionally enqueue the artifact into a human-review queue (e.g., a JSON file or database row) for verification and tagging.

## Outputs (artifact template)

- Output file: `Ideas/Processed/YYYYMMDD_HHMMSS--title-slug.md`
- YAML frontmatter (or simple metadata block):
  - title
  - created_at
  - source_file
  - duration
  - stt_engine
  - stt_confidence (aggregate)
  - classification
  - tags
  - status: draft | needs_review | verified
- Body: short Summary, Suggested Tasks (bullet list), Classification rationale, and full transcript (optionally collapsed or appended as `transcript.txt`).

Example Markdown header snippet:

```markdown
title: "AI Voice Journal to Idea Accelerator"
created_at: 2025-11-06T09:12:34Z
source_file: "Ideas/Inbox/20251106_091234--phone.mp3"
duration: "00:02:17"
stt_engine: "whisper-local"
stt_confidence: 0.92
classification: "Product Idea"
tags: ["idea", "product", "voice"]
status: "needs_review"
```

## CLI / Config options (minimal)

- --inbox: path to watch (default `Ideas/Inbox`)
- --processed-dir: where markdown/artifacts go (default `Ideas/Processed`)
- --failed-dir: where to move failed transcriptions (default `Ideas/Failed`)
- --stt-engine: `whisper-local` | `whisper-api` | `whisper-cpp` | `openai` (default `whisper-local`)
- --model: model name for STT or LM
- --chunk-seconds: integer, segment length to chunk long audio (default 300)
- --poll-interval: seconds to re-scan for new files when native watching isn't reliable (default 2)
- --dry-run: emit logs but do not move or write artifacts

## Error handling & edge cases

- Partial writes: wait for stable file size across configurable interval before processing.
- Locked files: retry with exponential backoff for N attempts, then move to `Ideas/Failed` and log error.
- Low STT confidence: mark artifact `needs_review` and include a notice in the Markdown; optionally send a desktop notification.
- Duplicate detection: simple filename/hash comparison; later phase will add semantic similarity checks and optional merge suggestions.
- Idempotency: create a sidecar `.processed` manifest entry (or store a DB/JSON index) to record processed file hashes and timestamps.

## Windows-specific notes

- Use the `watchdog` Python library which supports Windows event API; if edge cases appear (network drives, OneDrive sync), fall back to polling mode.
- Ensure path handling uses `pathlib.Path` and supports UNC paths or OneDrive-synced folders.
- Provide a PowerShell-friendly service wrapper or a shortcut to run the watcher at login.

## Minimal contract (inputs / outputs / error modes)

- Inputs: audio file in supported formats appearing in `--inbox`.
- Outputs: Markdown artifact in `--processed-dir` plus original file moved to `--processed-dir/originals` (or `--failed-dir` on error).
- Error modes: partial write, locked file, transcription failure, low-confidence transcription.

# Justification: why build the Watcher first (before drawing the full architecture)

1. High-leverage, low-effort MVP — The watcher is the smallest component that turns real user behavior (recording audio) into testable data (transcripts and Markdown). Getting ingestion right gives an immediate, tangible prototype to validate naming conventions, chunking strategy, STT choices (local vs cloud), and the markdown template.

2. Early validation of critical assumptions — Many assumptions (file write semantics across devices, OneDrive/Dropbox sync behavior, file locking on Windows, audio formats produced by target recorders) only become clear when you run a watcher against real files. Building it first surfaces these constraints early and reduces rework in the rest of the architecture.

3. Minimal surface area for iteration — The watcher can be implemented in a small Python script with well-defined inputs/outputs. That means we can iterate quickly: change naming conventions, swap STT engines, or add chunking without redesigning entire systems.

4. Enables end-to-end demos — With a working watcher plus a simple stub STT (or Whisper), you can produce processed Markdown notes that stakeholders can review. This is hugely valuable for feedback and prioritization before investing in more complex orchestration, queuing, or UI work.

5. Foundation for plumbing and integration — Once the watcher output format and behavior are stable, the architecture diagram and subsequent services (processing workers, human-review UI, storage sync) can be designed to a concrete contract rather than hypothetical interfaces. This reduces ambiguity and simplifies the architecture design step.

## Tradeoffs & alternative

- Tradeoff: a watcher-driven approach may handle many client sync mechanisms awkwardly (e.g., mobile apps that upload via API rather than place files into a folder). The watcher is intentionally local-first. If you expect most users to upload directly from mobile apps or if the recorder offers an API, consider adding an ingest API in parallel. For MVP and for your stated Windows development environment, the watcher is the quickest path to a working prototype.

---

Next: I'll create a minimal code scaffold for the watcher (Python) that implements the behaviors above (file-stability checks, chunking hook, STT abstraction) and a small test harness. Tell me to "Do watch-folder" to proceed.
