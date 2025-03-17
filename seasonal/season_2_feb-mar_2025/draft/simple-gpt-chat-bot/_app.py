from typing import Dict, Optional

from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    """Basic app configuration"""

    telegram_bot_token: str
    
    # LLM settings
    system_message: str = "You are a helpful assistant. Keep your responses concise and friendly."
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


class App:
    name = "Simple GPT Chat Bot"
    
    # Store user state
    user_states: Dict[int, Dict] = {}

    def __init__(self, **kwargs):
        self.config = AppConfig(**kwargs)
        
    def get_user_state(self, user_id: int) -> Dict:
        """Get the state for a specific user, initializing if it doesn't exist."""
        if user_id not in self.user_states:
            self.user_states[user_id] = {
                "chat_history": [],  # For future implementation
            }
        return self.user_states[user_id]
