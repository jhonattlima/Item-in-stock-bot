# Import smtplib for the actual sending function
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email Account
email_sender_account = 'senderAccountHere@example.com'  # Change
email_sender_username = 'usernameHere'  # Change
email_sender_password = 'mailPasswordHere'  # Change
email_smtp_server = 'mail.example.com'  # Change
email_smtp_port = 587  # Change the port as required by sender email

# Email Content
email_receivers = ["mailToReceiveAlert@example.com"]  # Change
email_subject = "New item available!"


def sendMail(itemLink):

    # login to email server
    server = smtplib.SMTP(email_smtp_server, email_smtp_port)
    server.starttls()
    server.login(email_sender_username, email_sender_password)

    # For loop, sending emails to all email recipients
    for recipient in email_receivers:
        print(f"Sending email to {recipient}")
        message = MIMEMultipart('alternative')
        message['From'] = email_sender_account
        message['To'] = recipient
        message['Subject'] = email_subject
        message.attach(MIMEText(f'The link {itemLink} is now available!'))
        text = message.as_string()
        server.sendmail(email_sender_account, recipient, text)

    # All emails sent, log out.
    server.quit()
