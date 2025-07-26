
from telegram_downloader.config import (
    StorageMode,
    TelegramDownloaderConfig,
    TelegramDownloaderEnvSettings,
    ChatCategoryConfig,
    SizeThresholds,
)


def test_storage_mode_enum():
    """Test the StorageMode enum values."""
    assert StorageMode.MONGO == "mongo"
    assert StorageMode.LOCAL == "local"


def test_telegram_downloader_env_settings():
    """Test that env settings are loaded correctly with defaults."""
    settings = TelegramDownloaderEnvSettings()
    
    # Required fields should be loaded from the mocked env
    assert settings.TELEGRAM_API_ID == 12345
    assert settings.TELEGRAM_API_HASH == "abcdef1234567890"
    assert settings.TELEGRAM_USER_ID == "291560340"
    
    # Optional fields should have defaults
    assert settings.TELETHON_SESSION_STR is None
    assert settings.MONGO_DB_NAME == "telegram-messages-dec-2024"
    assert settings.MONGO_MESSAGES_COLLECTION == "telegram_messages"
    assert settings.MONGO_CHATS_COLLECTION == "telegram_chats"
    assert settings.MONGO_USERS_COLLECTION == "telegram_users"
    assert settings.MONGO_HEARTBEATS_COLLECTION == "telegram_heartbeats"
    assert settings.MONGO_APP_DATA_COLLECTION == "telegram_downloader_app_data"


def test_size_thresholds_defaults():
    """Test SizeThresholds model defaults."""
    thresholds = SizeThresholds()
    assert thresholds.max_members_group == 1000
    assert thresholds.max_members_channel == 1000


def test_chat_category_config_defaults():
    """Test ChatCategoryConfig model defaults."""
    config = ChatCategoryConfig()
    assert config.enabled is False
    assert config.backdays is None
    assert config.limit is None
    assert config.download_attachments is False
    assert config.whitelist == []
    assert config.blacklist == []
    assert config.skip_big is True


def test_telegram_downloader_config_defaults():
    """Test TelegramDownloaderConfig model defaults."""
    config = TelegramDownloaderConfig()
    assert config.storage_mode == StorageMode.MONGO
    assert isinstance(config.size_thresholds, SizeThresholds)
    assert isinstance(config.owned_groups, ChatCategoryConfig)
    assert isinstance(config.owned_channels, ChatCategoryConfig)
    assert isinstance(config.other_groups, ChatCategoryConfig)
    assert isinstance(config.other_channels, ChatCategoryConfig)
    assert isinstance(config.private_chats, ChatCategoryConfig)
    assert isinstance(config.bots, ChatCategoryConfig)


def test_load_config_from_yaml(example_config_path):
    """Test loading config from YAML file."""
    config = TelegramDownloaderConfig.from_yaml(example_config_path)
    
    # Check a few values from the example config
    assert config.storage_mode == StorageMode.MONGO
    assert config.owned_groups.enabled is True
    assert config.owned_groups.backdays == 365
    assert config.owned_groups.limit == 100
    assert config.owned_groups.download_attachments is False
    assert config.bots.whitelist == ["test_bot"]
    assert config.bots.skip_big is False


def test_override_config_from_yaml(example_config_path):
    """Test overriding values when loading from YAML."""
    config = TelegramDownloaderConfig.from_yaml(
        example_config_path, storage_mode=StorageMode.LOCAL
    )
    
    # Check that the override was applied
    assert config.storage_mode == StorageMode.LOCAL
    
    # Other values should still be loaded from yaml
    assert config.owned_groups.enabled is True
    assert config.owned_groups.backdays == 365
