import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ParkSpider(scrapy.Spider):
    name = 'parkspider'   
    # Initalize the webdriver    
    def __init__(self, start_urls):
        self.write_to_file("")
        self.start_urls=start_urls

        # Parse through each Start URLs
    def start_requests(self):
        yield scrapy.Request(url="https://google.com", callback=self.parse)  

    # Parse function: Scrape the webpage and store it
    def parse(self, response):
        for url in self.start_urls:
            self.driver = webdriver.Firefox()
            self.parseURL(url)
            self.driver.quit()       
    
    def parseURL(self, url):
        self.driver.get(url)

        #Automate some clicks:
        #IF THE CRAWLER ISN'T WORKING: CHECK THE NUMBERS OF THE IDs. THEY MAY HAVE CHANGED
        if self.element_exists("consentButton"):  #only exists if we haven't already consented
            self.find_and_click_element("consentButton")
        self.find_and_click_element("filterButton")
        self.find_and_click_element("mat-select-7")
        self.find_and_click_element("mat-option-83")
        self.find_and_click_element("actionSearch")

        circles=[]
        circles = self.driver.find_elements_by_tag_name("circle")
        
        if circles == []:
            print("~~~~NO CIRCLES~~~~")
        
        for circle in circles:
            string=str(circle.get_attribute('id'))+': '+str(circle.get_attribute('fill'))+"\n"
            self.append_to_file(string)
        

    def write_to_file(self,stringToWrite):
        filename = 'park_info.txt'
        with open(filename, 'w') as f:
            f.write(stringToWrite)

    def append_to_file(self,stringToAppend):
        filename = 'park_info.txt'
        with open(filename, 'a') as f:
            f.write(stringToAppend)

    def element_exists(self,element_id):
        try:
            WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.ID, element_id)))
            return True #would throw an exception if not found
        except: 
            return False

    def find_and_click_element(self,element_id):
        try:
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, element_id)))
        except:
            self.driver.quit()
            print(f"Exception finding {element_id}")
            return False
        element.click()
        return True
