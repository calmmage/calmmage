from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from botspot.core.bot_manager import BotManager
from calmlib.utils.logging_utils import setup_logger, LogMode
from loguru import logger
from router import router

from app import App, PosterBotUser

# Initialize bot and dispatcher
dp = Dispatcher()
dp.include_router(router)


async def on_startup(dispatcher):
    app = dispatcher["app"]
    await app.schedule_posts_on_startup()


def main():
    setup_logger(logger, mode=LogMode.CUSTOM)

    app = App()

    bot = Bot(
        token=app.config.telegram_bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    # Setup bot manager with basic components
    bm = BotManager(bot=bot, user_class=PosterBotUser)
    bm.setup_dispatcher(dp)

    dp["app"] = app
    dp.startup.register(on_startup)

    # Start polling
    dp.run_polling(bot)


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    main()
