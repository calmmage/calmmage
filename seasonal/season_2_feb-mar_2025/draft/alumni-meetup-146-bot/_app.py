from pydantic_settings import BaseSettings
from pydantic import BaseModel
from enum import Enum


class City(str, Enum):
    MOSCOW = "Москва"
    SAINT_PETERSBURG = "Питер"
    PERM = "Пермь"


class Registration(BaseModel):
    full_name: str
    graduation_year: int
    class_letter: str
    city: City


class AppConfig(BaseSettings):
    """Basic app configuration"""

    telegram_bot_token: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


class App:
    name = "Alumni Meetup 146 Bot"

    def __init__(self, **kwargs):
        self.config = AppConfig(**kwargs)
        self.registrations = {}  # user_id -> Registration
