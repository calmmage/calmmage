from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from botspot.utils.deps_getters import get_user_manager
from typing import Any, Awaitable, Callable, Dict

from ._component import User


class UserTrackingMiddleware(BaseMiddleware):
    """Middleware to track users and ensure they're registered."""

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        # Only process messages with user information
        if isinstance(event, Message) and event.from_user:
            user_manager = get_user_manager()
            user = User(
                user_id=event.from_user.id,
                username=event.from_user.username,
                first_name=event.from_user.first_name,
                last_name=event.from_user.last_name
            )
            await user_manager.add_user(user)
            await user_manager.update_last_active(user.user_id)

        return await handler(event, data)
