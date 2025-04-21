"""
LLM Utils Test Router

This file tests the behavior of LLM for parsing structured data with optional fields.
"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from botspot import commands_menu
from botspot.components.new import llm_provider
from botspot.utils import send_safe, send_typing_status
from loguru import logger
from pydantic import BaseModel, Field
from typing import Optional, List

from _app import App

# Create router and app
router = Router()
app = App()


# Define test models with optional and required fields
class Person(BaseModel):
    name: str = Field(description="The person's full name")
    age: Optional[int] = Field(None, description="The person's age in years")
    email: str = Field(description="The person's email address")
    interests: Optional[List[str]] = Field(None, description="The person's interests or hobbies")


@commands_menu.add_command("form_test", "Test LLM with forms")
@router.message(Command("form_test"))
async def form_test_handler(message: Message):
    """Test if LLM can differentiate between optional and required fields."""
    from botspot import get_dependency_manager
    deps = get_dependency_manager()
    await send_safe(
        message.chat.id,
        "Testing LLM with a form that has both required and optional fields..."
    )
    
    await send_typing_status(message)
    
    # First, use complete but minimal information
    test_prompt = "Name: John Doe, Email: john@example.com"
    
    try:
        await send_safe(message.chat.id, f"Testing with minimal info: {test_prompt}")

        result = await deps.llm_provider.aquery_llm_structured(
        # result = await llm_provider.aquery_llm_structured(
            prompt=f"Parse this into a person record: {test_prompt}",
            output_schema=Person,
            user=str(message.from_user.id)
        )
        
        # Format the result
        interests_text = ", ".join(result.interests) if result.interests else "None provided"
        await send_safe(
            message.chat.id,
            f"Result with minimal info:\n"
            f"• Name: {result.name}\n"
            f"• Age: {result.age if result.age is not None else 'None provided'}\n"
            f"• Email: {result.email}\n"
            f"• Interests: {interests_text}"
        )
    except Exception as e:
        logger.error(f"Error in minimal info test: {e}")
        await send_safe(message.chat.id, f"❌ Error with minimal info: {str(e)}")
    
    # Second, use missing required information
    test_prompt = "Age: 30, Interests: reading, hiking"
    
    try:
        await send_safe(message.chat.id, f"Testing with missing required fields: {test_prompt}")
        result = await deps.llm_provider.aquery_llm_structured(
        # result = await llm_provider.aquery_llm_structured(
            prompt=f"Parse this into a person record: {test_prompt}",
            output_schema=Person,
            user=str(message.from_user.id)
        )
        
        # Format the result
        interests_text = ", ".join(result.interests) if result.interests else "None provided"
        await send_safe(
            message.chat.id,
            f"Result with missing required fields:\n"
            f"• Name: {result.name}\n"
            f"• Age: {result.age if result.age is not None else 'None provided'}\n"
            f"• Email: {result.email}\n"
            f"• Interests: {interests_text}"
        )
    except Exception as e:
        logger.error(f"Error in missing required fields test: {e}")
        await send_safe(
            message.chat.id, 
            f"❌ Error with missing required fields: {str(e)}\n\n"
            f"This shows the LLM doesn't automatically handle missing required fields."
        )
    
    # Third, test with irrelevant information to see what happens
    test_prompt = "Weather: sunny, Location: New York, Date: 2025-03-19"
    
    try:
        await send_safe(message.chat.id, f"Testing with irrelevant information: {test_prompt}")

        result = await deps.llm_provider.aquery_llm_structured(
        # result = await llm_provider.aquery_llm_structured(
            prompt=f"Parse this into a person record: {test_prompt}",
            output_schema=Person,
            user=str(message.from_user.id)
        )
        
        # Format the result
        interests_text = ", ".join(result.interests) if result.interests else "None provided"
        await send_safe(
            message.chat.id,
            f"Result with irrelevant info:\n"
            f"• Name: {result.name}\n"
            f"• Age: {result.age if result.age is not None else 'None provided'}\n"
            f"• Email: {result.email}\n"
            f"• Interests: {interests_text}"
        )
    except Exception as e:
        logger.error(f"Error in irrelevant info test: {e}")
        await send_safe(
            message.chat.id, 
            f"❌ Error with irrelevant info: {str(e)}\n\n"
            f"This shows the LLM struggles with completely irrelevant input."
        )
    
    # Summary
    await send_safe(
        message.chat.id,
        "📝 Summary of form parsing test:\n\n"
        "1. The LLM can handle optional fields when they're missing\n"
        "2. It requires all required fields (throws error otherwise)\n"
        "3. It struggles with completely irrelevant input\n\n"
        "This means we need to build a custom solution to handle missing required fields "
        "and communicate when information is missing or irrelevant."
    )