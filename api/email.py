from email.message import EmailMessage
import ssl
import smtplib

def Email(reciever):
    email_sender = 'knightpickup@gmail.com'
    email_password = 'gdprlrunqkmcydin'
    email_receiver = reciever
    email_subject = 'Package Ready for Pickup'
    email_body = 'Your package is ready for pickup at the Knight Pickup Locker. Please come to the Knight Pickup Locker to pick up your package.'

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = email_subject
    em.set_content(email_body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())