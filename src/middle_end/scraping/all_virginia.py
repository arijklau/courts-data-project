from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from constants import all_district_courts, dates
from case_objs import crim_case, civil_case


class virginia_scraper():
    def __init__(self):
        chrome_options = webdriver.ChromeOptions(); 
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']); 
        self.driver = webdriver.Chrome(options=chrome_options)
        self.crim_cases = []
        self.civil_cases = []

    def access_page(self):
        self.head_home()
        self.driver.find_element_by_css_selector("[value='Accept']").click()
    
    def navigate_page(self):
        count = 0
        for court in all_district_courts:
            count += 1 # TEMP: TO BE DELETED
            self.court_select(court)
            self.driver.find_element_by_xpath("//body").click()
            hearing_date = self.driver.find_elements(By.PARTIAL_LINK_TEXT, "Hearing Date")


            # Process civil cases
            hearing_date[1].click()
            for date in dates:
                self.date_select(date)
                if self.error_check():
                    print('error page found')
                    continue
                self.civil_cases.extend(self.process_page_civil(court))
                

            # # Process criminal cases
            # hearing_date[0].click()
            # for date in dates:
            #     self.date_select(date)

            #     # make sure it isn't an error page
                # if self.error_check():
                #     print('error page found')
                #     continue
            #     self.crim_cases.extend(self.process_page_crim(court))


            if count == 2: break # TEMP: TO BE DELETED
            else: self.head_home()

    def write_to_json(self):
        for case in self.crim_cases:
            print(case.to_json(), file=open("cases.json", "a"))
        
    def error_check(self):
        return self.driver.find_elements_by_css_selector("[class='errorFont']")


    def court_select(self,court_name):
        self.driver.find_element_by_css_selector("[name='selectedCourtName']").clear()
        court_field = self.driver.find_element_by_css_selector("[name='selectedCourtName']")
        court_field.click()
        court_field.send_keys(court_name)

    def date_select(self,date):
        date_field = self.driver.find_element_by_css_selector("[id='txthearingdate']")
        date_field.clear()
        date_field.click()
        date_field.send_keys(date)
        date_field.send_keys(Keys.ENTER)
    
    def head_home(self): self.driver.get("https://eapps.courts.state.va.us/gdcourts/welcomePage.do")

    
    def process_page_crim(self,court):
        all_cases = []
        breaker = 0
        while True:

            # check all of the boxes
            try:
                boxes = self.driver.find_elements_by_css_selector("[type='checkbox']")
                for b in boxes: b.click()
                self.driver.find_element_by_css_selector("[value='Display Case Details']").click()
                assert len(boxes) > 0
            except:
                print(":( => no boxes")

            # iterate through all of the results on the page
            for _ in range(len(boxes)):
                all_cases.append(self.page_helper_crim(court))
                try: self.driver.find_element_by_css_selector("[value='Next']").click()
                except: pass

            sleep(.5)
            self.driver.find_element_by_css_selector("[value='Back to Search Results']").click()

            # try to click on the next set of results, if you can't exit
            try: 
                self.driver.find_element_by_css_selector("[value='Next']").click()
            except: 
                breaker += 1
                if breaker > 1: print(":) ==> No more next pages, moving onto the next date or court!")

            if breaker > 1: 
                break

        return all_cases

    def page_helper_crim(self, court):
        def just_odds(table):
            return [table[i] for i in range(len(table)) if i % 2 == 0]

        table = [i.text for i in self.driver.find_elements_by_css_selector("td")]
        # table = [i for i in table if i != '']
        case_info = just_odds(table[table.index('Case Number :') + 1:table.index('DOB :')+2])
        charge_info = just_odds(table[table.index('Charge :')+1: table.index('Amended Case Type :')+2])
        dispo_info = just_odds(table[table.index('Final Disposition :')+1 : table.index('VASAP :')+2])
        print(f'processed case no: {case_info[0]}')
        return crim_case(case_info, charge_info, dispo_info, court)




    def process_page_civil(self,court):
        all_cases = []
        breaker = 0
        while True:

            # check all of the boxes
            try:
                boxes = self.driver.find_elements_by_css_selector("[type='checkbox']")
                for b in boxes: b.click()
                self.driver.find_element_by_css_selector("[value='Display Case Details']").click()
                assert len(boxes) > 0
            except:
                print(":( => no boxes")

            # iterate through all of the results on the page
            for _ in range(len(boxes)):
                all_cases.append(self.page_helper_civil(court))
                try: self.driver.find_element_by_css_selector("[value='Next']").click()
                except: pass

            sleep(.5)
            self.driver.find_element_by_css_selector("[value='Back to Search Results']").click()

            # try to click on the next set of results, if you can't exit
            try: 
                self.driver.find_element_by_css_selector("[value='Next']").click()
            except: 
                breaker += 1
                if breaker > 1: print(":) ==> No more next pages, moving onto the next date or court!")

            if breaker > 1: 
                break

        return all_cases

    def page_helper_civil(self, court):
        def just_odds(table): return [table[i] for i in range(len(table)) if i % 2 == 0]

        # try to get the garnishment twice
        if self.driver.find_element_by_xpath("//*[contains(text(),'Garnishee')]").text != 'Garnishee :': 
            print('going to click')
            self.driver.find_element_by_css_selector("[id='imgelapsedGarnish']").click()
        else:
            assert self.driver.find_element_by_xpath("//*[contains(text(),'Garnishee')]").text == 'Garnishee :'
            print('already here')
            print(table[table.index('Garnishee :')+1])

        table = [i.text for i in self.driver.find_elements_by_css_selector("td")]
        case_info = just_odds(table[table.index('Case Number :') + 1:table.index('Debt Type :')+2])
        judgement_info = just_odds(table[table.index('Judgment :')+1: table.index('Further Case Information :')+2])

        garnishment_info = just_odds(table[table.index('Garnishee :')+1 : table.index('Number of Checks Received :')+2])
        appeal_info = just_odds(table[table.index('Appeal Date :')+1 : table.index('Appealed By :')+2])
        hearing_info = just_odds(table[table.index('Appeal Date :')+1 : table.index('Appealed By :')+2])
        plaintiff_info = table[table.index('Plaintiff Information') + 1]
        defendant_info = table[table.index('Defendant Information') + 1]
        hearing_info = table[table.index('Hearing Information') + 1]
        print(f'processed case no: {case_info[0]}')
        return civil_case(case_info, judgement_info, garnishment_info, appeal_info, plaintiff_info, defendant_info, hearing_info, court)