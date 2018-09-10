# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def home():

    # Find data
    mars_collections = mongo.db.collection.find()
    

    # return template and data
    return render_template("index.html", mars_collections=mars_collections)



@app.route("/scrape")
def scrape():

    mars_collections = scrape_mars.scrape_all()
    mongo.db.collection.insert_one(mars_collections)

    # Redirect back to home page
    return redirect("/", code=302)
    

if __name__ == "__main__":
    app.run()
