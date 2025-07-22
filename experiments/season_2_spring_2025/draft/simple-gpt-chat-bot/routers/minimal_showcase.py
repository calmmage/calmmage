"""
Minimal Showcase Router

This file demonstrates just how easy it is to create a GPT-powered chat bot
using Botspot's LLM Provider component. The entire implementation is just a few lines!
"""

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from botspot import commands_menu
from botspot.components.new import llm_provider
from botspot.utils import send_safe, send_typing_status
from loguru import logger

from _app import App

# Create router and app
router = Router()
app = App()


@commands_menu.add_command("start", "Start the bot")
@router.message(CommandStart())
async def start_handler(message: Message):
    await send_safe(
        message.chat.id,
        f"👋 Hello! Welcome to Minimal GPT Chat Bot!\n\n"
        f"This bot demonstrates how easy it is to create a GPT-powered bot using Botspot.\n\n"
        f"Just send me any message and I'll respond!"
    )


@commands_menu.add_command("help", "Show help")
@router.message(Command("help"))
async def help_handler(message: Message):
    await send_safe(
        message.chat.id,
        "This is a minimal GPT chat bot built with Botspot's LLM Provider.\n\n"
        "The entire implementation is just a handful of lines, showcasing the simplicity "
        "of building AI-powered bots with Botspot."
    )


# This is all you need to handle chat messages with GPT!
@router.message()
async def chat_handler(message: Message):
    """Process messages with GPT"""
    # Skip messages without text
    if not message.text:
        return
    
    # Show typing indicator
    await send_typing_status(message)
    
    # Query LLM with just one line
    response = await llm_provider.aquery_llm(
        prompt=message.text,
        user=str(message.from_user.id)
    )
    
    # Send the response
    await send_safe(message.chat.id, response)