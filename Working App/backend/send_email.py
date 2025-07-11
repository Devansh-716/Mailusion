import os
from dotenv import load_dotenv
from email.message import EmailMessage
from email.utils import formataddr
import ssl #for security
import smtplib #used in sending email

load_dotenv() #loading the variables in .env to the environment

sender_mail = os.getenv("SENDER_MAILID")
sender_pass = os.getenv("EMAIL_PASS")
receiver_mail = 'agarwaldevansh1981@gmail.com'

def send_email(receiver_mail, subject, body):

    try:
        em = EmailMessage() #an object that will be used to write email
        em['From'] = formataddr(("Mailusion", f"{sender_mail}"))
        em['To'] = receiver_mail
        em['Subject'] = subject 
        em.set_content(body)

        context = ssl.create_default_context() #creates a secure context 

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(sender_mail, sender_pass) #logging into senders mail id
            smtp.sendmail(sender_mail, receiver_mail, em.as_string()) 
        return True
    except Exception as e:
        print ("status: failed","error:", str(e))

if __name__ == "__main__":
    send_email(receiver_mail,
               subject = "Wrong mail",
               body = '''Sorry for this mail. Something went wrong!''')
