import asyncio
import os
from dotenv import load_dotenv
from telethon import TelegramClient


class App:
    def __init__(self):
        self.client = None

    def setup(self):
        load_dotenv()

        api_id = int(os.getenv("TELEGRAM_API_ID"))
        api_hash = os.getenv("TELEGRAM_API_HASH")

        user_id = os.getenv("TELEGRAM_USER_ID")
        # Create the client
        # client = TelegramClient('calmmage_macbook_dec_2024', api_id, api_hash)
        client = TelegramClient(f"sessions/user_{user_id}", api_id, api_hash)

        # async def code_callback():
        #     # You can get this code from wherever you want - env var, config, etc.
        #     return input("CUSTOM MESSAGE - Enter code: ")
        #     # return os.getenv('TELEGRAM_CODE')  # or hardcode it for testing

        async def main():
            # Start the client with phone number and code callback
            client.connect()
            if not client.is_authorized():
                await client.start(
                    phone=os.getenv("TELEGRAM_PHONE_NUMBER"),
                    code_callback=code_callback,
                )
            print("Client Created")

            if await client.is_user_authorized():
                print("Successfully authenticated!")
            else:
                print("Authentication failed. Please check your credentials.")

            # await client.disconnect()

        asyncio.run(main())

    def get_all_chats(self):
        pass  # TODO: Implement this

    def load_chat_messages(self, chat_id):
        pass  # TODO: Implement this


if __name__ == "__main__":
    pass
