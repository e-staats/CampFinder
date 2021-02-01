import os
import sys

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, folder)
from services.email_services import ParkEmailer  # pylint: disable = import-error
from templates.email.BasicEmail import BasicEmailBody  # pylint: disable = import-error
import testing_tools
import global_test_setup


if __name__ == "__main__":
    global_test_setup.prep_db()
    testing_tools.setup_all_test_data()
    message = BasicEmailBody("testing!", "test 2", "test 3")
    html = message.create_message()
    emailer = ParkEmailer()
    emailer.send_email(
        to_address="eric.k.staats@gmail.com", subject="testing", html_message=html
    )
