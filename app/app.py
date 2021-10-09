from flask import Flask, render_template, url_for, request, redirect, Blueprint
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
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

db = SQLAlchemy(app)

class Word(db.Model):
    word = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return "<Keyword: {}>".format(self.word)

class TrendyArticle(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    title = db.Column(db.String(300))
    abstract = db.Column(db.String(5000))

    def __repr__(self):
        return "<Article: {}>".format(self.id, self.title, self.abstract)


class SearchArticle(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    title = db.Column(db.String(300))
    abstract = db.Column(db.String(5000))

    def __repr__(self):
        return "<Article: {}>".format(self.id, self.title, self.abstract)

db.create_all()

db.session.query(TrendyArticle).delete()
res = trending()
for i in res:
    if not Word.query.filter_by(pubmed_id=i['pubmed_id']).first():
        new_article = TrendyArticle(id=i['pubmed_id'], title=i['title'], abstract=i['text'])
        db.session.add(new_article)
db.session.commit()
today = date.today().strftime("%b %d, %Y")

message = ''

@app.route('/', methods=["GET", "POST"])
def index():
    message = ''
    if request.form:
        new_word = request.form.get("add_keyword")

        if len(str(new_word)) < 2:
            message = "type in valid keyword"
        elif Word.query.filter_by(word=new_word).first():
            message = "duplicate keyword"
        else:
            new_keyword = Word(word=new_word)
            db.session.add(new_keyword)
            db.session.commit()
    keywords = Word.query.all()
    articles = TrendyArticle.query.all()
    

    return render_template("index.html", trending_articles = articles, today = today, keywords = keywords, err_message = message)



@app.route("/delete", methods=["GET", "POST"])
def delete():
    if request.form:
        selected = request.form.get("delete_keyword")
        word = Word.query.filter_by(word=selected).first()
        db.session.delete(word)
        db.session.commit()
        return redirect(url_for('.index'))


# @app.route("/search", methods=["GET", "POST"])
# def search():
#     if request.form:
#         selected = request.form.get("keyword")
#         word = Word.query.filter_by(word=selected).first()
#         db.session.delete(word)
#         db.session.commit()
#         return redirect(url_for('.index'))


if __name__ == "__main__":
    app.run(debug=True)
