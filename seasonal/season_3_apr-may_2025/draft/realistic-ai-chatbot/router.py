from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from botspot import commands_menu
from botspot.utils import send_safe

from app import App, supported_models

router = Router()


@commands_menu.botspot_command("start", "Start the bot")
@router.message(CommandStart())
async def start_handler(message: Message, app: App):
    await send_safe(message.chat.id, f"Hello! Welcome to {app.name}!")


@commands_menu.botspot_command("help", "Show this help message")
@router.message(Command("help"))
async def help_handler(message: Message, app: App):
    """Basic help command handler"""
    await send_safe(message.chat.id, f"This is {app.name}. Use /start to begin.")


# @commands_menu.botspot_command("help", "Show this help message")
# @router.message(Command("help"))
@router.message()
async def chat_handler(message: Message, app: App):
    """Basic help command handler"""
    # await send_safe(message.chat.id, f"This is {app.name}. Use /start to begin.")

    input_text = message.text or message.caption
    assert input_text is not None
    assert message.from_user is not None

    # todo: support captions and media
    from botspot.utils.unsorted import get_message_attachments

    attachments = get_message_attachments(message)

    response = await app.generate_response(
        input_text, message.from_user.id, attachments
    )
    messages = app.split_message(response)
    await app.send_messages(messages, message)


@commands_menu.botspot_command("set_model", "Set the model")
@router.message(Command("set_model"))
async def set_model_handler(message: Message, app: App, state: FSMContext):
    """Basic help command handler"""

    from botspot.user_interactions import ask_user_choice

    choices = supported_models
    response = await ask_user_choice(
        chat_id=message.chat.id,
        question="Select a model",
        choices=choices,
        state=state,
    )
    if response is None:
        await send_safe(message.chat.id, "No model selected")
        return
    app.model = response
    await send_safe(message.chat.id, f"Model set to {response}")


@commands_menu.botspot_command("set_splitter_mode", "Set the splitter mode")
@router.message(Command("set_splitter_mode"))
async def set_splitter_mode_handler(message: Message, app: App, state: FSMContext):
    """Basic help command handler"""

    from botspot.user_interactions import ask_user_choice

    from app import SplitterMode

    choices = [mode.value for mode in SplitterMode]
    response = await ask_user_choice(
        chat_id=message.chat.id,
        question="Select a splitter mode",
        choices=choices,
        state=state,
    )
    if response is None:
        await send_safe(message.chat.id, "No splitter mode selected")
        return
    app.splitter_mode = response
    await send_safe(message.chat.id, f"Splitter mode set to {response}")


@commands_menu.botspot_command("set_delay_mode", "Set the delay mode")
@router.message(Command("set_delay_mode"))
async def set_delay_mode_handler(message: Message, app: App, state: FSMContext):
    """Basic help command handler"""

    from botspot.user_interactions import ask_user_choice

    from app import DelayMode

    choices = [mode.value for mode in DelayMode]
    response = await ask_user_choice(
        chat_id=message.chat.id,
        question="Select a delay mode",
        choices=choices,
        state=state,
    )
    if response is None:
        await send_safe(message.chat.id, "No delay mode selected")
        return
    app.delay_mode = response
    await send_safe(message.chat.id, f"Delay mode set to {response}")
