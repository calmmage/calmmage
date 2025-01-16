from pathlib import Path
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

from botspot.core.bot_manager import BotManager
from router import router, app
from calmlib.utils import setup_logger

# Load environment variables
load_dotenv(Path(__file__).parent / ".env")

# Initialize bot and dispatcher
dp = Dispatcher()
dp.include_router(router)

bot = Bot(token=app.config.telegram_bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))



def main():
    # Setup bot manager with basic components
    bm = BotManager(bot=bot)
    bm.setup_dispatcher(dp)
    
    # Start polling
    dp.run_polling(bot)


if __name__ == "__main__":
    main()

