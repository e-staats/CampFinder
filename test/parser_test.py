import os
import sys
import datetime

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, folder)
import global_test_setup
import testing_tools
import scraper.parse_results as parse_results  # pylint: disable = import-error
import scraper.scraper_shell as scraper_shell  # pylint: disable = import-error

if __name__ == "__main__":
    global_test_setup.prep_db()
    testing_tools.setup_all_test_data()
    
    # test db scraper:
    print("Testing DB scraper")
    scraper_shell.scrape_searches([True])
    parse_results.process_results()
   
    # test adhoc scraper
    print("Testing dictionary scraper...")
    start_date = datetime.date.today() + datetime.timedelta(days=100)
    end_date = datetime.date.today() + datetime.timedelta(days=101)
    print(scraper_shell.scrape_searches_adhoc(start_date=start_date, end_date=end_date))
    print(scraper_shell.scrape_searches_adhoc(start_date=start_date, end_date=end_date, region_id=1))
