from flask import url_for
import smtplib, ssl
import os
import templates.email.availability_message as availability_message
import services.token_services as token_service
from templates.email.BasicEmail import BasicEmail

####################### EMAILER CLASS ################################
class ParkEmailer:
    def __init__(self):
        # Create a secure SSL context
        self.context = ssl.create_default_context()
        self.sender_email = "wiparkscraper@gmail.com"
        self.password = os.environ["EMAIL_PASSWORD"]
        self.port = 465  # For SSL

    def send_email(self, to_address, message):
        with smtplib.SMTP_SSL(
            "smtp.gmail.com", self.port, context=self.context
        ) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, to_address, message.as_string())
        return True


####################### EMAILING FUNCTIONS ###########################
def send_confirmation_email(user_id, email):
    url = url_for(
        "account.reset_pw_get",
        token=token_service.serialize_url_time_sensitive_value(
            user_id, salt="reset_password"
        ),
        _external=True,
    )
    print(url)
    subject = "CampFinder Account Activation!"
    div1 = "Welcome to CampFinder! Please click below to activate your account and start getting notified when campsites are available!"
    div2 = f"<a href='{url}'>{url}</a>"
    div3 = "We look forward to helping you get out there and get camping!"
    email_message = BasicEmail(subject, div1, div2, div3)
    message = email_message.create_message()
    # message = pw_reset_message.create_message(reset_url)
    emailer = ParkEmailer()
    try:
        emailer.send_email(email, message)
        return True
    except smtplib.SMTPAuthenticationError as e:
        return False


def send_pw_reset_email(user_id, email):
    reset_url = url_for(
        "account.reset_pw_get",
        token=token_service.serialize_url_time_sensitive_value(
            user_id, salt="reset_password"
        ),
        _external=True,
    )
    print(reset_url)
    subject = "CampFinder Password Reset"
    div1 = "Someone requested to reset the password for your CampFinder account. If you would like to reset your password, click here:"
    div2 = f"<a href='{reset_url}'>{reset_url}</a>"
    div3 = "If you didn't ask to reset your password, you should ignore this email."
    email_message = BasicEmail(subject, div1, div2, div3)
    message = email_message.create_message()
    # message = pw_reset_message.create_message(reset_url)
    emailer = ParkEmailer()
    try:
        emailer.send_email(email, message)
        return True
    except smtplib.SMTPAuthenticationError as e:
        return False


def send_availability_notification_email():
    return