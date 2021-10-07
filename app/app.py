from flask import Flask, render_template
from datetime import date

import time
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from bs4 import BeautifulSoup
from app.selenium_proc import search, trending

app = Flask(__name__)


@app.route('/')
def index():
    # keyword = 'insulin'
    # res = search(keyword)

    res = trending()
    today = date.today()
    today = today.strftime("%b %d, %Y")
    return render_template("index.html", google_html = res, today = today)

if __name__ == "__main__":

    app.run(debug=True)
