from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import services.result_services as result_services  # pylint: disable = import-error
import services.park_services as park_services  # pylint: disable = import-error
import services.availability_services as availability_services  # pylint: disable = import-error
import data.db_session as db_session  # pylint: disable = import-error
import scraper.parse_results as parse_results  # pylint: disable = import-error
import datetime
import os
import time

# pylint: disable = no-member


class ParkScraper:
    # Initalize the webdriver
    def __init__(self, search_definitions: dict, adhoc=False):
        self.search_definitions = search_definitions
        self.adhoc = adhoc
        self.results_dict = {}

    def set_firefox_options(self):
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument("--headless")
        return firefox_options

    # Parse function: Scrape the webpage and store it
    def parse(self):
        self.firefox_options = self.set_firefox_options()

        # HACKY: I'm having trouble setting the permissions on the log file in
        # Linux, so I just send it to /dev/null. I should figure out how to
        # actually handle this.
        log_path = os.path.join("/", "dev", "null")
        if os.path.exists(log_path) == False:
            log_path = "geckodriver.log"
        self.driver = webdriver.Firefox(
            firefox_options=self.firefox_options, service_log_path=log_path
        )
        self.driver.set_window_size(1580, 1080)

        for date_range in self.search_definitions.keys():
            search_def = self.search_definitions[date_range]
            print(f"Scraping for {date_range}")
            self.parse_search(search_def)

        self.driver.quit()
        return

    def parse_search(self, search_def):
        self.parseURLs(search_def)
        if self.adhoc == False:
            self.add_result_in_db(search_def)
            parse_results.process_result(
                search_def["start_date"],
                search_def["end_date"],
                search_def["parks"],
                search_def["owner_id"],
            )
        return

    def add_result_in_db(self, search_def):
        session = db_session.create_session()
        result = result_services.find_result(
            search_def["start_date"],
            search_def["end_date"],
        )
        if result == None:
            result = result_services.create_result(
                search_def["start_date"],
                search_def["end_date"],
                datetime.datetime.now(),
            )
            session.add(result)
        else:
            result.retrieval_time = datetime.datetime.now()

        session.commit()
        session.close()
        return

    def parseURLs(self, search_def):
        for region in search_def["start_urls"].keys():
            before = time.perf_counter()
            url = search_def["start_urls"][region]
            self.driver.get(url)
            print("- scraping " + region, end="...")
            success = self.click_through_options()
            if success == False:
                continue  # sometimes the clicks just fail, and it's easier to give up and move on.

            circles = self.get_circles()

            for circle in circles:
                if circle.get_attribute("id") == None:
                    return
                park_name = str(circle.get_attribute("id"))
                park_id = park_services.get_id_from_name(park_name)
                if park_id == None:
                    continue
                value = self.temp_map_fill_value(str(circle.get_attribute("fill")))
                if self.adhoc == True and value == 1:
                    self.store_in_dict(park_id, park_name)
                else:
                    self.store_in_db(
                        search_def["start_date"],
                        search_def["start_date"],
                        park_id,
                        value,
                    )
            after = time.perf_counter()
            print(f"scraped in {after - before:0.4f} seconds")
        return

    def get_circles(self) -> list:
        """
        The circles on the app get updated when the filters are applied, so
        we need to get the circles, then wait for them to become stale
        (disconnected from the DOM when the underlying info changes after the
        filter is applied), then get them again.
        """
        circles = []
        circles = self.driver.find_elements_by_tag_name("circle")
        try:
            WebDriverWait(self.driver, 10).until(EC.staleness_of(circles[0]))
        except:
            print("scraping time out waiting for filters to be applied")
            return []
        circles = self.driver.find_elements_by_tag_name("circle")
        return circles

    def store_in_dict(self, park_id, value) -> None:
        self.results_dict[park_id] = value
        return

    def store_in_db(self, start_date, end_date, park_id, value) -> None:
        session = db_session.create_session()
        availability = availability_services.find_availability(
            start_date, end_date, park_id
        )
        if availability == None:
            availability = availability_services.create_availability(
                start_date, end_date, park_id, value
            )
            session.add(availability)
        else:
            availability.availability = value
        session.commit()
        session.close()
        return

    def click_through_options(self):
        # accept cookies
        if self.element_exists("consentButton"):
            result = self.find_and_click_element("consentButton")
            if result == False:
                return False

        # # open up the options panel
        # result = self.find_and_click_element("filterButton")
        # if result == False:
        #     return False

        # # open ADA menu
        # result = self.find_and_click_element("mat-select-6")
        # if result == False:
        #     return False

        # # select No (used to be mat-option-83)
        # result = self.find_and_click_element("mat-option-79")
        # if result == False:
        #     return False

        # click Search
        result = self.find_and_click_element("actionSearch")
        if result == False:
            return False

        return True

    def element_exists(self, element_id):
        try:
            WebDriverWait(self.driver, 1).until(
                EC.presence_of_element_located((By.ID, element_id))
            )
            return True  # would throw an exception if not found
        except:
            return False

    def find_and_click_element(self, element_id):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, element_id))
            )
        except:
            self.driver.quit()
            print(f"Exception finding {element_id}")
            return False
        element.click()

        return True

    def temp_map_fill_value(self, fill_value: str) -> int:
        value_map = {
            "icon-available": 1,
            "icon-unavailable": 0,
            "icon-invalid": 0,
            "icon-not-operating": 0,
        }

        if fill_value in value_map.keys():
            return value_map[fill_value]
        else:
            return 0

    def get_results_dict(self) -> dict:
        return self.results_dict
