from collections import defaultdict

import time
from datetime import datetime, timedelta
from lib import QueueTracker
from loguru import logger
from textwrap import dedent


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
