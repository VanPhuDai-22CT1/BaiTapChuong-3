import os
import time
import smtplib
import shutil
import schedule
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

EMAIL_FROM = os.getenv("SENDER_EMAIL")
EMAIL_PASS = os.getenv("SENDER_PASSWORD")
EMAIL_TO = os.getenv("RECEIVER_EMAIL")

db_path = os.path.join(os.getcwd(), "database", "SQL_Dai.sqlite3")
backup_path = os.path.join(os.getcwd(), "backup")

if not os.path.exists(backup_path):
    os.makedirs(backup_path)

def notify(subject, content):
    message = MIMEMultipart()
    message["From"] = EMAIL_FROM
    message["To"] = EMAIL_TO
    message["Subject"] = subject
    message.attach(MIMEText(content, "plain"))
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as mail:
            mail.login(EMAIL_FROM, EMAIL_PASS)
            mail.sendmail(EMAIL_FROM, EMAIL_TO, message.as_string())
        print("Mail sent.")
    except Exception as err:
        print(f"Mail error: {err}")

def backup():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = os.path.join(backup_path, f"backup_{timestamp}.sqlite3")
    try:
        shutil.copy(db_path, dest)
        print(f"Backup OK: {dest}")
        notify("Backup OK", f"Backup done at {timestamp}\nFile: {dest}")
    except Exception as err:
        print(f"Backup Failed: {err}")
        notify("Backup Failed", str(err))

schedule.every().day.at("00:00").do(backup)

print("Waiting for scheduled backup...")

while True:
    schedule.run_pending()
    time.sleep(60)
