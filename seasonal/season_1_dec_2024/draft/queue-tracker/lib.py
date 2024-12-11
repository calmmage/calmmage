from collections import defaultdict
from textwrap import dedent
from datetime import datetime, timedelta
import time
from pytimeparse import parse
from calmlib.utils import fix_path
from loguru import logger
from pathlib import Path
import json
from enum import Enum

QueueItem = str


class Queue:
    def __init__(self, name, cadence, items=None, callback=None):
        """
        :param cadence: how often to dispatch an item from the queue
        Can be:
        - timedelta object
        - string (e.g. "20s", "1h", "2d")
        - dict with 'total_seconds' key
        """
        self.name = name
        
        # Parse cadence
        if isinstance(cadence, str):
            self.cadence = timedelta(seconds=parse(cadence))
        elif isinstance(cadence, timedelta):
            self.cadence = cadence
        else:
            raise ValueError(f"Invalid cadence format: {cadence}")

        if callback is None:
            callback = self._default_callback
        self.callback = callback

        # Parse items
        self.items = []
        if items:
            # Parse items to QueueItem if necessary
            for item in items:
                if isinstance(item, QueueItem):
                    self.items.append(item)
                elif isinstance(item, dict):
                    self.items.append(QueueItem(**item))
                else:
                    self.items.append(QueueItem(item))

        self._last_dispatched = None

    def add_item(self, item):
        # todo: make Item a class
        self.items.append(item)

    def dispatch(self):
        if not self.items:
            logger.debug(f'No items in the queue "{self.name}"')
        elif self._last_dispatched is None or datetime.now() - self._last_dispatched > self.cadence:
            # todo: actually add priority to the queue
            item = self.items.pop(0)
            self.callback(item)
            # todo: in addition to calling a callback we want to log  that this item was dispatched
            #  note: not just a regular text log, but a custom structured event log for future reference
            #  and potentially for example re-add the item back. E.g. save the state or something.
            self._last_dispatched = datetime.now()
        else:
            logger.debug(f'Not enough time has passed since last dispatch in "{self.name}"')

    def _default_callback(self, item):
        print(f'Dispatching "{item}" from "{self.name}"')


class StorageMode(Enum):
    MEMORY = "memory"
    FILE = "file"
    DB = "db"


