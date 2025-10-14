# email_monitor.py
import imaplib
import email
from email.header import decode_header
import os
import requests
from pdf2image import convert_from_bytes
from PIL import Image
import io
import dotenv
import time

dotenv.load_dotenv()

# Email credentials
IMAP_SERVER = "imap.gmail.com"
EMAIL_USER = os.getenv("EMAIL_USER")       # Your email
EMAIL_PASS = os.getenv("EMAIL_PASS")       # App password or normal password

# FastAPI endpoint
UPLOAD_URL = "http://127.0.0.1:8000/upload-invoice/"

# Folder to save attachments temporarily
ATTACHMENT_DIR = "attachments"
os.makedirs(ATTACHMENT_DIR, exist_ok=True)

def process_attachment(file_data, filename):
    """Send image to FastAPI upload endpoint"""
    files = {}

    if filename.lower().endswith(".pdf"):
        # Convert PDF to images
        images = convert_from_bytes(file_data)
        for i, img in enumerate(images):
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG")
            buffer.seek(0)
            files = {"file": (f"{filename}_{i}.jpeg", buffer, "image/jpeg")}
            resp = requests.post(UPLOAD_URL, files=files)
            print(resp.json())
    else:
        files = {"file": (filename, io.BytesIO(file_data), "image/jpeg")}
        resp = requests.post(UPLOAD_URL, files=files)
        print(resp.json())

def check_email():
    """Connect to inbox and process new invoice attachments"""
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_USER, EMAIL_PASS)
    mail.select("inbox")

    # Search unseen emails with 'invoice' in subject
    status, messages = mail.search(None, '(UNSEEN SUBJECT "invoice")')
    email_ids = messages[0].split()

    for e_id in email_ids:
        res, msg_data = mail.fetch(e_id, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")
        print("Processing email:", subject)

        for part in msg.walk():
            if part.get_content_maintype() == "multipart":
                continue
            if part.get("Content-Disposition") is None:
                continue
            filename = part.get_filename()
            if filename:
                file_data = part.get_payload(decode=True)
                try:
                    process_attachment(file_data, filename)
                except Exception as e:
                    print(f"Error processing {filename}: {e}")

    mail.logout()

if __name__ == "__main__":
    while True:
        try:
            check_email()
        except Exception as e:
            print("Error checking email:", e)
        # Poll every 1 minute
        time.sleep(60)
