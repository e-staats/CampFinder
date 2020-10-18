import smtplib, ssl
import data.db_session
from data.user import User
import data.db_session

port = 465  # For SSL
password = "sickpassword" #This is a terrible thing
sender_email = "wiparkscraper@gmail.com"

class ParkEmailer:
    def __init__(self):
        # Create a secure SSL context
        self.context = ssl.create_default_context()

    def load_data_and_email(self):   
        return

    def send_email(self,to_address,message):        
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=self.context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, to_address, message)

    def build_message(self):
        return ""
        # return "The following parks are available for your requested dates \n" + results

    def load_data(self):
        return None