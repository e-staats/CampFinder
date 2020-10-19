import os
import sys
folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, folder)
import global_test_setup
import testing_tools
import parse_results # pylint: disable = import-error

if __name__=='__main__':
    global_test_setup.prep_db()
    testing_tools.setup_all_test_data()
    parse_results.process_results()

    
