from _app import App
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from botspot import commands_menu
from botspot.components.new import llm_provider
from botspot.utils import send_safe
from loguru import logger

router = Router()
app = App()


@commands_menu.add_command("start", "Start the bot")
@router.message(CommandStart())
async def start_handler(message: Message):
    await send_safe(
        message.chat.id,
        f"👋 Hello! Welcome to {app.name}!\n\n"
        f"Just send me a message and I'll respond using GPT.\n\n"
        f"Use /help to see available commands."
    )


@commands_menu.add_command("help", "Show this help message")
@router.message(Command("help"))
async def help_handler(message: Message):
    """Basic help command handler"""
    await send_safe(
        message.chat.id,
        f"This is {app.name}. I'm a simple chat bot powered by GPT.\n\n"
        f"Just send me any message and I'll respond!\n\n"
        f"Available commands:\n"
        f"/start - Restart the bot\n"
        f"/help - Show this help message\n"
        f"/test - Test all LLM provider features"
    )


@commands_menu.add_command("test", "Test LLM provider features")
@router.message(Command("test"))
async def test_handler(message: Message):
    """Test all LLM provider features"""
    
    await send_safe(message.chat.id, "🧪 Testing LLM Provider features...")
    
    # Test messages to try with different methods
    prompt = "What is the capital of France?"
    system_msg = "You are a helpful assistant. Be concise."
    
    results = []
    
    # Test each function with error handling
    try:
        # 1. Basic query_llm
        test_msg = await send_safe(message.chat.id, "1. Testing basic query_llm...")
        result = llm_provider.query_llm(prompt=prompt)
        await test_msg.edit_text(f"1. Basic query_llm: ✅\nResult: {result}")
        results.append("query_llm: ✅")
    except Exception as e:
        logger.error(f"Error testing query_llm: {e}")
        await test_msg.edit_text(f"1. Basic query_llm: ❌\nError: {str(e)}")
        results.append("query_llm: ❌")
    
    try:
        # 2. Async query with system message
        test_msg = await send_safe(message.chat.id, "2. Testing aquery_llm with system message...")
        result = await llm_provider.aquery_llm(prompt=prompt, system_message=system_msg)
        await test_msg.edit_text(f"2. aquery_llm: ✅\nResult: {result}")
        results.append("aquery_llm: ✅")
    except Exception as e:
        logger.error(f"Error testing aquery_llm: {e}")
        await test_msg.edit_text(f"2. aquery_llm: ❌\nError: {str(e)}")
        results.append("aquery_llm: ❌")
    
    try:
        # 3. Getting provider directly
        test_msg = await send_safe(message.chat.id, "3. Testing direct provider access...")
        provider = llm_provider.get_llm_provider()
        result = await provider.aquery_llm_text(prompt=prompt)
        await test_msg.edit_text(f"3. Direct provider: ✅\nResult: {result}")
        results.append("Direct provider: ✅")
    except Exception as e:
        logger.error(f"Error testing direct provider: {e}")
        await test_msg.edit_text(f"3. Direct provider: ❌\nError: {str(e)}")
        results.append("Direct provider: ❌")
    
    # Summary
    await send_safe(
        message.chat.id, 
        f"🧪 Test Results:\n\n" + "\n".join(results)
    )


# General message handler for chatting with the LLM
@router.message()
async def chat_handler(message: Message):
    """Process any non-command message through LLM"""
    
    # Skip messages without text
    if not message.text:
        return
    
    # Get the user prompt from the message
    prompt = message.text
    user_id = message.from_user.id
    
    # Get user state (for future history implementation)
    state = app.get_user_state(user_id)
    
    # Let the user know we're processing
    await message.chat.action("typing")
    
    try:
        # Simple implementation: just pass the message directly to the LLM
        response = await llm_provider.aquery_llm(
            prompt=prompt,
            system_message=app.config.system_message,
        )
        
        # Send the response
        await send_safe(message.chat.id, response)
    except Exception as e:
        logger.error(f"Error processing chat message: {e}")
        await send_safe(
            message.chat.id,
            "Sorry, I had trouble processing your message. Please try again later."
        )
