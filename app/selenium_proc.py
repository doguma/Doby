import re
import os, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


def start_chromedriver():
    options = webdriver.ChromeOptions()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument('headless')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=options)
    return driver


def trending():
    driver = start_chromedriver()
    driver.get('https://pubmed.ncbi.nlm.nih.gov/trending/')
    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')
    # time.sleep(1)

    temp = []
    for ar in soup.find_all('article'):
        temp_json = {}

        temp_str = ar.select_one('.docsum-title').get_text().strip("\n")
        temp_json['title'] = re.sub(r'\n', '', temp_str)

        temp.append(temp_json)

    driver.quit()

    return temp
    

def search(keyword):
    driver = start_chromedriver()
    driver.get('https://pubmed.ncbi.nlm.nih.gov/')

    time.sleep(1)
    search_box = driver.find_element_by_name('term')
    search_box.send_keys(keyword)
    search_box.submit()

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')
    
    temp = []
    for ar in soup.find_all('article'):
        temp_json = {}

        temp_str = ar.select_one('.docsum-title').get_text().strip("\n")
        temp_json['title'] = re.sub(r'\n', '', temp_str)

        temp.append(temp_json)

    driver.quit()
    
    return temp