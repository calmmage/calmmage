from _app import App
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from models import User
from typing import Any, Awaitable, Callable, Dict


class UserTrackingMiddleware(BaseMiddleware):
    """Middleware to track users and ensure they're registered."""

    def __init__(self, app: App):
        self.app = app
        super().__init__()

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        # Only process messages with user information
        if isinstance(event, Message) and event.from_user:
            user = User(
                user_id=event.from_user.id,
                username=event.from_user.username,
                first_name=event.from_user.first_name,
                last_name=event.from_user.last_name
            )
            await self.app.add_user(user)
            await self.app.update_last_active(user.user_id)

        return await handler(event, data)
