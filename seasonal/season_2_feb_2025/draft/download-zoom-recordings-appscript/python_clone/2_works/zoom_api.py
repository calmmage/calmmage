import requests
from config import settings
from loguru import logger
from typing import Optional


class ZoomAPI:
    TOKEN_URL = "https://zoom.us/oauth/token"
    API_BASE_URL = "https://api.zoom.us/v2"

    def __init__(self):
        self.client_id = settings.ZOOM_CLIENT_ID
        self.client_secret = settings.ZOOM_CLIENT_SECRET
        self.account_id = settings.ZOOM_ACCOUNT_ID
        self._access_token = None

    def _get_access_token(self) -> str:
        """Get OAuth access token from Zoom"""
        if not self._access_token:
            auth = (self.client_id, self.client_secret)
            response = requests.post(
                self.TOKEN_URL,
                auth=auth,
                data={
                    "grant_type": "account_credentials",
                    "account_id": self.account_id
                }
            )
            response.raise_for_status()
            self._access_token = response.json()["access_token"]
        return self._access_token

    def get_download_url(self, meeting_id: str, file_id: Optional[str] = None) -> str:
        """Get a fresh download URL for a recording"""
        headers = {
            "Authorization": f"Bearer {self._get_access_token()}",
            "Content-Type": "application/json"
        }

        # First get recording details
        url = f"{self.API_BASE_URL}/meetings/{meeting_id}/recordings"
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        recordings = response.json().get("recording_files", [])
        if not recordings:
            raise ValueError(f"No recordings found for meeting {meeting_id}")

        # If file_id is specified, find that specific recording
        if file_id:
            recording = next(
                (r for r in recordings if r["id"] == file_id),
                None
            )
            if not recording:
                raise ValueError(f"Recording {file_id} not found")
        else:
            # Get the first MP4 recording
            recording = next(
                (r for r in recordings if r["file_type"] == "MP4"),
                None
            )
            if not recording:
                raise ValueError("No MP4 recording found")

        # Get download URL
        download_url = recording["download_url"]
        logger.info(f"Got download URL for recording: {recording['recording_type']}")

        return download_url
