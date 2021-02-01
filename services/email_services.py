from flask import url_for
import os
import templates.email.availability_message as availability_message
import services.token_services as token_service
from templates.email.BasicEmail import BasicEmailBody
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


####################### EMAILER CLASS ################################
class ParkEmailer:
    def __init__(self):
        # Create a secure SSL context
        self.sender_email = "campfinder@campfinder.me"
        self.api_key = os.environ["SENDGRID_API_KEY"]

    def send_email(self, to_address=None, subject=None, html_message=None):
        message = Mail(
            from_email=self.sender_email,
            to_emails=to_address,
            subject=subject,
            html_content=html_message,
        )
        try:
            sg = SendGridAPIClient(self.api_key)
            response = sg.send(message)
            return response
        except Exception as e:
            print(e)


####################### EMAILING FUNCTIONS ###########################
def send_activation_email(user_id, email):
    url = url_for(
        "account.activate_account",
        token=token_service.serialize_url_time_sensitive_value(
            user_id, salt="activate"
        ),
        _external=True,
    )
    subject = "CampFinder Account Activation!"
    div1 = "Welcome to CampFinder! Please click below to activate your account and start getting notified when campsites are available!"
    div2 = f"<a href='{url}'>{url}</a>"
    div3 = "We look forward to helping you get out there and get camping!"
    email_message = BasicEmailBody(div1, div2, div3)
    html = email_message.create_message()
    emailer = ParkEmailer()
    try:
        emailer.send_email(to_address=email, subject=subject, html_message=html)
        return True
    except:
        return False


def send_pw_reset_email(user_id, email):
    reset_url = url_for(
        "account.reset_pw_get",
        token=token_service.serialize_url_time_sensitive_value(
            user_id, salt="reset_password"
        ),
        _external=True,
    )
    subject = "CampFinder Password Reset"
    div1 = "Someone requested to reset the password for your CampFinder account. If you would like to reset your password, click here:"
    div2 = f"<a href='{reset_url}'>{reset_url}</a>"
    div3 = "If you didn't ask to reset your password, you should ignore this email."
    email_message = BasicEmailBody(div1, div2, div3)
    message = email_message.create_message()
    emailer = ParkEmailer()
    try:
        emailer.send_email(to_address=email, subject=subject, html_message=message)
        return True
    except:
        return False


def send_availability_notification_email():
    return