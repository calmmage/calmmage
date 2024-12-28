"""Telegram message downloader using Telethon."""
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union, Callable

from loguru import logger
from telethon import TelegramClient
from telethon.tl.types import User, Chat, Channel, Message

from download_script.settings import DownloaderConfig


class TelegramDownloader:
    def __init__(
        self, 
        config: DownloaderConfig, 
        user_id: Union[int, str],
        phone: Optional[str] = None,
        code_callback: Optional[Callable] = None,
        sessions_dir: str = "sessions",
    ):
        """
        Initialize the downloader.
        
        Args:
            config: Downloader configuration
            user_id: Telegram user ID for the session
            phone: Phone number for authentication
            code_callback: Callback function to get verification code
            sessions_dir: Directory to store session files
        """
        self.config = config
        self.user_id = str(user_id)
        self.phone = phone
        self.code_callback = code_callback or (lambda: input("Enter the verification code: "))
        self.sessions_dir = Path(sessions_dir)
        self.sessions_dir.mkdir(exist_ok=True)
        self.session_name = str(self.sessions_dir / f"user_{self.user_id}")
        self.client: Optional[TelegramClient] = None
        
        # Stats
        self.stats = {
            "personal": 0,
            "groups": 0,
            "channels": 0,
            "bots": 0,
            "total_messages": 0,
        }
    
    async def init_client(self, api_id: int, api_hash: str) -> None:
        """Initialize Telethon client."""
        self.client = TelegramClient(self.session_name, api_id, api_hash)
        await self.client.connect()
        if not await self.client.is_user_authorized():
            try:
                # Start the client with phone number and code callback
                await self.client.start(
                    phone=self.phone,
                    code_callback=self.code_callback
                )
                
                if await self.client.is_user_authorized():
                    logger.info('Successfully authenticated!')
                else:
                    raise RuntimeError('Authentication failed. Please check your credentials.')
                
            except Exception as e:
                logger.error(f"Failed to initialize client: {e}")
                raise
        
    async def resolve_entity(self, entity_id: Union[str, int]):
        """Resolve entity by username or ID."""
        try:
            return await self.client.get_entity(entity_id)
        except Exception as e:
            logger.warning(f"Failed to resolve entity {entity_id}: {e}")
            return None
    
    def update_stats(self, entity) -> None:
        """Update stats based on entity type."""
        if isinstance(entity, User):
            if entity.bot:
                self.stats["bots"] += 1
            else:
                self.stats["personal"] += 1
        elif isinstance(entity, Chat):
            self.stats["groups"] += 1
        elif isinstance(entity, Channel):
            if entity.megagroup:
                self.stats["groups"] += 1
            else:
                self.stats["channels"] += 1
    
    async def download_messages(self, entity, since_time: datetime) -> List[Message]:
        """Download messages from an entity since given time."""
        messages = []
        try:
            logger.info(f"Starting download for entity: {entity.id} (name: {getattr(entity, 'username', 'N/A')})")
            logger.debug(f"Target time: {since_time} (timezone: {since_time.tzinfo})")
            
            async for message in self.client.iter_messages(entity, offset_date=since_time):
                # Ensure message date is timezone-aware
                msg_date = message.date.astimezone()
                logger.debug(f"Processing message from {msg_date} (timezone: {msg_date.tzinfo})")
                
                # Stop iteration if we hit messages older than our target time
                if msg_date < since_time:
                    logger.debug(f"Reached message older than target time: {msg_date} < {since_time}")
                    break
                
                messages.append(message)
                self.stats["total_messages"] += 1
                
                if len(messages) % 100 == 0:
                    logger.debug(f"Downloaded {len(messages)} messages from {entity.id}")
                
                if self.config.settings.download_media and message.media:
                    media_path = self.config.settings.media_dir / str(entity.id)
                    media_path.mkdir(exist_ok=True)
                    logger.debug(f"Downloading media from message {message.id} to {media_path}")
                    await self.client.download_media(message, file=media_path)
                    
        except Exception as e:
            logger.error(f"Failed to download messages from {entity.id}: {e}", exc_info=True)
        
        logger.info(f"Completed downloading {len(messages)} messages from entity {entity.id}")
        return messages
    
    async def run(self) -> None:
        """Run the downloader."""
        if not self.client:
            raise RuntimeError("Client not initialized. Call init_client first.")
        
        # Make sure we create a timezone-aware datetime
        since_time = datetime.now().astimezone()
        since_time = since_time - self.config.get_time_delta()
        logger.info(f"Will download messages since: {since_time} (timezone: {since_time.tzinfo})")
        
        # Process personal chats
        logger.info(f"Processing {len(self.config.chats.personal)} personal chats")
        for chat_id in self.config.chats.personal:
            logger.debug(f"Resolving personal chat: {chat_id}")
            entity = await self.resolve_entity(chat_id)
            if entity:
                logger.info(f"Found entity {chat_id}: {type(entity).__name__}")
                self.update_stats(entity)
                await self.download_messages(entity, since_time)
            else:
                logger.warning(f"Could not resolve personal chat: {chat_id}")
        
        # Process groups
        logger.info(f"Processing {len(self.config.chats.groups)} groups")
        for group_id in self.config.chats.groups:
            logger.debug(f"Resolving group: {group_id}")
            entity = await self.resolve_entity(group_id)
            if entity:
                logger.info(f"Found entity {group_id}: {type(entity).__name__}")
                self.update_stats(entity)
                await self.download_messages(entity, since_time)
            else:
                logger.warning(f"Could not resolve group: {group_id}")
        
        # Process channels
        logger.info(f"Processing {len(self.config.chats.channels)} channels")
        for channel_id in self.config.chats.channels:
            logger.debug(f"Resolving channel: {channel_id}")
            entity = await self.resolve_entity(channel_id)
            if entity:
                logger.info(f"Found entity {channel_id}: {type(entity).__name__}")
                self.update_stats(entity)
                await self.download_messages(entity, since_time)
            else:
                logger.warning(f"Could not resolve channel: {channel_id}")

        # Print stats
        logger.info("=== Download Summary ===")
        logger.info(f"Personal chats processed: {self.stats['personal']}")
        logger.info(f"Groups processed: {self.stats['groups']}")
        logger.info(f"Channels processed: {self.stats['channels']}")
        logger.info(f"Bots encountered: {self.stats['bots']}")
        logger.info(f"Total messages downloaded: {self.stats['total_messages']}")
    
    # async def close(self) -> None:
    #     """Close the client connection."""
    #     if self.client:
    #         await self.client.disconnect() 