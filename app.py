from flask import Flask, render_template, redirect
import pymongo
from mission_to_mars import updatePage

app = Flask(__name__)

# setup mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# connect to mongo db and collection
db = client.Mars_Data
Scrape_Results = db.Scrape_Results

@app.route("/")
def welcome():

    return render_template("index.html", Scrape_Results = db.Scrape_Results.find_one({}))

@app.route('/scrape')
def scrape():
    updatePage()
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)