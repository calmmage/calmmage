from pathlib import Path

from aiogram import Bot, Dispatcher, Router
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

# Import app from _app.py for settings
from _app import App

# Import both routers
from routers.minimal_showcase import router as minimal_router
from routers.advanced_scenarios import router as advanced_router
from routers.llm_utils_test import router as llm_utils_router

# Create app instance
app = App()


def main():
    # Setup logger
    setup_logger(logger)
    
    logger.info("Starting GPT Chat Bot with both minimal and advanced routers")
    
    # Initialize dispatcher
    dp = Dispatcher()
    
    # Include both routers
    dp.include_router(llm_utils_router)
    dp.include_router(advanced_router)
    dp.include_router(minimal_router)
    
    # Initialize bot
    bot = Bot(
        token=app.config.telegram_bot_token, 
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    # Configure settings for the bot with LLM Provider enabled
    settings = BotspotSettings(
        # Enable the LLM Provider component
        # llm_provider=LLMProviderSettings(
        #     enabled=True,
        #     default_model="gpt-4o",  # Using GPT-3.5 Turbo as default
        #     default_temperature=0.7,
        #     default_max_tokens=1000,
        # ),
    )

    
    # Setup bot manager with components
    bm = BotManager(bot=bot, **settings.model_dump())
    bm.setup_dispatcher(dp)

    # Start polling
    dp.run_polling(bot)


if __name__ == "__main__":
    main()
