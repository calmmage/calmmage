from enum import Enum
from pydantic_settings import BaseSettings
from botspot.components.new.queue_manager import create_queue, QueueItem


class AppConfig(BaseSettings):
    """Basic app configuration"""

    telegram_bot_token: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


class SaveMode(Enum):
    DATA = "data"  # save data to db and then post manually
    FORWARD = (
        "forward"  # save message id to db and then forward original message to channel
    )


class Readiness(Enum):
    DRAFT = "draft"
    UNPOLISHED = "unpolished"
    FINISHED = "finished"


class PosterBotQueueItem(QueueItem):
    pass
    # text: str
    # todo: readiness - enum
    # todo: topic(s) - set of enums


class App:
    name = "Poster Prototype Bot"

    def __init__(self, **kwargs):
        self.config = AppConfig(**kwargs)

        self._queue = None

    @property
    def queue(self):
        if self._queue is None:
            self._queue = create_queue(key="content", item_model=PosterBotQueueItem)
        return self._queue

    async def add_to_queue(self, text: str, user_id: int):
        item = PosterBotQueueItem(data=text)
        await self.queue.add_item(item, user_id=user_id)
