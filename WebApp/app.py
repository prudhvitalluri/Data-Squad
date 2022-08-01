from gettext import install
from unittest import result
from flask import Flask, render_template, request, redirect, url_for
#import psycopg2
import requests
from flask import jsonify
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
from nltk.tokenize import word_tokenize
import pandas as pd
import joblib
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import pickle
from flask import current_app

app = Flask(__name__)

app.questions = pickle.load(open("newfile",'rb'))
app.model = joblib.load("Completed_model.joblib")


def random_Forest(userQuery):
    userQuery = userQuery.lower()
    text_tokens = word_tokenize(userQuery)
    list_of_words = stopwords.words()
    list_of_words.append('?')
    
    tokens_without_sw = [word for word in text_tokens if not word in list_of_words]

    filtered_questions = current_app.questions[current_app.questions.stack().str.contains('|'.join(tokens_without_sw)).groupby(level=0).any()]

    similarity_scores = cosine_similarity([current_app.model.encode(userQuery)],filtered_questions.iloc[:,1].to_list())

    resultdata = list(set(zip(filtered_questions.iloc[:,0].to_list(),similarity_scores.tolist()[0])))
    resultdata.sort(key=lambda y: y[1],reverse=True)

    return resultdata[:20]

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/ModelInfo')
def modelInfo():
    return render_template('ModelInfo.html')

@app.route("/Search", methods=["POST","GET"])
def Search():
    results = []
    if request.method == "POST":
        userQuery = request.form["key"]
        similarQueries = random_Forest(userQuery)
        return render_template("Search.html",Results = similarQueries)
    else:
        return render_template("Search.html",Results = results)

@app.route("/Searchapi", methods=["POST","GET"])
def Searchapi():
    url = "http://suggestqueries.google.com/complete/search"
    params = {
        "client": "firefox",
        "q": request.args['key'],
        "hl": "en"
        }
    results = requests.get(url,params)
    results = results.json()[1]
    return jsonify(results)

@app.route("/EDA_page")
def EDA_page():
    return render_template('EDA_page.html')

@app.route("/Logistic")
def Logistic():
    return render_template('Logistic.html')

@app.route("/RandomForest")
def RandomForest():
    return render_template('RandomForest.html')

@app.route("/SVM")
def SVM():
    return render_template('SVM.html')

@app.route("/SBERT")
def SBERT():
    return render_template('SBERT.html')


@app.route("/LSTM")
def LSTM():
    return render_template('LSTM.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)

#app.run(host='0.0.0.0', port=80)