from email.message import EmailMessage
import ssl, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 

def Notification(email_receiver):
    # Login Information
    email_sender = 'knightpickup@gmail.com'
    email_password = ''

    # Setup for HTML Email
    email_message = MIMEMultipart()
    email_message['From'] = email_sender
    email_message['To'] = email_receiver
    email_message['Subject'] = 'Package Ready for Pickup'

    # HTML Email Body
    html = open('api/email.html')
    email_message.attach(MIMEText(html.read(), 'html'))
    email_string = email_message.as_string()

    # Send Email using Gmail SMTP Server
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, email_string)
