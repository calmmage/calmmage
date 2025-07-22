# Simple GPT Chat Bot

This is a Telegram bot that uses Botspot's LLM Provider component to create chat experiences powered by GPT, Claude, or other LLM models.

## Features

This project includes two complementary examples of how to use the LLM Provider:

1. **Minimal Showcase**: Shows how to create a simple, but powerful GPT-powered chat bot in just a few lines of code.
2. **Advanced Scenarios**: Demonstrates more complex features like AI personas, custom system prompts, and comprehensive LLM testing.

Both routers are included in the bot by default, allowing users to explore both simple and advanced functionality.

## Running the Bot

Simply run the bot with:

```bash
python bot.py
```

## Minimal Router Example

The minimal router demonstrates how easy it is to create a functional GPT chat bot with botspot:

```python
# This is all you need to handle chat messages with GPT!
@router.message()
async def chat_handler(message: Message):
    """Process messages with GPT"""
    # Skip messages without text
    if not message.text:
        return
    
    # Show typing indicator
    await send_typing_status(message)
    
    # Query LLM with just one line
    response = await llm_provider.aquery_llm(
        prompt=message.text,
        user=str(message.from_user.id)
    )
    
    # Send the response
    await send_safe(message.chat.id, response)
```

## Advanced Router with Scenarios

The advanced router adds multiple AI personas (scenarios) on top of the base functionality:

- Select from multiple pre-defined personas (helpful assistant, creative writer, technical expert, etc.)
- Create custom personas on-the-fly with the `/custom` command
- Per-user state and scenario tracking

## Commands

The bot supports a variety of commands from both minimal and advanced routers:

### Minimal Router Commands (Simple but Powerful)
- `/start` - Start the bot
- `/help` - Show help message

### Advanced Router Commands (Feature-Rich)
- `/test` - Test all LLM provider features (streaming, JSON mode, structured output, etc.)
- `/scenarios` - View available AI personas
- `/scenario_default` - Use the default helpful assistant persona
- `/scenario_creative` - Use the creative writer persona
- `/scenario_expert` - Use the technical expert persona
- `/scenario_philosopher` - Use the philosopher persona
- `/scenario_coach` - Use the life coach persona
- `/custom [prompt]` - Create a custom AI persona

## Setup

1. Copy `sample.env` to `.env` and fill in your Telegram bot token and API keys
2. Install dependencies
3. Run the bot as shown above