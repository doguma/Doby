from flask import Flask, render_template, Blueprint, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title='doelsevier : analyze scholarly articles')
