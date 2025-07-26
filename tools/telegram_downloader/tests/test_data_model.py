import json
from datetime import datetime, timezone, timedelta

from telegram_downloader.data_model import ChatData


def test_chat_data_init_with_entity(mock_user):
    """Test initializing ChatData with an entity."""
    now = datetime.now(timezone.utc)
    chat_data = ChatData(entity=mock_user, last_message_date=now)
    
    assert chat_data.entity == mock_user
    assert chat_data.last_message_date == now
    assert chat_data.finished_downloading is False
    assert chat_data.id == mock_user.id


def test_chat_data_init_with_dict(mock_user):
    """Test initializing ChatData with a dictionary."""
    now = datetime.now(timezone.utc)
    
    # Create dict representation of user with _ field for type
    user_dict = mock_user.to_dict()
    user_dict["_"] = "User"
    
    chat_data = ChatData(entity=user_dict, last_message_date=now.isoformat())
    
    assert chat_data.entity.id == mock_user.id
    assert chat_data.entity.first_name == mock_user.first_name
    assert chat_data.entity.last_name == mock_user.last_name
    assert chat_data.entity.username == mock_user.username
    assert chat_data.last_message_date.replace(microsecond=0) == now.replace(microsecond=0)
    assert chat_data.finished_downloading is False


def test_chat_data_to_json(mock_user):
    """Test serializing ChatData to JSON."""
    now = datetime.now(timezone.utc)
    chat_data = ChatData(entity=mock_user, last_message_date=now)
    
    json_str = chat_data.to_json()
    data = json.loads(json_str)
    
    assert data["id"] == mock_user.id
    assert "entity" in data
    assert data["last_message_date"] == now.isoformat()
    assert data["finished_downloading"] is False


def test_chat_data_to_dict(mock_user):
    """Test converting ChatData to dictionary."""
    now = datetime.now(timezone.utc)
    chat_data = ChatData(entity=mock_user, last_message_date=now)
    
    data = chat_data.to_dict()
    
    assert data["id"] == mock_user.id
    assert "entity" in data
    assert data["last_message_date"] == now
    assert data["finished_downloading"] is False


def test_chat_data_from_json(mock_user):
    """Test creating ChatData from JSON."""
    now = datetime.now(timezone.utc)
    chat_data = ChatData(entity=mock_user, last_message_date=now)
    
    json_str = chat_data.to_json()
    new_chat_data = ChatData.from_json(json_str)
    
    assert new_chat_data.id == chat_data.id
    assert new_chat_data.last_message_date.replace(microsecond=0) == chat_data.last_message_date.replace(microsecond=0)
    assert new_chat_data.finished_downloading == chat_data.finished_downloading


def test_chat_data_entity_category_user(mock_user):
    """Test entity_category for User."""
    chat_data = ChatData(entity=mock_user, last_message_date=datetime.now(timezone.utc))
    assert chat_data.entity_category == "private chat"


def test_chat_data_entity_category_bot(mock_bot_user):
    """Test entity_category for Bot."""
    chat_data = ChatData(entity=mock_bot_user, last_message_date=datetime.now(timezone.utc))
    assert chat_data.entity_category == "bot"


def test_chat_data_entity_category_group(mock_group):
    """Test entity_category for Group."""
    chat_data = ChatData(entity=mock_group, last_message_date=datetime.now(timezone.utc))
    assert chat_data.entity_category == "group"


def test_chat_data_entity_category_channel(mock_channel):
    """Test entity_category for Channel."""
    chat_data = ChatData(entity=mock_channel, last_message_date=datetime.now(timezone.utc))
    assert chat_data.entity_category == "channel"


def test_chat_data_entity_category_megagroup(mock_group_channel):
    """Test entity_category for Megagroup Channel."""
    chat_data = ChatData(entity=mock_group_channel, last_message_date=datetime.now(timezone.utc))
    assert chat_data.entity_category == "group"


def test_chat_data_is_recent(mock_group):
    """Test is_recent property with different timestamps."""
    now = datetime.now(timezone.utc)
    old_date = now - timedelta(days=60)
    recent_date = now - timedelta(days=15)
    
    old_chat = ChatData(entity=mock_group, last_message_date=old_date)
    recent_chat = ChatData(entity=mock_group, last_message_date=recent_date)
    
    assert old_chat.is_recent is False
    assert recent_chat.is_recent is True
    
    # Test with custom threshold
    assert old_chat.get_is_recent(timedelta(days=90)) is True
    assert recent_chat.get_is_recent(timedelta(days=10)) is False


def test_chat_data_is_owned(mock_channel, mock_group):
    """Test is_owned property."""
    chat_with_creator = ChatData(entity=mock_channel, last_message_date=datetime.now(timezone.utc))
    chat_without_creator = ChatData(entity=mock_group, last_message_date=datetime.now(timezone.utc))
    
    assert chat_with_creator.is_owned is True
    assert chat_without_creator.is_owned is False


def test_chat_data_is_big(mock_channel, mock_group):
    """Test is_big property with different participant counts."""
    big_channel = ChatData(entity=mock_channel, last_message_date=datetime.now(timezone.utc))  # 500 participants
    small_group = ChatData(entity=mock_group, last_message_date=datetime.now(timezone.utc))  # 100 participants
    
    # Default threshold is 1000
    assert big_channel.is_big is False
    assert small_group.is_big is False
    
    # Test with custom threshold
    assert big_channel.get_is_big(400) is True
    assert small_group.get_is_big(50) is True


def test_chat_data_name_user(mock_user):
    """Test name property for User entity."""
    chat_data = ChatData(entity=mock_user, last_message_date=datetime.now(timezone.utc))
    name = chat_data.name
    
    assert "Test User" in name
    assert "@testuser" in name
    assert f"[{mock_user.id}]" in name


def test_chat_data_name_channel(mock_channel):
    """Test name property for Channel entity."""
    chat_data = ChatData(entity=mock_channel, last_message_date=datetime.now(timezone.utc))
    name = chat_data.name
    
    assert "Test Channel" in name
    assert "@testchannel" in name
    assert f"[{mock_channel.id}]" in name
