from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from loguru import logger
from pydantic_settings import BaseSettings
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    mongodb_url: str
    mongodb_database: str

    class Config:
        env_file = ".env"

settings = Settings()
app = FastAPI(redirect_slashes=False)

class Item(BaseModel):
    name: str
    description: str

@app.on_event("startup")
async def startup_db_client():
    logger.info(f"Connecting to MongoDB at {settings.mongodb_url}")
    app.mongodb_client = AsyncIOMotorClient(settings.mongodb_url)
    app.mongodb = app.mongodb_client[settings.mongodb_database]
    logger.info("Connected to MongoDB")

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()
    logger.info("Disconnected from MongoDB")

@app.get("/")
async def root():
    return {"message": "API is running"}

@app.get("/health")
async def health():
    try:
        # Check MongoDB connection
        await app.mongodb.command("ping")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {str(e)}")

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    logger.info(f"Creating item: {item}")
    result = await app.mongodb["items"].insert_one(item.model_dump())
    if result.inserted_id:
        logger.info(f"Created item with id: {result.inserted_id}")
        return item
    raise HTTPException(status_code=400, detail="Failed to create item")

@app.get("/items/")
async def get_items():
    logger.info("Fetching all items")
    items = []
    cursor = app.mongodb["items"].find({})
    async for document in cursor:
        items.append(Item(**document))
    logger.info(f"Found {len(items)} items")
    return items 