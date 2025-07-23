from pydantic_settings import BaseSettings
from pydantic import BaseModel


class AppConfig(BaseSettings):
    """Basic app configuration"""

    telegram_bot_token: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

class Tool(BaseModel):
    name: str
    # description: str
    # function: Callable



class App:
    name = "Personal Toolkit Bot"

    def __init__(self, **kwargs):
        self.config = AppConfig(**kwargs)
