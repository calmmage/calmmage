import pickle
from pathlib import Path


def inspect_photo_message():
    sample_file = (
        Path(__file__).parent
        / "mocking_pyrogram_message_types/sample_messages/sample_photo_attached.pkl"
    )

    print(f"Loading pickle file: {sample_file}")
    with open(sample_file, "rb") as f:
        msg = pickle.load(f)

    print("\n=== MESSAGE OBJECT ===")
    print(f"Type: {type(msg)}")
    print(f"Has photo: {hasattr(msg, 'photo')}")
    print(f"Photo value: {msg.photo}")
    print(f"Photo type: {type(msg.photo)}")

    if msg.photo:
        print("\n=== PHOTO OBJECT DETAILS ===")
        if isinstance(msg.photo, list):
            print(f"Photo is a list with {len(msg.photo)} items")
            for i, photo in enumerate(msg.photo):
                print(f"\n--- Photo {i} ---")
                print(f"Type: {type(photo)}")
                print("All attributes:")
                for attr in dir(photo):
                    if not attr.startswith("_"):
                        try:
                            value = getattr(photo, attr)
                            if not callable(value):
                                print(f"  {attr}: {value} (type: {type(value)})")
                        except Exception as e:
                            print(f"  {attr}: <error getting value: {e}>")

            # Check the largest photo (what we use in our function)
            largest_photo = msg.photo[-1]
            print("\n=== LARGEST PHOTO (index -1) ===")
            print(f"file_id: {largest_photo.file_id}")
            print(f"file_unique_id: {getattr(largest_photo, 'file_unique_id', 'N/A')}")
            print(f"width: {getattr(largest_photo, 'width', 'N/A')}")
            print(f"height: {getattr(largest_photo, 'height', 'N/A')}")
            print(f"file_size: {getattr(largest_photo, 'file_size', 'N/A')}")

        else:
            print("Photo is not a list, single photo object:")
            print(f"Type: {type(msg.photo)}")
            print("All attributes:")
            for attr in dir(msg.photo):
                if not attr.startswith("_"):
                    try:
                        value = getattr(msg.photo, attr)
                        if not callable(value):
                            print(f"  {attr}: {value} (type: {type(value)})")
                    except Exception as e:
                        print(f"  {attr}: <error getting value: {e}>")

    print("\n=== CHECKING FOR FILE_NAME ATTRIBUTE ===")
    if msg.photo:
        photo_obj = msg.photo[-1] if isinstance(msg.photo, list) else msg.photo
        has_file_name = hasattr(photo_obj, "file_name")
        print(f"Photo has file_name attribute: {has_file_name}")
        if has_file_name:
            print(f"file_name value: {getattr(photo_obj, 'file_name')}")
        else:
            print("No file_name attribute found on photo object")

    print("\n=== OTHER MESSAGE ATTRIBUTES ===")
    print("Checking for other media types in the message:")
    media_attrs = [
        "document",
        "audio",
        "video",
        "voice",
        "video_note",
        "sticker",
        "animation",
    ]
    for attr in media_attrs:
        if hasattr(msg, attr):
            value = getattr(msg, attr)
            print(f"  {attr}: {value}")


if __name__ == "__main__":
    inspect_photo_message()
