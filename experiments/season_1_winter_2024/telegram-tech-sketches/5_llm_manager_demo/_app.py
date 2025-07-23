from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    """Basic app configuration"""

    telegram_bot_token: str
    system_message: str = (
        "You are a friendly and helpful AI assistant. "
        "Be concise but informative in your responses."
        "Use html for basic formatting: <b>bold</b>, <i>italic</i>, <code>code</code>. "
        "Avoid complex formatting to prevent crashes."
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


class App:
    name = "AI Chat Bot Demo"

    def __init__(self, **kwargs):
        self.config = AppConfig(**kwargs)
