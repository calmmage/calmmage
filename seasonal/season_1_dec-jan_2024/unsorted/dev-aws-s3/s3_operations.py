from pathlib import Path
from loguru import logger
from s3_client import get_s3_client
from config import settings

def upload_file(file_path: Path | str, object_name: str | None = None) -> bool:
    """
    Upload a file to S3 bucket
    
    Args:
        file_path: Path to the file to upload
        object_name: S3 object name. If not specified, file_path's name will be used
    
    Returns:
        bool: True if file was uploaded successfully, False otherwise
    """
    file_path = Path(file_path)
    
    # If S3 object_name not specified, use file_path's name
    if object_name is None:
        object_name = file_path.name

    s3_client = get_s3_client()
    
    try:
        logger.info(f"Uploading file {file_path} to bucket {settings.BUCKET_NAME}")
        s3_client.upload_file(
            str(file_path),
            settings.BUCKET_NAME,
            object_name
        )
        logger.success(f"Successfully uploaded {file_path} to {settings.BUCKET_NAME}/{object_name}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to upload file {file_path}: {e}")
        return False 

def download_file(object_name: str, file_path: Path | str | None = None) -> bool:
    """
    Download a file from S3 bucket
    
    Args:
        object_name: Name of the object in S3 bucket
        file_path: Local path where to save the file. If not specified,
                  the object name will be used as the file name
    
    Returns:
        bool: True if file was downloaded successfully, False otherwise
    """
    if file_path is None:
        file_path = Path(object_name)
    else:
        file_path = Path(file_path)

    # Create directory if it doesn't exist
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    s3_client = get_s3_client()
    
    try:
        logger.info(f"Downloading {object_name} from bucket {settings.BUCKET_NAME}")
        s3_client.download_file(
            settings.BUCKET_NAME,
            object_name,
            str(file_path)
        )
        logger.success(f"Successfully downloaded {object_name} to {file_path}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to download file {object_name}: {e}")
        return False 

def search_files(prefix: str = "", max_keys: int = 1000) -> list[dict]:
    """
    Search for files in S3 bucket with given prefix
    
    Args:
        prefix: Filter results to objects with keys that start with this prefix
        max_keys: Maximum number of keys to return
    
    Returns:
        list[dict]: List of objects with their details (key, size, last_modified)
    """
    s3_client = get_s3_client()
    
    try:
        logger.info(f"Searching for files with prefix '{prefix}' in bucket {settings.BUCKET_NAME}")
        response = s3_client.list_objects_v2(
            Bucket=settings.BUCKET_NAME,
            Prefix=prefix,
            MaxKeys=max_keys
        )
        
        if 'Contents' not in response:
            logger.info(f"No files found with prefix '{prefix}'")
            return []
            
        files = [{
            'key': obj['Key'],
            'size': obj['Size'],
            'last_modified': obj['LastModified']
        } for obj in response['Contents']]
        
        logger.success(f"Found {len(files)} files with prefix '{prefix}'")
        return files
        
    except Exception as e:
        logger.error(f"Failed to search files with prefix '{prefix}': {e}")
        return [] 