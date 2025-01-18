from datetime import datetime, timezone
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic_settings import BaseSettings
from botspot.utils.deps_getters import get_database

from models import User


class AppConfig(BaseSettings):
    """Basic app configuration"""
    telegram_bot_token: str
    users_collection: str = "botspot_users"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"



class App:
    name = "User Management Bot"

    def __init__(self, **kwargs):
        self.config = AppConfig(**kwargs)
        self._db: Optional[AsyncIOMotorDatabase] = None

    @property
    def db(self) -> AsyncIOMotorDatabase:
        if self._db is None:
            self._db = get_database()
        return self._db

    async def add_user(self, user: User) -> bool:
        """
        Add a new user or update existing one.
        Returns True if user was added/updated successfully.
        """
        try:
            existing = await self.get_user(user.user_id)
            if existing:
                if not existing.merge_with(user):
                    raise ValueError("Conflict in user data during merge")
                user = existing

            await self.db[self.config.users_collection].update_one(
                {"user_id": user.user_id},
                {"$set": user.model_dump()},
                upsert=True
            )
            return True
        except Exception as e:
            # Log the error
            return False

    async def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        data = await self.db[self.config.users_collection].find_one({"user_id": user_id})
        return User(**data) if data else None

    async def update_last_active(self, user_id: int) -> None:
        """Update user's last active timestamp."""
        await self.db[self.config.users_collection].update_one(
            {"user_id": user_id},
            {"$set": {"last_active": datetime.now(timezone.utc)}}
        )
