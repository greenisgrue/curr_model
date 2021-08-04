import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
from models.word2vec import W2v
import json
from bson.json_util import loads, dumps
from itertools import chain
import pymongo

from define_models import defined_models
from skolmedia_client.skolfilm_client import Skolfilm



connection_url = 'mongodb+srv://dbUser:dbUserPassword@cluster0.ifjkb.mongodb.net/CI_ratings?retryWrites=true&w=majority'
client = pymongo.MongoClient(connection_url)

# Database
Database = client.get_database('CI_ratings')

# Table
SampleTable = Database.ratings_opti

# Create flask app and initiate classes
flask_app = Flask(__name__)
model_w2v = W2v("search_ur_20210731_cleaned")
#models = defined_models()

# Get teacher type
teacher_subjects = ['Moderna språk']
teacher_grades = ['Grundskola 4-6']


@flask_app.route("/")
def Home():
    return render_template("base.html")

@flask_app.route("/recommend", methods = ["POST"])
def recommend():
    # Get provided id and transform it to a string
    form_object = request.form.values()
    provided_id = list(form_object)
    provided_id = provided_id[0]
    # result_model = model_w2v.predict_CI(provided_id)
    
    import pickle
    with open(f'massive_data/stored_data/pickles/model_pickle.pickle', 'rb') as f:
        df = pickle.load(f)

    selected = df.loc[df['uid'] == provided_id]
    results = selected.iloc[0]['result']
    content_metadata = results[0]
    keywords = content_metadata[1].get('keywords')
    subject = selected.iloc[0]['subject']
    user_id = 'user_id'
    subject_adjusted_values = False
    grades_adjusted_values = False
    if any(sub in subject.split(', ') for sub in teacher_subjects):
        subject_adjusted_values = True
    if any(sub in subject.split(', ') for sub in teacher_grades):
        grades_adjusted_values = True
    #         formatted_string = "{:.3f}".format(subject_adjusted_value)
    #         subject_adjusted_value = float(formatted_string)
    #         value['value'] = subject_adjusted_value
    # print(results)
    
    # Handle errors by redirecting to error page
    # try:
    #     result_model = model_w2v.predict_CI(provided_id)
    # except:
    #     return render_template("handle_error.html")


    # Get metadata to display on interface
    # content_id = model_w2v.content_id
    # keywords = model_w2v.keywords
    # title = model_w2v.title
    # surtitle = model_w2v.surtitle
    # subject = model_w2v.subject
    # audience = model_w2v.audience
    # thumbnail = model_w2v.thumbnail
    # description = model_w2v.description
    # user_id = 'user id'

    return render_template(
        "recommend.html",
        result_model=results, 
        title=selected.iloc[0]['title'],
        subject=subject,
        audience=selected.iloc[0]['audience'],
        keywords=selected.iloc[0]['keywords'],
        surtitle=selected.iloc[0]['surtitle'],
        thumbnail=selected.iloc[0]['thumbnail'],
        content_id=selected.iloc[0]['uid'],
        description=selected.iloc[0]['description'],
        user_id=user_id,
        subject_adjusted_values=subject_adjusted_values,
        grades_adjusted_values=grades_adjusted_values
        )

    # return render_template(
    #     "recommend.html",
    #     result_model=result_model, 
    #     title=title,
    #     subject=subject,
    #     audience=audience,
    #     keywords=keywords,
    #     surtitle=surtitle,
    #     thumbnail=thumbnail,
    #     content_id=content_id,
    #     description=description,
    #     user_id=user_id
    #     )



@flask_app.route("/random", methods = ["POST"])
def random_id():
    random_id = model_w2v.generate_id()
    result_model = model_w2v.predict_CI(random_id)
    
    # Get metadata to display on interface
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
        data = data[0]
        ratings_data = []
        ratings = {}
        for key, value in data.items():
            if type(value) == dict:
                ratings_data.append(value)
            else:
                ratings[key] = value

        ratings['ratings'] = ratings_data
        print(ratings)
        query = SampleTable.insert_many([ratings]) 

        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    return render_template("post_data.html")

@flask_app.route("/handle_error")
def error_handler():    
    return render_template("handle_error.html")

if __name__ == "__main__":
    flask_app.run(debug=True)