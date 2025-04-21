from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from botspot.core.bot_manager import BotManager
from calmlib.utils import setup_logger
from loguru import logger
from router import router

# Initialize bot and dispatcher
dp = Dispatcher()
dp.include_router(router)

bot = Bot(
    token=app.config.telegram_bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)


def main():
    setup_logger(logger)
    # Setup bot manager with basic components
    bm = BotManager(bot=bot)
    bm.setup_dispatcher(dp)

    app = App()
    dp["app"] = app

    # Start polling
    dp.run_polling(bot)


if __name__ == "__main__":
    main()
