import logging
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from pydantic import HttpUrl, EmailStr, ValidationError

from src.config import settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailGateway:
    base_template = """
        <!DOCTYPE html>
        <html lang="en">
        <body style="margin:0; padding:0; font-family:Arial,sans-serif; background-color:#f4f4f7; color:#51545E; line-height:1.6; -webkit-text-size-adjust:none; -ms-text-size-adjust:none;">
        <div style="width:100%; background-color:#f4f4f7; padding:20px 0;">
            <div style="max-width:600px; margin:0 auto; background:white; border-radius:8px; padding:40px 30px; box-shadow:0 2px 4px rgba(0,0,0,0.1);">
            <!-- Logo -->
            <div style="text-align:center; margin-bottom:30px;">
                <img src="{site_logo}" alt="Company Logo" style="max-width:100px; height:auto;">
            </div>
            <!-- Content -->
            {content}  
            <!-- Footer -->
            <div style="text-align:center; font-size:12px; color:#A8AAAF; margin-top:40px;">
                &copy;  {year} {site_name}. All rights reserved.
            </div>
            </div>
        </div>
        </body>
        </html>
    """

    templates = {
        "confirm_email": """
            <h1 style="font-size:24px; font-weight:bold; color:#333333; text-align:center; margin-bottom:20px;">
                Activate Your Account
            </h1>
            <p style="font-size:16px; color:#51545E; text-align:center; margin-bottom:30px;">
                Thank you for registering to {site_name}! Please click the button below to activate your new account.
            </p>
            <a href="{activate_url}" 
                style="display:block; width:220px; margin:0 auto; padding:15px 0; background-color:#3869D4; color:white !important; text-align:center; text-decoration:none; font-weight:bold; border-radius:6px; font-size:16px; box-shadow:0 2px 4px rgba(56, 105, 212, 0.4);"
                target="_blank" 
                rel="noopener noreferrer">
                Activate Account
            </a>
            <p style="font-size:16px; color:#51545E; text-align:center; margin-bottom:30px;">
                If you did not create this account, please ignore this email.
            </p>
        """
    }

    def __init__(self):
        self.host = settings.SMTP_HOST
        self.port = settings.SMTP_PORT
        self.sender = settings.SMTP_SENDER
        self.password = settings.SMTP_PASSWORD

    def init_message(self, recipient, subject, content):
        message = MIMEMultipart("alternative")

        message["From"] = self.sender
        message["To"] = recipient
        message["Subject"] = subject

        html_content = self.base_template.format(
            year=datetime.now().year,
            site_name=settings.SITE_NAME,
            site_logo=settings.SITE_LOGO,
            content=content,
        )

        html_content = MIMEText(html_content, "html")

        message.attach(html_content)

        return message

    def send_message(self, recipient, subject, message):
        try:
            if not subject.strip():
                raise ValueError("Subject cannot be empty")

            msg = self.init_message(recipient, subject, message)

            with smtplib.SMTP(self.host, self.port) as smtp_object:
                smtp_object.starttls()
                smtp_object.login(self.sender, self.password)
                smtp_object.sendmail(self.sender, recipient, msg.as_string())

            logger.info(f"Sent email to {recipient}")

            return True
        except (smtplib.SMTPException, ValidationError, ValueError) as e:
            logger.error(f"Failed to send email to {recipient}: {str(e)}")
            return False

    def send_email_confirmation(self, recipient, activate_url):
        content = self.templates["confirm_email"].format(
            activate_url=activate_url, site_name=settings.SITE_NAME
        )
        subject = "Confirm Your Email"

        return self.send_message(recipient, subject, message=content)
        


if __name__ == "__main__":
    email_gateway = EmailGateway()

    email_gateway.send_email_confirmation(
        "testmail@gmail.com", "https://godotengine.org/assets/press/icon_color.png"
    )
