import smtplib, ssl
import os

class ParkEmailer:
    def __init__(self):
        # Create a secure SSL context
        self.context = ssl.create_default_context()
        self.sender_email = "wiparkscraper@gmail.com"
        self.password = os.environ["EMAIL_PASSWORD"]
        self.port = 465  # For SSL

    def send_email(self,to_address,message):        
        with smtplib.SMTP_SSL("smtp.gmail.com", self.port, context=self.context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, to_address, message.as_string())
        return True
