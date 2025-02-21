"""
# - 1 - database
# - 2 - connection to telethon, session
# - 3 - get chats
# - 4 - yaml config
# - 5 - get messages
"""
import asyncio
import os
import sys
from dotenv import load_dotenv
from loguru import logger
from pathlib import Path
from pymongo import MongoClient
from telethon import TelegramClient
from telethon_manager import TelethonClientManager, StorageMode
from utils import setup_logger

load_dotenv()


# region 1 - database
def get_database():
    # option 1 - mongodb pymongo client

    logger.info("Starting MongoDB setup...")

    # Get MongoDB connection string and database name from environment variables
    conn_str = os.getenv("MONGO_CONN_STR")
    db_name = os.getenv("MONGO_DB_NAME", "telegram-messages-dec-2024")

    logger.debug(f"Using database name: {db_name}")
    logger.debug("Attempting to connect to MongoDB...")

    # Connect to MongoDB
    client = MongoClient(conn_str)
    logger.info("Successfully connected to MongoDB")

    # MongoDB creates databases and collections automatically when you first store data
    # But we can explicitly create them to ensure they exist
    logger.debug("Checking if database exists...")
    if db_name not in client.list_database_names():
        logger.debug(f"Creating database: {db_name}")
        db = client[db_name]
    else:
        logger.debug(f"Using existing database: {db_name}")
        db = client[db_name]

    # Define collections we'll need
    collections = {
        "messages": "telegram_messages",
        "chats": "telegram_chats",
        "users": "telegram_users",
        "heartbeats": "telegram_heartbeats"
    }

    logger.debug("Starting collection setup...")

    # Create collections if they don't exist
    for purpose, collection_name in collections.items():
        logger.debug(f"Checking collection: {collection_name}")
        if collection_name not in db.list_collection_names():
            logger.debug(f"Creating collection: {collection_name}")
            db.create_collection(collection_name)
        else:
            logger.debug(f"Using existing collection: {collection_name}")

    logger.debug("Collection setup complete")

    # add item, read items - to the test heartbeats collection
    logger.debug("Testing heartbeats collection...")
    heartbeats_collection = db.heartbeats
    from datetime import datetime
    logger.debug("Inserting test heartbeat...")
    heartbeats_collection.insert_one({"timestamp": datetime.now()})
    logger.debug("Reading test heartbeat...")
    heartbeats_collection.find_one()
    logger.info(
        f"MongoDB setup complete. Using database '{db_name}' with collections: {', '.join(collections.values())}")

    return db


# endregion 1

# region 2 - connection to telethon, session
async def get_telethon_client() -> TelegramClient:
    # Example initialization:
    SESSIONS_DIR = Path("sessions")
    SESSIONS_DIR.mkdir(exist_ok=True)
    TELEGRAM_API_ID = os.getenv('TELEGRAM_API_ID')
    if TELEGRAM_API_ID is None:
        raise ValueError("TELEGRAM_API_ID is not set")
    TELEGRAM_API_ID = int(TELEGRAM_API_ID)
    TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH')
    if TELEGRAM_API_HASH is None:
        raise ValueError("TELEGRAM_API_HASH is not set")
    telethon_manager = TelethonClientManager(
        storage_mode=StorageMode.TO_DISK,
        api_id=TELEGRAM_API_ID,
        api_hash=TELEGRAM_API_HASH,
        sessions_dir=SESSIONS_DIR
    )

    user_id = os.getenv('TELEGRAM_USER_ID')

    # Get client for user
    client = await telethon_manager.get_telethon_client(int(user_id))

    if not client:
        raise ValueError("Failed to get client")

    return client


# endregion 2

# region 3 - get chats


# endregion 3

# region 4 - yaml config
# endregion 4

# region 5 - get messages
# endregion 5

# region 6 - main
async def main(debug: bool = False):
    setup_logger(logger, level="DEBUG" if debug else "INFO")
    db = get_database()
    telethon_client = get_telethon_client()


# endregion 6


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    # Run the async main function
    asyncio.run(main(debug=args.debug))
