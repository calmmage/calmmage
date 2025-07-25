#!/usr/bin/env python3
"""
MongoDB Test Job - Database connectivity example.

This job demonstrates:
- Database connection
- Environment variable usage for sensitive data
- Error handling
- Logging structured data
"""

import os
from datetime import datetime

# Add calmlib to path if available
try:
    from calmlib.utils.logging_utils import setup_logging
    setup_logging()
except ImportError:
    import logging
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

# MongoDB connection
try:
    from pymongo import MongoClient
    HAS_PYMONGO = True
except ImportError:
    HAS_PYMONGO = False
    logger.warning("PyMongo not available - install with: pip install pymongo")


def connect_to_mongodb():
    """Connect to MongoDB using environment variables."""
    if not HAS_PYMONGO:
        return None
    
    mongo_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017/")
    database_name = os.getenv("MONGODB_DATABASE", "local")
    
    try:
        client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
        # Test connection
        client.server_info()
        db = client[database_name]
        logger.info(f"Connected to MongoDB: {database_name}")
        return db
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        return None


def test_database_operations(db):
    """Test basic database operations."""
    collection_name = os.getenv("MONGODB_COLLECTION", "test_jobs")
    collection = db[collection_name]
    
    # Insert test document
    job_run_data = {
        "job_name": "mongodb_test_job",
        "timestamp": datetime.now(),
        "status": "running",
        "host": os.getenv("HOSTNAME", "unknown"),
        "user": os.getenv("USER", "unknown"),
        "test_data": {
            "random_number": 42,
            "environment": os.getenv("ENVIRONMENT", "development")
        }
    }
    
    try:
        # Insert document
        result = collection.insert_one(job_run_data)
        logger.info(f"Inserted document with ID: {result.inserted_id}")
        
        # Update document status
        collection.update_one(
            {"_id": result.inserted_id},
            {"$set": {"status": "completed", "completed_at": datetime.now()}}
        )
        
        # Retrieve and verify
        document = collection.find_one({"_id": result.inserted_id})
        logger.info(f"Retrieved document: {document['job_name']} - {document['status']}")
        
        # Clean up - remove test document
        cleanup = os.getenv("CLEANUP_TEST_DATA", "true").lower() == "true"
        if cleanup:
            collection.delete_one({"_id": result.inserted_id})
            logger.info("Cleaned up test document")
        
        return True
        
    except Exception as e:
        logger.error(f"Database operation failed: {e}")
        return False


def main():
    """Main job function."""
    logger.info("🗄️  MongoDB Test Job Starting...")
    
    # Check environment
    required_env_vars = ["MONGODB_URL", "MONGODB_DATABASE"]
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.warning(f"Missing environment variables: {missing_vars}")
        logger.info("Using default values - this may fail if MongoDB is not available locally")
    
    # Connect to database
    db = connect_to_mongodb()
    if db is None:
        logger.error("❌ Cannot connect to MongoDB")
        return 1
    
    # Test operations
    logger.info("🧪 Testing database operations...")
    success = test_database_operations(db)
    
    if success:
        logger.info("✅ MongoDB Test Job Completed Successfully!")
        return 0
    else:
        logger.error("❌ MongoDB Test Job Failed!")
        return 1


if __name__ == "__main__":
    exit(main())