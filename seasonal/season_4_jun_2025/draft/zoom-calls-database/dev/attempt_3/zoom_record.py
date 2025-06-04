from datetime import datetime
from pathlib import Path
from typing import Optional
from pydantic import BaseModel


class ZoomRecord(BaseModel):
    name: str

    video_url: Optional[str] = None
    audio_url: Optional[str] = None
    chat_logs_url: Optional[str] = None
    transcript_url: Optional[str] = None

    date: datetime

    ai_transcript: Optional[str] = None
    ai_summary: Optional[str] = None

    # parsed info
    _video_path: Path
    _audio_path: Optional[Path] = None
    _chat_logs_path: Optional[Path] = None
    _transcript_path: Optional[Path] = None
