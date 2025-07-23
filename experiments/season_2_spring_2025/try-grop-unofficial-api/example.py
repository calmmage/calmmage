from grok_client import Grok3Client
from pathlib import Path
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def main():
    # Load cookies from environment variables or a config file
    cookies = {
        "x-anonuserid": os.getenv("GROK_ANONUSERID"),
        "x-challenge": os.getenv("GROK_CHALLENGE"),
        "x-signature": os.getenv("GROK_SIGNATURE"),
        "sso": os.getenv("GROK_SSO"),
        "sso-rw": os.getenv("GROK_SSO_RW")
    }
    
    # Initialize the client
    client = Grok3Client(cookies)
    
    # Create a new conversation
    conversation_id = client.create_conversation()
    print(f"Created conversation with ID: {conversation_id}")
    
    # Send a message and get response
    message = "Write a short poem about artificial intelligence"
    response = client.send_message(message)
    
    # Print the response
    print("\nResponse from Grok:")
    print(json.dumps(response, indent=2))
    
    # Get conversation history
    history = client.get_conversation_history()
    print("\nConversation history:")
    for msg in history:
        role = msg.get("role", "unknown")
        content = msg.get("content", "")
        print(f"{role}: {content}")

if __name__ == "__main__":
    main() 