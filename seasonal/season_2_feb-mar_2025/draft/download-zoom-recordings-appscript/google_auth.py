import pickle
from config import settings
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from pathlib import Path


def get_google_creds():
    """Get credentials for all Google APIs"""
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
                    "3. Enable required APIs:\n"
                    "   - Google Drive API\n"
                    "   - Google Sheets API\n"
                    "   - Gmail API\n"
                    "   - YouTube Data API v3\n"
                    "4. Create OAuth 2.0 credentials\n"
                    "5. Download as credentials.json"
                )

            flow = InstalledAppFlow.from_client_secrets_file(
                str(settings.CREDENTIALS_PATH),
                [
                    'https://www.googleapis.com/auth/drive.file',  # Drive file access
                    'https://www.googleapis.com/auth/spreadsheets',  # Sheets access
                    'https://www.googleapis.com/auth/gmail.send',  # Send emails
                    'https://www.googleapis.com/auth/youtube.upload',  # YouTube uploads
                    'https://www.googleapis.com/auth/youtube.readonly',  # YouTube read access
                    'https://www.googleapis.com/auth/youtube.force-ssl'  # YouTube API access
                ]
            )
            creds = flow.run_local_server(port=0)

        with open(settings.TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)

    return creds
