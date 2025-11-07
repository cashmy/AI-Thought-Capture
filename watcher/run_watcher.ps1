# PowerShell helper to run the watcher from the workspace root
param(
    [string]$Inbox = "Ideas/Inbox",
    [string]$Processed = "Ideas/Processed",
    [switch]$Once
)

python -m pip install -r watcher/requirements.txt

if ($Once) {
    python watcher/watcher.py --inbox $Inbox --processed-dir $Processed --once
} else {
    python watcher/watcher.py --inbox $Inbox --processed-dir $Processed
}
