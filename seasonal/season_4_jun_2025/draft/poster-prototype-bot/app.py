from enum import Enum
from pydantic_settings import BaseSettings
from botspot.components.new.queue_manager import create_queue, QueueItem
from botspot.components.main.event_scheduler import get_scheduler
from typing import Optional
from datetime import datetime
from pydantic import model_validator
from croniter import croniter
from botspot.utils import send_safe
from loguru import logger
from botspot.components.data.user_data import User


class SchedulingMode(Enum):
    PERIOD = "period"
    CRON = "cron"


class AppConfig(BaseSettings):
    """Basic app configuration"""

    telegram_bot_token: str
    post_channel_id: int
    scheduling_mode: SchedulingMode = SchedulingMode.PERIOD
    scheduling_period_seconds: int = 60
    scheduling_cron_expr: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    @model_validator(mode="after")
    def check_cron_expr_if_cron(self):
        if self.scheduling_mode == SchedulingMode.CRON:
            if not self.scheduling_cron_expr:
                raise ValueError(
                    "scheduling_cron_expr must be set when scheduling_mode is CRON"
                )
            # Validate cron expression
            try:
                croniter(self.scheduling_cron_expr)
            except Exception as e:
                raise ValueError(
                    f"Invalid cron expression: {self.scheduling_cron_expr}. Error: {e}"
                )
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


class PosterBotUser(User):
    target_channel_id: int | None = None
    scheduling_mode: SchedulingMode | None = None
    scheduling_period_seconds: int | None = None
    scheduling_cron_expr: str | None = None
    auto_posting_enabled: bool = False


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

    # async def post_from_queue(self, channel_id: int):
    #     """Post the oldest item from the queue to the specified channel."""
    #
    #     # todo:
    #
    #     # todo: implement a special method that picks the item to be posted
    #     #  a) just random
    #     #  b) make sure post is ready (for this channel - for when we add multiple channels)
    #     #  c) make sure post is not already posted (to this channel - for when we add multiple channels)
    #     logger.debug(f"Attempting to post from queue to channel {channel_id}")
    #     records = await self.queue.get_records()
    #     logger.debug(f"Queue records fetched: {len(records)} items")
    #     if records:
    #         item = records[0]  # Get the oldest item
    #         logger.info(f"Posting item to channel {channel_id}: {item}")
    #         from botspot.utils import send_safe
    #         await send_safe(channel_id, item["data"])
    #         await self.queue.collection.update_one(
    #             {"_id": item["_id"]},
    #             {
    #                 "$set": {
    #                     "posted": True,
    #                     "posted_channel_id": channel_id,
    #                     "posted_at": datetime.now(),
    #                 }
    #             },
    #         )
    #         logger.info(f"Marked item as posted in DB: id={item['_id']}")
    #     else:
    #         logger.info(f"No items in queue to post for channel {channel_id}")
    #         from botspot.utils import send_safe
    #         await send_safe(channel_id, "No items in queue to post.")

    async def get_users(self) -> list[PosterBotUser]:
        from botspot.utils import get_user_manager

        user_manager = get_user_manager()
        return await user_manager.get_users()

    def schedule_posts_on_startup(self):
        """Schedule posting from queue at regular intervals or cron."""

        # go over all existing users and schedule posting job if they have auto-posting enabled
        users = self.get_users()

        for user in users:
            if user.auto_posting_enabled:
                logger.info(
                    f"Scheduling posts for user {user.user_id} to channel {user.target_channel_id}"
                )
                self._schedule_user_posting_job(user)
            else:
                logger.info(
                    f"Auto-posting is disabled for user {user.user_id}, skipping scheduling."
                )

    def _schedule_user_posting_job(self, user: PosterBotUser):
        """
        Schedule a posting job for a user based on their settings.
        """
        if user.scheduling_mode == SchedulingMode.PERIOD:
            self.scheduler.add_job(
                func=self.post_content_job,
                trigger="interval",
                seconds=user.scheduling_period_seconds,
                args=[user.user_id],
                id=f"post_content_job_{user.user_id}",
            )
        elif user.scheduling_mode == SchedulingMode.CRON:
            self.scheduler.add_job(
                func=self.post_content_job,
                trigger="cron",
                args=[user.user_id],
                id=f"post_content_job_{user.user_id}",
                cron=user.scheduling_cron_expr,
            )

    def get_default_user_config(self):
        return dict(
            target_channel_id=self.config.post_channel_id,
            scheduling_mode=self.config.scheduling_mode,
            scheduling_period_seconds=self.config.scheduling_period_seconds,
            scheduling_cron_expr=self.config.scheduling_cron_expr,
        )

    # async def _get_user(self, user_id: int) -> PosterBotUser:
    #     # TODO: fetch user from user manager
    #     # If user config is not initialized, call self.initialize_user(user_id)
    #     # For now, always initialize with defaults
    #     return await self.initialize_user(user_id)
    #
    # async def _initialize_user(self, user_id: int) -> PosterBotUser:
    #     # TODO: ask user for settings (cron schedule, etc) via bot conversation
    #     # For now, populate all values with defaults from AppConfig
    #     defaults = self.get_default_user_config()
    #     user = PosterBotUser(user_id=user_id, auto_posting_enabled=True, **defaults)
    #     # TODO: save user to db
    #     return user

    async def post_content_job(self, user_id: int):
        """
        A job that runs on a schedule for a particular user.
        """

        user = await self._get_user(user_id)

        post = await self._pick_post_from_queue(user_id)
        channel_id = user.target_channel_id
        assert channel_id is not None, "Target channel ID is not set for user"

        if not post:
            logger.info(f"No posts in queue for user {user_id}")
            # notify the user.
            await send_safe(
                user_id,
                "Scheduled posting time is due, but there are no posts in queue to post.",
            )
            return

        # todo: send the post to the channel
        await send_safe(channel_id, post.data)
        logger.info(f"Posted content to channel {channel_id}: {post.data}")

        # todo: notify the user that the post was sent, and the amount of remaining posts in queue

        # todo: mark the post as posted

    async def _pick_post_from_queue(self, user_id: int) -> PosterBotQueueItem | None:
        """
        Pick a post from the queue for a user.
        """
        # todo: implement a special method that picks the item to be posted
        #  a) just random
        #  b) make sure post is ready (for this channel - for when we add multiple channels)
        #  c) make sure post is not already posted (to this channel - for when we add multiple channels)

        all_posts = await self.queue.get_items(user_id=user_id)
        if not all_posts:
            logger.info(f"No posts in queue for user {user_id}")
            return None

        # todo: pick a post from the queue
        return all_posts[0]

    async def activate_user(self, user_id: int):
        """
        Activate a user.
        """
        # todo: 0) check if user has all the settings specified. if not - launch the setup flow
        user = await self.get_user(user_id)
        user.auto_posting_enabled = True

        await self.update_user(user)
        self._schedule_user_posting_job(user)

    async def deactivate_user(self, user_id: int):
        """
        Deactivate a user.
        """
        # user = await self._get_user(user_id)
        # user.auto_posting_enabled = False
        # await self._save_user(user)
        # todo: 1) disable the flag
        # todo: 2) cancel the job
        raise NotImplementedError
