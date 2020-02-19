from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from constants import all_courts, dates


class virginia_scraper():
    def __init__(self):
        chrome_options = webdriver.ChromeOptions(); 
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']); 
        self.driver = webdriver.Chrome(options=chrome_options)

    def access_page(self):
        self.head_home()
        self.driver.find_element_by_css_selector("[value='Accept']").click()
    
    def navigate_page(self):
        count = 0
        for court in all_courts:
            count += 1 # TEMP: TO BE DELETED
            self.court_select(court)
            self.driver.find_element_by_xpath("//body").click()
            hearing_date = self.driver.find_element(By.PARTIAL_LINK_TEXT, "Hearing Date")
            hearing_date.click()
            for date in dates:
                self.date_select(date)
                self.process_page()
                break
            if count == 2: break # TEMP: TO BE DELETED
            else: self.head_home()

    def court_select(self,court_name):
        self.driver.find_element_by_css_selector("[name='selectedCourtName']").clear()
        court_field = self.driver.find_element_by_css_selector("[name='selectedCourtName']")
        court_field.click()
        court_field.send_keys(court_name)

    def date_select(self,date):
        date_field = self.driver.find_element_by_css_selector("[id='txthearingdate']")
        date_field.click()
        date_field.send_keys(date)
        date_field.send_keys(Keys.ENTER)
    
    def head_home(self): self.driver.get("https://eapps.courts.state.va.us/gdcourts/welcomePage.do")

    
    def process_page(self):
        while True:
            # check all of the boxes
            boxes = self.driver.find_elements_by_css_selector("[type='checkbox']")
            for b in boxes: b.click()
            self.driver.find_element_by_css_selector("[value='Display Case Details']").click()

            # iterate through all of the results on the page
            for _ in range(len(boxes) - 1):
                sleep(.5)         
                self.driver.find_element_by_css_selector("[value='Next']").click()
            self.driver.find_element_by_css_selector("[value='Back to Search Results']").click()

            # try to click on the next set of results, if you can't exit
            try: self.driver.find_element_by_css_selector("[value='Next']").click()
            except: break