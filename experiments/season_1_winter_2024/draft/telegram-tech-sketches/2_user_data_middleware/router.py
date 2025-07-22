"""Router module for handling telegram bot commands."""
from _app import App
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from botspot.components.bot_commands_menu import add_command
from botspot.utils import send_safe
from loguru import logger
from middleware import UserTrackingMiddleware

router = Router()
app = App()

# Add middleware to track users
router.message.middleware(UserTrackingMiddleware(app))


@add_command("start", "Start the bot")
@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    """Register new user and send welcome message."""
    user = await app.get_user(message.from_user.id)
    await send_safe(
        message.chat.id,
        f"Hello {user.full_name}! Welcome to {app.name}!\n"
        f"Your timezone is set to: {user.timezone}"
    )


@add_command("help", "Show this help message")
@router.message(Command("help"))
async def help_handler(message: Message) -> None:
    """Show help message."""
    await send_safe(
        message.chat.id,
        f"This is {app.name}.\n\n"
        f"Commands:\n"
        f"/start - Register and get welcome message\n"
        f"/me - Show your profile info\n"
        f"/help - Show this help message"
    )


@add_command("me", "Show your profile info")
@router.message(Command("me"))
async def profile_handler(message: Message) -> None:
    """Show user profile information."""
    user = await app.get_user(message.from_user.id)
    if not user:
        await send_safe(message.chat.id, "Error: User not found. Please use /start first.")
        return

    await send_safe(
        message.chat.id,
        f"Your profile:\n"
        f"ID: {user.user_id}\n"
        f"Name: {user.full_name}\n"
        f"Username: @{user.username or 'not set'}\n"
        f"Timezone: {user.timezone}\n"
        f"Registered: {user.created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
        f"Last active: {user.last_active.strftime('%Y-%m-%d %H:%M:%S UTC')}"
    )
