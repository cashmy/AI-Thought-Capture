"""CLI entry for the watcher.

Supports a one-shot processing mode (`--once`) and a continuous mode that watches the inbox.
"""
from pathlib import Path
import argparse
import time
import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .watcher_core import process_file

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


class NewFileHandler(FileSystemEventHandler):
    def __init__(self, processed_dir: Path, failed_dir: Path):
        super().__init__()
        self.processed_dir = processed_dir
        self.failed_dir = failed_dir

    def on_created(self, event):
        if event.is_directory:
            return
        path = Path(event.src_path)
        logging.info(f"Detected new file: {path}")
        time.sleep(0.2)  # brief debounce
        res = process_file(path, self.processed_dir, self.failed_dir)
        logging.info(f"Processed: {res}")


def scan_once(inbox: Path, processed_dir: Path, failed_dir: Path):
    for ext in ("*.wav", "*.mp3", "*.m4a", "*.flac"):
        for p in inbox.glob(ext):
            print("Processing", p)
            r = process_file(p, processed_dir, failed_dir)
            print(r)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inbox", default="Ideas/Inbox")
    parser.add_argument("--processed-dir", default="Ideas/Processed")
    parser.add_argument("--failed-dir", default="Ideas/Failed")
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args()

    inbox = Path(args.inbox)
    processed_dir = Path(args.processed_dir)
    failed_dir = Path(args.failed_dir)
    inbox.mkdir(parents=True, exist_ok=True)

    if args.once:
        scan_once(inbox, processed_dir, failed_dir)
        return

    event_handler = NewFileHandler(processed_dir, failed_dir)
    observer = Observer()
    observer.schedule(event_handler, str(inbox), recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
