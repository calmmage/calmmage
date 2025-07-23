from pydantic import BaseModel
from pathlib import Path
from typing import Optional
from datetime import datetime


class ZoomCall(BaseModel):
    # parsed info
    video_url: Optional[str] = None
    audio_url: Optional[str] = None
    chat_logs: Optional[str] = None
    ai_transcript: Optional[str] = None
    ai_summary: Optional[str] = None

    # metadata
    call_date: Optional[datetime] = None
    name: str

    # raw data
    # _s3_video_key: Optional[str] = None
    # _s3_audio_key: Optional[str] = None
    _video_path: Optional[Path] = None
    _audio_path: Optional[Path] = None
