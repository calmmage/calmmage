import boto3
from config import settings
from loguru import logger


def get_s3_client():
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        return s3_client
    except Exception as e:
        logger.error(f"Failed to create S3 client: {e}")
        raise
