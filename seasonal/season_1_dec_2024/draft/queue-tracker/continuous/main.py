from collections import defaultdict
from textwrap import dedent
from datetime import datetime, timedelta
import time
from loguru import logger


class Queue:
    def __init__(self, name, cadence):
        """
        :param cadence: how often to dispatch an item from the queue
        """

        self.name = name
        # todo: parse a text-based cadence into a timedelta
        if isinstance(cadence, str):
            raise ValueError("str based cadence is Not implemented, please provide a timedelta")
        elif isinstance(cadence, timedelta):
            self.cadence = cadence
        self.items = []

        self._last_dispatched = None

    def add_item(self, item):
        self.items.append(item)

    def dispatch(self):
        if not self.items:
            logger.debug(f'No items in the queue "{self.name}"')
        elif self._last_dispatched is None or datetime.now() - self._last_dispatched > self.cadence:
            item = self.items.pop(0)
            # todo: make this a callback
            print(f'Dispatching "{item}" from "{self.name}"')
            # todo: in addition to calling a callback we want to 
            self._last_dispatched = datetime.now()
        else:
            logger.debug(f'Not enough time has passed since last dispatch in "{self.name}"')


class QueueTracker:
    def __init__(self):
        self.queues = {}  # dict name -> Queue

    def add_queue(self, name, cadence):
        # todo: check if busy
        self.queues[name] = Queue(name=name, cadence=cadence)

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

    def bulk_add(self, data: str, format=1):
        parsed_data = self._parse_items(data, format=format)

        for queue_name, items in parsed_data.items():
            if queue_name not in self.queues:
                raise ValueError(f'Trying to add items to a non-existing queue: "{queue_name}"')
                # self.add_queue(queue_name, timedelta(days=1))
            for item in items:
                self.queues[queue_name].add_item(item)

    def run(self):
        while True:
            for queue in self.queues.values():
                # dispatch item if enough time has passed
                queue.dispatch()
            time.sleep(5)


def main():
    qt = QueueTracker()

    # add queues
    qt.add_queue("cool things to buy", timedelta(seconds=15))
    qt.add_queue("things to release at work", timedelta(seconds=25))
    qt.add_queue("games to play", timedelta(seconds=5))

    # add items
    data = dedent(
        """
        # cool things to buy
        - psvr
        - apple studio monitor
        - fpv drone
        
        # things to release at work
        - syntax check
        - message history slider
        - custom prompts + auto-reminder
        
        # games to play
        - baldurs gate 3
        - minecraft
        - skyrim
        - fallout 4
        - portal stories mel
        - rdr2
        - cyberpunk 2077
        - death stranding
        - enderall
        """
    )

    # todo: in real-world setup we're not doing this on every launch - but add up interactively.
    #  and then we save the state and recover on load
    #  to support that we need to rework the system completely
    qt.bulk_add(data)

    qt.run()


if __name__ == "__main__":
    main()
