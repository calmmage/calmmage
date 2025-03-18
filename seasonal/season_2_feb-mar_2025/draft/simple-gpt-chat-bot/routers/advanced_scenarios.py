"""
Advanced Scenarios Router

This file demonstrates more advanced features built on top of Botspot's LLM Provider:
- Multiple AI personas (scenarios)
- Custom persona creation
- Per-user state management
"""

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from botspot import commands_menu
from botspot.components.new import llm_provider
from botspot.utils import send_safe, send_typing_status
from loguru import logger

from _app import App

# Create router and app
router = Router()
app = App()


@commands_menu.add_command("start", "Start the bot")
@router.message(CommandStart())
async def start_handler(message: Message):
    await send_safe(
        message.chat.id,
        f"👋 Hello! Welcome to Advanced GPT Chat Bot with Scenarios!\n\n"
        f"This bot demonstrates how to create multiple AI personas using Botspot.\n\n"
        f"Try /scenarios to see available AI personas, or just send a message to chat."
    )
    
    # Initialize user state with default scenario
    user_id = message.from_user.id
    state = app.get_user_state(user_id)
    state["active_scenario"] = "default"
    state["custom_system_message"] = None


@commands_menu.add_command("help", "Show help")
@router.message(Command("help"))
async def help_handler(message: Message):
    await send_safe(
        message.chat.id,
        "This is an advanced GPT chat bot with scenarios built with Botspot.\n\n"
        "Commands:\n"
        "/start - Restart the bot\n"
        "/help - Show this help message\n"
        "/scenarios - View available AI personas\n"
        "/custom [prompt] - Create a custom AI persona"
    )


@commands_menu.add_command("scenarios", "View available AI personas")
@router.message(Command("scenarios"))
async def scenarios_handler(message: Message):
    """Show available scenarios and how to select them"""
    scenarios_list = []
    
    for key, scenario in app.get_available_scenarios().items():
        scenarios_list.append(f"• {scenario['name']} - {scenario['description']}\n  Select with: /scenario_{key}")
    
    await send_safe(
        message.chat.id,
        f"🎭 Available AI Personas\n\n"
        f"{chr(10).join(scenarios_list)}\n\n"
        f"You can also create a custom persona with:\n"
        f"/custom [your system prompt]"
    )


@router.message(Command(commands=["scenario_default", "scenario_creative", "scenario_expert", 
                                  "scenario_philosopher", "scenario_coach"]))
async def set_scenario_handler(message: Message):
    """Set the active scenario for the user"""
    command = message.text.split()[0][1:]  # Remove the / and get command name
    scenario_key = command.replace("scenario_", "")
    
    # Update user state
    state = app.get_user_state(message.from_user.id)
    state["active_scenario"] = scenario_key
    state["custom_system_message"] = None  # Clear any custom message
    
    # Get the selected scenario
    scenario = app.scenarios.get(scenario_key)
    
    await send_safe(
        message.chat.id,
        f"🎭 Switched to {scenario['name']} persona\n\n"
        f"{scenario['description']}\n\n"
        f"Send a message to start chatting!"
    )


@router.message(Command("custom"))
async def custom_scenario_handler(message: Message):
    """Set a custom system message"""
    # Get the custom prompt (everything after /custom )
    if len(message.text.split(maxsplit=1)) < 2:
        await send_safe(
            message.chat.id,
            "⚠️ Please provide a system prompt after /custom\n\n"
            "Example: /custom You are a pirate that speaks in pirate dialect. Yarr!"
        )
        return
        
    custom_prompt = message.text.split(maxsplit=1)[1].strip()
    
    # Update user state
    state = app.get_user_state(message.from_user.id)
    state["custom_system_message"] = custom_prompt
    
    await send_safe(
        message.chat.id,
        f"✨ Custom persona set!\n\n"
        f"System prompt: {custom_prompt}\n\n"
        f"Send a message to start chatting!"
    )


@router.message()
async def advanced_chat_handler(message: Message):
    """Process messages with scenario support"""
    # Skip messages without text
    if not message.text:
        return
    
    # Get the user prompt and state
    prompt = message.text
    user_id = message.from_user.id
    state = app.get_user_state(user_id)
    
    # Let the user know we're processing
    await send_typing_status(message)
    
    # Get the current system message based on active scenario
    system_message = app.get_system_message(user_id)
    
    # Pass message to LLM with appropriate system message
    response = await llm_provider.aquery_llm(
        prompt=prompt,
        system_message=system_message,
        user=str(user_id)
    )
    
    # Send the response
    await send_safe(message.chat.id, response)