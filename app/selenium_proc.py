import re
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


def start_chromedriver():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome('/Users/doguma/Documents/chromedriver', chrome_options=options)
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