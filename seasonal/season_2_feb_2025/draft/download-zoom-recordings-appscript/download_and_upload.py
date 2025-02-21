import os
import pickle
import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from pathlib import Path
from urllib.parse import urlparse, parse_qs

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.file']


def get_google_creds():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds


def download_file(url, output_path):
    """Download file using curl command"""
    print(f"Downloading to {output_path}...")

    # Use curl with progress bar and follow redirects
    curl_cmd = [
        'curl',
        '--location',  # follow redirects
        '--verbose',  # show detailed output
        '--progress-bar',  # show progress
        '--output', str(output_path),  # output file
        '--write-out', '\nDownload stats:\n'
                       'Response code: %{response_code}\n'
                       'Size downloaded: %{size_download} bytes\n'
                       'Average speed: %{speed_download} bytes/sec\n',  # detailed stats
        url
    ]

    import subprocess
    try:
        result = subprocess.run(curl_cmd, check=True, capture_output=True, text=True)
        print("\nCurl stdout:")
        print(result.stdout)
        if result.stderr:
            print("\nCurl detailed output:")
            print(result.stderr)

        # Check if file exists and has size
        if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
            raise Exception("Download failed - file is empty or missing")

        size = os.path.getsize(output_path)
        print(f"\nFinal file size: {size / (1024 * 1024):.2f} MB")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"Download failed with exit code {e.returncode}")
        print("\nCurl stdout:")
        print(e.stdout)
        print("\nCurl stderr:")
        print(e.stderr)
        raise


def upload_to_drive(file_path, folder_name="Zoom Recordings"):
    """Upload file to Google Drive"""
    print(f"Uploading {file_path} to Drive...")

    creds = get_google_creds()
    service = build('drive', 'v3', credentials=creds)

    # Get or create folder
    folder_id = None
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
    results = service.files().list(q=query).execute()
    folders = results.get('files', [])

    if not folders:
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = service.files().create(body=folder_metadata, fields='id').execute()
        folder_id = folder.get('id')
    else:
        folder_id = folders[0]['id']

    # Upload file
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [folder_id]
    }

    media = MediaFileUpload(
        file_path,
        mimetype='video/mp4',
        resumable=True,
        chunksize=256 * 1024  # 256KB chunks
    )

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id,name,size'
    ).execute()

    print(f"Upload complete! File ID: {file.get('id')}")
    print(f"Size: {file.get('size', 'unknown')} bytes")
    return file


def main():
    # Your Zoom download URL
    zoom_url = "https://ssrweb.zoom.us/replay04/2024/10/22/426D060F-C418-4C75-B9FE-EE25A0CB4E8B/GMT20241022-151248_Recording_1920x1030.mp4?response-content-disposition=attachment&response-content-type=application%2Foctet-stream&response-cache-control=max-age%3D0%2Cs-maxage%3D86400&fid=s9zmg9T54x3MGKhdbxM4vbbqdgRSFjVLv3FL5iFQciDKGV6wzUPHdM6zd4fMVCZ32ocOJYbBzzgZZli0.UTAvHW8KjvelSwjo&tid=v=2.0;clid=us06;rid=WEB_160d1852c95fab6d3b9b3c1c6c95c280&Policy=eyJTdGF0ZW1lbnQiOiBbeyJSZXNvdXJjZSI6Imh0dHBzOi8vc3Nyd2ViLnpvb20udXMvcmVwbGF5MDQvMjAyNC8xMC8yMi80MjZEMDYwRi1DNDE4LTRDNzUtQjlGRS1FRTI1QTBDQjRFOEIvR01UMjAyNDEwMjItMTUxMjQ4X1JlY29yZGluZ18xOTIweDEwMzAubXA0P3Jlc3BvbnNlLWNvbnRlbnQtZGlzcG9zaXRpb249YXR0YWNobWVudCZyZXNwb25zZS1jb250ZW50LXR5cGU9YXBwbGljYXRpb24lMkZvY3RldC1zdHJlYW0mcmVzcG9uc2UtY2FjaGUtY29udHJvbD1tYXgtYWdlJTNEMCUyQ3MtbWF4YWdlJTNEODY0MDAmZmlkPXM5em1nOVQ1NHgzTUdLaGRieE00dmJicWRnUlNGalZMdjNGTDVpRlFjaURLR1Y2d3pVUEhkTTZ6ZDRmTVZDWjMyb2NPSlliQnp6Z1pabGkwLlVUQXZIVzhLanZlbFN3am8mdGlkPXY9Mi4wO2NsaWQ9dXMwNjtyaWQ9V0VCXzE2MGQxODUyYzk1ZmFiNmQzYjliM2MxYzZjOTVjMjgwIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNzQwMTU1NDE5fX19XX0_&Signature=F-fo0pVZULrnCnAPCZaAZehmF0giGBgubPcG9Os1y5w8AnV1V9m8mwiMxVtedNwPT7V5cWlf~Uhxiei4rK-GstmjPUhBUwE05j-Fn5U9~WgTOANFaxjPn5SChxByFX3WXdT~MfvQ~DaQ-i-~o0kUjM~~Nsis8sw9apOHI26Yrt3iWhovVJuwqeXWD6yn4a2pz4yhuLt0omSA8pbgM0g13pWB7ypizja3LBiKeudS7fyBy6aJYHGm3OWrGRE1woiOLsbhCmGVrleIOcIhxW1g8-dYJDt6gl-DpacrYk5XkKdRjeiiM2gjrmRNg9vIGDhCvQRFNF21~qEEqPcTBHp-LA__&Key-Pair-Id=APKAJFHNSLHYCGFYQGIA"  # Will be replaced with actual URL

    # Create temp directory if it doesn't exist
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)

    # Download and upload
    try:
        file_path = temp_dir / "recording.mp4"
        download_file(zoom_url, file_path)
        upload_to_drive(file_path)
    finally:
        # Clean up
        if file_path.exists():
            file_path.unlink()
        if temp_dir.exists():
            temp_dir.rmdir()


if __name__ == "__main__":
    main()
