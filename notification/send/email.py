import smtplib
from email.message import EmailMessage
import json
import os

def send(message):
    message = json.loads(message)
    audio_fid = message["audio_fid"]

    msg = EmailMessage()
    msg.set_content(f'Audio file {audio_fid} is now ready')
    
    
    sender_address = os.environ.get("GMAIL_ID")
    sender_password = os.environ.get("GMAIL_PASSWORD")
    reciever_address = message["username"]

    msg['Subject'] = "Audio file download"
    msg['From'] = sender_address
    msg['To'] = message["username"]

    s = smtplib.SMTP('smtp.gmail.com')
    s.starttls()

    s.login(sender_address,sender_password)

    s.send_message(msg,sender_address,reciever_address)
    s.quit()