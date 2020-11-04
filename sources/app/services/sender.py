import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def sender_email(receiver, url):
    smtp_server="smtp.gmail.com"
    port=587
    login=os.getenv("email_login")
    password=os.getenv("email_password")
    sender=os.getenv("email_sender")

    mail_content=rf'''Dear user, Task is complete!
Download file: {url}
Thank You

Best Regards,
Super Team
'''
    message=MIMEMultipart()
    message['From'] = receiver
    message['To'] = sender
    message['Subject'] = "Task complete"
    message.attach(MIMEText(mail_content, 'plain'))
    text=message.as_string()

    s=smtplib.SMTP(smtp_server, port)
    s.ehlo()
    s.starttls()
    s.login(login, password)  # See https://support.google.com/accounts/answer/6010255
    try:
        s.sendmail(sender, receiver, text)
    except Exception as e:
        print(e)
