import os
from email.message import EmailMessage
import ssl, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup

def notification(email_receiver, email_name):
    # Login Information
    email_sender = 'teamknightpickup@gmail.com'
    email_password = os.environ.get('EMAIL_KEY')

    # Setup for HTML Email
    email_message = MIMEMultipart()
    email_message['From'] = email_sender
    email_message['To'] = email_receiver
    email_message['Subject'] = 'Package Ready for Pickup'

    # Customize HTML Email
    custom_string = "Hello " + email_name + ", your package is ready for pickup. Please proceed to the dorm lobby to pick up your package."
    with open("api/email.html") as html_file:
        soup = BeautifulSoup(html_file, "html.parser")
        name_element = soup.find("p", class_="para", id="name")
        name_element.string = custom_string
        html_file.close()
    with open("api/email.html", "w") as html_file:
        html_file.write(str(soup))
        html_file.close()

    # HTML Email Body
    html = open('api/email.html')
    email_message.attach(MIMEText(html.read(), 'html'))
    email_string = email_message.as_string()

    # Send Email using Gmail SMTP Server
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, email_string)
