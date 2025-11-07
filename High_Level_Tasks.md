# AI Task List

## Concept: AI Thought Capture & Synthesis

1.  Design the architecture diagram (showing the flow from recording → transcription → classification → task generation).

2. Propose a scaffolded project structure for this application

3. Create an MVP plan (Python/JS-based, Whisper + GPT integration).

4. Develop a product name and brand concept (e.g., “EchoForge,” “MindStream,” or “Auralynx”).

5. Create a minimal watch-folder script (Python) you can drop into Windows 11, and

6. Create a simple Electron recorder with a hotkey + auto-save to Ideas/Inbox.

### Options: 
1. AI can now implement a real STT adapter (Whisper/local or OpenAI) replacing stt_stub.py and wire confidence thresholds & chunking.
2. Or AI can produce the architecture diagram and full project scaffold (broader repo layout + Electron app folder) next.
3. Or AI can harden the watcher (add logging, desktop notifications, a small JSON manifest for idempotency, and improved duplicate detection).


### Folder Creation: 
# create folders if needed
mkdir "Ideas/Inbox"; mkdir "Ideas/Processed"; mkdir "Ideas/Processed/originals"

# install deps into the workspace venv (if not already)
"D:/Concepts/AI Thought Capture/.venv/Scripts/python.exe" -m pip install -r watcher/requirements.txt

# process files once
&D:/Concepts/AI Thought Capture/.venv/Scripts/python.exe -m watcher.watcher --inbox "Ideas/Inbox" --processed-dir "Ideas/Processed" --once

# or run continuously
&D:/Concepts/AI Thought Capture/.venv/Scripts/python.exe -m watcher.watcher --inbox "Ideas/Inbox" --processed-dir "Ideas/Processed"

### Next up: 
Exporting PNG versions of both Mermaid diagrams