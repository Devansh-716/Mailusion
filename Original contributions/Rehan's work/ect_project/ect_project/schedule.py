# schedule.py
# Purpose: Schedule email campaigns using Celery Beat.
from celery import Celery
from celery.schedules import crontab
from tasks import send_email
from datetime import datetime
import logging
import os
from config import LOG_DIR
import os

# Configure logging
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "schedule_logs.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Initialize Celery for scheduling
app = Celery("scheduler", broker="amqp://guest:guest@localhost:5672//")

# Celery Beat configuration
app.conf.update(
    beat_schedule={
        "send-campaign-emails": {
            "task": "schedule.send_campaign",
            "schedule": crontab(hour=10, minute=15),  # Run daily at 8:10 AM
            "args": (
                ["ahmedcollegework@gmail.com", "rehanahmad0486@gmail.com"],  # Replace with your recipient list
                "Test Campaign",
                "This is a test email campaign from ECT!",
            ),
        }
    }
)

@app.task
def send_campaign(recipients, subject, body):
    """Send email campaign to a list of recipients."""
    for recipient in recipients:
        result = send_email.delay(recipient, subject, body)
        logging.info(f"Scheduled email task for {recipient}, Task ID: {result.id}")
    return {"status": "scheduled", "recipients": recipients}