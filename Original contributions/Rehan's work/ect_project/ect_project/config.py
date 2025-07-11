
import os

# SMTP settings for sending emails (e.g., Gmail)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_EMAIL = "collespefix750@gmail.com"  # Replace with your email
SMTP_PASSWORD = "...."   # Use Gmail App Password (not regular password)

# Celery settings
CELERY_BROKER_URL = "amqp://guest:guest@localhost:5672//"  # RabbitMQ URL
CELERY_RESULT_BACKEND = "rpc://"

# Directory for logs
LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)