import os
import pytest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch, MagicMock

from telethon.types import Channel, Chat, User, Dialog, Message, PeerUser


@pytest.fixture(autouse=True)
def mock_env_settings():
    """Mock environment variables for tests."""
    env_vars = {
        'TELEGRAM_API_ID': '12345',
        'TELEGRAM_API_HASH': 'abcdef1234567890',
        'TELEGRAM_USER_ID': '291560340',
        'MONGO_CONN_STR': 'mongodb://localhost:27017',
        'MONGO_DB_NAME': 'test-telegram-messages',
        'MONGO_MESSAGES_COLLECTION': 'test_telegram_messages',
        'MONGO_CHATS_COLLECTION': 'test_telegram_chats',
        'MONGO_USERS_COLLECTION': 'test_telegram_users',
        'MONGO_HEARTBEATS_COLLECTION': 'test_telegram_heartbeats',
        'MONGO_APP_DATA_COLLECTION': 'test_telegram_app_data',
    }
    
    with patch.dict(os.environ, env_vars):
        yield


@pytest.fixture
def example_config_path():
    """Return path to example config for testing."""
    return Path(__file__).parent.parent / 'example.config.yaml'


@pytest.fixture
def mock_mongo_client():
    """Mocks MongoDB client for testing."""
    with patch('pymongo.MongoClient') as mock_client:
        # Setup mock collections
        mock_collections = {
            'test_telegram_messages': MagicMock(),
            'test_telegram_chats': MagicMock(),
            'test_telegram_users': MagicMock(),
            'test_telegram_heartbeats': MagicMock(),
            'test_telegram_app_data': MagicMock(),
        }
        
        # Setup mock database
        mock_db = MagicMock()
        mock_db.__getitem__.side_effect = lambda x: mock_collections.get(x, MagicMock())
        mock_db.list_collection_names.return_value = list(mock_collections.keys())
        
        # Setup mock client
        mock_client.return_value.__getitem__.return_value = mock_db
        mock_client.return_value.list_database_names.return_value = ['test-telegram-messages']
        
        yield mock_client


@pytest.fixture
def mock_telethon_client():
    """Mocks Telethon TelegramClient for testing."""
    with patch('telethon.TelegramClient') as mock_client:
        # Setup client instance
        instance = MagicMock()
        mock_client.return_value = instance
        
        # Setup methods
        instance.connect = MagicMock(return_value=None)
        instance.is_user_authorized = MagicMock(return_value=True)
        instance.start = MagicMock(return_value=None)
        
        yield mock_client, instance


@pytest.fixture
def mock_user():
    """Creates a mock User entity."""
    return User(
        id=123456,
        first_name="Test",
        last_name="User",
        username="testuser",
        phone="1234567890",
        bot=False,
        access_hash=1234567890,
        photo=None,
    )


@pytest.fixture
def mock_bot_user():
    """Creates a mock Bot User entity."""
    return User(
        id=654321,
        first_name="Test",
        last_name="Bot",
        username="testbot",
        phone=None,
        bot=True,
        access_hash=1234567890,
        photo=None,
    )


@pytest.fixture
def mock_channel():
    """Creates a mock Channel entity."""
    return Channel(
        id=789012,
        title="Test Channel",
        username="testchannel",
        photo=None,
        participants_count=500,
        megagroup=False,
        access_hash=1234567890,
        creator=True,
    )


@pytest.fixture
def mock_group_channel():
    """Creates a mock Group Channel entity (megagroup=True)."""
    return Channel(
        id=345678,
        title="Test Group Channel",
        username="testgroupchannel",
        photo=None,
        participants_count=200,
        megagroup=True,
        access_hash=1234567890,
        creator=True,
    )


@pytest.fixture
def mock_group():
    """Creates a mock Chat (group) entity."""
    return Chat(
        id=901234,
        title="Test Group",
        photo=None,
        participants_count=100,
        creator=False,
    )


@pytest.fixture
def mock_message(mock_user):
    """Creates a mock Message entity."""
    now = datetime.now(timezone.utc)
    return Message(
        id=1,
        peer_id=PeerUser(user_id=mock_user.id),
        date=now,
        message="Test message",
        out=False,
        from_id=PeerUser(user_id=mock_user.id),
    )


@pytest.fixture
def mock_dialogs(mock_user, mock_bot_user, mock_channel, mock_group_channel, mock_group):
    """Creates a list of mock Dialog entities."""
    now = datetime.now(timezone.utc)
    return [
        Dialog(peer=mock_user, top_message=1, date=now, entity=mock_user, name="Test User"),
        Dialog(peer=mock_bot_user, top_message=2, date=now, entity=mock_bot_user, name="Test Bot"),
        Dialog(peer=mock_channel, top_message=3, date=now, entity=mock_channel, name="Test Channel"),
        Dialog(peer=mock_group_channel, top_message=4, date=now, entity=mock_group_channel, name="Test Group Channel"),
        Dialog(peer=mock_group, top_message=5, date=now, entity=mock_group, name="Test Group"),
    ]
