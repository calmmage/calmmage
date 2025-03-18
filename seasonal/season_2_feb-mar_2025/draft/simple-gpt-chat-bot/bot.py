from pathlib import Path
import argparse
import sys

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from botspot.components.new.llm_provider import LLMProviderSettings
from botspot.core.bot_manager import BotManager
from botspot.core.botspot_settings import BotspotSettings
from calmlib.utils import setup_logger
from dotenv import load_dotenv
from loguru import logger
# from routers.minimal_showcase import router

# Load environment variables
load_dotenv(Path(__file__).parent / ".env")

# Import app from _app.py for settings
from _app import App

# Create app instance
app = App()


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run GPT Chat Bot with different routers')
    parser.add_argument(
        '--router', 
        choices=['minimal', 'advanced'], 
        default='minimal',
        help='Router to use: minimal (default) or advanced with scenarios'
    )
    args = parser.parse_args()
    
    # Setup logger
    setup_logger(logger)
    
    # Import the selected router
    if args.router == 'minimal':
        logger.info("Using minimal showcase router")
        from routers.minimal_showcase import router
        bot_name = "Minimal GPT Chat Bot"
    else:
        logger.info("Using advanced scenarios router")
        from routers.advanced_scenarios import router
        bot_name = "Advanced GPT Chat Bot with Scenarios"
    
    # Initialize dispatcher
    dp = Dispatcher()
    dp.include_router(router)
    
    # Initialize bot
    bot = Bot(
        token=app.config.telegram_bot_token, 
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
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
    
    logger.info(f"Starting {bot_name}")
    
    # Setup bot manager with components
    bm = BotManager(bot=bot, **settings.model_dump())
    bm.setup_dispatcher(dp)

    # Start polling
    dp.run_polling(bot)


if __name__ == "__main__":
    main()
