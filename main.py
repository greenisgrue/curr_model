from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/")
def index():
    sentence = request.args.get("sentence", "")
    if sentence:
        sim = jaccard_similarity(sentence)
    else:
        sim = ""
    return (
        """<form action="" method="get">
                Sentence: <input type="text" name="sentence">
                <input type="submit" value="Calculate Jaccard Similarity">
            </form>"""
        + sentence + " has Jaccard similarity: "
        + sim
    )

@app.route("/<sentence>")
def jaccard_similarity(query):
    document = 'Restaurangen serverar måltider varje lunch'
    try:
        query = query.split()
        document = document.split()
        intersection = set(query).intersection(set(document))
        union = set(query).union(set(document))
        return str(len(intersection)/len(union))

    except ValueError:
        return "invalid input"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
