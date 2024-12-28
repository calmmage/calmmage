from os import getenv

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from loguru import logger

# Load environment variables
load_dotenv()

from botspot.core.bot_manager import BotManager

# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv("TELEGRAM_BOT_TOKEN")


async def main() -> None:
    # Initialize Bot instance with default bot properties
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    # Initialize BotManager with required components
    bm = BotManager(
        bot=bot,
        # Enable ask_user component as it's required for telethon_manager
        ask_user={"enabled": True},
        # Enable bot_commands_menu to register commands
        bot_commands_menu={"enabled": True},
    )

    # Setup dispatcher with components
    bm.setup_dispatcher(dp)

    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Error during polling: {e}")


if __name__ == "__main__":
    asyncio.run(main())
