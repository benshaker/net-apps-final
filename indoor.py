#!/usr/bin/env python3
# services.py
#
from indoor_keys import CloudVisionKey
import json
import pymongo
import requests
from pymongo import UpdateOne
from six.moves import input
from flask import Flask, jsonify, make_response, request, render_template
import sass
import numpy as np
import cv2
import base64
import time
from bson.json_util import dumps
import ast
import re

app = Flask(__name__)
sass.compile(dirname=('assets/scss', 'static/css'))
# BEGIN APP

# IP = 'localhost'
# PORT = 8080

@app.route("/")
def root_get():
    return render_template("html/index.html")


@app.route("/settings")
def settings_get():
    return render_template("html/settings.html")


@app.route("/history")
def history_get():
    return render_template("html/history.html")


@app.route("/testing")
def testing_get():
    return render_template("html/testing.html")


@app.route("/info")
def root_info_get():
    return make_response(jsonify({
        'success': 'Choose from the following routes: ' +
        '/Canvas or ' +
        '/LED'
    }), 200)


@app.route("/load_settings", methods=['GET'])
def load_settings_get():
  coll = db.getSettings()
  settings = coll.find({}, {'_id': False})

  settings = dumps(settings)
  # action = {"success":"woohoo!!1"}
  return make_response(settings, 201)

@app.route("/save_settings", methods=['PUT'])
def save_settings_put():
  r = request.data.decode("utf-8")
  r = json.loads(r)

  settings = db.getSettings()
  operations = []
  for ob in r["data"]:
    settings.find_one_and_update({"name": ob['name']},
                                 {"$set": ob})

  action = {"success":"woohoo!!1"}
  return make_response(jsonify(action), 200)


@app.route("/load_history", methods=['GET'])
def load_history_get():
	col = db.getHistory()
	hist = col.find({}, {'_id': False})

	hist = dumps(hist)
	return make_response(hist, 201)

def add_to_history(data):
    animal, time, sound, light = data
    history = db.getHistory()
    #print(data)
    post = {
        "animal_detected": animal,
        "time_of_occurrence": time,
        "action_sound": sound,
        "action_light": light
    }

    history.insert_one(post)
    return

@app.route("/image", methods=['POST'])
def image_post():
    r = request
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img_str = base64.b64encode(nparr)

    img_str = img_str.decode("utf-8")

    data = {
      "requests":[
        {
          "image":{
            "content":str(img_str)
          },
          "features":[
            {
              "type":"LABEL_DETECTION",
              "maxResults":10
            },
            {
              "type":"FACE_DETECTION",
              "maxResults":10
            }
          ]
        }
      ]
    }

    r = requests.post(
        'https://vision.googleapis.com/v1/images:annotate?key='
         + CloudVisionKey,
        json=data)
    json_res = r.json()

    falseAlarm = False

    if not json_res:
        return make_response(jsonify({
            'error': 'No file names matched your search term.'
        }), 404)
    elif json_res:
        responses = json_res['responses']
        annotations = responses[0]['labelAnnotations']
        if 'faceAnnotations' in responses[0]:
            # human face detected
            face = responses[0]['faceAnnotations']
            confidence = face[0]['detectionConfidence']
            if confidence > 0.5:
                falseAlarm = True

    labels = []
    for annote in annotations:
        labels.append(annote['description'].lower())

    if falseAlarm:
        # human // may be ignored
        action = {"sound":None, "light":None}
    else:
        # not human // determine action
        action = determineAction(labels)

    return make_response(jsonify(action), 201)


def determineAction(labels):

    mytime = time.localtime()
    time_date = time.strftime("%b %d %Y %H:%M:%S", mytime)
    
    if mytime.tm_hour < 6 or mytime.tm_hour > 18:
        nighttime = True
    else:
        nighttime = False

    coll = db.getSettings()
    settings = coll.find({}, {'_id': False})
    settings = dumps(settings)
    settings = ast.literal_eval(settings)
    
    for ob in settings:
        name = ob['name']
        if name == "whitelist":
            whitelist = ob[name]
        elif name == "blacklist":
            blacklist = ob[name]
        elif name == "daytime":
            daytime_responses = ob[name]
        elif name == "nighttime":
            nighttime_responses = ob[name]

    for item in whitelist:
        if item in labels:
            action = {"sound" : None, "light" : None}

    known_animal = False
    animal = None
    for item in blacklist:
        if item in labels or (item + 's') in labels:
            known_animal = True
            animal = item
            if nighttime:
                action = {"sound" : None, "light" : nighttime_responses[item]}
            else:
                action = {"sound" : daytime_responses[item], "light" : None}

    if not known_animal:
        item = "default"
        animal = item
        if nighttime:
            action = {"sound" : None, "light" : nighttime_responses[item]}
        elif not nighttime:
            action = {"sound" : daytime_responses[item], "light" : None}

    event = animal, time_date, action["sound"], action["light"]
    add_to_history(event)

    return action


# this is a helper function that handles blanket 404 errors
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({
        'error': 'Invalid route. ' +
        'See /info'
    }), 404)

# this fn initializes our mongodb instance and collection
# and adds a short list of usernames and passwords to it
class HistoryDB(object):

    def __init__(self):
        self._client = pymongo.MongoClient("mongodb://localhost:27017/")
        self._db = self._client.scarecrow
        self.history_collection = self._db.history
        self.settings_collection = self._db.settings

    def getHistory(self):
        return self.history_collection

    def getSettings(self):
        return self.settings_collection


if __name__ == "__main__":
    db = HistoryDB()
    app.run(host='0.0.0.0', port=8080, debug=True)
