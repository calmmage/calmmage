import json
import uuid
import requests
from typing import Dict, Any, Optional, List
from loguru import logger


class Grok3Client:
    """
    Unofficial Python client for interacting with the Grok 3 API.
    This client leverages cookies from browser requests to authenticate and access the API endpoints.
    """
    
    BASE_URL = "https://grok.com/rest"
    
    def __init__(self, cookies: Dict[str, str]):
        """
        Initialize the Grok3 client with authentication cookies.
        
        Args:
            cookies: Dictionary containing the required cookie values:
                    - x-anonuserid
                    - x-challenge
                    - x-signature
                    - sso
                    - sso-rw
        """
        self.cookies = cookies
        self.session = requests.Session()
        self.session.cookies.update(cookies)
        self.conversation_id = None
        
        # Validate required cookies
        required_cookies = ["x-anonuserid", "x-challenge", "x-signature", "sso", "sso-rw"]
        missing_cookies = [cookie for cookie in required_cookies if cookie not in cookies]
        
        if missing_cookies:
            logger.error(f"Missing required cookies: {', '.join(missing_cookies)}")
            raise ValueError(f"Missing required cookies: {', '.join(missing_cookies)}")
        
        logger.info("Grok3 client initialized successfully")
    
    def create_conversation(self) -> str:
        """
        Create a new conversation and return the conversation ID.
        
        Returns:
            str: The ID of the newly created conversation
        """
        url = f"{self.BASE_URL}/app-chat/conversations/new"
        
        try:
            response = self.session.post(url)
            response.raise_for_status()
            data = response.json()
            
            self.conversation_id = data.get("id")
            logger.info(f"Created new conversation with ID: {self.conversation_id}")
            
            return self.conversation_id
        
        except requests.RequestException as e:
            logger.error(f"Failed to create conversation: {str(e)}")
            raise
    
    def send_message(self, message: str, conversation_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Send a message to Grok and get the response.
        
        Args:
            message: The message to send to Grok
            conversation_id: Optional conversation ID. If not provided, a new conversation will be created.
            
        Returns:
            Dict containing the response from Grok
        """
        if not conversation_id and not self.conversation_id:
            self.create_conversation()
        
        conv_id = conversation_id or self.conversation_id
        url = f"{self.BASE_URL}/app-chat/conversations/{conv_id}/messages"
        
        payload = {
            "message": message,
            "messageId": str(uuid.uuid4())
        }
        
        try:
            response = self.session.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            
            logger.info(f"Message sent successfully to conversation {conv_id}")
            return data
        
        except requests.RequestException as e:
            logger.error(f"Failed to send message: {str(e)}")
            raise
    
    def get_conversation_history(self, conversation_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get the message history for a conversation.
        
        Args:
            conversation_id: Optional conversation ID. If not provided, uses the current conversation.
            
        Returns:
            List of messages in the conversation
        """
        if not conversation_id and not self.conversation_id:
            logger.error("No conversation ID provided or available")
            raise ValueError("No conversation ID provided or available")
        
        conv_id = conversation_id or self.conversation_id
        url = f"{self.BASE_URL}/app-chat/conversations/{conv_id}"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            
            logger.info(f"Retrieved conversation history for {conv_id}")
            return data.get("messages", [])
        
        except requests.RequestException as e:
            logger.error(f"Failed to get conversation history: {str(e)}")
            raise 