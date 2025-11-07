import tempfile
from pathlib import Path
import time

from watcher.watcher_core import is_file_stable, process_file


def test_is_file_stable(tmp_path: Path):
    f = tmp_path / "t.txt"
    f.write_text("hello")
    assert is_file_stable(f, checks=1, interval=0.01)


def test_process_file_once(tmp_path: Path):
    inbox = tmp_path / "inbox"
    processed = tmp_path / "processed"
    failed = tmp_path / "failed"
    inbox.mkdir()
    p = inbox / "sample.mp3"
    p.write_text("audiocontent")
    res = process_file(p, processed, failed)
    assert res["status"] == "ok"
    assert (processed / "originals" / "sample.mp3").exists()
    assert any(str(x).endswith(".md") for x in processed.iterdir())
