from loguru import logger
from pathlib import Path
from s3_operations import upload_file, download_file, search_files


def main():
    # Create a test file
    test_file = Path("playground/test.txt")
    test_file.parent.mkdir(exist_ok=True)
    test_file.write_text("Hello AWS S3! This is a test file.")

    logger.info("Starting S3 operations demo...")

    # 1. Upload file
    logger.info("1. Uploading file...")
    upload_file(test_file)
    upload_file(test_file, "folder1/test1.txt")

    # 2. Search files
    logger.info("\n2. Searching for files...")
    files = search_files()
    for file in files:
        logger.info(f"Found file: {file['key']} (size: {file['size']} bytes)")

    # 3. Download file
    logger.info("\n3. Downloading files...")
    download_path = Path("playground/downloaded_test.txt")
    download_file("test.txt", download_path)


if __name__ == "__main__":
    main()
