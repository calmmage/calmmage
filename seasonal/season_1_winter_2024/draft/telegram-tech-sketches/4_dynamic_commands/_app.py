from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    """Basic app configuration"""

    telegram_bot_token: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class App:
    name = "Mini Botspot Template"

    def __init__(self, **kwargs):
        self.config = AppConfig(**kwargs)
