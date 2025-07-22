"""
A job to run
"""

import typer
from lib import QueueTracker, StorageMode

app = typer.Typer()

qt = QueueTracker(storage_mode=StorageMode.FILE, storage_path="queue_tracker_state.json")

if __name__ == "__main__":
    qt.dispatch_items()
