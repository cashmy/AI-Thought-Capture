from pathlib import Path
import time
import shutil
import hashlib
import json
from datetime import datetime, timezone

from .stt_stub import transcribe


def is_file_stable(path: Path, checks: int = 3, interval: float = 0.5) -> bool:
    """Return True when file size is stable across `checks` checks spaced by `interval` seconds."""
    if not path.exists():
        return False
    last_size = path.stat().st_size
    for _ in range(checks):
        time.sleep(interval)
        size = path.stat().st_size
        if size != last_size:
            last_size = size
        else:
            return True
    return False


def file_hash(path: Path, block_size: int = 65536) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(block_size), b""):
            h.update(block)
    return h.hexdigest()


def emit_markdown(metadata: dict, transcript: str, processed_dir: Path) -> Path:
    """Create a markdown file from metadata and transcript. Returns path to md file."""
    timestamp = metadata.get("created_at") or datetime.now(timezone.utc).isoformat()
    title = metadata.get("title") or metadata.get("source_file", "untitled")
    slug = "-".join(title.lower().split())[:60]
    name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}--{slug}.md"
    out_path = processed_dir / name
    front = {
        "title": title,
        "created_at": timestamp,
        **{k: v for k, v in metadata.items() if k not in ("title", "created_at")},
    }

    with out_path.open("w", encoding="utf-8") as f:
        f.write("---\n")
        json.dump(front, f, indent=2)
        f.write("\n---\n\n")
        f.write("## Summary\n\n")
        f.write((metadata.get("summary") or "(no summary)") + "\n\n")
        f.write("## Transcript\n\n")
        f.write(transcript + "\n")

    return out_path


def process_file(path: Path, processed_dir: Path, failed_dir: Path) -> dict:
    """Process a single audio file: wait for stability, transcribe, emit markdown, and move original.

    Returns a result dict with status and paths.
    """
    processed_dir.mkdir(parents=True, exist_ok=True)
    (processed_dir / "originals").mkdir(parents=True, exist_ok=True)
    failed_dir.mkdir(parents=True, exist_ok=True)

    if not is_file_stable(path):
        return {"status": "unstable", "file": str(path)}

    try:
        stt = transcribe(str(path))
    except Exception as e:
        # on STT failure move to failed
        dest = failed_dir / path.name
        shutil.move(str(path), str(dest))
        return {"status": "stt_error", "error": str(e), "file": str(dest)}

    metadata = {
        "title": path.stem,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_file": str(path),
        "duration": stt.get("duration_seconds"),
        "stt_engine": "stub",
        "stt_confidence": stt.get("confidence"),
        "classification": "unknown",
        "tags": [],
        "status": "needs_review",
    }

    md_path = emit_markdown(metadata, stt.get("transcript", ""), processed_dir)

    # move original
    dest = processed_dir / "originals" / path.name
    shutil.move(str(path), str(dest))

    return {"status": "ok", "markdown": str(md_path), "original": str(dest)}
