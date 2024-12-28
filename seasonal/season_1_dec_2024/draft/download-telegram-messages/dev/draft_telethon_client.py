from telethon import TelegramClient
from dotenv import load_dotenv
import os
import asyncio

if __name__ == "__main__":
    load_dotenv()

    api_id = int(os.getenv('TELEGRAM_API_ID'))
    api_hash = os.getenv('TELEGRAM_API_HASH')

    # Create the client
    client = TelegramClient('calmmage_macbook_dec_2024', api_id, api_hash)

    async def code_callback():
        # You can get this code from wherever you want - env var, config, etc.
        return input("CUSTOM MESSAGE - Enter code: ")
        # return os.getenv('TELEGRAM_CODE')  # or hardcode it for testing

    async def main():
        # Start the client with phone number and code callback
        await client.start(
            phone=os.getenv('TELEGRAM_PHONE_NUMBER'),
            code_callback=code_callback
        )
        print("Client Created")
        
        if await client.is_user_authorized():
            print('Successfully authenticated!')
        else:
            print('Authentication failed. Please check your credentials.')
        
        await client.disconnect()

    asyncio.run(main())
