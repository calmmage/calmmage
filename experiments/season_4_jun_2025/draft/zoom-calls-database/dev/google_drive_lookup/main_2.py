"""
THIS DOES NOT WORK
"""

from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
api_key = os.getenv("GOOGLE_DRIVE_API_KEY")

# Build Drive service with API key
drive_service = build("drive", "v3", developerKey=api_key)

# Search for the file by name
file_name = "2022-08-02 -060855 - форум.mp4"
query = f"name contains '{file_name}'"

try:
    results = (
        drive_service.files().list(q=query, fields="files(id, webViewLink)").execute()
    )
    files = results.get("files", [])
    if files:
        print("Shareable URL:", files[0].get("webViewLink"))
    else:
        print(f"File {file_name} not found.")
except Exception as e:
    print(f"Error: {e}")
