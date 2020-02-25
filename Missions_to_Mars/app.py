from flask import Flask, render_template
import pymongo
from scrape_mars import *

app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.mars_db

@app.route("/scrape")
def scrape():
    result_dict = {}
    db = client.mars_db
    db.news_collection.drop()
    db.mars_fact.drop()
    db.mars_weather.drop()
    db.mars_featured_images.drop()
    db.scrape_hemispheres_images.drop()
    db.news_collection.insert_many(scrape_news())
    db.mars_fact.insert_one(scrape_facts())
    db.mars_featured_images.insert_many(scrape_featured_images())
    db.scrape_hemispheres_images.insert_many(scrape_hemispheres_images())
    db.mars_weather.insert_many(scrape_weather())
    # List of dictionary object
    result_dict['facts'] = list(db.mars_fact.find({}, {"_id": 0}))
    result_dict['hemispheres'] = list(db.scrape_hemispheres_images.find({}, {"_id": 0}))
    result_dict['news'] = list(db.news_collection.find({}, {"_id": 0}).limit(2))
    result_dict['weather'] = list(db.mars_weather.find({}, {"_id": 0}).limit(2))
    result_dict['featured'] = list(db.mars_featured_images.find({}, {"_id": 0}).limit(2))
    return render_template("index.html", result_dict=result_dict)

@app.route("/")
def index():
    # teams = list(db.team.find())  # List of dictionary objects
    # return render_template("index.html", teams=teams)
    return render_template("index.html", result_dict=None)


if __name__ == "__main__":
    app.run(debug=True)
