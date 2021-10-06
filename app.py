from flask import Flask, json, jsonify, render_template
from flask.wrappers import Response
import pymongo

app = Flask(__name__)

# setup mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# connect to mongo db and collection
db = client.Mars_Data
Scrape_Results = db.Scrape_Results

@app.route("/api/1/ScrapeResults", methods = ["GET"])
def api_output_barchart():
    try:
        print("this works")
        return jsonify(f'{list(Scrape_Results.find())}')
    except Exception as ex:
        print(ex)
        return Response(
            response= json.dumps({"message":"Messed up"}),
            status = 500
        )

@app.route("/")
def welcome():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)