from aiogram import types
from bot_lib import BotConfig, HandlerDisplayMode

# todo use calmmage logger from calmlib
from loguru import logger


def set_commands_on_startup(dispatcher, bot_config: BotConfig, extra_handlers=None):
    # step 1 - build commands list
    commands = []

    handlers = [handler() for handler in bot_config.handlers]
    if extra_handlers:
        handlers += extra_handlers

    for handler in handlers:
        if handler.display_mode != HandlerDisplayMode.FULL:
            continue
        for command, aliases in handler.commands.items():
            if isinstance(aliases, str):
                aliases = [aliases]
            for alias in aliases:
                commands.append((alias, getattr(handler, command).__doc__))
            # commands.append((command, aliases))
    # here's an example:
    NO_COMMAND_DESCRIPTION = "No description"

    # todo: make this less ugly
    async def _set_aiogram_bot_commands(bot):
        bot_commands = [
            types.BotCommand(command=c, description=d or NO_COMMAND_DESCRIPTION)
            for c, d in commands
        ]
        await bot.set_my_commands(bot_commands)

    dispatcher.startup.register(_set_aiogram_bot_commands)
