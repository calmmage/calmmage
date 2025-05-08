from _app import App
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from botspot import commands_menu
from botspot.utils import send_safe

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

    from botspot.llm_provider import aquery_llm_text

    response = await aquery_llm_text(
        prompt = input_text,
        user = message.from_user.id,
        attachments = attachments,
    )

    await send_safe(message.chat.id, response)



