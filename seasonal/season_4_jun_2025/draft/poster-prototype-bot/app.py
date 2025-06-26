from enum import Enum
from pydantic_settings import BaseSettings
from botspot.components.new.queue_manager import create_queue, QueueItem
from botspot.components.main.event_scheduler import get_scheduler
from typing import Optional
from datetime import datetime
from pydantic import model_validator
from croniter import croniter


class SchedulingMode(Enum):
    PERIOD = "period"
    CRON = "cron"


class AppConfig(BaseSettings):
    """Basic app configuration"""

    telegram_bot_token: str
    post_channel_id: int
    scheduling_mode: SchedulingMode = SchedulingMode.PERIOD
    scheduling_period_minutes: int = 60
    scheduling_cron_expr: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    @model_validator(mode="after")
    def check_cron_expr_if_cron(self):
        if self.scheduling_mode == SchedulingMode.CRON:
            if not self.scheduling_cron_expr:
                raise ValueError("scheduling_cron_expr must be set when scheduling_mode is CRON")
            # Validate cron expression
            try:
                croniter(self.scheduling_cron_expr)
            except Exception as e:
                raise ValueError(f"Invalid cron expression: {self.scheduling_cron_expr}. Error: {e}")
        return self


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
    posted: bool = False
    posted_channel_id: Optional[int] = None
    posted_at: Optional[datetime] = None
    # text: str
    # todo: readiness - enum
    # todo: topic(s) - set of enums


class App:
    name = "Poster Prototype Bot"

    def __init__(self, **kwargs):
        self.config = AppConfig(**kwargs)

        self._queue = None
        self._scheduler = None

    @property
    def queue(self):
        if self._queue is None:
            self._queue = create_queue(key="content", item_model=PosterBotQueueItem)
        return self._queue

    @property
    def scheduler(self):
        if self._scheduler is None:
            self._scheduler = get_scheduler()
        return self._scheduler

    async def add_to_queue(self, text: str, user_id: int):
        item = PosterBotQueueItem(data=text)
        await self.queue.add_item(item, user_id=user_id)

    async def post_from_queue(self, channel_id: int):
        """Post the oldest item from the queue to the specified channel."""
        # todos:
        #  1) do NOT delete item from db - instead
        #  2) implement a special method that picks the item to be posted
        #    a) just random
        #    b) make sure post is ready (for this channel - for when we add multiple channels)
        #    c) make sure post is not already posted (to this channel - for when we add multiple channels)
        records = await self.queue.get_records()
        if records:
            item = records[0]  # Get the oldest item
            from botspot.utils import send_safe
            await send_safe(channel_id, item["data"])
            await self.queue.collection.update_one(
                {"_id": item["_id"]},
                {"$set": {
                    "posted": True,
                    "posted_channel_id": channel_id,
                    "posted_at": datetime.now()
                }}
            )
        else:
            from botspot.utils import send_safe
            await send_safe(channel_id, "No items in queue to post.")

    def schedule_posts(self):
        """Schedule posting from queue at regular intervals or cron."""
        if self.config.scheduling_mode == SchedulingMode.PERIOD:
            self.scheduler.add_job(
                func=self.post_from_queue,
                trigger='interval',
                minutes=self.config.scheduling_period_minutes,
                args=[self.config.post_channel_id],
                id='post_from_queue'
            )
        elif self.config.scheduling_mode == SchedulingMode.CRON:
            self.scheduler.add_job(
                func=self.post_from_queue,
                trigger='cron',
                args=[self.config.post_channel_id],
                id='post_from_queue',
                cron=self.config.scheduling_cron_expr
            )
