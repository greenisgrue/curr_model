import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
from models.jaccard import Jaccard
from models.word2vec import W2v
import json
from bson.json_util import loads, dumps
from itertools import chain
import pymongo


connection_url = 'mongodb+srv://dbUser:dbUserPassword@cluster0.ifjkb.mongodb.net/CI_ratings?retryWrites=true&w=majority'
client = pymongo.MongoClient(connection_url)
# Database
Database = client.get_database('CI_ratings')
# Table
SampleTable = Database.ratings

# Create flask app
flask_app = Flask(__name__)
model_jaccard = Jaccard()
model_w2v = W2v()


@flask_app.route("/")
def Home():
    return render_template("base.html")

@flask_app.route("/jaccard", methods = ["POST"])
def jaccard():
    provided_id = request.form.values()
    provided_id = list(provided_id)
    provided_id = provided_id[0]
    result = model_jaccard.predict_CI(provided_id)
    return render_template("recommend.html",provided_id=provided_id, prediction=result)


@flask_app.route("/recommend", methods = ["POST"])
def recommend():
    provided_id = request.form.values()
    provided_id = list(provided_id)
    provided_id = provided_id[0]
    model_1 = 'cos sim'
    model_2 = 'cos sim including CI titles'
    keywords = ['keywords']
    result_model_1 = model_w2v.predict_CI(model_1, provided_id)
    result_model_2 = model_w2v.predict_CI(model_2, provided_id)
    
    content_id = model_w2v.content_id
    keywords = model_w2v.keywords
    title = model_w2v.title
    surtitle = model_w2v.surtitle
    subject = model_w2v.subject
    audience = model_w2v.audience
    thumbnail = model_w2v.thumbnail
    description = model_w2v.description

    return render_template(
        "recommend.html",
        result_model_1=result_model_1, 
        result_model_2=result_model_2, 
        model_1=model_1,
        model_2=model_2,
        title=title,
        subject=subject,
        audience=audience,
        keywords=keywords,
        surtitle=surtitle,
        thumbnail=thumbnail,
        content_id=content_id,
        description=description
        )

@flask_app.route("/random", methods = ["POST"])
def random_id():
    random_id = model_w2v.generate_id()
    model_1 = 'cos sim'
    model_2 = 'cos sim double titles'
    result_model_1 = model_w2v.predict_CI(model_1, random_id)
    result_model_2 = model_w2v.predict_CI(model_2 , random_id)
    
    content_id = model_w2v.content_id
    keywords = model_w2v.keywords
    title = model_w2v.title
    surtitle = model_w2v.surtitle
    subject = model_w2v.subject
    audience = model_w2v.audience
    thumbnail = model_w2v.thumbnail
    description = model_w2v.description
        
    return render_template(
        "recommend.html",
        result_model_1=result_model_1, 
        result_model_2=result_model_2, 
        model_1=model_1,
        model_2=model_2,
        subject=subject,
        audience=audience,
        keywords=keywords,
        title=title,
        surtitle=surtitle,
        thumbnail=thumbnail,
        content_id=content_id,
        description=description
        )

@flask_app.route("/post_data", methods = ["GET", "POST"])
def post_data():    
    if request.method == 'POST':
        data = request.get_json()
        queryObject = data
        query = SampleTable.insert(queryObject) 
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    return render_template("post_data.html")


if __name__ == "__main__":
    flask_app.run(debug=True)