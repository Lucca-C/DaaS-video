# ----- IMPORTS -----
from flask import render_template, request, redirect, url_for
import requests
import os
from . import application
from app.skeptic import Skeptic
import json

application.config[
    "DATA_FOLDER"
] = "data/"  # Configuration for flask from data/26171_xaif.json


# ----- METHODS ------


# Decorators for the function below to redirect / or /index to video
@application.route("/")
@application.route("/index")
def index():  # Called when a user visits / or /index
    return redirect("/video")


# Decorator daas_video to be called on /video
@application.route("/video", methods=["GET", "POST"])
def daas_video():
    try:
        # Retreive mapID and video_url from incoming http request
        mapID = request.args.get("mapID")
        video_url = request.args.get("video_url")

        # Throws 400 if mapID isn't provided
        if not mapID:
            print("mapID is not provided")
            return "mapID not provided", 400

        try:
            # get request on json_url
            response = requests.get(json_url(mapID))
            # Raises an HTTPError if the HTTP request returned an unsuccessful status code
            response.raise_for_status()
        except (
            requests.RequestException
        ) as e:  # This will catch any type of RequestException including HTTPError
            print(f"Error fetching data from URL: {str(e)}")
            return f"Error fetching data: {str(e)}", 500

        if response.status_code != 200:
            return f"Error fetching data. HTTP status: {response.status_code}", 500

        data = response.text
        print("DEBUG data: " + data)

        if not data:
            return "Data fetched is empty", 500
        try:
            aifdb_data = json.loads(data)
        except json.JSONDecodeError:
            return "Error processing json data", 500
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

    # Loads xaif data
    xaif_data = load_xaif_json(mapID)

    # If xaid data exists, add timestamp to it, save it, call skeptic
    if xaif_data is not None:
        add_timestamps_to_xaif(aifdb_data, xaif_data)
        filename = saveToFile(mapID, xaif_data)
        skeptic_data = call_skeptic(filename)
        removeFile(filename)

        # print(skeptic_data)
        # nodes = skeptic_data['AIF']['nodes']
        locutions = []

        sk = Skeptic()
        prompts, locutions = sk.generate_interventions(skeptic_data)

    else:
        locutions = None
    # Populate HTML template to show the user
    return render_template(
        "index.html",
        video_url=video_url,
        mapID=mapID,
        locutions=locutions,
        prompts=prompts,
    )


# Searches for a given locution in a dictionary
def find_locution_in_AIFdb(locution, locutions_aifdb):
    for loc in locutions_aifdb:
        if loc["text"] == locution["text"]:
            return loc
    return None


# Takes 2 dictionaries
def add_timestamps_to_xaif(aifdb_data, xaif_data):
    # Extracts the aifdb nodes from the aifdb_data dictionary
    nodes_aifdb = aifdb_data["nodes"]
    # Creates a list of nodes that are locutions
    locutions_aifdb = [x for x in nodes_aifdb if x["type"] == "L"]
    # Extracts the xaif nodes from the xaif_data dictionary
    xaif_nodes = xaif_data["AIF"]["nodes"]
    # Loops through xaif_nodes and looks for a matching node in aifdb
    # Transfers the timestamp to xaif if found
    for i in range(len(xaif_nodes)):
        if xaif_nodes[i]["type"] == "L":
            aifdb_loc = find_locution_in_AIFdb(xaif_nodes[i], locutions_aifdb)
            if aifdb_loc != None:
                xaif_data["AIF"]["nodes"][i]["timestamp"] = aifdb_loc["timestamp"]

    return xaif_data


def load_xaif_json(mapID):
    # Calls function to generate path with given inputs
    if os.path.exists(application.config["DATA_FOLDER"]):
        print("Data directory exists!")
    else:
        print("Data directory does not exist.")

    path = generate_filename(mapID, "_xaif")
    print("Current Working Directory:", os.getcwd())
    print("Trying to access file at:", path)

    # Check is path exists, return JSON
    if os.path.exists(path):
        with open(path, "r") as file:
            xaif_json = json.load(file)
            return xaif_json
    else:
        print("The file " + path + " does not exist")
        return None


def removeFile(filename):
    if os.path.exists(filename):
        os.remove(filename)
    else:
        print("The file " + filename + " does not exist")


def saveToFile(mapID, json_data):
    filename = generate_filename(mapID, "_for_skeptic")

    with open(filename, "w") as outfile:
        outfile.write(json.dumps(json_data))

    return filename


def json_url(argument_map):
    return "http://www.aifdb.org/json/" + argument_map


def generate_filename(mapID, suffix=""):
    return os.path.join(application.config["DATA_FOLDER"], f"{mapID}{suffix}.json")


def call_skeptic(filename):
    upload_url = "http://skeptic-ws.arg.tech/"
    file_ = {"file": (filename, open(filename, "rb"))}
    try:
        r = requests.post(upload_url, files=file_)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"Error posting data to URL: {str(e)}")
        return f"Error posting data: {str(e)}", 500
    data = json.loads(r.text)

    return data
