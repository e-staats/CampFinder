from flask import url_for
import smtplib, ssl
import os
import templates.email.pw_reset_message as pw_reset_message
import templates.email.availability_message as availability_message
import services.token_services as token_service
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
def send_confirmation_email():
    return


def send_pw_reset_email(user_id, email):
    reset_url = url_for(
        "account.reset_pw_get",
        token=token_service.serialize_url_time_sensitive_value(
            user_id, salt="reset_password"
        ),
        _external=True,
    )
    print(reset_url)
    message = pw_reset_message.create_message(reset_url)
    emailer = ParkEmailer()
    try: 
        emailer.send_email(email, message)
        return True
    except smtplib.SMTPAuthenticationError as e:
        return False


def send_availability_notification_email():
    return