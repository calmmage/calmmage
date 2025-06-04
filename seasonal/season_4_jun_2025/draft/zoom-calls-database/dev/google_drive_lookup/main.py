from lib import get_client, find_file
from pathlib import Path

# Get authenticated client
drive = get_client(
    client_secrets_file=Path(__file__).parent / "client_secrets.json",
    credentials_file=Path(__file__).parent / "google_drive_creds.json",
)

# Search for the file
file_name = "2022-08-02 -060855 - форум.mp4"
file = find_file(file_name, drive)

# Get shareable link
if file:
    shareable_link = file["alternateLink"]
    print("Shareable URL:", shareable_link)
else:
    print(f"File {file_name} not found.")
