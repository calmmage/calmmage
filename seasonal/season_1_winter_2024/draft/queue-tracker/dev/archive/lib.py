import json
from datetime import datetime
from loguru import logger
from pathlib import Path
from pydantic import BaseModel
from typing import List, Optional, Callable, Dict


class QueueItem(BaseModel):
    id: str
    content: str
    created_at: datetime = datetime.now()
    processed_at: Optional[datetime] = None


class Queue:
    def __init__(
            self,
            name: str,
            storage_path: Optional[Path] = None,
            low_threshold: int = 5,
            on_low_queue: Optional[Callable] = None,
    ):
        self.name = name
        self.storage_path = storage_path or Path(f"queue_{name}.json")
        self.low_threshold = low_threshold
        self.on_low_queue = on_low_queue or self._default_low_queue_callback
        self._ensure_storage()

    def _ensure_storage(self):
        """Initialize storage file if it doesn't exist"""
        if not self.storage_path.exists():
            self._save_items([])

    def _load_items(self) -> List[QueueItem]:
        """Load items from storage"""
        with open(self.storage_path, "r") as f:
            data = json.load(f)
            return [QueueItem.model_validate(item) for item in data]

    def _save_items(self, items: List[QueueItem]):
        """Save items to storage"""
        with open(self.storage_path, "w") as f:
            json.dump([item.model_dump() for item in items], f, default=str)

    def add_items(self, contents: List[str]) -> List[QueueItem]:
        """Add multiple items to queue"""
        items = self._load_items()
        new_items = [
            QueueItem(id=f"{self.name}_{datetime.now().timestamp()}_{i}", content=content)
            for i, content in enumerate(contents)
        ]
        items.extend(new_items)
        self._save_items(items)
        self._check_queue_level()
        return new_items

    def process_next(self) -> Optional[QueueItem]:
        """Process next item in queue"""
        items = self._load_items()
        if not items:
            return None

        item = items[0]
        item.processed_at = datetime.now()
        items = items[1:]  # Remove processed item
        self._save_items(items)
        self._check_queue_level()
        return item

    def _check_queue_level(self):
        """Check if queue is running low"""
        items = self._load_items()
        if len(items) <= self.low_threshold:
            self.on_low_queue(self.name, len(items))

    def _default_low_queue_callback(self, queue_name: str, items_count: int):
        """Default callback for low queue notification"""
        logger.warning(f"Queue {queue_name} running low! Only {items_count} items remaining")

    def get_size(self) -> int:
        """Get current queue size"""
        return len(self._load_items())


class QueueTracker:
    def __init__(self, storage_dir: Optional[Path] = None):
        self.storage_dir = storage_dir or Path.cwd()
        self.queues: Dict[str, Queue] = {}

    def create_queue():
        pass
