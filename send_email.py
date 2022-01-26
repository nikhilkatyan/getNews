import os
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# import nkk_tools as nkk

# req_folder_name = nkk.check_make_folder()
# filename_path = os.path.join(req_folder_name, "1212121-30054_4.txt")


def send_attach_email(subject, filename, attachment_name, tag, receiver_email):
    sender_email = "mailer@newsdiarytoday.com"
    # receiver_email = "nikhilkatyan@gmail.com"
    password = "Kat9niki"

    # Create MIMEMultipart object
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "%s - %s" % (tag, subject)
    msg["From"] = sender_email
    msg["To"] = receiver_email
    # filename = "document.pdf"

    # HTML Message Part
    html = """\
    <html>
      <body>
        <p><b>Check attachment</b>
        <br>
           This email contains attachment.
        </p>
      </body>
    </html>
    """

    part = MIMEText(html, "html")
    msg.attach(part)

    # Add Attachment
    with open(filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)

    # Set mail headers
    part.add_header(
        "Content-Disposition",
        "attachment", filename=attachment_name
    )
    msg.attach(part)

    # Create secure SMTP connection and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("sv81.ifastnet.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, msg.as_string()
        )


if __name__ == "__main__":
    pass
