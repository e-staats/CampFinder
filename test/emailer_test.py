
import os
import sys
folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, folder)
from emailer import ParkEmailer # pylint: disable = import-error
import testing_tools
import global_test_setup

if __name__=='__main__':
    global_test_setup.prep_db()
    testing_tools.setup_all_test_data()
    emailer = ParkEmailer()
    # emailer.send_email("eric.k.staats@gmail.com","hello from python")

