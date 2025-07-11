import os
from flask import Flask, render_template, request
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx'}

SENDER_EMAIL = 'devil2005sepl@gmail.com'
SENDER_PASSWORD = '' 
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def send_birthday_email(name, email):
    subject = 'Happy Birthday!'
    body = f"""Dear {name},

Wishing you a very Happy Birthday! Have a wonderful year ahead.

Best wishes,
Your Team
"""
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, email, msg.as_string())

def send_bill_email(name, email):
    subject = 'Your Bill/Payment Information'
    body = f"""Dear {name},

This is a reminder regarding your bill/payment. Please check the attached details or contact us for more information.

Best regards,
Your Team
"""
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, email, msg.as_string())

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    message = ""
    if 'fileUpload' not in request.files:
        message = "No file part"
        return render_template('index.html', message=message)
    file = request.files['fileUpload']
    mail_type = request.form.get('mailType')

    if file.filename == '' or not allowed_file(file.filename):
        message = "Invalid file type. Please upload an .xlsx file."
        return render_template('index.html', message=message)

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    try:
        df = pd.read_excel(filepath)
        df.columns = df.columns.str.strip()
    except Exception as e:
        message = f"Error reading Excel file: {e}"
        return render_template('index.html', message=message)

    sent_list = []
    if mail_type == 'birthday':
        df['DOB'] = pd.to_datetime(df['DOB'], errors='coerce')
        today = datetime.now()
        birthday_people = df[(df['DOB'].dt.day == today.day) & (df['DOB'].dt.month == today.month)]
        if not birthday_people.empty:
            for _, row in birthday_people.iterrows():
                send_birthday_email(row['Name'], row['Email'])
                sent_list.append(f"{row['Name']} &lt;{row['Email']}&gt;")
            message = f"Birthday emails sent to:<br>{'<br>'.join(sent_list)}"
        else:
            message = "No birthdays today. No emails sent."
    elif mail_type == 'bill':
        for _, row in df.iterrows():
            send_bill_email(row['Name'], row['Email'])
            sent_list.append(f"{row['Name']} &lt;{row['Email']}&gt;")
        message = f"Bill/payment emails sent to:<br>{'<br>'.join(sent_list)}"
    else:
        message = "Invalid mail type selected."

    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(debug=True) 
