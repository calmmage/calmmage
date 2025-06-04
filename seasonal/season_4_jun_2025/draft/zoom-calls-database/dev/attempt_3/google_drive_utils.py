from typing import Optional
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pathlib import Path


def get_client(
    client_secrets_file: Optional[Path] = None, credentials_file: Optional[Path] = None
) -> GoogleDrive:
    """Get authenticated Google Drive client."""
    if client_secrets_file is None:
        client_secrets_file = Path("client_secrets.json")
    if credentials_file is None:
        credentials_file = Path("google_drive_creds.json")

    gauth = GoogleAuth()
    gauth.settings["client_config_file"] = client_secrets_file
    gauth.LoadCredentialsFile(credentials_file)

    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
        gauth.SaveCredentialsFile(credentials_file)
    else:
        gauth.Refresh()

    return GoogleDrive(gauth)


def find_file(
    file_name: str, drive: Optional[GoogleDrive] = None, ignore_trash: bool = True
) -> Optional[dict]:
    """Find file by name in Google Drive."""
    if drive is None:
        drive = get_client()

    # Escape single quotes in filename for Google Drive API query
    escaped_file_name = file_name.replace("'", "\\'")
    query = f"title contains '{escaped_file_name}'"
    if ignore_trash:
        query += " and trashed=false"

    file_list = drive.ListFile({"q": query}).GetList()

    if len(file_list) > 1:
        raise ValueError(f"Multiple files found for {file_name}: {file_list}")
    if len(file_list) == 0:
        raise ValueError(f"No files found for {file_name}")
    return file_list[0]
