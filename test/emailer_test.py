
import os
import sys
folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, folder)
from emailer import ParkEmailer # pylint: disable = import-error
import testing_tools

if __name__=='__main__':
    testing_tools.setup_all_test_data()
    emailer = ParkEmailer()
    emailer.load_data_and_email()

