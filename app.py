import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
from models.word2vec import W2v
import json
from bson.json_util import loads, dumps
from itertools import chain
import pymongo

from define_models import defined_models


connection_url = 'mongodb+srv://dbUser:dbUserPassword@cluster0.ifjkb.mongodb.net/CI_ratings?retryWrites=true&w=majority'
client = pymongo.MongoClient(connection_url)

# Database
Database = client.get_database('CI_ratings')

# Table
SampleTable = Database.ratings_opti

# Create flask app and initiate classes
flask_app = Flask(__name__)
model_w2v = W2v()
#models = defined_models()


@flask_app.route("/")
def Home():
    return render_template("base.html")

@flask_app.route("/recommend", methods = ["POST"])
def recommend():
    # Get provided id and transform it to a string
    form_object = request.form.values()
    provided_id = list(form_object)
    provided_id = provided_id[0]
    result_model = model_w2v.predict_CI(provided_id)

    # try:
    #     result_model = model_w2v.predict_CI(provided_id)
    # except:
    #     return render_template("handle_error.html")

    content_id = model_w2v.content_id
    keywords = model_w2v.keywords
    title = model_w2v.title
    surtitle = model_w2v.surtitle
    subject = model_w2v.subject
    audience = model_w2v.audience
    thumbnail = model_w2v.thumbnail
    description = model_w2v.description
    user_id = 'user id'

    return render_template(
        "recommend.html",
        result_model=result_model, 
        title=title,
        subject=subject,
        audience=audience,
        keywords=keywords,
        surtitle=surtitle,
        thumbnail=thumbnail,
        content_id=content_id,
        description=description,
        user_id=user_id
        )

@flask_app.route("/random", methods = ["POST"])
def random_id():
    random_id = model_w2v.generate_id()
    result_model = model_w2v.predict_CI(random_id)
    
    content_id = model_w2v.content_id
    keywords = model_w2v.keywords
    title = model_w2v.title
    surtitle = model_w2v.surtitle
    subject = model_w2v.subject
    audience = model_w2v.audience
    thumbnail = model_w2v.thumbnail
    description = model_w2v.description
    user_id = 'user id'
        
    return render_template(
        "recommend.html",
        result_model=result_model,
        subject=subject,
        audience=audience,
        keywords=keywords,
        title=title,
        surtitle=surtitle,
        thumbnail=thumbnail,
        content_id=content_id,
        description=description,
        user_id=user_id
        )

@flask_app.route("/post_data", methods = ["GET", "POST"])
def post_data():    
    if request.method == 'POST':
        data = request.get_json()
        queryObject = data
        query = SampleTable.insert_many(queryObject) 
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    return render_template("post_data.html")

@flask_app.route("/handle_error")
def error_handler():    
    return render_template("handle_error.html")


if __name__ == "__main__":
    flask_app.run(debug=True)