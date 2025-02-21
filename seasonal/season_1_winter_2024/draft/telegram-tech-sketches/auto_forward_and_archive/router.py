from _app import App
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

router = Router()
app = App()


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(f"Hello! Welcome to {app.name}!")


@router.message(Command("help"))
async def help_handler(message: Message):
    """Basic help command handler"""
    await message.answer(f"This is {app.name}. Use /start to begin.")
