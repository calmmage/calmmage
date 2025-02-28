import subprocess
from config import settings
from loguru import logger
from pathlib import Path


def download_file_with_curl(file_metadata: dict) -> Path:
    """Download file using curl command"""
    # Create downloads directory if needed
    settings.DOWNLOADS_DIR.mkdir(exist_ok=True)
    output_path = settings.DOWNLOADS_DIR / file_metadata['name']

    # Check if file already exists
    if output_path.exists():
        logger.debug(f"File already exists: {output_path}")
        logger.debug(f"Size: {output_path.stat().st_size / (1024 * 1024):.2f} MB")
        return output_path

    logger.debug(f"Downloading to {output_path}...")

    curl_cmd = [
        'curl',
        '--location',  # follow redirects
        '--progress-bar',  # show progress
        '--output', str(output_path),
        file_metadata['downloadUrl']
    ]

    try:
        subprocess.run(curl_cmd, check=True)
        size = output_path.stat().st_size
        logger.debug(f"Download complete! File size: {size / (1024 * 1024):.2f} MB")
        return output_path
    except subprocess.CalledProcessError as e:
        logger.error(f"Download failed with exit code {e.returncode}")
        raise
