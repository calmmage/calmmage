import asyncio
import httpx
from dotenv import load_dotenv
from loguru import logger
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SERVICE_NAME: str = "test-heartbeat-service"
    REGISTRY_URL: str = "http://localhost:8000"
    HEARTBEAT_INTERVAL: int = 60  # seconds

    class Config:
        env_file = ".env"


async def send_heartbeat(settings: Settings) -> None:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{settings.REGISTRY_URL}/heartbeat",
                json={"service_key": settings.SERVICE_NAME}
            )
            if response.status_code == 200:
                logger.info(f"Heartbeat sent successfully for {settings.SERVICE_NAME}")
            else:
                logger.error(f"Failed to send heartbeat: {response.status_code}")
        except Exception as e:
            logger.error(f"Error sending heartbeat: {e}")


async def main():
    load_dotenv()

    settings = Settings()
    logger.info(f"Starting heartbeat service for {settings.SERVICE_NAME}")
    logger.debug(f"settings: {settings}")

    while True:
        await send_heartbeat(settings)
        await asyncio.sleep(settings.HEARTBEAT_INTERVAL)


if __name__ == "__main__":
    asyncio.run(main())
