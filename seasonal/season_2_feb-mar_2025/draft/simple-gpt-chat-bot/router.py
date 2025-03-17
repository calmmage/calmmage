from _app import App
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from botspot import commands_menu
from botspot.components.new import llm_provider
from botspot.utils import send_safe, send_typing_status
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
    
    # More interesting prompt for testing
    prompt = "What is a truly unique idea in modern philosophy or science that challenges conventional thinking?"
    system_msg = "You are a helpful assistant. Provide a thoughtful but concise response."
    
    results = []
    user = str(message.from_user.id)
    
    # Test each function with error handling
    try:
        # 1. Async query with system message
        test_msg = await send_safe(message.chat.id, "1. Testing aquery_llm with system message...")
        result = await llm_provider.aquery_llm(
            prompt=prompt, 
            system_message=system_msg,
            user=user
        )
        await test_msg.edit_text(f"1. aquery_llm: ✅\nResult: {result}")
        results.append("aquery_llm: ✅")
    except Exception as e:
        logger.error(f"Error testing aquery_llm: {e}")
        await test_msg.edit_text(f"1. aquery_llm: ❌\nError: {str(e)}")
        results.append("aquery_llm: ❌")
    
    try:
        # 2. Testing with different model
        test_msg = await send_safe(message.chat.id, "2. Testing with different model (claude-3.7)...")
        result = await llm_provider.aquery_llm(
            prompt="Explain quantum entanglement briefly", 
            model="claude-3.7",
            user=user
        )
        await test_msg.edit_text(f"2. Model selection: ✅\nResult: {result}")
        results.append("Model selection: ✅")
    except Exception as e:
        logger.error(f"Error testing model selection: {e}")
        await test_msg.edit_text(f"2. Model selection: ❌\nError: {str(e)}")
        results.append("Model selection: ❌")
    
    # 3. Structured output with Pydantic
    from pydantic import BaseModel, Field
    
    class PhilosophicalIdea(BaseModel):
        name: str = Field(description="The name of the philosophical concept")
        description: str = Field(description="A brief description of the concept")
        key_thinkers: list[str] = Field(description="Key philosophers associated with this concept")
        
    try:
        test_msg = await send_safe(message.chat.id, "3. Testing structured output with Pydantic...")
        result = await llm_provider.aquery_llm_structured(
            prompt="Describe the concept of 'Intersubjectivity'",
            output_schema=PhilosophicalIdea,
            user=user
        )
        await test_msg.edit_text(f"3. Structured output: ✅\nResult:\nName: {result.name}\nDescription: {result.description}\nThinkers: {', '.join(result.key_thinkers)}")
        results.append("Structured output: ✅")
    except Exception as e:
        logger.error(f"Error testing structured output: {e}")
        await test_msg.edit_text(f"3. Structured output: ❌\nError: {str(e)}")
        results.append("Structured output: ❌")
    
    try:
        # 4. Getting provider directly
        test_msg = await send_safe(message.chat.id, "4. Testing direct provider access...")
        provider = llm_provider.get_llm_provider()
        result = await provider.aquery_llm_text(
            prompt="What is the most fascinating aspect of black holes?", 
            user=user
        )
        await test_msg.edit_text(f"4. Direct provider: ✅\nResult: {result}")
        results.append("Direct provider: ✅")
    except Exception as e:
        logger.error(f"Error testing direct provider: {e}")
        await test_msg.edit_text(f"4. Direct provider: ❌\nError: {str(e)}")
        results.append("Direct provider: ❌")
    
    try:
        # 5. Testing with different parameters
        test_msg = await send_safe(message.chat.id, "5. Testing with temperature/max_tokens...")
        result = await llm_provider.aquery_llm(
            prompt="Generate a creative concept for a sci-fi novel", 
            temperature=0.9,
            max_tokens=150,
            user=user
        )
        await test_msg.edit_text(f"5. Custom parameters: ✅\nResult: {result}")
        results.append("Custom parameters: ✅")
    except Exception as e:
        logger.error(f"Error testing custom parameters: {e}")
        await test_msg.edit_text(f"5. Custom parameters: ❌\nError: {str(e)}")
        results.append("Custom parameters: ❌")
    
    try:
        # 6. Test with streaming (collect chunks and then display)
        test_msg = await send_safe(message.chat.id, "6. Testing streaming response...")
        
        chunks = []
        async for chunk in llm_provider.astream_llm(
            prompt="What are three emerging trends in artificial intelligence?",
            user=user
        ):
            chunks.append(chunk)
        
        result = "".join(chunks)
        await test_msg.edit_text(f"6. Streaming: ✅\nReceived {len(chunks)} chunks\nFull result: {result}")
        results.append("Streaming: ✅")
    except Exception as e:
        logger.error(f"Error testing streaming: {e}")
        await test_msg.edit_text(f"6. Streaming: ❌\nError: {str(e)}")
        results.append("Streaming: ❌")
    
    try:
        # 7. Test with JSON mode
        test_msg = await send_safe(message.chat.id, "7. Testing JSON mode...")
        result = await llm_provider.aquery_llm(
            prompt="List three philosophers and their main contributions", 
            response_format={"type": "json_object"},
            user=user
        )
        await test_msg.edit_text(f"7. JSON mode: ✅\nResult: {result}")
        results.append("JSON mode: ✅")
    except Exception as e:
        logger.error(f"Error testing JSON mode: {e}")
        await test_msg.edit_text(f"7. JSON mode: ❌\nError: {str(e)}")
        results.append("JSON mode: ❌")
        
    try:
        # 8. Test with streaming to chat (real-time updates)
        test_msg = await send_safe(message.chat.id, "8. Testing live streaming to chat...")
        
        message_text = "8. Live streaming: The response will appear below gradually...\n\n"
        message_obj = await send_safe(message.chat.id, message_text)
        
        async for chunk in llm_provider.astream_llm(
            prompt="Explain the concept of emergent complexity in nature",
            user=user
        ):
            message_text += chunk
            # Update message every few chunks to avoid rate limiting
            if len(message_text) % 20 == 0:
                try:
                    await message_obj.edit_text(message_text)
                except:
                    pass  # Ignore errors from rate limits
        
        # Final update with complete text
        await message_obj.edit_text(message_text)
        results.append("Live streaming: ✅")
    except Exception as e:
        logger.error(f"Error testing live streaming: {e}")
        await send_safe(message.chat.id, f"8. Live streaming: ❌\nError: {str(e)}")
        results.append("Live streaming: ❌")
    
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
    await send_typing_status(message)

    # Simple implementation: just pass the message directly to the LLM
    response = await llm_provider.aquery_llm(
        prompt=prompt,
        system_message=app.config.system_message,
        user=str(user_id),  # Convert to string to ensure compatibility
    )

    # Send the response
    await send_safe(message.chat.id, response)
