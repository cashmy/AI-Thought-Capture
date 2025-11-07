"""Simple STT adapter stub.

Replace the functions here with calls to Whisper, whisper.cpp, or any cloud STT.
"""
from pathlib import Path
import random
import time

def transcribe(file_path: str):
    """Pretend to transcribe the audio file and return a dict with keys:
    - transcript (str)
    - confidence (float 0..1)
    - duration_seconds (float)
    """
    p = Path(file_path)
    # Simulate work
    time.sleep(0.1)
    transcript = f"(stub) Transcript of {p.name}. Replace with real STT."
    return {
        "transcript": transcript,
        "confidence": round(0.85 + random.random() * 0.14, 2),
        "duration_seconds": 0.0,
    }
