import pytest
from datetime import datetime, timezone
from unittest.mock import patch, AsyncMock, MagicMock

from telegram_downloader.config import StorageMode
from telegram_downloader.telegram_downloader import TelegramDownloader
from telegram_downloader.data_model import ChatData


@pytest.fixture
def mock_telegram_downloader(example_config_path, mock_mongo_client):
    """Create a TelegramDownloader instance with mocked dependencies."""
    with patch('telegram_downloader.telegram_downloader.TelegramClient') as mock_client_class:
        # Setup mock telethon client
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client
        mock_client.connect = AsyncMock()
        mock_client.start = AsyncMock()
        mock_client.is_user_authorized = AsyncMock(return_value=True)
        
        # Create downloader instance
        downloader = TelegramDownloader(config_path=example_config_path)
        
        yield downloader, mock_client


def test_telegram_downloader_init(example_config_path, mock_mongo_client):
    """Test initialization of TelegramDownloader."""
    # Initialize downloader
    downloader = TelegramDownloader(config_path=example_config_path)
    
    # Check properties
    assert downloader.config.storage_mode == StorageMode.MONGO
    assert downloader._telethon_client is None
    assert downloader._db is None
    
    # Check that properties were reset
    assert downloader._messages is None
    assert downloader._messages_raw is None
    assert downloader._chats is None
    assert downloader._chats_raw is None
    assert downloader._chat_names is None


@pytest.mark.asyncio
async def test_get_telethon_client(mock_telegram_downloader):
    """Test get_telethon_client method."""
    downloader, mock_client = mock_telegram_downloader
    
    # Patch the _get_telethon_client method
    with patch.object(downloader, '_get_telethon_client', new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_client
        
        # First call should call _get_telethon_client
        client = await downloader.get_telethon_client()
        mock_get.assert_called_once()
        assert client == mock_client
        
        # Reset mock
        mock_get.reset_mock()
        
        # Second call should use cached client
        client = await downloader.get_telethon_client()
        mock_get.assert_not_called()
        assert client == mock_client


def test_storage_mode(example_config_path):
    """Test storage_mode property."""
    # Test with default config (MONGO)
    downloader = TelegramDownloader(config_path=example_config_path)
    assert downloader.storage_mode == StorageMode.MONGO
    
    # Test with overridden config (LOCAL)
    downloader = TelegramDownloader(
        config_path=example_config_path, storage_mode=StorageMode.LOCAL
    )
    assert downloader.storage_mode == StorageMode.LOCAL


@pytest.mark.asyncio
async def test_pick_chat_config(mock_telegram_downloader, mock_user, mock_bot_user, 
                             mock_channel, mock_group_channel, mock_group):
    """Test _pick_chat_config method with different chat types."""
    downloader, _ = mock_telegram_downloader
    now = datetime.now(timezone.utc)
    
    # Test private chat
    private_chat = ChatData(entity=mock_user, last_message_date=now)
    config = downloader._pick_chat_config(private_chat)
    assert config == downloader.config.private_chats
    
    # Test bot
    bot_chat = ChatData(entity=mock_bot_user, last_message_date=now)
    config = downloader._pick_chat_config(bot_chat)
    assert config == downloader.config.bots
    
    # Test owned channel
    owned_channel = ChatData(entity=mock_channel, last_message_date=now)  # has creator=True
    config = downloader._pick_chat_config(owned_channel)
    assert config == downloader.config.owned_channels
    
    # Test owned group (megagroup channel)
    owned_group = ChatData(entity=mock_group_channel, last_message_date=now)  # has creator=True
    config = downloader._pick_chat_config(owned_group)
    assert config == downloader.config.owned_groups
    
    # Test other group
    other_group = ChatData(entity=mock_group, last_message_date=now)  # has creator=False
    config = downloader._pick_chat_config(other_group)
    assert config == downloader.config.other_groups


@pytest.mark.asyncio
async def test_filter_redundant_chats(mock_telegram_downloader, mock_channel, mock_group):
    """Test _filter_redundant_chats method."""
    downloader, _ = mock_telegram_downloader
    now = datetime.now(timezone.utc)
    
    # Create a regular group and a channel
    group = ChatData(entity=mock_group, last_message_date=now)
    channel = ChatData(entity=mock_channel, last_message_date=now)
    
    # Create a migrated group (has migrated_to field pointing to channel)
    migrated_group = MagicMock()
    migrated_group.id = 12345
    migrated_group.entity = MagicMock()
    migrated_group.entity.migrated_to = MagicMock()
    migrated_group.entity.migrated_to.channel_id = mock_channel.id
    migrated_group.last_message_date = now
    migrated_group.name = "Migrated Group"
    
    # Filter the chats
    filtered = downloader._filter_redundant_chats([group, channel, migrated_group])
    
    # Should only keep the non-migrated group and channel
    assert len(filtered) == 2
    assert any(c.id == mock_group.id for c in filtered)
    assert any(c.id == mock_channel.id for c in filtered)
    assert not any(c.id == migrated_group.id for c in filtered)