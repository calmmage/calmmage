from _app import App
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from botspot import commands_menu
from botspot.utils import send_safe

router = Router()


@commands_menu.botspot_command("start", "Start the bot")
@router.message(CommandStart())
async def start_handler(message: Message, app: App):
    await send_safe(message.chat.id, f"Hello! Welcome to {app.name}!")


@commands_menu.botspot_command("help", "Show this help message")
@router.message(Command("help"))
async def help_handler(message: Message, app: App):
    """Basic help command handler"""
    await send_safe(message.chat.id, f"This is {app.name}. Use /start to begin.")



@commands_menu.botspot_command("help", "Show this help message")
@router.message(Command("add"))
@router.message()
async def add_command_handler(message: Message, app: App):
    """Basic help command handler"""
    # await send_safe(message.chat.id, f"This is {app.name}. Use /start to begin.")
    # step 0: 
    # get text, strip command
    from botspot.utils import get_message_text, strip_command
    text = get_message_text(message)
    text = strip_command(text)
    
    
    # step 1: 

    # step 2: 



