import pytest
from pathlib import Path
from unittest.mock import patch, AsyncMock

from telegram_downloader.config import StorageMode
from telegram_downloader.telethon_client_manager import TelethonClientManager


@pytest.fixture
def telethon_env_settings():
    """Create environment settings for TelethonClientManager tests."""
    return {
        'TELEGRAM_API_ID': 12345,
        'TELEGRAM_API_HASH': 'abcdef1234567890',
        'SESSIONS_DIR': Path('/tmp/test_sessions'),
    }


async def test_telethon_client_manager_init(telethon_env_settings):
    """Test initialization of TelethonClientManager."""
    # Create a temporary sessions directory for testing
    Path('/tmp/test_sessions').mkdir(exist_ok=True)
    
    try:
        # Initialize manager
        manager = TelethonClientManager(**telethon_env_settings)
        
        # Check properties
        assert manager.storage_mode == StorageMode.LOCAL
        assert manager.api_id == telethon_env_settings['TELEGRAM_API_ID']
        assert manager.api_hash == telethon_env_settings['TELEGRAM_API_HASH']
        assert manager.sessions_dir == telethon_env_settings['SESSIONS_DIR']
        assert isinstance(manager.clients, dict)
        assert len(manager.clients) == 0
    finally:
        # Cleanup
        if Path('/tmp/test_sessions').exists():
            import shutil
            shutil.rmtree('/tmp/test_sessions')


async def test_telethon_client_manager_mongo_mode(telethon_env_settings):
    """Test initialization with MONGO storage mode."""
    manager = TelethonClientManager(storage_mode=StorageMode.MONGO, **telethon_env_settings)
    assert manager.storage_mode == StorageMode.MONGO


@pytest.mark.asyncio
async def test_get_telethon_client_new_client(mock_telethon_client, telethon_env_settings):
    """Test get_telethon_client when creating a new client."""
    mock_client_class, mock_client_instance = mock_telethon_client
    
    with patch('telegram_downloader.telethon_client_manager.TelegramClient', mock_client_class):
        with patch.object(TelethonClientManager, '_check_if_conn_is_present_on_disk', return_value=False):
            with patch.object(TelethonClientManager, '_create_new_telethon_client_and_save_to_disk',
                               new_callable=AsyncMock) as mock_create:
                # Setup the create method to return a client instance
                mock_create.return_value = mock_client_instance
                
                # Create manager and get client
                manager = TelethonClientManager(**telethon_env_settings)
                client = await manager.get_telethon_client(123)
                
                # Verify correct methods were called
                mock_create.assert_called_once_with(123)
                assert client == mock_client_instance


@pytest.mark.asyncio
async def test_get_telethon_client_existing_client(mock_telethon_client, telethon_env_settings):
    """Test get_telethon_client when client already exists on disk."""
    mock_client_class, mock_client_instance = mock_telethon_client
    
    with patch('telegram_downloader.telethon_client_manager.TelegramClient', mock_client_class):
        with patch.object(TelethonClientManager, '_check_if_conn_is_present_on_disk', return_value=True):
            with patch.object(TelethonClientManager, '_load_conn_from_disk',
                               new_callable=AsyncMock) as mock_load:
                # Setup the load method to return a client instance
                mock_load.return_value = mock_client_instance
                
                # Create manager and get client
                manager = TelethonClientManager(**telethon_env_settings)
                client = await manager.get_telethon_client(123)
                
                # Verify correct methods were called
                mock_load.assert_called_once_with(123)
                assert client == mock_client_instance


@pytest.mark.asyncio
async def test_get_telethon_client_mongo_mode(mock_telethon_client, telethon_env_settings):
    """Test get_telethon_client in MongoDB mode."""
    mock_client_class, mock_client_instance = mock_telethon_client
    
    with patch('telegram_downloader.telethon_client_manager.TelegramClient', mock_client_class):
        with patch.object(TelethonClientManager, '_check_if_conn_is_present_in_db',
                          new_callable=AsyncMock) as mock_check:
            with patch.object(TelethonClientManager, '_create_new_telethon_client_and_save_to_db',
                             new_callable=AsyncMock) as mock_create:
                with patch.object(TelethonClientManager, '_load_conn_from_db',
                                 new_callable=AsyncMock) as mock_load:
                    # Setup method returns
                    mock_check.return_value = False
                    mock_create.return_value = mock_client_instance
                    
                    # Create manager and get client
                    manager = TelethonClientManager(storage_mode=StorageMode.MONGO, **telethon_env_settings)
                    
                    # This will raise NotImplementedError since MongoDB methods are not implemented
                    with pytest.raises(NotImplementedError):
                        await manager.get_telethon_client(123)


