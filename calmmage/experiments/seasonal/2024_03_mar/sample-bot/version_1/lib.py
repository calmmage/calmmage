from aiogram.types import Message

from bot_lib import App, Handler, HandlerDisplayMode


class MyApp(App):
    secret_message = "Hello, Calm world!"


class MyHandler(Handler):
    name = "myBot"
    display_mode = HandlerDisplayMode.FULL
    commands = {
        "custom_handler": "custom"
    }

    async def custom_handler(self, message: Message, app: MyApp):
        await message.answer(app.secret_message)
