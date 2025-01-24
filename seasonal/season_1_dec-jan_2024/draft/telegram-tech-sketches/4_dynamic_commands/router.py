from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from botspot.components.bot_commands_menu import (
    add_command, set_aiogram_bot_commands, commands as bot_commands,
    CommandInfo, Visibility
)
from botspot.components.ask_user_handler import ask_user
from botspot.utils import send_safe
import re

from _app import App

router = Router()
app = App()

# Store for dynamic commands - in memory for now
# Format: {"command_name": "command_text"}
dynamic_commands = {}


def is_valid_command_name(name: str) -> bool:
    """Validate command name - letters, numbers and underscores only"""
    return bool(re.match(r'^[a-zA-Z0-9_]+$', name))


@add_command("start", "Start the bot")
@router.message(CommandStart())
async def start_handler(message: Message):
    await send_safe(message.chat.id, f"Hello! Welcome to {app.name}!")


@add_command("help", "Show this help message")
@router.message(Command("help"))
async def help_handler(message: Message):
    """Basic help command handler"""
    commands_list = "\n".join([
        f"/{cmd} - {text}" for cmd, text in dynamic_commands.items()
    ])
    help_text = f"This is {app.name}. Use /start to begin.\n\n"
    help_text += "Dynamic Commands:\n" + commands_list if commands_list else "No dynamic commands yet."
    await send_safe(message.chat.id, help_text)


@add_command("new_command", "Create a new command")
@router.message(Command("new_command"))
async def new_command_handler(message: Message, state):
    """Handler for creating new commands"""
    # Parse command format: /new_command command_name\n text
    # todo: bad logic. Need to strip everything 
    parts = message.text.strip().split('\n', 1)
    command_parts = parts[0].strip().split(maxsplit=1)
    
    # Get command name from message if provided
    command_name = command_parts[1] if len(command_parts) > 1 else None
    command_text = parts[1] if len(parts) > 1 else None
    
    # If command name not provided, ask for it
    if not command_name:
        command_name = await ask_user(
            message.chat.id,
            "What should be the command name? (without /)\n"
            "Use only letters, numbers and underscores.",
            timeout=600,
            state=state
        )
        if not command_name:
            await send_safe(message.chat.id, "Command creation cancelled.")
            return
    
    # Validate command name
    if not is_valid_command_name(command_name):
        await send_safe(
            message.chat.id, 
            "Invalid command name. Use only letters, numbers and underscores."
        )
        return
        
    if command_name in dynamic_commands:
        await send_safe(message.chat.id, "This command already exists!")
        return
    
    # If text not provided, ask for it
    if not command_text:
        command_text = await ask_user(
            message.chat.id,
            "What should the command reply with?",
            timeout=600,
            state=state
        )
        if not command_text:
            await send_safe(message.chat.id, "Command creation cancelled.")
            return
    
    # Store the new command
    dynamic_commands[command_name] = command_text
    
    # Register command in bot_commands_menu
    description = command_text.split('\n')[0]  # Use first line as description
    bot_commands[command_name] = CommandInfo(description, visibility=Visibility.PUBLIC)
    
    # Update bot's command list
    await set_aiogram_bot_commands(message.bot)
    
    await send_safe(
        message.chat.id,
        f"Command /{command_name} created successfully!\n"
        f"It will reply with: {command_text}"
    )


@router.message()
async def handle_potential_command(message: Message):
    """Handle dynamic commands"""
    if not message.text or not message.text.startswith('/'):
        return
        
    command = message.text.split()[0][1:]  # Remove the '/' and get command name
    if command in dynamic_commands:
        await send_safe(message.chat.id, dynamic_commands[command])
