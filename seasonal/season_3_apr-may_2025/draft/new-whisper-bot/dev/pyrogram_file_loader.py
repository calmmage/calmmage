import os
from pathlib import Path
from typing import Optional
from aiogram.types import Message as AiogramMessage
from functools import lru_cache
from pyrogram.types import Message as PyrogramMessage


@lru_cache
async def get_pyrogram_client(
    api_id: Optional[int] = None,
    api_hash: Optional[str] = None,
    bot_token: Optional[str] = None,
):
    # telegram bot token,
    # api_id
    # api_hash
    if api_id is None:
        from botspot import get_dependency_manager

        deps = get_dependency_manager()
        api_id = deps.botspot_settings.telethon_manager.api_id
    if api_hash is None:
        from botspot import get_dependency_manager

        deps = get_dependency_manager()
        assert deps.botspot_settings.telethon_manager.api_hash is not None
        api_hash = deps.botspot_settings.telethon_manager.api_hash.get_secret_value()
    if bot_token is None:
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

    import pyrogram

    assert api_id is not None
    assert api_hash is not None
    assert bot_token is not None

    pyrogram_client = pyrogram.Client(
        "telegram_downloader", api_id=api_id, api_hash=api_hash, bot_token=bot_token
    )
    await pyrogram_client.start()
    return pyrogram_client


def extract_file_name_from_pyrogram_message(msg: PyrogramMessage) -> str:
    # Try document, audio, video (these have file_name)
    for attr in ("document", "audio", "video"):
        media = getattr(msg, attr, None)
        if media and getattr(media, "file_name", None):
            return media.file_name
    # Voice, video_note, photo: generate default name
    if msg.voice:
        return f"{msg.voice.file_id}.ogg"
    if msg.video_note:
        return f"{msg.video_note.file_id}.mp4"
    if msg.photo:
        # Use the largest photo size
        photo = msg.photo[-1] if isinstance(msg.photo, list) else msg.photo
        return f"{photo.file_id}.jpg"
    # Fallback
    return "file.bin"


async def download_file_1(
    message: AiogramMessage,
    target_dir: Optional[Path] = None,
    file_name: Optional[str] = None,
):
    """
    Returns: path to a file on disk
    """
    message_id = message.message_id
    assert message.from_user is not None
    username = message.from_user.username

    return await download_file_2(message_id, username, target_dir, file_name)


async def download_file_2(
    message_id,
    username,
    target_dir: Optional[Path] = None,
    file_name: Optional[str] = None,
):
    pyrogram_client = await get_pyrogram_client()

    pyrogram_message = await pyrogram_client.get_messages(
        username, message_ids=message_id
    )
    assert not isinstance(pyrogram_message, list)

    if target_dir is None:
        target_dir = Path(".")

    # todo: figure out the file name - get from attachment or smth?
    if file_name is None:
        file_name = extract_file_name_from_pyrogram_message(pyrogram_message)

    file_path = target_dir / file_name
    result = await pyrogram_message.download(file_name=str(file_path))

    return file_path


if __name__ == "__main__":
    import asyncio

    asyncio.run(download_file_1(message))