class QueueTracker:
    def __init__(self, storage_mode: StorageMode = StorageMode.MEMORY, storage_path: str = None):
        """
        WARNING: Current implementation has limitations:
        1. Only default callback (_default_callback) is supported when loading from storage
        2. Custom callbacks will be lost after save/load cycle
        """
        self.queues = {}  # dict name -> Queue
        self.storage_mode = storage_mode
        if self.storage_mode == StorageMode.MEMORY:
            pass
        elif self.storage_mode == StorageMode.FILE:
            if storage_path is None:
                storage_path = fix_path("queue_tracker_state.json")
            else:
                storage_path = fix_path(storage_path)
            self.storage_path = storage_path

            if storage_path.exists():
                # load the state from the file
                data = json.loads(storage_path.read_text())
                for queue_name, queue_data in data["queues"].items():
                    # Only try to parse last_dispatched if it's not None
                    if queue_data.get("last_dispatched"):
                        try:
                            queue_data["last_dispatched"] = datetime.fromisoformat(queue_data["last_dispatched"])
                        except (ValueError, TypeError) as e:
                            logger.warning(f"Failed to parse last_dispatched for queue '{queue_name}': {e}")
                            queue_data["last_dispatched"] = None
                    
                    # Check callback - warn if non-default was used
                    saved_callback = queue_data.get("callback", "_default_callback")
                    if saved_callback != "_default_callback":
                        logger.warning(
                            f"Queue '{queue_name}' was saved with a custom callback '{saved_callback}'. "
                            "Using default callback instead as custom callbacks are not supported in storage."
                        )
                    
                    # Create queue with default callback
                    queue = Queue(
                        name=queue_data["name"],
                        cadence=queue_data["cadence"],  # Now handles string format like "20.0s"
                        items=queue_data["items"],
                    )
                    queue._last_dispatched = queue_data["last_dispatched"]
                    self.queues[queue_name] = queue
            else:
                # create an empty file
                self.export_state()
        elif storage_mode == StorageMode.DB:
            # todo: requires a db connection
            raise NotImplementedError("DB storage is not implemented")

    def add_queue(self, name, cadence, skip_export: bool = False):
        # todo: check if busy
        self.queues[name] = Queue(name=name, cadence=cadence)
        if not skip_export:
            self.export_state()

    def add_item(self, queue_name, item, skip_export: bool = False):
        if queue_name not in self.queues:
            raise ValueError(f'Queue "{queue_name}" does not exist')
        self.queues[queue_name].add_item(item)
        if not skip_export:
            self.export_state()

    # region 1 - parsing
    def _parse_items(self, data: str, format=1):
        if format == 1:
            # sample:
            # """
            # # cool things to buy
            # - psvr
            # - apple studio monitor
            # - fpv drone
            #
            # # things to release at work
            # - syntax check
            # - message history slider
            # - custom prompts + auto-reminder
            #
            # # games to play
            # - baldurs gate 3
            # - minecraft
            # - skyrim
            # - fallout 4
            # - portal stories mel
            # - rdr2
            # - cyberpunk 2077
            # - death stranding
            # - enderall
            # """
            # -> dict: {queue_name: [items]}
            res = defaultdict(list)
            queue_name = None
            for line in data.splitlines():
                if not line.strip():
                    continue
                elif line.startswith("#"):
                    queue_name = line[1:].strip()
                elif line.startswith("-"):
                    if queue_name is None:
                        raise ValueError(f"Item {line} has no queue name")
                    res[queue_name].append(line[1:].strip())
                else:
                    raise ValueError(f"Unknown line format: {line}")
            return res

        # todo: support more formats with better features if needed

    def bulk_add(self, data: str, format=1, skip_export: bool = False):
        parsed_data = self._parse_items(data, format=format)

        for queue_name, items in parsed_data.items():
            if queue_name not in self.queues:
                raise ValueError(f'Trying to add items to a non-existing queue: "{queue_name}"')
                # self.add_queue(queue_name, timedelta(days=1))
            for item in items:
                self.add_item(queue_name, item, skip_export=True)
        if not skip_export:
            self.export_state()

    # endregion 1

    # region 2 - running continuously
    def run(self, period=1):
        while True:
            self.dispatch_items()
            time.sleep(period)

    def dispatch_items(self, skip_export: bool = False):
        for queue in self.queues.values():
            # todo: actually, we need to save a structured log of events
            #  option 1: store events in a separate file
            #  option 2: keep all items in queue, just mark some as Done
            queue.dispatch()
        if not skip_export:
            self.export_state()

    # endregion 2

    # region 3 - saving and loading
    def export_state(self):
        if self.storage_mode == StorageMode.MEMORY:
            logger.debug("Memory storage does not need to save state")
        elif self.storage_mode == StorageMode.FILE:
            logger.debug(f"Exporting state to {self.storage_path}")
            res = {"queues": {}}
            for queue_name, queue in self.queues.items():
                res["queues"][queue_name] = {
                    "name": queue.name,
                    "items": queue.items,
                    "last_dispatched": queue._last_dispatched.isoformat() if queue._last_dispatched else None,
                    "cadence": str(queue.cadence.total_seconds()) + "s",
                    "callback": "_default_callback",
                }
            with open(self.storage_path, "w") as f:
                json.dump(res, f, indent=2)

        elif self.storage_mode == StorageMode.DB:
            # todo: save the state to the db
            raise NotImplementedError("DB storage state saving is not implemented")

    # endregion 3
