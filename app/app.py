from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date

import json
import time, os, sys
import psycopg2

from app.selenium_proc import search, trending

app = Flask(__name__)


SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://')
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Word(db.Model):
    word = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return "<Keyword: {}>".format(self.word)

db.create_all()

res = trending()
today = date.today().strftime("%b %d, %Y")


@app.route('/', methods=["GET", "POST"])
def index():

    keywords = Word.query.all()

    if request.form:
        try:
            keyword = Word(word=request.form.get("keyword"))
            db.session.add(keyword)
            db.session.commit()
        except Exception as e:
            print("Failed to add keyword")
            print(e)

    return render_template("index.html", google_html = res, today = today, keywords = keywords)


@app.route("/update", methods=["POST"])
def update():
    message = ''
    try:
        newword = request.form.get("newkeyword")
        oldword = request.form.get("oldkeyword")
        keyword = Word.query.filter_by(word=oldword).first()
        if Word.query.filter_by(word=newword).first():
            message = "duplicate keyword"
        else:
            keyword.word = newword
        db.session.commit()

    except Exception as e:
        message = "Couldn't update keywords"
        print(e)
    return redirect(request.referrer, err_message = message)


@app.route("/delete", methods=["POST"])
def delete():
    selected = request.form.get("keyword")
    word = Word.query.filter_by(word=selected).first()
    db.session.delete(word)
    db.session.commit()
    return redirect(request.referrer)


if __name__ == "__main__":
    app.run(debug=True)
