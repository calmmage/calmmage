import asyncio
import json
import os
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
from get_chat_list import get_chats
from loguru import logger
from main import get_telethon_client
from pathlib import Path
from telethon_manager import TelethonClientManager, StorageMode
from typing import Dict, List, Any
from utils import setup_logger


# c) get sample messages for each chat
async def get_messages_sample(client, chats, limit: int = 100):
    logger.debug(f"Getting {limit} messages from each chat")
    messages_by_chat = {}

    for chat in chats:
        chat_messages = []
        try:
            async for message in client.iter_messages(chat['entity'], limit=limit):
                # chat_messages.append({
                #     'id': message.id,
                #     'date': message.date.isoformat(),
                #     'text': message.text,
                #     'from_id': message.from_id.user_id if message.from_id else None,
                #     'has_media': bool(message.media)
                # })
                chat_messages.append(message)
            chat_messages = sorted(chat_messages, key=lambda x: x.date)
        except Exception as e:
            logger.warning(f"Failed to get messages for chat {chat['name']}: {e}")
            continue

        chat_id = chat['entity'].id
        messages_by_chat[chat_id] = chat_messages

    return messages_by_chat


# d) save to disk placeholder
def save_messages(messages_by_chat, output_path: Path = Path("data/messages_sample.json")):
    logger.debug("Saving messages placeholder - implement proper storage later")
    output_path.parent.mkdir(exist_ok=True)
    # TODO: Implement proper storage solution
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(messages_by_chat, f, indent=2, default=str)


# e) calculate basic stats
def calculate_stats(messages_by_chat):
    stats = {
        'total_chats': len(messages_by_chat),
        'total_messages': sum(len(messages) for messages in messages_by_chat.values()),
    }

    # TODO: Add more advanced stats in jupyter notebook:
    # - Message length distribution
    # - Time patterns (hour of day, day of week)
    # - Media type distribution
    # - Most active chats
    # - Most active users

    return stats


async def main(debug: bool = False):
    load_dotenv()
    setup_logger(logger, level="DEBUG" if debug else "INFO")

    client = await get_telethon_client()
    if not client:
        logger.error("Failed to get client")
        return

    chats = await get_chats()
    logger.info(f"Found {len(chats)} chats")

    # let's select a random sub-sample of chats
    random.shuffle(chats)
    chats = chats[:20]

    messages = await get_messages_sample(client, chats)  # Start with just 5 chats for testing
    logger.info(f"Downloaded messages from {len(messages)} chats")

    save_messages(messages)

    stats = calculate_stats(messages)
    logger.info("Message statistics:")
    for key, value in stats.items():
        logger.info(f"{key}: {value}")

    return messages  # For jupyter notebook usage


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    asyncio.run(main(debug=args.debug))
