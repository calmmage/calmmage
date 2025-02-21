"""
Typer CLI for the queue tracker
"""

import typer
from lib import QueueTracker, StorageMode
from typing_extensions import Annotated

app = typer.Typer()

qt = QueueTracker(storage_mode=StorageMode.FILE, storage_path="queue_tracker_state.json")


@app.command(name="add-queue", help="Add a new queue")
@app.command(name="aq", help="Add a new queue")
def add_queue(
        name: Annotated[str, typer.Option("-n", "--name", help="Name of the queue to add")],
        cadence: Annotated[str, typer.Option("-c", "--cadence", help="Cadence/frequency for the queue")]
):
    """Add a new queue with specified name and cadence."""
    qt.add_queue(name, cadence)


@app.command(name="add-item", help="Add an item to a queue")
@app.command(name="ai", help="Add an item to a queue")
def add_item(
        queue_name: Annotated[str, typer.Option("-q", "--queue", help="Name of the queue to add item to")],
        item: Annotated[str, typer.Option("-i", "--item", help="Item to add to the queue")]
):
    """Add a new item to specified queue."""
    qt.add_item(queue_name, item)


@app.command(name="bulk-add", help="Bulk add items from a file")
@app.command(name="ba", help="Bulk add items from a file")
def bulk_add(
        data_path: Annotated[str, typer.Option("-p", "--path", help="Path to data file for bulk import")]
):
    """Bulk add items from a data file."""
    with open(data_path, "r") as f:
        data = f.read()
    qt.bulk_add(data)


if __name__ == "__main__":
    app()
