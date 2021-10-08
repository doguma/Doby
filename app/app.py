from flask import Flask, render_template
from datetime import date

import time, os
import psycopg2

from app.selenium_proc import search, trending

app = Flask(__name__)


DATABASE_URL = os.environ['postgres://lwtngwvvvflocb:19903cd3c1362eb18aadd3dc9225827123278ca939e0df869d7852c8241bc909@ec2-44-196-8-220.compute-1.amazonaws.com:5432/dd340sme9uu5or']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')


@app.route('/')
def index():

    res = trending()
    today = date.today()
    today = today.strftime("%b %d, %Y")
    return render_template("index.html", google_html = res, today = today)

if __name__ == "__main__":

    app.run(debug=True)
