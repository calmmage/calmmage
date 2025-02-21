from config import settings
from google_auth import get_google_creds
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from pathlib import Path


def get_or_create_folder(service, folder_name: str) -> str:
    """Get or create a folder in Drive"""
    # Check if folder exists
    results = service.files().list(
        q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'",
        spaces='drive',
        fields='files(id, name)'
    ).execute()

    if results['files']:
        folder_id = results['files'][0]['id']
        print(f"Found existing folder: {folder_name}")
    else:
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = service.files().create(
            body=folder_metadata,
            fields='id'
        ).execute()
        folder_id = folder['id']
        print(f"Created new folder: {folder_name}")

    return folder_id


def upload_to_drive(file_path: Path, folder_name: str = "Zoom Recordings") -> dict:
    """Upload file to Google Drive"""
    creds = get_google_creds()
    service = build('drive', 'v3', credentials=creds)

    # Get or create folder
    folder_id = get_or_create_folder(service, folder_name)

    # Upload file
    file_metadata = {
        'name': file_path.name,
        'parents': [folder_id]
    }

    mime_type = 'video/mp4' if file_path.suffix == '.mp4' else 'audio/m4a'
    media = MediaFileUpload(
        str(file_path),
        mimetype=mime_type,
        resumable=True
    )

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, webViewLink'
    ).execute()

    print(f"File uploaded to Drive: {file['webViewLink']}")
    return {
        'id': file['id'],
        'url': file['webViewLink']
    }
