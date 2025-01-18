from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from botspot.components.bot_commands_menu import add_command
from botspot.utils import send_safe

from _app import App

router = Router()
app = App()


@add_command("start", "Start the bot")
@router.message(CommandStart())
async def start_handler(message: Message):
    await send_safe(message.chat.id, f"Hello! Welcome to {app.name}!")


@add_command("help", "Show this help message")
@router.message(Command("help"))
async def help_handler(message: Message):
    """Basic help command handler"""
    await send_safe(message.chat.id, f"This is {app.name}. Use /start to begin.")
