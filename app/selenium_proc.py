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


def remove_space(string):
    return re.sub(r'\n', '', string)

def trending():
    driver = start_chromedriver()
    driver.get('https://pubmed.ncbi.nlm.nih.gov/trending/')
    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')
    time.sleep(1)

    temp = []
    for ar in soup.find_all('article'):
        temp_json = {}

        temp_json['title'] = remove_space(ar.select_one('.docsum-title').get_text())

        temp_author = remove_space(ar.select_one('.docsum-citation').get_text())
        return_author = (temp_author[:30] + '..') if len(temp_author)>30 else ''
        temp_json['authors'] = return_author

        pubmed_id = str(ar.find('a').get('href'))
        temp_json['pubmed_id'] = re.sub("/", "", pubmed_id)
        temp_json['url'] = 'https://pubmed.ncbi.nlm.nih.gov' + pubmed_id

        driver.get(temp_json['url'])
        temp_html = driver.page_source
        temp_soup = BeautifulSoup(temp_html, 'html.parser')
        temp_str = temp_soup.find('div', id='enc-abstract')
        if temp_str:
            temp_str = temp_str.get_text()
            if len(temp_str)> 300 and len(temp_author) > 25:
                temp_json['text_full'] = temp_str
                return_text = temp_str[:300] + '..'
                temp_json['text'] = return_text

                temp.append(temp_json)
    

    driver.quit()

    return temp
    

def search_keyword(keyword):
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

        temp_json['title'] = remove_space(ar.select_one('.docsum-title').get_text())

        temp_author = remove_space(ar.select_one('.docsum-citation').get_text())
        return_author = (temp_author[:30] + '..') if len(temp_author)>30 else ''
        temp_json['authors'] = return_author

        pubmed_id = str(ar.find('a').get('href'))
        temp_json['pubmed_id'] = re.sub("/", "", pubmed_id)
        temp_json['url'] = 'https://pubmed.ncbi.nlm.nih.gov' + pubmed_id

        driver.get(temp_json['url'])
        temp_html = driver.page_source
        temp_soup = BeautifulSoup(temp_html, 'html.parser')
        temp_str = temp_soup.find('div', id='enc-abstract')
        if temp_str:
            temp_str = temp_str.get_text()
            if len(temp_str)> 300 and len(temp_author) > 25:
                temp_json['text_full'] = temp_str
                return_text = temp_str[:300] + '..'
                temp_json['text'] = return_text

                temp.append(temp_json)

    driver.quit()
    
    return temp