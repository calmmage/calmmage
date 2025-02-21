import os
import pickle
import subprocess
from config import settings
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from loguru import logger
from pathlib import Path
from zoom_api import ZoomAPI


def get_google_creds():
    """Get Google Drive credentials"""
    creds = None
    if settings.TOKEN_PATH.exists():
        with open(settings.TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not settings.CREDENTIALS_PATH.exists():
                raise FileNotFoundError(
                    "credentials.json not found. Please download it from Google Cloud Console:\n"
                    "1. Go to https://console.cloud.google.com\n"
                    "2. Create a project or select existing\n"
                    "3. Enable Drive API\n"
                    "4. Create OAuth 2.0 credentials\n"
                    "5. Download as credentials.json"
                )

            flow = InstalledAppFlow.from_client_secrets_file(
                str(settings.CREDENTIALS_PATH),
                ['https://www.googleapis.com/auth/drive.file']
            )
            creds = flow.run_local_server(port=0)

        with open(settings.TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)

    return creds


def download_file(url: str, output_path: Path) -> Path:
    """Download file using curl command"""
    logger.info(f"Downloading to {output_path}...")

    curl_cmd = [
        'curl',
        '--location',  # follow redirects
        '--verbose',  # show detailed output
        '--progress-bar',  # show progress
        '--output', str(output_path),  # output file
        '--write-out', '\nDownload stats:\n'
                       'Response code: %{response_code}\n'
                       'Size downloaded: %{size_download} bytes\n'
                       'Average speed: %{speed_download} bytes/sec\n',
        url
    ]

    try:
        result = subprocess.run(curl_cmd, check=True, capture_output=True, text=True)
        logger.info("Curl stdout:")
        logger.info(result.stdout)
        if result.stderr:
            logger.debug("Curl detailed output:")
            logger.debug(result.stderr)

        if not output_path.exists() or output_path.stat().st_size == 0:
            raise Exception("Download failed - file is empty or missing")

        size = output_path.stat().st_size
        logger.info(f"Final file size: {size / (1024 * 1024):.2f} MB")
        return output_path

    except subprocess.CalledProcessError as e:
        logger.error(f"Download failed with exit code {e.returncode}")
        logger.error("Curl stdout:")
        logger.error(e.stdout)
        logger.error("Curl stderr:")
        logger.error(e.stderr)
        raise


def upload_to_drive(file_path: Path) -> str:
    """Upload file to Google Drive"""
    creds = get_google_creds()
    service = build('drive', 'v3', credentials=creds)

    # Create folder if it doesn't exist
    folder_name = settings.GOOGLE_DRIVE_FOLDER
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }

    # Check if folder exists
    results = service.files().list(
        q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'",
        spaces='drive',
        fields='files(id, name)'
    ).execute()

    if results['files']:
        folder_id = results['files'][0]['id']
        logger.info(f"Found existing folder: {folder_name}")
    else:
        folder = service.files().create(
            body=folder_metadata,
            fields='id'
        ).execute()
        folder_id = folder['id']
        logger.info(f"Created new folder: {folder_name}")

    # Upload file
    file_metadata = {
        'name': file_path.name,
        'parents': [folder_id]
    }

    media = MediaFileUpload(
        str(file_path),
        mimetype='video/mp4',
        resumable=True
    )

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    logger.info(f"File uploaded to Drive with ID: {file['id']}")
    return file['id']


def main():
    # Initialize Zoom API client
    zoom = ZoomAPI()

    # Get meeting ID from URL or command line
    meeting_id = "your_meeting_id"  # Replace with actual meeting ID

    # Get fresh download URL
    download_url = zoom.get_download_url(meeting_id)
    logger.info(f"Got fresh download URL from Zoom API")

    # Create temp directory
    temp_dir = settings.TEMP_DIR
    temp_dir.mkdir(exist_ok=True)

    # Download and upload
    try:
        file_path = temp_dir / "recording.mp4"
        download_file(download_url, file_path)
        upload_to_drive(file_path)
    finally:
        # Clean up
        if file_path.exists():
            file_path.unlink()
        if temp_dir.exists() and not any(temp_dir.iterdir()):
            temp_dir.rmdir()


if __name__ == "__main__":
    # Configure logging
    logger.remove()  # Remove default handler
    logger.add(
        "download.log",
        rotation="1 day",
        retention="7 days",
        level="DEBUG"
    )
    logger.add(lambda msg: print(msg), level="INFO")

    main()
