from aiogram.fsm.context import FSMContext
from app import App
from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from botspot import commands_menu
from botspot.utils import send_safe
from loguru import logger
from botspot.utils.unsorted import get_message_attachments
from pathlib import Path

router = Router()

SAMPLE_DATA_DIR = Path("./sample_data")
SAMPLE_DATA_DIR.mkdir(exist_ok=True)


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


def convert_video_to_audio(video_path: Path) -> Path:
    """Convert video file to mp3 using ffmpeg, in-place, minimal memory usage."""
    import subprocess

    audio_path = video_path.with_suffix(".mp3")
    logger.info(f"Converting {video_path} to {audio_path} using ffmpeg...")
    result = subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(video_path),
            "-vn",
            "-acodec",
            "libmp3lame",
            str(audio_path),
        ],
        capture_output=True,
    )
    if result.returncode != 0:
        logger.error(f"ffmpeg failed: {result.stderr.decode()}")
        raise RuntimeError(f"ffmpeg failed: {result.stderr.decode()}")
    logger.info(f"Audio saved to {audio_path}")
    return audio_path


@router.message(F.audio | F.voice | F.video | F.document | F.video_note)
async def media_downloader_handler(message: Message, app: App, state: FSMContext):
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

    # from botspot.utils.deps_getters import get_telethon_client

    # from telethon import TelegramClient
    # telethon_bot_client = TelegramClient(
    #     api_id=,
    #     api_hash=,
    #     token=
    # )

    # it seems... I will have to use pyrogram?! What the fuck...

    # telethon_client = await get_telethon_client(user_id=message.from_user.id, state=state)
    # telethon_message = await telethon_client.get_messages(message.bot.id, ids=message.message_id)
    #
    # logger.info(f"telethon_message: {telethon_message}")
    #
    # file_bytes = await download_telegram_file(attachment, message=message, user=message.from_user, state=state)
    file_name, mime_type = get_file_info(attachment)
    # logger.info(f"Downloaded file: {file_name}, mime_type: {mime_type}")
    save_path = SAMPLE_DATA_DIR / file_name
    # with open(save_path, "wb") as f:
    #     f.write(file_bytes.read())
    # logger.info(f"File saved to {save_path}")
    # # If video, convert to audio
    # if mime_type and mime_type.startswith("video"):
    #     try:
    #         audio_path = convert_video_to_audio(save_path)
    #         logger.info(f"Video converted to audio: {audio_path}")
    #     except Exception as e:
    #         logger.error(f"Failed to convert video to audio: {e}")
    # await send_safe(message.chat.id, f"Downloaded file: {file_name}, type: {mime_type}, saved to {save_path}")

    # let's do a simple thing
    import pyrogram
    from botspot import get_dependency_manager

    deps = get_dependency_manager()
    pyrogram_client = pyrogram.Client(
        "telegram_downloader",
        api_id=deps.botspot_settings.telethon_manager.api_id,
        api_hash=deps.botspot_settings.telethon_manager.api_hash.get_secret_value(),
        bot_token=app.config.telegram_bot_token.get_secret_value(),
    )

    username = message.from_user.username
    message_id = message.message_id

    async def main(pyrogram_client):
        async with pyrogram_client:
            pyrogram_message = await pyrogram_client.get_messages(
                username, message_ids=message_id
            )
            result = await pyrogram_message.download(file_name=save_path)
        # print(target_path)

    pyrogram_client.run(main(pyrogram_client))

    # logger.info(f"pyrogram_message: {pyrogram_message}")
    logger.info(f"save_path: {save_path}")
