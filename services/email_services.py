from flask import url_for
import services.token_services as token_service

def send_confirmation_email():
    return

def send_pw_reset_email(user_id, email):
    reset_url = url_for('account.reset_pw_get', token=token_service.serialize_url_time_sensitive_value(user_id, salt='reset_password'), _external=True)
    print(reset_url)
    return True

def send_availability_notification_email():
    return