from aiogram import Dispatcher
from bot_lib import BotConfig, setup_dispatcher
from bot_lib.demo import create_bot, run_bot
from dotenv import load_dotenv

from lib import MyHandler, MyApp

bot_config = BotConfig(app=MyApp())

# set up dispatcher
dp = Dispatcher()

setup_dispatcher(dp, bot_config, extra_handlers=[MyHandler()])

load_dotenv()
bot = create_bot()

if __name__ == "__main__":
    run_bot(dp, bot)
