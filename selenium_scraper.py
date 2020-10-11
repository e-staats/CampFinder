from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ParkScraper:
    # Initalize the webdriver
    def __init__(self, start_urls: dict):
        self.write_to_file("")
        self.start_urls = start_urls

    def set_firefox_options(self):
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument("--headless")
        return firefox_options

    # Parse function: Scrape the webpage and store it
    def parse(self):
        self.firefox_options = self.set_firefox_options()
        for region in self.start_urls.keys():
            self.driver = webdriver.Firefox(firefox_options=self.firefox_options)
            self.parseURL(self.start_urls[region], region)
            self.driver.quit()

    def parseURL(self, url, region: str):
        self.driver.get(url)

        print("scraping " + region)

        # Automate some clicks:
        # IF THE CRAWLER ISN'T WORKING: CHECK THE NUMBERS OF THE IDs. THEY MAY HAVE CHANGED
        if self.element_exists(
            "consentButton"
        ):  # only exists if we haven't already consented
            self.find_and_click_element("consentButton")
        self.find_and_click_element("filterButton")
        self.find_and_click_element("mat-select-7")
        self.find_and_click_element("mat-option-83")
        self.find_and_click_element("actionSearch")

        circles = []
        circles = self.driver.find_elements_by_tag_name("circle")

        for circle in circles:
            string = (
                str(circle.get_attribute("id"))
                + " - "
                + region
                + ": "
                + self.map_fill_value(str(circle.get_attribute("fill")))
                + "\n"
            )
            self.append_to_file(string)

    def write_to_file(self, stringToWrite):
        filename = "park_info.txt"
        with open(filename, "w") as f:
            f.write(stringToWrite)

    def append_to_file(self, stringToAppend):
        filename = "park_info.txt"
        with open(filename, "a") as f:
            f.write(stringToAppend)

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

    def map_fill_value(self, fill_value: str) -> str:
        value_map = {
            "icon-available": "~~AVAILABLE~~~~~~~~~~~~~~~~~~~~",
            "icon-unavailable": "unavailable",
            "icon-invalid": "unavailable",
            "icon-not-operating": "not operating",
        }

        if fill_value in value_map.keys():
            return value_map[fill_value]
        else:
            return "UNMAPPED VALUE - " + fill_value
