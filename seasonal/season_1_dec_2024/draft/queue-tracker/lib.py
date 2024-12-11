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
        """

        self.name = name
        # todo: parse a text-based cadence into a timedelta
        if isinstance(cadence, str):
            self.cadence = timedelta(seconds=parse(cadence))
        elif isinstance(cadence, timedelta):
            self.cadence = cadence

        if callback is None:
            callback = self._default_callback
        self.callback = callback

        if items is None:
            items = []
        else:
            # todo: parse items to classes if necessary
            parsed_items = []
            for item in items:
                if isinstance(item, QueueItem):
                    parsed_items.append(item)
                elif isinstance(item, dict):
                    # dict, i guess..
                    parsed_items.append(QueueItem(**item))
                else:
                    parsed_items.append(QueueItem(item))
        self.items = []

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
        self.queues = {}  # dict name -> Queue
        self.storage_mode = storage_mode
        if self.storage_mode == StorageMode.MEMORY:
            # todo: integrate storage mode in all places
            pass
        elif self.storage_mode == StorageMode.FILE:
            # todo: requires a file path
            if storage_path is None:
                # default storage path is ... the pwd / storage.json
                storage_path = fix_path("queue_tracker_state.json")
            else:
                storage_path = fix_path(storage_path)
            self.storage_path = storage_path

            if storage_path.exists():
                # load the state from the file
                data = json.loads(storage_path.read_text())
                # todo: ... - add the data from the state
                for queue in data["queues"]:
                    self.queues[queue["name"]] = Queue(**queue)
                #  to make this work we need to init the queues first, with proper callbacks and stuff
            else:
                # create an empty file
                self.export_state()
            # raise NotImplementedError("File storage is not implemented")
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
            # raise NotImplementedError("Memory storage does not need to save state")
            logger.debug("Memory storage does not need to save state")
        elif self.storage_mode == StorageMode.FILE:
            logger.debug(f"Exporting state to {self.storage_path}")
            # todo: save the state to the file
            res = {"queues": {}}
            for queue_name, queue in self.queues.items():
                res["queues"][queue_name] = {
                    "items": queue.items,
                    "last_dispatched": queue._last_dispatched,
                    "cadence": queue.cadence,
                    "callback": queue.callback.__name__,
                }
            with open(self.storage_path, "w") as f:
                json.dump(res, f)

        elif self.storage_mode == StorageMode.DB:
            # todo: save the state to the db
            raise NotImplementedError("DB storage state saving is not implemented")
