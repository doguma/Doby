from flask import Flask, render_template, url_for, request, redirect, Blueprint
from flask_sqlalchemy import SQLAlchemy
from datetime import date

import json
import time, os, sys
import psycopg2

from app.selenium_proc import search_keyword, trending
from app.wordcloud import createcloud

app = Flask(__name__)

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://')
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

db = SQLAlchemy(app)

class Word(db.Model):
    word = db.Column(db.String(80), nullable=False, primary_key=True)

    def __repr__(self):
        return "<Keyword: {}>".format(self.word)

class TrendyArticle(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    title = db.Column(db.String(300))
    authors = db.Column(db.String(300))
    abstract = db.Column(db.String(5000))
    url = db.Column(db.String(500))

    def __repr__(self):
        return "<Article: {}>".format(self.id, self.title, self.authors, self.abstract, self.url)


class SearchArticle(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    title = db.Column(db.String(300))
    authors = db.Column(db.String(300))
    abstract = db.Column(db.String(5000))
    url = db.Column(db.String(500))

    def __repr__(self):
        return "<Article: {}>".format(self.id, self.title, self.authors, self.abstract, self.url)


class WordCloudT1(db.Model):
    word = db.Column(db.String(100), unique=True, nullable=False, primary_key=True)
    count = db.Column(db.Integer)

    def __repr__(self):
        return "<Article: {}>".format(self.word, self.count)

class WordCloudT2(db.Model):
    word = db.Column(db.String(100), unique=True, nullable=False, primary_key=True)
    count = db.Column(db.Integer)

    def __repr__(self):
        return "<Article: {}>".format(self.word, self.count)

class WordCloudT3(db.Model):
    word = db.Column(db.String(100), unique=True, nullable=False, primary_key=True)
    count = db.Column(db.Integer)

    def __repr__(self):
        return "<Article: {}>".format(self.word, self.count)                

class WordCloudS1(db.Model):
    word = db.Column(db.String(100), unique=True, nullable=False, primary_key=True)
    count = db.Column(db.Integer)

    def __repr__(self):
        return "<Article: {}>".format(self.word, self.count)


class WordCloudS2(db.Model):
    word = db.Column(db.String(100), unique=True, nullable=False, primary_key=True)
    count = db.Column(db.Integer)

    def __repr__(self):
        return "<Article: {}>".format(self.word, self.count)

class WordCloudS3(db.Model):
    word = db.Column(db.String(100), unique=True, nullable=False, primary_key=True)
    count = db.Column(db.Integer)

    def __repr__(self):
        return "<Article: {}>".format(self.word, self.count)


db.create_all()

db.session.query(TrendyArticle).delete()
db.session.query(WordCloudT1).delete()
db.session.query(WordCloudT2).delete()
db.session.query(WordCloudT3).delete()


res = trending()
for i in res:
    if not TrendyArticle.query.filter_by(id=i['pubmed_id']).first():
        new_article = TrendyArticle(id=i['pubmed_id'], title=i['title'], authors=i['authors'], abstract=i['text'], url=i['url'])
        db.session.add(new_article)


ngram1_t, ngram2_t, ngram3_t = createcloud(res)

for key, value in ngram1_t.items():
    if not WordCloudT1.query.filter_by(word=key).first():
        new_ngram1 = WordCloudT1(word=key, count=value)
        db.session.add(new_ngram1)

for key, value in ngram2_t.items():
    if not WordCloudT2.query.filter_by(word=key).first():
        new_ngram2 = WordCloudT2(word=key, count=value)
        db.session.add(new_ngram2)

for key, value in ngram3_t.items():
    if not WordCloudT3.query.filter_by(word=key).first():
        new_ngram3 = WordCloudT3(word=key, count=value)
        db.session.add(new_ngram3)

db.session.commit()
today = date.today().strftime("%b %d, %Y")

message = ''
toggle = False

@app.route('/', methods=["GET", "POST"])
def index():
    message = ''
    if request.form:
        new_word = request.form.get("add_keyword")

        if len(str(new_word).strip()) < 2:
            message = "type in valid keyword"
        elif Word.query.filter_by(word=new_word).first():
            message = "duplicate keyword"
        else:
            new_keyword = Word(word=new_word)
            db.session.add(new_keyword)
            db.session.commit()
    keywords = Word.query.all()
    articles = TrendyArticle.query.all()
    

    return render_template("index.html", trending_articles = articles, today = today, keywords = keywords, err_message = message, ngram1 = ngram1_t, ngram2 = ngram2_t, ngram3 = ngram3_t)


@app.route("/delete", methods=["GET", "POST"])
def delete():
    if request.form:
        selected = request.form.get("delete_keyword")
        word = Word.query.filter_by(word=selected).first()
        db.session.delete(word)
        db.session.commit()
        return redirect(url_for('.index'))


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.form:
        request.form.get("search_keyword")
        keywords = Word.query.all()

        temp_string = ''
        for i in keywords:
            temp_string = ' ' + str(i.word)
        
        db.session.query(SearchArticle).delete()
        db.session.query(WordCloudS1).delete()
        db.session.query(WordCloudS2).delete()
        db.session.query(WordCloudS3).delete()

        res2 = search_keyword(temp_string)
        for i in res2:
            if not SearchArticle.query.filter_by(id=i['pubmed_id']).first():
                new_article = SearchArticle(id=i['pubmed_id'], title=i['title'], authors=i['authors'], abstract=i['text'], url=i['url'])
                db.session.add(new_article)

        ngram1_s, ngram2_s, ngram3_s = createcloud(res2)

        for key, value in ngram1_s.items():
            if not WordCloudS1.query.filter_by(word=key).first():
                new_ngram1 = WordCloudS1(word=key, count=value)
                db.session.add(new_ngram1)

        for key, value in ngram2_s.items():
            if not WordCloudS2.query.filter_by(word=key).first():
                new_ngram2 = WordCloudS2(word=key, count=value)
                db.session.add(new_ngram2)

        for key, value in ngram3_s.items():
            if not WordCloudS3.query.filter_by(word=key).first():
                new_ngram3 = WordCloudS3(word=key, count=value)
                db.session.add(new_ngram3)

        db.session.commit()

        articles = SearchArticle.query.all()

        return render_template("search.html", search_articles = articles, keywords = keywords, ngram1 = ngram1_s, ngram2 = ngram2_s, ngram3 = ngram3_s)

@app.route("/go-home", methods=["GET", "POST"])
def delete():
    if request.form:
        request.form.get("go-home")

        return redirect(url_for('.index'))


if __name__ == "__main__":
    app.run(debug=True)
