from flask import render_template, request, redirect, url_for
import requests
import os
from . import application
from app.skeptic import Skeptic
import json


application.config["DATA_FOLDER"] = "data/"

@application.route('/')
@application.route('/index')
def index():
    return redirect('/video')


@application.route('/video', methods=['GET', 'POST'])
def daas_video():
    mapID = request.args.get('mapID')
    video_url = request.args.get('video_url')
    
    data = requests.get(json_url(mapID)).text

    aifdb_data = json.loads(data)
    xaif_data = load_xaif_json()

    if xaif_data != None : 
        add_timestamps_to_xaif(aifdb_data, xaif_data)
        filename = saveToFile(mapID, xaif_data)
        skeptic_data = call_skeptic(filename)
        removeFile(filename)
        
        #print(skeptic_data)
       # nodes = skeptic_data['AIF']['nodes']
        locutions = []
       
    
        sk = Skeptic() 
        prompts, locutions = sk.generate_interventions(skeptic_data)
        
    else:
        locutions = None

    return render_template('index.html', video_url=video_url, mapID=mapID, locutions=locutions, prompts=prompts)


def find_locution_in_AIFdb(locution, locutions_aifdb):
    for loc in locutions_aifdb:
        if loc['text'] == locution['text']:
            return loc
    return None


def add_timestamps_to_xaif(aifdb_data, xaif_data):
    nodes_aifdb = aifdb_data['nodes']
    locutions_aifdb = [x for x in nodes_aifdb if x['type'] == 'L']

    xaif_nodes = xaif_data['AIF']['nodes']
    for i in range(len(xaif_nodes)):
        if xaif_nodes[i]['type'] == "L":
            aifdb_loc = find_locution_in_AIFdb(xaif_nodes[i], locutions_aifdb)
            if(aifdb_loc != None):
                xaif_data['AIF']['nodes'][i]['timestamp'] = aifdb_loc['timestamp']

    return xaif_data


def load_xaif_json():
    path = os.path.join(application.config['DATA_FOLDER'], '26171_xaif.json')

    if os.path.exists(path):
        with(open(path, "r")) as file:
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
    filename = os.path.join(application.config['DATA_FOLDER'], '26171_for_skeptic.json')

    with open(filename, "w") as outfile:
        outfile.write(json.dumps(json_data))

    return filename


def json_url(argument_map):
    return 'http://www.aifdb.org/json/' + argument_map


def call_skeptic(filename):
    upload_url = 'http://skeptic-ws.arg.tech/'
    file_ = {'file': (filename, open(filename, 'rb'))}
    r = requests.post(upload_url, files=file_)
    data = json.loads(r.text)

    return data