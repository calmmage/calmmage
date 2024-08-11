from bot_lib import App, Handler, HandlerDisplayMode
from aiogram.types import Message
from collections import defaultdict
import asyncio
from calmlib.utils import get_logger

logger = get_logger(__name__)


class MyApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.user_message_queue = defaultdict(asyncio.Queue)
        self.user_lock = defaultdict(asyncio.Lock)


class MainHandler(Handler):
    name = "main"
    display_mode = HandlerDisplayMode.FULL
    pass

    # 500 ms delay
    MULTI_MESSAGE_DELAY = 0.5

    multi_message_handler_lock = asyncio.Lock()

    async def multi_message_handler(self, message: Message, app: MyApp):
        user = self.get_user(message)
        queue = app.user_message_queue[user]
        await queue.put(message)

        # try to grab the lock
        async with app.user_lock[user]:
            # wait for the delay
            await asyncio.sleep(self.MULTI_MESSAGE_DELAY)

            # grab all the messages from the queue
            messages = []
            while not queue.empty():
                messages.append(queue.get())
            if not messages:
                logger.info(
                    "Aborting message processing. Messages got processed by another handler."
                )
                return
            # test: send user the message count
            await message.answer(f"Received {len(messages)} messages")
