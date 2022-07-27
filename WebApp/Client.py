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

app = Flask(__name__)


def random_Forest(userQuery):
    filename = "Completed_model.joblib"
    loaded_model = joblib.load(filename)
    with open('newfile','rb') as fp:
        row = pickle.load(fp)
    userQuery = userQuery.lower()
    text_tokens = word_tokenize(userQuery)
    tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]
    #filtered_results_df = row[row.stack().str.contains('|'.join(tokens_without_sw)).any(level=0)]
    userQuery_embeddings = loaded_model.encode(userQuery)
    smr = cosine_similarity([userQuery_embeddings],row[1].to_list())
    res = pd.DataFrame(zip(row[0].to_list(),smr[0]))
    res = res.drop_duplicates()
    res = res.sort_values(by = 1, ascending = False)
    return res.values.tolist()

    df = pd.read_csv('quora_duplicate_questions.tsv',sep = '\t')
    df = df[["question1","question2"]]
    df_2 = df[df.stack().str.contains('|'.join(tokens_without_sw)).any(level=0)]

    df_dict = {'question1':[], 'question2':[]}
    df_dict['question1'] = df_2['question1'].append(df_2['question2']).reset_index(drop=True).values.tolist()
    df_dict['question2'] = [userQuery]*len(df_dict['question1'])
    #df_dict['similarity_Score'] = [0]*len(df_dict['question1'])

    final_df = pd.DataFrame(df_dict)
    final_df = final_df.dropna(how='any',axis=0)

    filename = "Completed_model.joblib"
    loaded_model = joblib.load(filename)
    result = []
    for index, row in final_df.iterrows():
        sentences = [row[0],row[1]]
        temmp_result = compute_similarity(sentences,loaded_model)
        result.append(temmp_result[0][0])
    sim_df = pd.DataFrame({'similarity_Score':result})
    final_df = final_df.join(sim_df)
    final_df = final_df.sort_values(by='similarity_Score', ascending=False)
    final_df = final_df[["question1","similarity_Score"]]
    
    return final_df.iloc[:,0].values.tolist()#list(final_df.iloc[:,0].values.tolist())


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

if __name__ == "__main__":
    app.run(debug=True)