# Simple GPT Chat Bot

A minimalist Telegram bot that uses the botspot LLM Provider component to integrate with GPT. 

## Features

- Simple chat interface - send a message, get a GPT response
- Uses the new botspot LLM Provider component
- Demo of basic query_llm and aquery_llm functionality
- Test command to verify all LLM provider features

## Implementation Details

This bot includes:

1. Basic setup of the botspot LLM Provider component
2. Configuration for default model and parameters
3. Simple message handler that passes user input directly to the LLM
4. Error handling for failed API calls
5. Test command to verify all LLM provider features are working

## Future Improvements

In the future, this bot could be enhanced with:

- Chat history support for contextual conversations
- Streaming responses
- Model selection commands
- System message customization
- Structured outputs with Pydantic models

## Usage

To use the bot:
1. Set your OpenAI API key in the .env file
2. Run the bot with `python bot.py`
3. Send messages to chat with GPT