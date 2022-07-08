from unittest import result
from flask import Flask, render_template, request, redirect, url_for
#import psycopg2
import requests
from flask import jsonify


app = Flask(__name__)



@app.route("/")
def home():
    return render_template("home.html")


@app.route('/ModelInfo')
def modelInfo():
    return render_template('ModelInfo.html')


@app.route("/Search", methods=["POST", "GET"])
def Search():
    results = []
    if request.method == "POST":
        url = "http://suggestqueries.google.com/complete/search"
        params = {
            "client": "firefox",
            "q": request.form["key"],
            "hl": "en"
        }
        results = requests.get(url, params)
        results = results.json()[1]
        return render_template("Search.html", Results=results)
        # render_template("SearchResult.html",Results = results)
    else:
        return render_template("Search.html", Results=results)


@app.route("/Searchapi", methods=["POST", "GET"])
def Searchapi():
    url = "http://suggestqueries.google.com/complete/search"
    params = {
        "client": "firefox",
        "q": request.args['key'],
        "hl": "en"
    }
    results = requests.get(url, params)
    results = results.json()[1]
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
