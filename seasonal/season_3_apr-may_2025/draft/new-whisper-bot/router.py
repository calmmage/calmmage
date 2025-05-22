from app import App
from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from botspot import commands_menu
from botspot.utils import send_safe
from loguru import logger
from botspot.utils.unsorted import download_telegram_file, get_message_attachments

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


def get_file_info(attachment):
    """
    Extract file name and mime type from aiogram attachment (Audio, Voice, Video, Document).
    If file_name is missing (e.g. for voice), generate a default name with the correct extension.
    """
    file_name = getattr(attachment, "file_name", None)
    mime_type = getattr(attachment, "mime_type", None)
    logger.info(
        f"Extracting file info: file_name={file_name}, mime_type={mime_type}, type={type(attachment)}"
    )
    # Handle voice messages (no file_name)
    if file_name is None:
        if hasattr(attachment, "mime_type") and attachment.mime_type == "audio/ogg":
            file_name = "voice_message.ogg"
        elif hasattr(attachment, "mime_type") and attachment.mime_type:
            ext = attachment.mime_type.split("/")[-1]
            file_name = f"file.{ext}"
        else:
            file_name = "file.bin"
    logger.info(f"Final file_name: {file_name}, mime_type: {mime_type}")
    return file_name, mime_type


@router.message(F.audio | F.voice | F.video | F.document | F.video_note)
async def media_downloader_handler(message: Message, app: App):
    logger.info(
        f"media_downloader_handler: received message {message.message_id} from chat {message.chat.id}"
    )

    attachments = get_message_attachments(message)
    logger.info(f"Extracted attachments: {attachments}")
    if not attachments:
        logger.warning("No attachments found in message!")
        await send_safe(message.chat.id, "No media found in your message.")
        return
    if len(attachments) > 1:
        logger.warning(f"More than one attachment found: {attachments}")
    attachment = attachments[0]
    logger.info(f"Selected attachment: {attachment}")
    file_bytes = await download_telegram_file(attachment)
    logger.info(f"Downloaded file bytes: {file_bytes}")
    file_name, mime_type = get_file_info(attachment)
    logger.info(f"Downloaded file: {file_name}, mime_type: {mime_type}")
    # Example: save to disk (uncomment to use)
    # save_path = Path("downloads") / file_name
    # with open(save_path, "wb") as f:
    #     f.write(file_bytes.read())
    await send_safe(message.chat.id, f"Downloaded file: {file_name}, type: {mime_type}")
