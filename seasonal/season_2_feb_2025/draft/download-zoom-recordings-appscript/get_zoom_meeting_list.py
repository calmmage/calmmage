import requests
from config import settings
from datetime import datetime, timedelta


def get_zoom_token():
    """Get OAuth token for Zoom API"""
    credentials = f"{settings.ZOOM_CLIENT_ID}:{settings.ZOOM_CLIENT_SECRET}"
    import base64
    credentials_base64 = base64.b64encode(credentials.encode()).decode()

    response = requests.post(
        'https://zoom.us/oauth/token',
        headers={'Authorization': f'Basic {credentials_base64}'},
        data={
            'grant_type': 'account_credentials',
            'account_id': settings.ZOOM_ACCOUNT_ID
        }
    )
    response.raise_for_status()
    return response.json()['access_token']


def get_zoom_meeting_list(from_date: datetime, to_date: datetime = None) -> list:
    """Get list of Zoom recordings between dates"""
    if to_date is None:
        to_date = datetime.now()

    print(f"Original date range request: {from_date.isoformat()} to {to_date.isoformat()}")

    # Zoom API has a 30-day limit for listing recordings
    MAX_DAYS = 30
    current_from = from_date
    all_meetings = []

    while current_from < to_date:
        # Calculate chunk end date (either 30 days from start or final end date)
        chunk_end = min(
            current_from + timedelta(days=MAX_DAYS),
            to_date
        )

        print(f"Fetching chunk: {current_from.isoformat()} to {chunk_end.isoformat()}")

        token = get_zoom_token()
        headers = {
            'Authorization': f'Bearer {token}'
        }

        # Format dates as YYYY-MM-DD for Zoom API
        from_str = current_from.strftime('%Y-%m-%d')
        to_str = chunk_end.strftime('%Y-%m-%d')

        next_page_token = ''
        page = 1

        while True:
            page_param = f'&next_page_token={next_page_token}' if next_page_token else ''
            url = f'https://api.zoom.us/v2/users/{settings.ZOOM_USER_ID}/recordings?from={from_str}&to={to_str}&page_size=300{page_param}'
            print(f"Fetching page {page} from Zoom API: {url}")

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

        # Move to next chunk
        current_from = chunk_end + timedelta(days=1)

    # Sort meetings by date
    all_meetings.sort(key=lambda m: m['start_time'])

    print(f"Found total {len(all_meetings)} recordings")
    return all_meetings
