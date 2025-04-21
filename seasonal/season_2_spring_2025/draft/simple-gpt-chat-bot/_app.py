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
    
    # Available scenarios
    scenarios = {
        "default": {
            "name": "Helpful Assistant",
            "description": "A helpful, friendly assistant that provides concise responses.",
            "system_message": "You are a helpful assistant. Keep your responses concise and friendly."
        },
        "creative": {
            "name": "Creative Writer",
            "description": "A creative writer that helps generate stories, poems, and imaginative content.",
            "system_message": "You are a creative writer with a vivid imagination. Help the user with creative writing, storytelling, and generating imaginative content. Be descriptive and engaging."
        },
        "expert": {
            "name": "Technical Expert",
            "description": "A technical expert that provides in-depth explanations on complex topics.",
            "system_message": "You are a technical expert capable of explaining complex topics in detail. Provide thorough, accurate information with proper context and nuance."
        },
        "philosopher": {
            "name": "Philosopher",
            "description": "A philosopher that explores deep questions and encourages critical thinking.",
            "system_message": "You are a philosopher with deep knowledge of various philosophical traditions. Help the user explore profound questions, encourage critical thinking, and provide thoughtful analysis of philosophical concepts. Consider multiple perspectives and encourage nuanced understanding."
        },
        "coach": {
            "name": "Life Coach",
            "description": "A supportive life coach that helps with personal development and goals.",
            "system_message": "You are a supportive life coach focused on helping people achieve their goals and improve their lives. Provide encouragement, practical advice, and thoughtful questions to help the user gain insight. Be positive but realistic."
        }
    }

    def __init__(self, **kwargs):
        self.config = AppConfig(**kwargs)
        
    def get_user_state(self, user_id: int) -> Dict:
        """Get the state for a specific user, initializing if it doesn't exist."""
        if user_id not in self.user_states:
            self.user_states[user_id] = {
                "chat_history": [],  # For future implementation
                "active_scenario": "default",  # Default scenario
                "custom_system_message": None,  # For custom scenarios
            }
        return self.user_states[user_id]
        
    def get_system_message(self, user_id: int) -> str:
        """Get the active system message for the user."""
        state = self.get_user_state(user_id)
        
        # If user has a custom system message, use that
        if state.get("custom_system_message"):
            return state["custom_system_message"]
            
        # Otherwise use the active scenario's system message
        scenario_key = state.get("active_scenario", "default")
        return self.scenarios.get(scenario_key, self.scenarios["default"])["system_message"]
        
    def get_available_scenarios(self) -> Dict:
        """Get dictionary of available scenarios."""
        return self.scenarios
