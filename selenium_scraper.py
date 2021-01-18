from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy.sql.expression import extract
import services.result_services as result_services
import services.region_services as region_services
import services.park_services as park_services
import services.availability_services as availability_services
import data.db_session as db_session  # pylint: disable = import-error
import os
import datetime

# pylint: disable = no-member


class ParkScraper:
    # Initalize the webdriver
    def __init__(self, search_definitions: dict):
        self.search_definitions = search_definitions

    def set_firefox_options(self):
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument("--headless")
        return firefox_options

    # Parse function: Scrape the webpage and store it
    def parse(self):
        self.firefox_options = self.set_firefox_options()
        session = db_session.create_session()
        for date_range in self.search_definitions.keys():
            search_def = self.search_definitions[date_range]
            print(f"Scraping for {date_range}")
            self.parse_search(search_def, session)
        session.close()

    def parse_search(self, search_def, session):
        for region in search_def["start_urls"].keys():
            self.driver = webdriver.Firefox(firefox_options=self.firefox_options)
            url = search_def["start_urls"][region]
            start_date = search_def["start_date"]
            end_date = search_def["end_date"]
            session = self.parseURL(url, region, start_date, end_date, session)
            self.driver.quit()

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

    def parseURL(self, url, region: str, start_date, end_date, session):
        self.driver.get(url)

        print("scraping " + region)

        # Automate some clicks:
        # IF THE CRAWLER ISN'T WORKING: CHECK THE NUMBERS OF THE IDs. THEY MAY HAVE CHANGED
        if self.element_exists(
            "consentButton"
        ):  # only exists if we haven't already consented
            result = self.find_and_click_element("consentButton")
            if result == False:
                return session
        result = self.find_and_click_element("filterButton")
        if result == False:
            return session
        result = self.find_and_click_element("mat-select-7")
        if result == False:
            return session
        result = self.find_and_click_element("mat-option-83")
        if result == False:
            return session
        result = self.find_and_click_element("actionSearch")
        if result == False:
            return session

        circles = []
        circles = self.driver.find_elements_by_tag_name("circle")

        for circle in circles:
            if circle.get_attribute("id") != None:
                park_id = park_services.get_id_from_name(
                    str(circle.get_attribute("id"))
                )
                if park_id == False:
                    continue
                value = self.temp_map_fill_value(str(circle.get_attribute("fill")))
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

        return session

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
