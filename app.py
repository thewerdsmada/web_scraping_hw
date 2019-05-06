# Import all the stuff 
from flask import Flask, render_template, redirect 
from flask_pymongo import pymongo
import scrape_functions
import os
import pymongo

# Use Flask to make an app
app = Flask(__name__)



#Import the mongo client to set up the database connection
from pymongo import MongoClient

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['mars_app'] 

# Home Route that shows the stuff
@app.route("/")
def home(): 

    # Find data
    mars_info = db.mars_info.find_one()

    # Return template and data
    return render_template("index.html", mars_info=mars_info)

# Route / Link for the button to go to
@app.route("/scrape")
def scrape(): 

    # Scape Scrape Scrape!!
    mars_info = db.mars_info
    mars_data = scrape_functions.scrape_mars_news()
    mars_data = scrape_functions.scrape_mars_image()
    mars_data = scrape_functions.scrape_mars_facts()
    mars_data = scrape_functions.scrape_mars_weather()
    mars_data = scrape_functions.scrape_mars_hemispheres()
    mars_info.update({}, mars_data, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug= True)
