from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from all_courts import all_courts

dates = ["02/03/2020"]

class virginia_scraper():
    def __init__(self):
        chrome_options = webdriver.ChromeOptions(); 
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']); 
        self.driver = webdriver.Chrome(options=chrome_options)

    def access_page(self):
        self.driver.get("https://eapps.courts.state.va.us/gdcourts/caseSearch.do")
        # sleep(1)
        # login_btn = bot.driver.find_elements_by_xpath("//*[contains(text(), 'Sign in')]")
        # login_btn[0].click()
        accept_field = bot.driver.find_element_by_css_selector("[value='Accept']")
        accept_field.click()
    
    def navigate_page(self):
        for court in all_courts:
            self.court_select(court)
            hearing_date = self.driver.find_element(By.PARTIAL_LINK_TEXT, "Hearing Date")
            hearing_date.click()
            for date in dates:
                court_field = bot.driver.find_element_by_css_selector("[id='txthearingdate']")
                court_field.click()
                court_field.send_keys("02/03/2020")
                court_field.send_keys(Keys.ENTER)
                break
            break

    def court_select(self,court_name):
        court_field = self.driver.find_element_by_css_selector("[name='selectedCourtName']")
        court_field.click()
        court_field.send_keys(court_name)