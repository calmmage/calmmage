from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Zoom API credentials
    ZOOM_CLIENT_ID: str
    ZOOM_CLIENT_SECRET: str
    ZOOM_ACCOUNT_ID: str
    ZOOM_USER_ID: str = "me"  # Optional, defaults to 'me'

    # Google Drive settings
    GOOGLE_DRIVE_FOLDER: str = "Zoom Recordings"

    # Paths
    CREDENTIALS_PATH: Path = Path("credentials.json")
    TOKEN_PATH: Path = Path("token.pickle")
    TEMP_DIR: Path = Path("temp")
    DOWNLOADS_DIR: Path = Path("downloads")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
