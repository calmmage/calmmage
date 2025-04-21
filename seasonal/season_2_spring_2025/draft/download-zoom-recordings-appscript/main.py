from config import settings
from datetime import datetime, timedelta
from dotenv import load_dotenv
from download_file_with_curl import download_file_with_curl
from drive_uploader import upload_to_drive
from email_notifier import send_video_links
from generate_zoom_download_url import generate_zoom_download_url
from get_zoom_meeting_list import get_zoom_meeting_list, get_meeting_participants
from loguru import logger
from pathlib import Path
from sheets_tracker import is_recording_processed, track_recording
from youtube_uploader import upload_to_youtube, is_youtube_enabled


def process_zoom_recordings(from_date=None, to_date=None):
    """Process Zoom recordings within date range"""
    # Use settings if provided, otherwise use defaults
    if from_date is None:
        from_date = settings.START_DATE or datetime.now() - timedelta(days=settings.DEFAULT_DAYS_BACK)
    if to_date is None:
        to_date = settings.END_DATE or datetime.now()

    logger.info(f"Processing recordings from {from_date.isoformat()} to {to_date.isoformat()}")
    meetings = get_zoom_meeting_list(from_date, to_date)

    # Process each meeting
    for meeting in meetings:
        logger.info(f"\nProcessing meeting: {meeting['topic']} ({meeting['start_time']})")

        # Get participants
        try:
            participants = get_meeting_participants(meeting['uuid'])
            participant_count = len(participants)
            logger.info(f"Found {participant_count} participants")
        except Exception as e:
            logger.warning(f"Could not get participants: {e}")
            participant_count = None

        # First process video recordings
        video_recordings = [r for r in meeting['recording_files'] if r['file_type'] == 'MP4']
        logger.debug(f"Found {len(video_recordings)} video recordings")

        for recording in video_recordings:
            if settings.ENABLE_SHEETS_TRACKING and is_recording_processed(recording['id']):
                logger.debug(f"Skipping already processed video: {recording['id']}")
                continue

            # Generate filename with participant count
            file_name = f"{meeting['start_time'].split('T')[0]} - {meeting['topic']}"
            if participant_count:
                file_name += f" ({participant_count} participants)"
            if len(video_recordings) > 1:
                file_name += f" - {recording['recording_type']}"
            file_name += ".mp4"

            # Get direct download URL
            file_metadata = generate_zoom_download_url(recording['download_url'], file_name)

            # Download file
            file_path = download_file_with_curl(file_metadata)

            # Upload to Drive
            drive_info = upload_to_drive(file_path)
            logger.info(f"Uploaded to Drive: {drive_info['url']}")

            # Upload to YouTube if enabled
            youtube_info = None
            if is_youtube_enabled():
                # Add participant info to description
                description = f"Zoom recording from {meeting['start_time'].split('T')[0]}"
                if participant_count:
                    description += f"\nParticipants: {participant_count}"
                
                youtube_info = upload_to_youtube(
                    file_path,
                    file_name,
                    description
                )
                logger.info(f"Uploaded to YouTube: {youtube_info['url']}")

            # Track in sheet if enabled
            if settings.ENABLE_SHEETS_TRACKING:
                track_recording(
                    date=meeting['start_time'],
                    topic=meeting['topic'],
                    recording_id=recording['id'],
                    drive_link=drive_info['url'],
                    youtube_link=youtube_info['url'] if youtube_info else ''
                )

            # Send email notification if enabled
            if settings.ENABLE_EMAIL_NOTIFICATIONS:
                send_video_links(
                    topic=meeting['topic'],
                    date=meeting['start_time'],
                    drive_link=drive_info['url'],
                    youtube_link=youtube_info['url'] if youtube_info else ''
                )

            # Clean up
            file_path.unlink()

        # Then process audio recordings
        audio_recordings = [r for r in meeting['recording_files'] if r['file_type'] == 'M4A']
        logger.debug(f"Found {len(audio_recordings)} audio recordings")

        for recording in audio_recordings:
            if settings.ENABLE_SHEETS_TRACKING and is_recording_processed(recording['id']):
                logger.debug(f"Skipping already processed audio: {recording['id']}")
                continue

            # Generate filename with participant count
            file_name = f"{meeting['start_time'].split('T')[0]} - {meeting['topic']}"
            if participant_count:
                file_name += f" ({participant_count} participants)"
            if len(audio_recordings) > 1:
                file_name += f" - {recording['recording_type']}"
            file_name += ".m4a"

            # Get direct download URL
            file_metadata = generate_zoom_download_url(recording['download_url'], file_name)

            # Download file
            file_path = download_file_with_curl(file_metadata)

            # Upload to Drive
            drive_info = upload_to_drive(file_path)
            logger.info(f"Uploaded to Drive: {drive_info['url']}")

            # Track in sheet if enabled
            if settings.ENABLE_SHEETS_TRACKING:
                track_recording(
                    date=meeting['start_time'],
                    topic=meeting['topic'],
                    recording_id=recording['id'],
                    drive_link=drive_info['url']
                )

            # Clean up
            file_path.unlink()


if __name__ == "__main__":
    # Load environment variables
    load_dotenv()

    # Create downloads directory
    settings.DOWNLOADS_DIR.mkdir(exist_ok=True)

    try:
        process_zoom_recordings()  # Will use settings by default
    finally:
        # Clean up downloads directory if empty
        if settings.DOWNLOADS_DIR.exists() and not any(settings.DOWNLOADS_DIR.iterdir()):
            settings.DOWNLOADS_DIR.rmdir()
