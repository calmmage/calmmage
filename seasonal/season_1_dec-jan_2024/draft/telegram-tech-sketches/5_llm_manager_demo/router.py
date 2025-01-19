from aiogram import Router, F
from aiogram import html
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from _app import App
from botspot.components.bot_commands_menu import add_command
from botspot.utils import send_safe
from calmlib.utils.gpt_utils import aquery_llm_text

router = Router()
app = App()

# Maximum message length for Telegram
MAX_MESSAGE_LENGTH = 4096


@add_command("start", "Start the bot")
@router.message(CommandStart())
async def start_handler(message: Message):
    """Start command handler"""
    await send_safe(
        message.chat.id,
        f"Hello <b> {message.from_user.full_name} </b>! "
        f"👋 Welcome to {app.name}!\n\n"
        "I'm an AI assistant " + html.quote("powered by GPT.") + " Just send me a message and I'll respond.\n"
                                                                 "Use " + html.bold(
            "/help") + " to see available commands."
    )


@add_command("help", "Show this help message")
@router.message(Command("help"))
async def help_handler(message: Message):
    """Help command handler"""
    await send_safe(
        message.chat.id,
        "🤖 I'm here to chat! Just send me any message and I'll respond.\n\n"
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message"
    )


@router.message(F.text)
async def chat_handler(message: Message):
    """Handle chat messages"""
    user_message = message.text.strip()

    # Skip empty messages
    if not user_message:
        return

    # Send typing action
    # await message.answer_chat_action("typing")

    # Get AI response
    response = await aquery_llm_text(
        prompt=user_message,
        system=app.config.system_message,
        max_tokens=MAX_MESSAGE_LENGTH // 2,  # Leave room for UTF-8 chars
    )

    await send_safe(message.chat.id, response)
