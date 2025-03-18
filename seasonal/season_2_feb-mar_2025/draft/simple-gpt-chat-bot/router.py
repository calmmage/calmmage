from _app import App
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from botspot import commands_menu
from botspot.components.new import llm_provider
from botspot.utils import send_safe, send_typing_status
from loguru import logger

# Create the base app
app = App()

# Simple router for showcasing core LLM functionality with minimal code
simple_router = Router(name="simple_showcase")

# Advanced router with full features
advanced_router = Router(name="advanced_features")

# Combined router for the application
router = Router()

# We'll include both routers in the main router
def setup_routers():
    # Include both routers in the main router
    router.include_router(simple_router)
    router.include_router(advanced_router)
    return router


# -------------------------------------------------
# Simple Showcase Router - Minimal Implementation
# -------------------------------------------------

@commands_menu.add_command("simple", "Switch to simple mode")
@router.message(Command("simple"))
async def switch_to_simple_mode(message: Message):
    """Switch to simple showcase mode"""
    await send_safe(
        message.chat.id,
        "📱 Switched to Simple Mode\n\n"
        "This mode demonstrates the core LLM Provider functionality with minimal code.\n\n"
        "Just send a message and I'll respond using the LLM Provider component.\n\n"
        "Use /advanced to switch to advanced mode with scenarios."
    )

    # Update user state to use simple mode
    state = app.get_user_state(message.from_user.id)
    state["router_mode"] = "simple"


@simple_router.message()
async def simple_chat_handler(message: Message):
    """
    Simple chat handler with minimal code.
    Shows how easy it is to use the LLM Provider component.
    """
    if not message.text:
        return

    # Show typing indicator
    await send_typing_status(message)

    # This is all you need to query an LLM!
    response = await llm_provider.aquery_llm(
        prompt=message.text,
        user=str(message.from_user.id)
    )

    # Send the response
    await send_safe(message.chat.id, response)


# -------------------------------------------------
# Advanced Router - Full Features
# -------------------------------------------------

@commands_menu.add_command("start", "Start the bot")
@router.message(CommandStart())
async def start_handler(message: Message):
    await send_safe(
        message.chat.id,
        f"👋 Hello! Welcome to {app.name}!\n\n"
        f"Just send me a message and I'll respond using the LLM provider.\n\n"
        f"Try /scenarios to see available AI personas, or /help for more commands."
    )

    # Set default mode to advanced
    state = app.get_user_state(message.from_user.id)
    state["router_mode"] = "advanced"


@commands_menu.add_command("help", "Show this help message")
@router.message(Command("help"))
async def help_handler(message: Message):
    """Basic help command handler"""
    await send_safe(
        message.chat.id,
        f"This is {app.name}. I'm a smart chat bot powered by LLM Provider.\n\n"
        f"Just send me any message and I'll respond!\n\n"
        f"Available commands:\n"
        f"/start - Restart the bot\n"
        f"/help - Show this help message\n"
        f"/test - Test all LLM provider features\n"
        f"/scenarios - View available AI personas\n"
        f"/simple - Switch to simple mode\n"
        f"/advanced - Switch to advanced mode"
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

        # First try with aquery_llm_structured method
        try:
            result = await llm_provider.aquery_llm_structured(
                prompt="Describe the concept of 'Intersubjectivity' in JSON format",
                output_schema=PhilosophicalIdea,
                user=user
            )
            await test_msg.edit_text(f"3. Structured output: ✅\nResult:\nName: {result.name}\nDescription: {result.description}\nThinkers: {', '.join(result.key_thinkers)}")
            results.append("Structured output: ✅")
        except Exception as e:
            # Alternative approach using JSON mode
            json_prompt = """
            Describe the concept of 'Intersubjectivity'.
            Return a JSON object with these exact fields:
            - name: The name of the philosophical concept
            - description: A brief description of the concept
            - key_thinkers: An array of key philosophers associated with this concept

            Format your response as a valid JSON object.
            """

            json_result = await llm_provider.aquery_llm(
                prompt=json_prompt,
                response_format={"type": "json_object"},
                user=user
            )

            # Parse the JSON and create the Pydantic model
            import json
            data = json.loads(json_result)
            result = PhilosophicalIdea(**data)

            await test_msg.edit_text(f"3. Structured output (alt method): ✅\nResult:\nName: {result.name}\nDescription: {result.description}\nThinkers: {', '.join(result.key_thinkers)}")
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

        # Get provider directly for streaming
        provider = llm_provider.get_llm_provider()

        chunks = []
        async for chunk in provider.aquery_llm_stream(
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
            prompt="Generate a JSON object that lists three philosophers and their main contributions. Return your response as a valid JSON object.",
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

        # Get provider directly for streaming
        provider = llm_provider.get_llm_provider()

        # Counter to update message periodically
        update_counter = 0

        async for chunk in provider.aquery_llm_stream(
            prompt="Explain the concept of emergent complexity in nature",
            user=user
        ):
            message_text += chunk
            update_counter += 1

            # Update message every 5 chunks to avoid rate limiting
            if update_counter % 5 == 0:
                try:
                    await message_obj.edit_text(message_text)
                except Exception as edit_error:
                    logger.warning(f"Error updating message: {edit_error}")
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


@commands_menu.add_command("advanced", "Switch to advanced mode")
@router.message(Command("advanced"))
async def switch_to_advanced_mode(message: Message):
    """Switch to advanced features mode"""
    await send_safe(
        message.chat.id,
        "🚀 Switched to Advanced Mode\n\n"
        "This mode provides multiple AI personas and customizable features.\n\n"
        "Use /scenarios to see and select available AI personas.\n"
        "Use /simple to switch back to simple mode."
    )

    # Update user state to use advanced mode
    state = app.get_user_state(message.from_user.id)
    state["router_mode"] = "advanced"


@commands_menu.add_command("scenarios", "View and select AI personas")
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


# The advanced message handler with scenario support
@advanced_router.message()
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


# Router selector handler - must be last
@router.message()
async def router_selector(message: Message):
    """Route messages to the appropriate handler based on user state"""
    user_id = message.from_user.id
    state = app.get_user_state(user_id)

    # Get active router mode (default to advanced)
    router_mode = state.get("router_mode", "advanced")

    if router_mode == "simple":
        # Pass to simple handler
        await simple_chat_handler(message)
    else:
        # Pass to advanced handler
        await advanced_chat_handler(message)
