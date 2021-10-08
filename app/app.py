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

message = ''

@app.route('/')
def index(message):
    
    keywords = Word.query.all()

    return render_template("index.html", trending_articles = res, today = today, keywords = keywords, err_message = message)


@app.route("/add", methods=["GET", "POST"])
def add():
    message = ''
    if request.form:
        new_word = request.form.get("keyword")

        if len(str(new_word)) < 2:
            message = "type valid keyword"
        elif Word.query.filter_by(word=new_word).first():
            message = "duplicate keyword"
        else:
            new_keyword = Word(word=new_word)
            db.session.add(new_keyword)
            db.session.commit()
            message = ''

            # keywords = Word.query.all()

    return redirect(url_for('.index', err_message=message))


@app.route("/delete", methods=["GET", "POST"])
def delete():
    if request.form:
        selected = request.form.get("keyword")
        word = Word.query.filter_by(word=selected).first()
        db.session.delete(word)
        db.session.commit()
        return redirect(url_for('.index'))


if __name__ == "__main__":
    app.run(debug=True)
