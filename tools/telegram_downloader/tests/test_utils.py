import sys
from datetime import datetime, timezone, timedelta
from unittest.mock import patch

from telegram_downloader.utils import setup_logger, ensure_utc_datetime
from loguru import logger


def test_setup_logger():
    """Test setup_logger function."""
    # Mock logger.remove() and logger.add()
    with patch.object(logger, 'remove') as mock_remove:
        with patch.object(logger, 'add') as mock_add:
            # Call setup_logger
            setup_logger(logger, level="DEBUG")
            
            # Verify logger was configured correctly
            mock_remove.assert_called_once()
            mock_add.assert_called_once()
            
            # Check arguments to add
            args, kwargs = mock_add.call_args
            assert kwargs['sink'] == sys.stderr
            assert kwargs['level'] == "DEBUG"
            assert kwargs['colorize'] is True


def test_ensure_utc_datetime_none():
    """Test ensure_utc_datetime with None input."""
    assert ensure_utc_datetime(None) is None


def test_ensure_utc_datetime_naive():
    """Test ensure_utc_datetime with naive datetime."""
    naive_dt = datetime(2023, 1, 1, 12, 0, 0)
    assert naive_dt.tzinfo is None
    
    utc_dt = ensure_utc_datetime(naive_dt)
    assert utc_dt.tzinfo is not None
    assert utc_dt.tzinfo == timezone.utc
    assert utc_dt.year == naive_dt.year
    assert utc_dt.month == naive_dt.month
    assert utc_dt.day == naive_dt.day
    assert utc_dt.hour == naive_dt.hour


def test_ensure_utc_datetime_aware():
    """Test ensure_utc_datetime with timezone-aware datetime."""
    # Create a non-UTC timezone
    est = timezone(timedelta(hours=-5))
    est_dt = datetime(2023, 1, 1, 12, 0, 0, tzinfo=est)
    
    utc_dt = ensure_utc_datetime(est_dt)
    assert utc_dt.tzinfo == timezone.utc
    # EST is UTC-5, so 12:00 EST = 17:00 UTC
    assert utc_dt.hour == 17


def test_ensure_utc_datetime_already_utc():
    """Test ensure_utc_datetime with datetime already in UTC."""
    utc_dt = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    result = ensure_utc_datetime(utc_dt)
    
    assert result == utc_dt
    assert result.tzinfo == timezone.utc
