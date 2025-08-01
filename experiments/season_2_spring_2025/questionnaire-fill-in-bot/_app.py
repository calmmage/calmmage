from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    """Basic app configuration"""

    telegram_bot_token: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


class App:
    name = "Questionnaire Fill In Bot"

    def __init__(self, **kwargs):
        self.config = AppConfig(**kwargs)
