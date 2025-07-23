from aiogram.fsm.context import FSMContext

from _app import App
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from botspot import commands_menu
from botspot.utils import send_safe
from botspot.components.features.user_interactions import ask_user_raw

router = Router()
app = App()


@commands_menu.add_command("start", "Start the bot")
@router.message(CommandStart())
async def start_handler(message: Message):
    await send_safe(message.chat.id, f"Hello! Welcome to {app.name}!")
    await send_safe(
        message.chat.id,
        "This bot demonstrates the Telethon message retrieval functionality.\n\n"
        "First, authenticate with Telethon using /setup_telethon\n"
        "Then use the available commands to interact with Telegram chats."
    )


@commands_menu.add_command("help", "Show this help message")
@router.message(Command("help"))
async def help_handler(message: Message):
    """Basic help command handler"""
    help_text = (
        f"This is {app.name}. It demonstrates message retrieval using Telethon.\n\n"
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/setup_telethon - Authenticate with Telegram API\n"
        "/check_telethon - Check if you're authenticated\n"
        "/get_hardcoded_chat - Get messages from a hardcoded chat\n"
        "/list_chats - Show your recent chats\n"
        "/forward_message - Get message by forwarding and extract its data\n"
    )
    await send_safe(message.chat.id, help_text)


@commands_menu.add_command("get_hardcoded_chat", "Get messages from a hardcoded chat")
@router.message(Command("get_hardcoded_chat"))
async def get_hardcoded_chat_handler(message: Message, state: FSMContext):
    """Get messages from a hardcoded chat with chat name"""
    hardcoded_chat_id = -1001568072211

    from botspot.utils import get_telethon_client

    tc = await get_telethon_client(user_id=message.from_user.id, state=state)
    
    if not tc:
        await send_safe(message.chat.id, "You need to authenticate first. Use /setup_telethon")
        return
        
    try:
        # First get chat entity to show chat name
        chat_entity = await tc.get_entity(hardcoded_chat_id)
        chat_name = getattr(chat_entity, 'title', None) or getattr(chat_entity, 'username', None) or str(hardcoded_chat_id)
        
        # Then get messages
        messages = await tc.get_messages(hardcoded_chat_id, limit=10)
        
        summary = f"Retrieved {len(messages)} messages from chat '{chat_name}'\n\n"
        for i, msg in enumerate(messages, 1):
            content = msg.message if msg.message else "[Media content]"
            if len(content) > 50:
                content = content[:47] + "..."
            summary += f"{i}. ID: {msg.id} | {content}\n"
            
        await send_safe(message.chat.id, summary)
        
    except Exception as e:
        await send_safe(message.chat.id, f"Error: {e}")


@commands_menu.add_command("list_chats", "Show your recent chats")
@router.message(Command("list_chats"))
async def list_chats_handler(message: Message, state: FSMContext):
    """Show list of recent chats"""
    from botspot.utils import get_telethon_client
    
    tc = await get_telethon_client(user_id=message.from_user.id, state=state)
    
    if not tc:
        await send_safe(message.chat.id, "You need to authenticate first. Use /setup_telethon")
        return
        
    try:
        dialogs = await tc.get_dialogs(limit=10)
        
        summary = "Your recent chats:\n\n"
        for i, dialog in enumerate(dialogs, 1):
            chat_name = dialog.name if dialog.name else f"Chat {dialog.id}"
            summary += f"{i}. {chat_name} (ID: {dialog.id})\n"
            
        await send_safe(message.chat.id, summary)
        
    except Exception as e:
        await send_safe(message.chat.id, f"Error: {e}")


@commands_menu.add_command("forward_message", "Extract info from a forwarded message")
@router.message(Command("forward_message"))
async def forward_message_handler(message: Message, state: FSMContext):
    """Ask user to forward a message and extract its data"""
    # Ask the user to forward a message
    forwarded_message = await ask_user_raw(
        chat_id=message.chat.id,
        question="Please forward a message from any chat. I'll extract its details.",
        state=state,
        timeout=120.0
    )
    
    if not forwarded_message:
        await send_safe(message.chat.id, "No message received or operation timed out.")
        return
    
    # Check if the message is a forwarded message
    if not forwarded_message.forward_from and not forwarded_message.forward_from_chat:
        await send_safe(message.chat.id, "This doesn't appear to be a forwarded message. Please use /forward_message again and forward a message from another chat.")
        return
    
    # Extract information from the forwarded message
    if forwarded_message.forward_from:
        # Message forwarded from a user
        from_user = forwarded_message.forward_from
        origin_info = f"User: {from_user.first_name} {from_user.last_name or ''} (@{from_user.username or 'no username'})\nID: {from_user.id}"
    elif forwarded_message.forward_from_chat:
        # Message forwarded from a channel or group
        from_chat = forwarded_message.forward_from_chat
        origin_info = f"Chat: {from_chat.title or from_chat.username or 'Unknown'}\nType: {from_chat.type}\nID: {from_chat.id}"
        if forwarded_message.forward_from_message_id:
            origin_info += f"\nOriginal Message ID: {forwarded_message.forward_from_message_id}"
    else:
        origin_info = "Unknown origin"
    
    # Display the message information
    message_content = forwarded_message.text or forwarded_message.caption or "[No text content]"
    if len(message_content) > 200:
        message_content = message_content[:197] + "..."
    
    response = f"📨 Forwarded Message Info\n\n"
    response += f"From: {origin_info}\n\n"
    response += f"Content: {message_content}\n\n"
    response += f"Date: {forwarded_message.forward_date.strftime('%Y-%m-%d %H:%M:%S') if forwarded_message.forward_date else 'Unknown'}"
    
    await send_safe(message.chat.id, response)