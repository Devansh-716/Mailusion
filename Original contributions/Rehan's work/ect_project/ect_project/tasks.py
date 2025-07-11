
from celery import Celery
import smtplib
from email.mime.text import MIMEText
from config import SMTP_SERVER, SMTP_PORT, SMTP_EMAIL, SMTP_PASSWORD, LOG_DIR
import os
import logging

#configure logging
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "email_logs.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = Celery("email_tasks", broker="amqp://guest:guest@localhost:5672//")

app.conf.update(
    result_backend="rpc://",
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

@app.task
def send_email(recipient, subject, body):
    """Send an email to the recipient and log the status."""
    try:
        # Create email message
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = SMTP_EMAIL
        msg["To"] = recipient

        # Connect to SMTP server
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
        
        logging.info(f"Email sent to {recipient}")
        return {"status": "success", "recipient": recipient}
    except Exception as e:
        logging.error(f"Failed to send email to {recipient}: {str(e)}")
        return {"status": "failed", "recipient": recipient, "error": str(e)}