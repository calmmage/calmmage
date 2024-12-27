import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from loguru import logger

from botspot.components.bot_commands_menu import add_command
from botspot.core.bot_manager import BotManager
from botspot.components.ask_user_handler import ask_user, ask_user_choice

load_dotenv()
# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv("TELEGRAM_BOT_TOKEN")

dp = Dispatcher()


@add_command("start")
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Send a welcome message when the command /start is issued"""
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


# @add_command("error")
# @dp.message(Command("error"))
# async def command_error_handler(message: Message) -> None:
#     """Raise an exception to test error handling"""
#     raise Exception("Something Went Wrong")


# @dp.message()
# async def echo_handler(message: Message) -> None:
#     try:
#         # Send a copy of the received message
#         await message.send_copy(chat_id=message.chat.id)
#     except TypeError:
#         # But not all the types is supported to be copied so need to handle it
#         await message.answer("Nice try!")


@add_command("chat_id", "Get current chat ID")
@dp.message(Command("chat_id"))
async def command_chat_id_handler(message: Message) -> None:
    """Send the current chat ID when the command /chat_id is issued"""
    await message.answer(f"Current chat ID: {html.code(str(message.chat.id))}")


@add_command("user_id", "Get user ID (yours or another user's)")
@dp.message(Command("user_id"))
async def command_user_id_handler(message: Message, state: FSMContext) -> None:
    """Handle the /user_id command"""
    logger.debug(f"Starting user_id command handler with message: {message}")
    
    # Check if username was provided directly with command
    command_parts = message.text.split()
    if len(command_parts) > 1 and command_parts[1].startswith('@'):
        username = command_parts[1]
        logger.debug(f"Username provided in command: {username}")
        await message.answer(
            "Sorry, getting user ID by username is not supported by Telegram API.\n"
            "Please either:\n"
            "• Forward a message from that user, or\n"
            "• Ask them to use /user_id command"
        )
        return

    choices = ["Get my own ID", "Provide user tag", "Forward a message from user"]
    logger.debug("Asking user to choose action")
    response = await ask_user_choice(
        message.chat.id,
        "Whose ID would you like to get?",
        choices,
        state,
        timeout=60.0
    )
    
    logger.debug(f"User chose: {response}")
    if not response:
        await message.answer("Operation cancelled.")
        return
        
    if response == "Get my own ID":
        user_id = message.from_user.id
        username = message.from_user.username
        logger.debug(f"Getting own ID: {user_id}, username: {username}")
        await message.answer(
            f"Your user ID: {html.code(str(user_id))}\n"
            f"Your username: {html.code('@' + username if username else 'not set')}"
        )
    elif response == "Provide user tag":
        username_msg = await ask_user(
            message.chat.id,
            "Please provide the user's @username:",
            state,
            timeout=60.0
        )
        logger.debug(f"User provided message: {username_msg}")
        
        if not username_msg or not isinstance(username_msg, Message) or not username_msg.text or not username_msg.text.startswith('@'):
            await message.answer("No valid username provided. Operation cancelled.")
            return
            
        username = username_msg.text
        logger.debug(f"User provided username: {username}")
        await message.answer(
            "Sorry, getting user ID by username is not supported by Telegram API.\n"
            "Please either:\n"
            "• Forward a message from that user, or\n"
            "• Ask them to use /user_id command"
        )
    else:  # Forward a message from user
        logger.debug("Waiting for forwarded message")
        forward_msg = await ask_user(
            message.chat.id,
            "Please forward a message from the user whose ID you want to get.",
            state,
            timeout=60.0,
            return_raw=True
        )
        
        logger.debug(f"Received message: {forward_msg}")
        if not forward_msg:
            await message.answer("No message was forwarded or operation timed out.")
            return
            
        if not isinstance(forward_msg, Message) or not forward_msg.forward_from:
            logger.warning("Received message without forward_from field")
            await message.answer(
                "Sorry, I couldn't get the user information from this message.\n"
                "This can happen if:\n"
                "• The message wasn't forwarded\n"
                "• The user has privacy settings that hide their forwards\n\n"
                "Please try again with a different message or user."
            )
            return
            
        user = forward_msg.forward_from
        logger.debug(f"Successfully got user info: {user}")
        await message.answer(
            f"User ID for {html.bold(user.full_name)}: {html.code(str(user.id))}\n"
            f"Username: {html.code('@' + user.username if user.username else 'not set')}"
        )


async def main() -> None:
    # Configure logging
    logger.remove()  # Remove default handler
    logger.add(sys.stdout, level="DEBUG")
    logger.debug("Starting bot...")
    
    # Initialize Bot instance with default bot properties
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    bm = BotManager(bot=bot)
    bm.setup_dispatcher(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
