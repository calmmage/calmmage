import pickle
from pathlib import Path

SAMPLE_DIR = Path(__file__).parent / "mocking_pyrogram_message_types/sample_messages"


def get_file_ids():
    files_to_check = [
        "sample_audio_attached.pkl",
        "sample_video_attached.pkl",
        "sample_document_attached.pkl",
    ]

    for file_name in files_to_check:
        file_path = SAMPLE_DIR / file_name
        print(f"\n=== {file_name} ===")

        with open(file_path, "rb") as f:
            msg = pickle.load(f)

        # Check each media type
        for attr in ["document", "audio", "video"]:
            media = getattr(msg, attr, None)
            if media:
                file_id = media.file_id
                short_id = file_id[-12:]
                original_name = getattr(media, "file_name", "N/A")

                print(f"{attr}:")
                print(f"  file_id: {file_id}")
                print(f"  short_id (last 12): {short_id}")
                print(f"  original_name: {original_name}")

                if original_name != "N/A" and "." in original_name:
                    ext = original_name.split(".")[-1]
                    print(f"  shortened name: {attr}_{short_id}.{ext}")


if __name__ == "__main__":
    get_file_ids()
