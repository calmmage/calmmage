import pickle
from config import settings
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from pathlib import Path


def get_youtube_creds():
    """Get YouTube API credentials"""
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
                    "3. Enable YouTube Data API v3\n"
                    "4. Create OAuth 2.0 credentials\n"
                    "5. Download as credentials.json"
                )

            flow = InstalledAppFlow.from_client_secrets_file(
                str(settings.CREDENTIALS_PATH),
                ['https://www.googleapis.com/auth/youtube.upload']
            )
            creds = flow.run_local_server(port=0)

        with open(settings.TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)

    return creds


def is_youtube_enabled() -> bool:
    """Check if YouTube API is enabled"""
    try:
        creds = get_youtube_creds()
        service = build('youtube', 'v3', credentials=creds)
        # Try a simple API call
        service.channels().list(part='snippet', mine=True).execute()
        return True
    except Exception as e:
        if 'insufficientPermissions' in str(e):
            raise RuntimeError(
                "YouTube API permissions error. Please:\n"
                "1. Go to Google Cloud Console\n"
                "2. Enable YouTube Data API v3\n"
                "3. Add these OAuth scopes to your credentials:\n"
                "   - youtube.upload\n"
                "   - youtube.readonly\n"
                "   - youtube.force-ssl\n"
                "4. Delete token.pickle and try again"
            )
        raise  # Re-raise any other errors


def upload_to_youtube(file_path: Path, title: str, description: str = '') -> dict:
    """Upload video to YouTube"""
    if not is_youtube_enabled():
        raise Exception(
            'YouTube API is not enabled. Please:\n'
            '1. Go to Google Cloud Console\n'
            '2. Enable YouTube Data API v3\n'
            '3. Create OAuth credentials\n'
            '4. Download credentials.json'
        )

    if not description:
        description = f'Zoom recording from {title.split(" - ")[0]}'

    creds = get_youtube_creds()
    service = build('youtube', 'v3', credentials=creds)

    body = {
        'snippet': {
            'title': title,
            'description': description
        },
        'status': {
            'privacyStatus': 'unlisted'
        }
    }

    # Upload file
    media = MediaFileUpload(
        str(file_path),
        mimetype='video/mp4',
        resumable=True
    )

    request = service.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=media
    )

    response = request.execute()
    video_id = response['id']
    video_url = f'https://youtu.be/{video_id}'

    print(f"Video uploaded to YouTube: {video_url}")
    return {
        'id': video_id,
        'url': video_url
    }
