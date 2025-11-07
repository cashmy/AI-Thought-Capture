# Project Context Understanding: AI Thought Capture & Synthesis System

## Original AI Prompt/Request

"Lets rebuild your contenxt inference prompt for this project.
Analyze the files in the durrent context. Then describe your understanding of the total context for this project."

## Response follows

Based on my analysis of all project files, here is my comprehensive understanding:

## Core Problem & Vision

This project addresses the "liminal cognition paradox" — creative professionals generate their best ideas during free-flowing mental states (driving, walking, showering), but these insights fade rapidly due to cognitive load switching. By the time they reach a workstation, the spark, contextual nuance, and mental momentum are lost.

**Solution**: A hands-free voice capture system + AI processing pipeline that bridges spontaneous ideation moments and actionable project development workflows.

## Current State: MVP in Progress

**Phase**: Watcher-First Prototype (Bottom-Up Approach)
The project has deliberately started with the Watcher component before designing the full architecture — a strategic choice justified by:

- High-leverage validation of critical assumptions (file I/O, Windows sync behavior, naming conventions)
- Immediate tangible prototype (audio → markdown)
- Minimal surface area for rapid iteration
- Enables end-to-end demos early

### What's Built

  1. **Watcher Service** (watcher) — Python-based file monitoring system:
    - Monitors Ideas/Inbox for new audio files (wav, mp3, m4a, flac)
    - File stability detection (prevents partial-write processing)
    - Idempotent processing (hash-based duplicate detection)
    - Two modes: one-shot (--once) and continuous watching
    - Resilient error handling (failed files → Ideas/Failed)
    - Outputs: Structured Markdown artifacts with YAML frontmatter
  
  2. **STT Stub** (stt_stub.py) — Placeholder transcription adapter:
    - Currently returns stub transcripts
    - Ready to swap with Whisper (local/cloud), whisper.cpp, or OpenAI API
    - Interface contract: transcribe(file_path) → {transcript, confidence, duration}

  3. **Architecture Documentation**:
    - Two Mermaid diagrams (landscape + portrait) showing full system flow
    - Component contracts and data flow specifications
    - Cross-platform considerations (Windows-first, but portable)
  
## Technology Stack (Planned/Partial)

| Layer | Current/Planned | Notes |
|-------|-----------------|----------------------- |
| Audio Input | Sony ICD-UX570, Zoom F2-BT, or mobile voice memos | Hardware recorders recommended |
| File Sync | Local folders, OneDrive, Dropbox | Windows-first, cloud-sync aware |
| Watcher | ✅ Python + watchdog | Built & functional |
| STT | 🔄 Stub (needs Whisper/OpenAI) | Next priority |
| NLP Processing | Planned: GPT/Claude | Summarize, classify, generate tasks |
| Storage | Markdown files + JSON/SQLite manifest | Lightweight, human-readable |
| Review UI | Planned: Electron app | Approve/reclassify/merge interface |
| Sync Targets | Obsidian, Notion, Trello, GitHub Issues | Push verified artifacts |

## Architecture Flow (5-Stage Pipeline)

```markdown
  1. CAPTURE → Voice recorder saves audio
  2. INGEST → Files appear in Ideas/Inbox → Watcher detects
  3. PROCESS → STT → NLP (summarize, classify, tasks) → Metadata index
  4. REVIEW → Human verifies/enriches via UI
  5. SYNC → Push to Obsidian/Notion/Trello/GitHub
```

**Alternate path**: Mobile companion app uploads directly via API (bypasses file sync).

## Data Contract: Markdown Artifacts

Output: Ideas/Processed/YYYYMMDD_HHMMSS--title-slug.md

YAML Frontmatter:

```yaml
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

Body: Summary → Suggested Tasks → Full Transcript

## Windows-Specific Considerations

- Uses watchdog library (native Windows FS events)
- pathlib.Path for robust path handling (UNC, OneDrive-synced folders)
- PowerShell-friendly (run_watcher.ps1 convenience script)
- Handles cloud sync races (OneDrive/Dropbox) via file-stability checks

## Next Priorities (Per High_Level_Tasks.md)

### Immediate

  1. Implement real STT adapter (replace stt_stub.py):
     - Local Whisper or OpenAI API
     - Wire confidence thresholds & chunking (5-10 min segments)

### Near-term

  2. Harden watcher:
     - Add structured logging
     - Desktop notifications (Windows toast)
     - JSON manifest for idempotency tracking
     - Improved duplicate detection (semantic similarity)
  
  3. Architecture visualization:
     - Export PNG/SVG versions of Mermaid diagrams
  
  4. Electron recorder app:
     - Simple UI with Record button
     - Hotkey support (Ctrl+Shift+R)
     - Auto-save to Ideas/Inbox
  
### Future Enhancements

- Mobile integration: iOS Shortcuts automation, Android Tasker flows
- Desktop quick-capture: Zero-friction Windows 11 Voice Recorder integration
- NLP worker: Full summarization + classification (LangChain/CrewAI)
- Review UI: Electron app for human verification loop
- Advanced features:
  - Contextual memory (recurring themes)
  - Temporal awareness (idea relationships)
  - Voice pattern learning
  - Morning Review Mode (daily digest)
  
## Innovative Use Cases (Noted in Actual Steps.md)

Beyond personal ideation, potential cross-context applications:

- Coaching: Record coachee sessions → personalized task generation
- Healthcare: Doctor patient notes → follow-up suggestions
- Dental: Procedure tracking → recommended next steps
- (These represent MVP 2.0+ scope)

## Project Philosophy

- Local-first: Privacy by default (local STT preferred)
- Human-in-the-loop: AI suggests, human verifies
- Idempotent & resilient: Handle real-world file sync chaos
- Iterative: Build smallest working piece first (watcher), then expand
- Cross-platform aware: Windows dev priority, but portable design

## Current Gaps

  1. ❌ Real STT integration (stub only)
  2. ❌ NLP/summarization worker
  3. ❌ Manifest store (SQLite/JSON tracking)
  4. ❌ Review UI
  5. ❌ Sync adapters (Obsidian, Notion, etc.)
  6. ❌ Product branding/naming (suggested: "EchoForge", "MindStream", "Auralynx")

## Development Context

- OS: Windows 11
- Shell: PowerShell
- Workspace: e:\Concepts\AI Thought Capture
- Virtual environment: .venv (expected, not yet confirmed)
- Testing: pytest framework included
- Dependencies: watchdog>=2.1.9, pytest>=7.0.0

**Summary**: This is a thoughtfully architected, bottom-up MVP for capturing and synthesizing spontaneous creative thoughts. The watcher foundation is solid and ready for STT integration, which is the critical next step to make the system functional end-to-end.
