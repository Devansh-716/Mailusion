import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import schedule
import time
from datetime import datetime

# *Load config from config.json*
def load_config():
    with open('config.json', 'r') as file:
        return json.load(file)

# *Function to log email sending activity*
def log_email(receiver, subject, status):
    with open('email_log.txt', 'a') as log_file:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_file.write(f"[{timestamp}] Sent to {receiver} | Subject: {subject} | Status: {status}\n")

# *Function to send email*
def send_email(receiver_emails, subject, body):
    config = load_config()
    sender_email = config['sender_email']
    password = config['password']
    smtp_server = config['smtp_server']
    smtp_port = config['smtp_port']

    # Create the email content
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(receiver_emails)  # *Support multiple receivers*
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure connection
            server.login(sender_email, password)  # Login
            server.send_message(message)  # Send email
            print(f"Email sent successfully to {receiver_emails}")
            log_email(receiver_emails, subject, "Success")  # *Log success*
    except Exception as e:
        print(f"Error sending email: {e}")
        log_email(receiver_emails, subject, f"Failed: {e}")  # *Log failure*

# *Function to schedule emails*
def schedule_email(receiver_emails, subject, body, send_time):
    # Format: "YYYY-MM-DD HH:MM" e.g., "2025-07-05 14:00"
    schedule.every().day.at(send_time.split(" ")[1]).do(
        send_email, receiver_emails=receiver_emails, subject=subject, body=body
    )
    print(f"Scheduled email to {receiver_emails} at {send_time}")

# *Main function to run the scheduler*
def main():
    # Example: Schedule an email for today at a specific time
    receiver_emails = ["rehanahmad0486@gmail.com", "ahmedcollegework@gmail.com","agarwaldevansh1981@gmail.com","busyemail4321@gmail.com"]  # *Multiple receivers*
    subject = "Scheduled Test Email"
    body = "Hello, this is an automated scheduled email from AutoMailBlaster under the project of (AUTOMATED EMAIL SENDER) Bhai, yeh ek aisa tool hai jo emails ko automatically specific time pe bhejta hai. Jaise, tu bolta hai ki “5 baje shaam ko yeh email is bande ko chala jaaye,” toh yeh apne aap us time pe email bhej dega. Isme tu ek baar settings daal deta hai (like email ID, password, etc.), aur phir yeh khud ba khud kaam karta hai. Plus, yeh log bhi rakhta hai ki kaunse emails kab bheje, success hua ya fail hua. Yeh ek chhota sa automation tool hai jo time save karta hai. !" 

    send_time = "2025-07-05 14:24"  # *Change this to your desired date and time*

    schedule_email(receiver_emails, subject, body, send_time)

    # *Run the scheduler*
    print("Scheduler started. Waiting for scheduled time...")
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()