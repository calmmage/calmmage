from config import settings
from datetime import datetime
from google_auth import get_google_creds
from googleapiclient.discovery import build
from loguru import logger
from pathlib import Path


def get_or_create_sheet():
    """Get or create tracking spreadsheet"""
    if not settings.ENABLE_SHEETS_TRACKING:
        return None

    creds = get_google_creds()
    service = build('sheets', 'v4', credentials=creds)

    # Try to open existing sheet
    if settings.SHEET_ID:
        try:
            sheet = service.spreadsheets().get(
                spreadsheetId=settings.SHEET_ID
            ).execute()
            logger.debug(f"Found existing sheet: {sheet['properties']['title']}")
            return settings.SHEET_ID
        except Exception as e:
            logger.error(f"Error opening sheet: {e}")

    # Create new sheet
    sheet = service.spreadsheets().create(body={
        'properties': {'title': 'Zoom Recordings Tracker'},
        'sheets': [{
            'properties': {'title': 'Recordings'},
            'data': [{
                'rowData': [{
                    'values': [
                        {'userEnteredValue': {'stringValue': h}}
                        for h in ['Date', 'Meeting Topic', 'Recording ID',
                                  'Drive Link', 'YouTube Link', 'Processing Date']
                    ]
                }]
            }]
        }]
    }).execute()

    sheet_id = sheet['spreadsheetId']
    logger.debug(f"Created new tracking sheet: {sheet['properties']['title']}")
    return sheet_id


def is_recording_processed(recording_id: str) -> bool:
    """Check if recording was already processed"""
    if not settings.ENABLE_SHEETS_TRACKING or not settings.SHEET_ID:
        return False

    creds = get_google_creds()
    service = build('sheets', 'v4', credentials=creds)

    # Get all recording IDs from column C (Recording ID)
    result = service.spreadsheets().values().get(
        spreadsheetId=settings.SHEET_ID,
        range='A:F'  # Get all columns to ensure sheet exists
    ).execute()

    values = result.get('values', [])
    if not values:
        return False

    # Find Recording ID column (should be 3rd column, index 2)
    recording_ids = [row[2] for row in values[1:] if len(row) > 2]  # Skip header, ensure row has enough columns
    return recording_id in recording_ids


def track_recording(date: str, topic: str, recording_id: str,
                    drive_link: str = '', youtube_link: str = ''):
    """Track processed recording in sheet"""
    if not settings.ENABLE_SHEETS_TRACKING:
        return

    if not settings.SHEET_ID:
        settings.SHEET_ID = get_or_create_sheet()
        if not settings.SHEET_ID:
            raise ValueError("Failed to create or get sheet ID")

    creds = get_google_creds()
    service = build('sheets', 'v4', credentials=creds)

    # Format date for better readability
    try:
        # Try to parse and format the date
        parsed_date = datetime.fromisoformat(date.replace('Z', '+00:00'))
        formatted_date = parsed_date.strftime('%Y-%m-%d %H:%M:%S')
    except:
        # If parsing fails, use the original date string
        formatted_date = date

    # Append row
    values = [[
        formatted_date,  # Date
        topic,  # Meeting Topic
        recording_id,  # Recording ID
        drive_link,  # Drive Link
        youtube_link,  # YouTube Link
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Processing Date
    ]]

    body = {
        'values': values
    }

    service.spreadsheets().values().append(
        spreadsheetId=settings.SHEET_ID,
        range='A:F',  # Simplified range format
        valueInputOption='RAW',
        body=body
    ).execute()

    logger.debug(f"Tracked recording in sheet: {topic}")
