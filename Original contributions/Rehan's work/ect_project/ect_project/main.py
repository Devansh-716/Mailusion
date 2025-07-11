# main.py
# Purpose: Main script to test and run the ECT project.
from tasks import send_email
from tracker import save_metrics
import time

def test_email_campaign():
    """Test the email campaign by sending emails to a sample list."""
    recipients = ["ahmedcollegework@gmail.com", "rehanahmad0486@gmail.com"]  # Replace with real emails
    subject = "Welcome to ECT!"
    body = "This is a test email from the EmailCampaign Tracker."
    
    for recipient in recipients:
        result = send_email.delay(recipient, subject, body)
        print(f"Task for {recipient}: Task ID {result.id}")
    
    # Wait for tasks to complete
    time.sleep(5)
    
    # Print metrics
    metrics = save_metrics()
    print("Campaign Metrics:", metrics)

if __name__ == "__main__":
    test_email_campaign()