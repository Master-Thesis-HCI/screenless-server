from urllib.parse import urlparse
from flask import render_template, redirect, request

from app import database as db
from app import app


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/download', methods=['GET', 'POST'])
def download():
    return redirect("https://files.romanpeters.nl/s/QAc4cBTGMKcZiQH")




