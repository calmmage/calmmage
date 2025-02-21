import os
import smtplib
from config import settings
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from loguru import logger

def send_video_links(topic: str, date: str, drive_link: str = '', youtube_link: str = ''):
    """Send notification with video links"""
    if not settings.ENABLE_EMAIL_NOTIFICATIONS:
        return

    subject = f"Zoom Recording Processed: {topic}"
    body = f"Your Zoom recording from {date} has been processed:\n\n"

    if drive_link:
        body += f"Google Drive: {drive_link}\n"
    if youtube_link:
        body += f"YouTube: {youtube_link}\n"

    body += "\nOriginal recording will be automatically deleted from Zoom after 30 days."

    # Create message
    msg = MIMEMultipart()
    msg['From'] = settings.EMAIL_FROM
    msg['To'] = settings.EMAIL_TO
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Send email
        with smtplib.SMTP_SSL(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
        logger.debug(f"Sent email notification for: {topic}")
        return True
    except Exception as e:
        logger.error(f"Error sending notification for {topic}: {e}")
        return False
