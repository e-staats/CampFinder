import os
import sys
folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, folder)
import global_test_setup
import scraper_shell # pylint: disable = import-error

if __name__=='__main__':
    global_test_setup.prep_db()
    info_dict = scraper_shell.setup_info_dict()
    scraper_shell.start_scraper(info=info_dict)

    
