#!/usr/bin/env python3
# services.py
#
from indoor_keys import CloudVisionKey
import requests

import json
import pymongo
import requests

from pymongo import UpdateOne
from socket import inet_ntoa
from six.moves import input
from zeroconf import ServiceBrowser, Zeroconf
from flask import Flask, jsonify, make_response, request, abort, render_template, Response
import sass
import argparse
import sys
import jsonpickle
import numpy as np
import cv2
import base64
import re

import time

from bson.json_util import dumps
import ast

app = Flask(__name__)
sass.compile(dirname=('assets/scss', 'static/css'))
# BEGIN APP

IP = 'localhost'
PORT = 8080

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

  operations = []
  for ob in r["data"]:
    print(ob)
    operations.append(
        UpdateOne({"name": ob['name']},
              {"$set": ob},
              upsert=False)
        )

  settings = db.getSettings()
  settings.bulk_write(operations)

  action = {"success":"woohoo!!1"}
  return make_response(jsonify(action), 200)


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

    # handle the Canvas response
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
        # TODO determine action based on the animal found

    if falseAlarm:
        action = {"sound":None, "light":None}
    else:
        action = determineAction(labels)
    print("HERE")
    print(action)

    return make_response(jsonify(action), 201)


def determineAction(labels):
    # to do:
    # determine action to send to outdoor pi
    #
    # this requires
    # determining the time of day
    # pulling in the black & white lists
    # pulling in day_responses, night_responses
    #
    # using these lists to determine the action
    # recording the action in the History collection

    mytime = time.localtime()

    if mytime.tm_hour < 6 or mytime.tm_hour > 18:
        nighttime = True
    else:
        nighttime = False

    coll = db.getSettings()
    settings = coll.find({}, {'_id': False})
    settings = dumps(settings)
    settings = ast.literal_eval(settings)

    # print(settings)
    # print("settings")

    whitelist = settings[0]['whitelist']
    blacklist = settings[1]['blacklist']
    response_daytime = settings[2]['response_daytime']
    response_nighttime = settings[3]['response_nighttime']

<<<<<<< HEAD
    for item in whitelist:
        if item in labels:
            return ("sound" : None, "light" : None)
=======

>>>>>>> debd336f0e373ab31dac5791ef83a025c37af018

    for item in blacklist:
        if item in labels or (item + 's') in labels:
            if nighttime:
                return ("sound" : None, "light" : response_nighttime[item])
            else:
                return ("sound" : response_daytime[item], "light" : None)

    if nighttime:
        return ("sound" : None, "light" : response_nighttime[default])
    else:
        return ("sound" : response_daytime[default], "light" : None)


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
