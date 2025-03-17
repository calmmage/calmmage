from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from botspot.components.new.llm_provider import LLMProviderSettings
from botspot.core.bot_manager import BotManager
from botspot.core.botspot_settings import BotspotSettings
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
    
    # Configure settings for the bot with LLM Provider enabled
    settings = BotspotSettings(
        # Enable the LLM Provider component
        llm_provider=LLMProviderSettings(
            enabled=True,
            default_model="gpt-3.5",  # Using GPT-3.5 Turbo as default
            default_temperature=0.7,
            default_max_tokens=1000,
        ),
    )
    
    # Setup bot manager with components
    bm = BotManager(bot=bot, **settings.model_dump())
    bm.setup_dispatcher(dp)

    # Start polling
    dp.run_polling(bot)


if __name__ == "__main__":
    main()
