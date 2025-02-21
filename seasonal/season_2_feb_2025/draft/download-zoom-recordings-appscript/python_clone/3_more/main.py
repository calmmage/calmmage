from datetime import datetime, timedelta
from dotenv import load_dotenv
from download_file_with_curl import download_file_with_curl
from generate_zoom_download_url import generate_zoom_download_url
from get_zoom_meeting_list import get_zoom_meeting_list


def process_zoom_recordings(from_date=None, to_date=None):
    """Process Zoom recordings within date range"""
    # Default to last 30 days if no date provided
    if from_date is None:
        from_date = datetime.now() - timedelta(days=30)
    if to_date is None:
        to_date = datetime.now()

    print(f"Processing recordings from {from_date.isoformat()} to {to_date.isoformat()}")
    meetings = get_zoom_meeting_list(from_date, to_date)

    # Process each meeting
    for meeting in meetings:
        print(f"\nProcessing meeting: {meeting['topic']} ({meeting['start_time']})")

        # First process video recordings
        video_recordings = [r for r in meeting['recording_files'] if r['file_type'] == 'MP4']
        print(f"Found {len(video_recordings)} video recordings")

        for recording in video_recordings:
            # Generate filename
            file_name = f"{meeting['start_time'].split('T')[0]} - {meeting['topic']}"
            if len(video_recordings) > 1:
                file_name += f" ({recording['recording_type']})"
            file_name += ".mp4"

            try:
                # Get direct download URL
                file_metadata = generate_zoom_download_url(recording['download_url'], file_name)

                # Download file
                output_path = download_file_with_curl(file_metadata)
                print(f"Successfully downloaded to {output_path}")

            except Exception as e:
                print(f"Failed to process recording: {e}")
                continue


if __name__ == "__main__":
    # Load environment variables
    load_dotenv()

    # Process last 7 days by default
    from_date = datetime.now() - timedelta(days=7)
    process_zoom_recordings(from_date)
