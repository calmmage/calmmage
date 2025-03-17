from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from botspot.core.bot_manager import BotManager
from calmlib.utils import setup_logger
from dotenv import load_dotenv
from loguru import logger

# Load environment variables
load_dotenv(Path(__file__).parent / ".env")

from router import app, router

# Initialize bot and dispatcher
dp = Dispatcher()
dp.include_router(router)

bot = Bot(
    token=app.config.telegram_bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)


def main():
    setup_logger(logger)
    # Setup bot manager with telethon components
    bm = BotManager(
        bot=bot,
        # Enable ask_user component as it's required for telethon_manager and our forward_message handler
        ask_user={"enabled": True},
        # Enable telethon_manager to handle Telegram user authentication
        telethon_manager={
            "enabled": True,
            # Ensure to set API_ID and API_HASH in your .env file
        },
    )
    bm.setup_dispatcher(dp)

    # Start polling
    dp.run_polling(bot)


if __name__ == "__main__":
    main()