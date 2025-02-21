from datetime import datetime, timedelta
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Date range settings
    START_DATE: datetime | None = None  # If None, defaults to 30 days ago
    END_DATE: datetime | None = None  # If None, defaults to now
    DEFAULT_DAYS_BACK: int = 30  # Number of days to look back by default

    # Zoom API credentials
    ZOOM_CLIENT_ID: str
    ZOOM_CLIENT_SECRET: str
    ZOOM_ACCOUNT_ID: str
    ZOOM_USER_ID: str = "me"  # Optional, defaults to 'me'

    # Google API settings
    CREDENTIALS_PATH: Path = Path("credentials.json")
    TOKEN_PATH: Path = Path("token.pickle")

    # Google Drive settings
    DRIVE_FOLDER: str = "Zoom Recordings"

    # Google Sheets settings
    ENABLE_SHEETS_TRACKING: bool = False
    SHEET_ID: str = ""  # Will be set when sheet is created

    # Email notification settings
    ENABLE_EMAIL_NOTIFICATIONS: bool = False
    EMAIL_FROM: str = ""
    EMAIL_TO: str = ""
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 465
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""

    # Paths
    DOWNLOADS_DIR: Path = Path("downloads")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
