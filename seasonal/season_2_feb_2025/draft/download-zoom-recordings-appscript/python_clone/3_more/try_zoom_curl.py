import base64
import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv


def get_zoom_token():
    client_id = os.getenv('ZOOM_CLIENT_ID')
    client_secret = os.getenv('ZOOM_CLIENT_SECRET')
    account_id = os.getenv('ZOOM_ACCOUNT_ID')

    credentials = f"{client_id}:{client_secret}"
    credentials_base64 = base64.b64encode(credentials.encode()).decode()

    response = requests.post(
        'https://zoom.us/oauth/token',
        headers={'Authorization': f'Basic {credentials_base64}'},
        data={
            'grant_type': 'account_credentials',
            'account_id': account_id
        }
    )
    response.raise_for_status()
    return response.json()['access_token']


def get_zoom_recordings(from_date, to_date=None):
    if to_date is None:
        to_date = datetime.now()

    token = get_zoom_token()
    user_id = os.getenv('ZOOM_USER_ID', 'me')

    # Format dates as YYYY-MM-DD for Zoom API
    from_str = from_date.strftime('%Y-%m-%d')
    to_str = to_date.strftime('%Y-%m-%d')

    print(f"Getting recordings from {from_str} to {to_str}")

    headers = {
        'Authorization': f'Bearer {token}'
    }

    all_meetings = []
    next_page_token = ''
    page = 1

    while True:
        page_param = f'&next_page_token={next_page_token}' if next_page_token else ''
        url = f'https://api.zoom.us/v2/users/{user_id}/recordings?from={from_str}&to={to_str}&page_size=300{page_param}'
        print(f"Fetching page {page}")

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        result = response.json()

        if result.get('meetings'):
            all_meetings.extend(result['meetings'])
            print(f"Added {len(result['meetings'])} meetings from page {page}")

        next_page_token = result.get('next_page_token', '')
        if not next_page_token:
            break

        page += 1

    print(f"Found total {len(all_meetings)} recordings")
    return all_meetings


def get_direct_download_url(download_url):
    token = get_zoom_token()

    response = requests.get(
        download_url,
        headers={'Authorization': f'Bearer {token}'},
        allow_redirects=False
    )

    if response.status_code != 302:
        raise Exception('Expected redirect response from Zoom')

    direct_url = response.headers['Location']
    print(f"Got direct download URL: {direct_url}")
    return direct_url


if __name__ == "__main__":
    load_dotenv()

    # Get last 7 days of recordings
    from_date = datetime.now() - timedelta(days=7)
    meetings = get_zoom_recordings(from_date)

    for meeting in meetings:
        print(f"\nMeeting: {meeting['topic']} ({meeting['start_time']})")
        for recording in meeting.get('recording_files', []):
            if recording['file_type'].lower() == 'mp4':
                print(f"Found MP4 recording: {recording['recording_type']}")
                direct_url = get_direct_download_url(recording['download_url'])
                print(f"Download URL: {direct_url}")
                break  # Just get the first MP4 recording