@pytest.mark.asyncio
async def test_check_if_conn_is_present_on_disk(telethon_env_settings):
    """Test _check_if_conn_is_present_on_disk method."""
    # Create test sessions dir
    sessions_dir = Path('/tmp/test_sessions')
    sessions_dir.mkdir(exist_ok=True)
    
    try:
        # Create a test session file
        test_session_file = sessions_dir / 'user_123.session'
        test_session_file.touch()
        
        # Initialize manager and check for existing session
        manager = TelethonClientManager(SESSIONS_DIR=sessions_dir, **telethon_env_settings)
        
        # Check for existing and non-existing sessions
        assert manager._check_if_conn_is_present_on_disk(123) is True
        assert manager._check_if_conn_is_present_on_disk(456) is False
    finally:
        # Cleanup
        if sessions_dir.exists():
            import shutil
            shutil.rmtree(sessions_dir)


@pytest.mark.asyncio
async def test_load_conn_from_disk(mock_telethon_client, telethon_env_settings):
    """Test _load_conn_from_disk method."""
    mock_client_class, mock_client_instance = mock_telethon_client
    
    # Create test sessions dir
    sessions_dir = Path('/tmp/test_sessions')
    sessions_dir.mkdir(exist_ok=True)
    
    try:
        # Create a test session file
        test_session_file = sessions_dir / 'user_123.session'
        test_session_file.touch()
        
        # Mock TelegramClient
        with patch('telegram_downloader.telethon_client_manager.TelegramClient', mock_client_class):
            # Setup mock client
            mock_client_instance.connect = AsyncMock()
            mock_client_instance.is_user_authorized = AsyncMock(return_value=True)
            
            # Initialize manager
            manager = TelethonClientManager(SESSIONS_DIR=sessions_dir, **telethon_env_settings)
            
            # Load connection
            client = await manager._load_conn_from_disk(123)
            
            # Verify
            assert client == mock_client_instance
            mock_client_instance.connect.assert_called_once()
            mock_client_instance.is_user_authorized.assert_called_once()
            assert 123 in manager.clients
            assert manager.clients[123] == mock_client_instance
    finally:
        # Cleanup
        if sessions_dir.exists():
            import shutil
            shutil.rmtree(sessions_dir)


@pytest.mark.asyncio
async def test_load_conn_from_disk_not_authorized(mock_telethon_client, telethon_env_settings):
    """Test _load_conn_from_disk when session exists but is not authorized."""
    mock_client_class, mock_client_instance = mock_telethon_client
    
    # Create test sessions dir
    sessions_dir = Path('/tmp/test_sessions')
    sessions_dir.mkdir(exist_ok=True)
    
    try:
        # Create a test session file
        test_session_file = sessions_dir / 'user_123.session'
        test_session_file.touch()
        
        # Mock TelegramClient
        with patch('telegram_downloader.telethon_client_manager.TelegramClient', mock_client_class):
            # Setup mock client as not authorized
            mock_client_instance.connect = AsyncMock()
            mock_client_instance.is_user_authorized = AsyncMock(return_value=False)
            
            # Initialize manager
            manager = TelethonClientManager(SESSIONS_DIR=sessions_dir, **telethon_env_settings)
            
            # Load connection should raise exception
            with pytest.raises(Exception, match="Session exists but not authorized"):
                await manager._load_conn_from_disk(123)
            
            # Verify
            mock_client_instance.connect.assert_called_once()
            mock_client_instance.is_user_authorized.assert_called_once()
            assert 123 not in manager.clients
    finally:
        # Cleanup
        if sessions_dir.exists():
            import shutil
            shutil.rmtree(sessions_dir)


@pytest.mark.asyncio
async def test_load_conn_from_disk_no_session(telethon_env_settings):
    """Test _load_conn_from_disk when session file doesn't exist."""
    # Create test sessions dir
    sessions_dir = Path('/tmp/test_sessions')
    sessions_dir.mkdir(exist_ok=True)
    
    try:
        # Initialize manager
        manager = TelethonClientManager(SESSIONS_DIR=sessions_dir, **telethon_env_settings)
        
        # Load connection should raise exception
        with pytest.raises(Exception, match="No session file found"):
            await manager._load_conn_from_disk(123)
    finally:
        # Cleanup
        if sessions_dir.exists():
            import shutil
            shutil.rmtree(sessions_dir)