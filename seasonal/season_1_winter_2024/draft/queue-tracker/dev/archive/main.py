from lib import QueueTracker
from loguru import logger
from pathlib import Path


def main():
    # Initialize queue tracker
    tracker = QueueTracker()

    while True:
        print("\nQueue Tracker Demo")
        print("1. Create new queue")
        print("2. Add items to queue")
        print("3. Process next item from queue")
        print("4. Show queue sizes")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Enter queue name: ").strip()
            try:
                queue = tracker.create_queue(name)
                logger.info(f"Created queue: {name}")
            except ValueError as e:
                logger.error(str(e))

        elif choice == "2":
            name = input("Enter queue name: ").strip()
            queue = tracker.get_queue(name)
            if not queue:
                logger.error(f"Queue {name} not found")
                continue

            items = input("Enter items (comma-separated): ").split(",")
            items = [item.strip() for item in items if item.strip()]
            added = queue.add_items(items)
            logger.info(f"Added {len(added)} items to queue {name}")

        elif choice == "3":
            name = input("Enter queue name: ").strip()
            queue = tracker.get_queue(name)
            if not queue:
                logger.error(f"Queue {name} not found")
                continue

            item = queue.process_next()
            if item:
                logger.info(f"Processed item from {name}: {item.content}")
            else:
                logger.warning(f"No items in queue {name}")

        elif choice == "4":
            queues = tracker.list_queues()
            if not queues:
                logger.info("No queues created yet")
                continue

            for queue_name in queues:
                queue = tracker.get_queue(queue_name)
                size = queue.get_size()
                logger.info(f"Queue {queue_name}: {size} items")
            logger.info(f"Total items: {tracker.get_total_items()}")

        elif choice == "5":
            break


if __name__ == "__main__":
    main()
