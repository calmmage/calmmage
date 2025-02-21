import requests
from get_zoom_meeting_list import get_zoom_token
from loguru import logger


def generate_zoom_download_url(download_url: str, file_name: str) -> dict:
    """Get direct download URL that doesn't require auth"""
    token = get_zoom_token()

    # First get download URL that doesn't require auth
    response = requests.get(
        download_url,
        headers={'Authorization': f'Bearer {token}'},
        allow_redirects=False
    )

    if response.status_code != 302:
        raise Exception('Expected redirect response from Zoom')

    direct_url = response.headers['Location']
    logger.debug(f"Got direct download URL: {direct_url}")

    # Return metadata for download
    return {
        'name': file_name,
        'mimeType': 'video/mp4',
        'downloadUrl': direct_url
    }
