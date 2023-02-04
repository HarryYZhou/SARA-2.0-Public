from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib, ssl



def attach_file_to_email(email_message, filename, extra_headers=None):
    '''Attaches a file to an email'''
    # Open attachment file and read it in binary mode, and make it a MIMEApplication class
    with open(filename, "rb") as f:
        file_attachment = MIMEApplication(f.read())
    # Add header/name to the attachments
    file_attachment.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )
    # Set up the input extra_headers for img
    # Default is None: since for regular file attachments, it's not needed
    # When given a value: the following code will run
    # Used to set the cid for image
    if extra_headers is not None:
        for name, value in extra_headers.items():
            file_attachment.add_header(name, value)
    # Attach the file to the message
    email_message.attach(file_attachment)


def create_email(sender=str, recipient=str, subject=str, body_html=str) -> object:
    """Creates an email object that can be modified/added to in order to generate an email"""
    # Create a MIME Multipart object to send an email with attachments
    email_message = MIMEMultipart()
    email_message['From'] = sender
    email_message['To'] = recipient
    email_message['Subject'] = subject

    # Attach the body of the text to the email
    email_message.attach(MIMEText(body_html, "html"))

    return email_message


def send_email(sender=str, recipient=str, email_message=object, password = str) -> None:
    """Sends an email object from the sender email to recipient email using SSL as security"""
    email_string = email_message.as_string()


    # Add SSL Security to the email
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, recipient, email_string)


