# Importing
from random import randint
from time import sleep
from csv import reader
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

#  Variables
browser_file_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
search_engine_url = "https:www.google.com"

accept_cookie_xpath = "//*[@id=\"L2AGLb\"]/div"
search_bar_xpath = "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input"

url_class = "MjjYud"

#  Initialise
if __name__ == "__main__":
    with open('concatenated search .csv') as csvfile:
        spamreader = reader(csvfile, delimiter=',')
        for row in spamreader:
            # Randomise wait time between clicks
            time_to_sleep = randint(3, 10)

            # Creating an instance
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            chrome_options = Options()
            chrome_options.add_argument("--window-size=1100,1000")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
            driver.get(browser_file_location)
            driver.get(search_engine_url)
            sleep(time_to_sleep)

            # Accept cookie policy
            driver.find_element(By.XPATH, accept_cookie_xpath).click()
            sleep(time_to_sleep)

            # Search current row in browser
            search_query = driver.find_element(By.XPATH, search_bar_xpath)
            search_query.send_keys(row)
            sleep(time_to_sleep)

            # Query to obtain links
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            search = soup.find_all('div', class_=url_class)
            for h in search:
                with open('urls.csv', 'a') as fd:
                    fd.write(h.a.get('href'))
                    fd.write('\n')

            driver.quit()
