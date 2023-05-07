import sys

from flask import Flask,request
import scrape
import datetime
import json

app = Flask(__name__)

@app.route("/")
def index():
    with open('static/data.json') as f:
        json_data = json.load(f)
    if json_data['updated'] != datetime.date.today().strftime("%Y-%m-%d"):
        scrape.scrape()
    with open('static/data.json') as f:
        json_data = json.load(f)
    return json_data


if __name__=="__main__":
    app.run()