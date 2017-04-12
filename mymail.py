"""##################################################################################
Anto .I. Lonappan
Nov 16 16.

USAGE:
1. Import this file      :  from emailclient import *
2. Send email            :  send('to@example.com','filename.extension')
3. Multiple destination  :  send(['to1@example.com','to2@example.com'],'filename.extension')
######################################################################################"""


import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
COMMASPACE = ', '


def send(emailto,fileToSend):
    # For gmail the username below can just be your user name, you can remove @gmail.com, this is only for other email clients
    # If above method is not working add @gmail.com or check forwarding is allowed or not in your gmail settings
    emailfrom = 'from email'
    username = 'username'
    password = 'password'
    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = COMMASPACE.join(emailto)
    msg["Subject"] = "Automated python mail"
    msg.preamble = "Automated python mail"

    ctype, encoding = mimetypes.guess_type(fileToSend)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"
  
    maintype, subtype = ctype.split("/", 1)

    if maintype == "text":
       fp = open(fileToSend)
        # Note: we should handle calculating the charset
       attachment = MIMEText(fp.read(), _subtype=subtype)
       fp.close()
    elif maintype == "image":
        fp = open(fileToSend, "rb")
        attachment = MIMEImage(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "audio":
        fp = open(fileToSend, "rb")
        attachment = MIMEAudio(fp.read(), _subtype=subtype)
        fp.close()
    else:
        fp = open(fileToSend, "rb")
        attachment = MIMEBase(maintype, subtype)
        attachment.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
    msg.attach(attachment)

    server = smtplib.SMTP("smtp server:port")#for gmail change it to 'smtp.gmail.com'
    server.starttls()
    server.login(username,password)
    server.sendmail(emailfrom, emailto, msg.as_string())
    server.quit()
