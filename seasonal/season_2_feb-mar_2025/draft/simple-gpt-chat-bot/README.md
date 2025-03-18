# Simple GPT Chat Bot

This is a Telegram bot that uses Botspot's LLM Provider component to create chat experiences powered by GPT, Claude, or other LLM models.

## Features

This project demonstrates two ways to use the LLM Provider:

1. **Minimal Showcase Router**: Shows how to create a GPT-powered chat bot in just a few lines of code.
2. **Advanced Scenarios Router**: Demonstrates more complex features like AI personas and custom system prompts.

## Running the Bot

You can run the bot with either router:

```bash
# Run with minimal showcase router (default)
python bot.py

# Run with advanced scenarios router
python bot.py --router advanced
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

### Minimal Router
- `/start` - Start the bot
- `/help` - Show help message

### Advanced Router
- `/start` - Start the bot
- `/help` - Show help message
- `/scenarios` - View available AI personas
- `/scenario_[name]` - Select a specific persona
- `/custom [prompt]` - Create a custom AI persona

## Setup

1. Copy `sample.env` to `.env` and fill in your Telegram bot token and API keys
2. Install dependencies
3. Run the bot as shown above