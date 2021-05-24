from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import traceback
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import ast
import csv

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless=true')
user_agents = "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36" 
chrome_options.add_argument(user_agents)

class TdSCrapper:
    
    driver = webdriver.Chrome('chromedriver', options=chrome_options)
    csv_filename = "td-data-%s.csv" % time.strftime("%Y%m%d-%H%M%S")

    def getResponse(self):
        """
        checks popup appears or not, call get getNavYieldDataCSV method based on that
        """
        try:
            url = "https://www.td.com/ca/en/asset-management/institutional/funds/FundCard/?phoenixCode=E1600"
            self.driver.get(url)
            modal = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "termsConditions"))
            )
            # set display none
            self.driver.execute_script("document.getElementById('termsConditions').style.display = 'none';")
            # remove another popup
            btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "ensCall"))
            )
            btn.click()
            time.sleep(0.5)
            self.getNavYieldDataCSV()
        except TimeoutException:
            print('Terms & Condition modal is not found.')
            self.getNavYieldDataCSV()
        except Exception as ex:
            traceback.print_exception(type(ex), ex, ex.__traceback__)
        finally:
            self.driver.close()     

    def getNavYieldDataCSV(self):
        """
        finds title, date & amount for nav yield div and write to csv 
        """
        nav_div = self.driver.find_element_by_xpath("//div[contains(@class, 'fund-info-box')][1]")
        info_hdr_div = nav_div.find_element_by_class_name("info-header")
        title = info_hdr_div.find_element_by_xpath('div').text
        date_div = info_hdr_div.find_element_by_xpath('div[2]/span').text
        amount = self.driver.find_element_by_class_name("info-copy").find_element_by_xpath("div").text
        date_str = date_div.replace("as of ", '')
        if title and date_str and amount:
            odf = pd.DataFrame([[title, date_str, amount]], columns =['Title', 'Date', 'Amount'], dtype='str')
            odf.to_csv(self.csv_filename, index=False,  sep="\t")

def main():
    obj = TdSCrapper()
    obj.getResponse()


if __name__ == '__main__':
    main()
