import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List
import logging
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def send_email(subject: str, body: str, attachments: List[str] = None):
    try:
        logger.info("Preparing email to send")
        msg = MIMEMultipart()
        msg["From"] = SMTP_USER
        msg["To"] = TO_EMAIL
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        if attachments:
            for file_path in attachments:
                with open(file_path, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename={Path(file_path).name}",
                    )
                    msg.attach(part)
                    logger.info(f"Attached file: {file_path}")

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
            logger.info("Email sent successfully")
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        raise