import os
import string

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///study.db")

# welcome page
@app.route("/", methods=["GET", "POST"])
def welcome():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("homepage.html")
    else:
        # name of user
        name = request.form.get("name")

        return render_template("welcome.html", name=name)


# noise level page
@app.route("/noise", methods=["GET", "POST"])
def noise():
    """Determine noise level"""
    if request.method == "GET":
        return render_template("welcome.html")
    else:
        # result for noise
        global noise
        noise = str.lower(request.form.get("noise"))

        space = db.execute("SELECT placeName FROM places INNER JOIN noise ON places.noiseID = noise.noiseID WHERE noise = ?", noise)
        spaces = []

        for row in space:
            spaces.append(row["placeName"])

        return render_template("noise.html", noise=noise, spaces=spaces)


# seating page
@app.route("/seating", methods=["GET", "POST"])
def seating():
    """Determine seating"""
    if request.method == "GET":
        return render_template("noise.html")
    else:
        # result for seating
        global seating
        seating = str.lower(request.form.get("seating"))

        space = db.execute("SELECT placeName FROM places INNER JOIN noise ON places.noiseID = noise.noiseID INNER JOIN seating ON places.seatingID = seating.seatingID WHERE noise = ? AND seating = ?", noise, seating)
        spaces = []

        for row in space:
            spaces.append(row["placeName"])

        return render_template("seating.html", seating=seating, spaces=spaces)


# food page
@app.route("/food", methods=["GET", "POST"])
def food():
    """Determine food availability"""
    if request.method == "GET":
        # return render_template("seating.html")
        return render_template("food.html")
    else:
        # result for food availability
        global food
        food = str.lower(request.form.get("food"))
        if food == "yes":
            foodoption = "do"
        else:
            foodoption = "don't"

        space = db.execute("SELECT placeName FROM places INNER JOIN noise ON places.noiseID = noise.noiseID INNER JOIN seating ON places.seatingID = seating.seatingID INNER JOIN food ON places.foodID = food.foodID INNER JOIN groupstudy ON places.groupID = groupstudy.groupID WHERE noise = ? AND seating = ? AND food = ? AND groupstudy = ?", noise, seating, food, groupstudy)
        spaces = []

        for row in space:
            spaces.append(row["placeName"])

        return render_template("food.html", foodoption=foodoption, spaces=spaces)


# group study page
@app.route("/groupstudy", methods=["GET", "POST"])
def groupstudy():
    """Determine group study availability"""
    if request.method == "GET":
        return render_template("seating.html")
    else:
        # result for group study
        global groupstudy
        groupstudy = str.lower(request.form.get("groupstudy"))
        if groupstudy == "yes":
            groupstudyoption = "do"
        else:
            groupstudyoption = "don't"

        space = db.execute("SELECT placeName FROM places INNER JOIN noise ON places.noiseID = noise.noiseID INNER JOIN seating ON places.seatingID = seating.seatingID INNER JOIN food ON places.foodID = food.foodID INNER JOIN groupstudy ON places.groupID = groupstudy.groupID WHERE noise = ? AND seating = ? AND groupstudy = ?", noise, seating, groupstudy)
        spaces = []

        for row in space:
            spaces.append(row["placeName"])

        return render_template("groupstudy.html", groupstudyoption=groupstudyoption, spaces=spaces)


# results page
@app.route("/results", methods=["GET", "POST"])
def results():
    """Determine group study availability"""
    if request.method == "GET":
        return render_template("groupstudy.html")
    else:

        if noise == "loud" and seating == "rolling chairs":
            return render_template("results1.html")
        else:
            if food == "yes":
                space = db.execute("SELECT placeName FROM places INNER JOIN noise ON places.noiseID = noise.noiseID INNER JOIN seating ON places.seatingID = seating.seatingID INNER JOIN food ON places.foodID = food.foodID INNER JOIN groupstudy ON places.groupID = groupstudy.groupID WHERE noise = ? AND seating = ? AND food = ? AND groupstudy = ?", noise, seating, food, groupstudy)
                spaces = []
            else:
                space = db.execute("SELECT placeName FROM places INNER JOIN noise ON places.noiseID = noise.noiseID INNER JOIN seating ON places.seatingID = seating.seatingID INNER JOIN food ON places.foodID = food.foodID INNER JOIN groupstudy ON places.groupID = groupstudy.groupID WHERE noise = ? AND seating = ? AND groupstudy = ?", noise, seating, groupstudy)
                spaces = []

            for row in space:
                spaces.append(row["placeName"])

            return render_template("results.html", spaces=spaces)


# page to browse spaces
@app.route("/browse")
def browse():
    """Show available spaces"""
    space = db.execute("SELECT placeName FROM places ORDER BY placeName")
    spaces = []

    for row in space:
        if row["placeName"] not in spaces:
            spaces.append(row["placeName"])

    return render_template("browse.html", spaces=spaces)


    # page for cabot
@app.route("/cabot")
def cabot():

    return render_template("cabot.html")

    # page for capital one cafe
@app.route("/capitalonecafe")
def capitalonecafe():

    return render_template("capitalonecafe.html")

    # page for flour
@app.route("/flour")
def flour():

    return render_template("flour.html")

    # page for art museum
@app.route("/artmuseum")
def artmuseum():

    return render_template("artmuseum.html")

    # page for lamont poetry room
@app.route("/lamontpoetryroom")
def lamontpoetryroom():

    return render_template("lamontpoetryroom.html")

    # page for lamont cafe
@app.route("/lamontcafe")
def lamontcafe():

    return render_template("lamontcafe.html")

    # page for lamont media lab
@app.route("/lamontmedialab")
def lamontmedialab():

    return render_template("lamontmedialab.html")

    # page for lamont nooks
@app.route("/lamontnooks")
def lamontnooks():

    return render_template("lamontnooks.html")

    # page for law school library
@app.route("/lawschoollibrary")
def lawschoollibrary():

    return render_template("lawschoollibrary.html")

    # page for memorial church basement
@app.route("/memchurch")
def memchurch():

    return render_template("memchurch.html")

    # page for peets
@app.route("/peets")
def peets():

    return render_template("peets.html")

    # page for smith tenth floor
@app.route("/smith10")
def smith10():

    return render_template("smith10.html")

    # page for smith collaborative commons
@app.route("/smithcc")
def smithcc():

    return render_template("smithcc.html")

    # page for starbucks
@app.route("/starbucks")
def starbucks():

    return render_template("starbucks.html")

    # page for straus
@app.route("/straus")
def straus():

    return render_template("straus.html")

    # page for tatte
@app.route("/tatte")
def tatte():

    return render_template("tatte.html")

    # page for thayer
@app.route("/thayer")
def thayer():

    return render_template("thayer.html")

    # page for widener - loker reading room
@app.route("/widenerloker")
def widenerloker():

    return render_template("widenerloker.html")

    # page for widener - phillips reading room
@app.route("/widenerphillips")
def widenerphillips():

    return render_template("widenerphillips.html")