from datetime import datetime
from itertools import chain
import os
from pathlib import Path
from typing import Optional, Dict, Any
from collections import defaultdict
from dotenv import load_dotenv
import re
from loguru import logger

# GMT20240915-124831_Recording_2080x1170
gmt_re = re.compile(r"GMT\d{8}-\d{6}.*")

# 2024-01-27 -175939_640x360.mp4
date_re = re.compile(r"\d{4}-\d{2}-\d{2} -\d{6}.*")

# Unparsed video: Recording Sep 8.mp4
# Unparsed video: Recording Sep 8 2024.mp4
# Unparsed video: Recording Sep 11 2024 171555.mp4
hr_date_re = re.compile(r"Recording \w+ \d{2} \d{4}.*")


def get_zoom_records(
    path_to_zoom_records: Optional[Path] = None,
) -> Dict[str, Dict[str, Any]]:
    logger.info("Starting zoom records discovery")

    if path_to_zoom_records is None:
        path_env = os.getenv("PATH_TO_ZOOM_RECORDS")
        if path_env is None:
            raise ValueError("PATH_TO_ZOOM_RECORDS environment variable is not set")
        path_to_zoom_records = Path(path_env)

    logger.info(f"Scanning directory: {path_to_zoom_records}")

    # first - let's look at the files here
    files = list(path_to_zoom_records.glob("*"))
    video_files = [file for file in files if file.suffix == ".mp4"]
    audio_files = [file for file in files if file.suffix == ".m4a"]
    chat_logs_files = [file for file in files if file.suffix == ".txt"]
    transcript_files = [file for file in files if file.suffix == ".vtt"]

    logger.info(f"Found {len(files)} files")
    logger.info(f"Found {len(video_files)} video files")
    logger.info(f"Found {len(audio_files)} audio files")
    logger.info(f"Found {len(chat_logs_files)} chat logs files")
    logger.info(f"Found {len(transcript_files)} transcript files")

    # now, let's try to match them up.
    records = defaultdict(dict)
    unparsed_videos = 0
    unparsed_audios = 0
    unparsed_chat_logs = 0
    unparsed_transcripts = 0
    date_regex = re.compile(r".*(\d{4}-\d{2}-\d{2}).*")
    for video_file in video_files:
        # case 1: GMT...
        if video_file.name.startswith("GMT"):
            assert gmt_re.match(video_file.name)
            key = video_file.name[:15]
            records[key]["video"] = video_file
            records[key]["date"] = datetime.strptime(key[3:11], "%Y%m%d")

        # case 2: custom name that I created...
        elif date_re.match(video_file.name):
            key = video_file.name[:18]
            records[key]["video"] = video_file
            records[key]["date"] = datetime.strptime(key[:10], "%Y-%m-%d")
        else:
            unparsed_videos += 1
            key = video_file.stem
            records[key]["video"] = video_file
            match = date_regex.match(video_file.name)
            if match:
                records[key]["date"] = datetime.strptime(match.group(1), "%Y-%m-%d")
            else:
                logger.warning(f"Unparsed date: {video_file.name}")
            continue

    for audio_file in audio_files:
        if audio_file.name.startswith("GMT"):
            assert gmt_re.match(audio_file.name)
            key = audio_file.name[:15]
            records[key]["audio"] = audio_file
        elif date_re.match(audio_file.name):
            key = audio_file.name[:18]
            records[key]["audio"] = audio_file
        else:
            # print(f"Unparsed audio: {audio_file.name}")
            unparsed_audios += 1
            key = audio_file.stem
            records[key]["audio"] = audio_file
            continue

    for chat_log_file in chat_logs_files:
        if chat_log_file.name.startswith("GMT"):
            assert gmt_re.match(
                chat_log_file.name
            ), f"GMT chat log file: {chat_log_file.name}"
            key = chat_log_file.name[:15]
            records[key]["chat_logs"] = chat_log_file
        elif date_re.match(chat_log_file.name):
            key = chat_log_file.name[:18]
            records[key]["chat_logs"] = chat_log_file
        else:
            # print(f"Unparsed chat log: {chat_log_file.name}")
            unparsed_chat_logs += 1
            key = chat_log_file.stem
            records[key]["chat_logs"] = chat_log_file
            continue

    for transcript_file in transcript_files:
        if transcript_file.name.startswith("GMT"):
            assert gmt_re.match(
                transcript_file.name
            ), f"GMT transcript file: {transcript_file.name}"
            key = transcript_file.name[:15]
            records[key]["transcript"] = transcript_file
        elif date_re.match(transcript_file.name):
            key = transcript_file.name[:18]
            records[key]["transcript"] = transcript_file
        else:
            # print(f"Unparsed transcript: {transcript_file.name}")
            unparsed_transcripts += 1
            key = transcript_file.stem
            records[key]["transcript"] = transcript_file
            continue

    done = path_to_zoom_records / "Done"

    dates_re = [
        re.compile(r".*\d{4}-\d{2}-\d{2}.*"),
        re.compile(r".*\d{4}_\d{2}_\d{2}.*"),
        # re.compile(r".*\d{8}.*"),
    ]

    # now, process subdirs
    for subdir in chain(path_to_zoom_records.glob("*"), done.glob("*")):
        if subdir.is_dir():
            for file in subdir.glob("*"):
                if file.is_file():
                    if file.suffix == ".mp4":
                        records[subdir.name]["video"] = file
                    elif file.suffix == ".m4a":
                        records[subdir.name]["audio"] = file
                    elif file.suffix == ".txt":
                        records[subdir.name]["chat_logs"] = file
                    elif file.suffix == ".vtt":
                        records[subdir.name]["transcript"] = file

            if subdir.name in records:
                # todo: parse date from subdir name
                for regex in dates_re:
                    match = regex.match(subdir.name)
                    if match:
                        year = match.group(0)[:4]
                        month = match.group(0)[5:7]
                        day = match.group(0)[8:10]
                        records[subdir.name]["date"] = datetime.strptime(
                            f"{year}-{month}-{day}", "%Y-%m-%d"
                        )
                        break
                else:
                    logger.warning(f"Unparsed date: {subdir.name}")

    # now, calculate records that are not matched up
    unmatched_videos = 0
    unmatched_audios = 0
    unmatched_chat_logs = 0
    unmatched_transcripts = 0
    matched_records = 0
    for key, record in records.items():
        target = 2
        if "date" not in record:
            logger.warning(f"No date for {key}")
            target -= 1
        if len(record) == target:
            if "video" in record:
                unmatched_videos += 1
                logger.warning(f"Unmatched video: {key}")
            elif "audio" in record:
                unmatched_audios += 1
                logger.warning(f"Unmatched audio: {key}")
            elif "chat" in record:
                unmatched_chat_logs += 1
                logger.warning(f"Unmatched chat log: {key}")
            elif "transcript" in record:
                unmatched_transcripts += 1
                logger.warning(f"Unmatched transcript: {key}")
        else:
            matched_records += 1
    logger.info(f"Found {unparsed_videos} unparsed videos")
    logger.info(f"Found {unparsed_audios} unparsed audios")
    logger.info(f"Found {unparsed_chat_logs} unparsed chat logs")
    logger.info(f"Found {unparsed_transcripts} unparsed transcripts")
    logger.info(f"Found {unmatched_videos} unmatched videos")
    logger.info(f"Found {unmatched_audios} unmatched audios")
    logger.info(f"Found {unmatched_chat_logs} unmatched chat logs")
    logger.info(f"Found {unmatched_transcripts} unmatched transcripts")

    logger.info(f"Found {matched_records} matched records")
    logger.info("Zoom records discovery completed")

    return records


if __name__ == "__main__":
    load_dotenv()

    path_env = os.getenv("PATH_TO_ZOOM_RECORDS")
    if path_env is None:
        raise ValueError("PATH_TO_ZOOM_RECORDS environment variable is not set")
    path_to_zoom_records = Path(path_env)
    records = get_zoom_records(path_to_zoom_records)

    logger.info("Sample record:")
    for key, record in records.items():
        logger.info(f"{key}: {record}")
        break
