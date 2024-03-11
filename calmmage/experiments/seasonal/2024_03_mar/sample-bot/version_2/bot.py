from aiogram import Dispatcher
from bot_lib import (
    BotConfig,
    setup_dispatcher,
)
from bot_lib.demo import create_bot, run_bot
from dotenv import load_dotenv

from lib import MyPlugin, MyApp, MyHandler
from version_2.utils import set_commands_on_startup

plugins = [MyPlugin]
app = MyApp(plugins=plugins)
bot_config = BotConfig(app=app)

# set up dispatcher
dp = Dispatcher()

my_handler = MyHandler()
handlers = [my_handler]
setup_dispatcher(dp, bot_config, extra_handlers=handlers)

load_dotenv()
bot = create_bot()

# let's set the bot to update all commands on startup
# set_commands_on_startup(dp, bot_config, extra_handlers=handlers)

if __name__ == "__main__":
    run_bot(dp, bot)
