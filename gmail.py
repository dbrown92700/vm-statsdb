#!python3

#
# Gmail integration requires an account with "Less Secure App Access" enabled
# in the security settings.  Consider using a dedicated gmail account for this
# app.
#

#import smtplib, email, ssl
import smtplib
import sys
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def create_email(local_user, to, subject, body, filename=None):
    # Defines function to send email using generic SMTP service
    # local_password is currently not implemented and requires a server without authentication

    if type(to) == list:
        email_to = ', '.join(to)
    else:
        email_to = to

    message = MIMEMultipart()
    message["From"] = local_user
    message["To"] = email_to
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    if filename != None:
        if type(filename) == str:
            filename == [filename]
        for file in filename:
            with open(file, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {file}",
            )
            message.attach(part)

    text = message.as_string()

    return text

def send_email(local_user, to, message, mail_server, mail_port):

    # Defines function to send email using generic SMTP service
    # local_password is currently not implemented and requires a server without authentication

    if type(to) == list:
        email_to = ', '.join(to)
    else:
        email_to = to

    try:
        server = smtplib.SMTP(mail_server, mail_port)
        server.ehlo()
    except:
        raise Exception('something went wrong with login')
        exit()

    try:
        server.sendmail(local_user, email_to, message)
        print('Email sent.')
    except:
        raise Exception('something went wrong with email send')
        exit()

    server.close()


def send_gmail(gmail_user, gmail_password, to, message):

    # Defines function to send e-mail using gmail service.  Requires gmail account settings
    # to allow "Less secure apps" or login will be rejected.

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
    except:
        print('Something went wrong with login...')
        exit()

    if type(to) == list:
        email_to = ', '.join(to)
    else:
        email_to = to

    try:
        server.sendmail(gmail_user, to, message)
        print('Email sent!')
    except:
        print('Something went wrong with email send...')
        exit()

    server.close()

if __name__ == '__main__':
    #
    # send e-mail with cli
    # python3 gmail.py gmail_user@gmail.com password 'recipient1,recipient2,etc' 'subject' 'body' 'filename'
    #
    print(sys.argv[2])
    message = create_email(sys.argv[1], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
    send_gmail(sys.argv[1], sys.argv[2], sys.argv[3], message)
