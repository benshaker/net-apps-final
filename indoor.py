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
from flask_scss import Scss
import sass
import argparse
import sys
import jsonpickle
import numpy as np
import cv2
import base64

app = Flask(__name__)
Scss(app)
sass.compile(dirname=('assets/scss', 'static/css'))
# BEGIN APP

IP = '127.0.0.1'
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

# curl -X POST -d '{"requests":[{"image":{"content":img_str},"features":[{"type":"LABEL_DETECTION","maxResults":1}]}]}' "http://10.0.0.180:8080"

# curl -X POST -d '{"image":img_str}' "http://0.0.0.0:8080/image"

@app.route("/image", methods=['POST'])
def image_post():
    # img_str = None
    # print("args",request.args)
    # print("json",request.json)
    # if not request.args or 'image' not in request.args:
    #     if not request.json or 'image' not in request.json:
    #         pass
    #     else:
    #         img_str = request.json['image']
    # else:
    #     img_str = request.args['image']
    # print(img_str)

    r = request
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img_str = base64.b64encode(nparr)
    # img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # print(b64_jpg)
    # img

    # plain import base64 image = img
    # #open binary file in read mode
    # image_read = image.read()
    # img_str = base64.encodestring(image_read)

    # print(image_64_encode)

    # do some fancy processing here....

    # # build a response dict to send back to client
    # response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])
    # }
    # # encode response using jsonpickle
    # response_pickled = jsonpickle.encode(response)

    # return Response(response=response_pickled, status=200, mimetype="application/json")

    # if not request.args or 'image' not in request.args:
    #     return make_response(jsonify({
    #         'error': 'No image provided'}), 400)
    # else:
    #     img_str = request.args['image']

    # example request below
    #   note that content must be a base64 string
    #   starting with /9j/ or whatever

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
              "maxResults":5
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

        # handle the Canvas response
    if not json_res:
        return make_response(jsonify({
            'error': 'No file names matched your search term.'
        }), 404)
    elif json_res:
        # if multiple results, we choose the most recently created
        # print("HEREHERE")
        # print(json_res)
        responses = json_res['responses']
        annotations = responses[0]['labelAnnotations']

    labels = []
    for annote in annotations:
        labels.append({"label":annote['description'], "score":annote['score']})
        # TODO determine action based on the animal found

    return make_response(jsonify(labels), 201)


@app.route("/LED/info")
def led_info_get():
    colors_allowed = listener.getColors()
    return make_response(jsonify({
        'success': 'GET /LED requires no params. ' +
        'PUT /LED accepts the following params: ' +
        '\'status\': [\'on\', \'off\'] (optional), ' +
        '\'color\': ' + str(colors_allowed) + ' (optional), ' +
        '\'intensity\': int(0 to 100) (optional)'}), 200)


@app.route("/LED", methods=['GET'])
def led_get():
    # get the latest information about the LED RPi
    ip = listener.getIP()
    port = listener.getPort()
    colors_allowed = listener.getColors()

    # Handle cases where LED RPi or its service is not available.
    if None not in (ip, port, colors_allowed):
        pass
    else:
        return make_response(jsonify({
            'error': 'LED RPi appears to be offline. Please try again.'
        }), 502)

    # send our request to LED RPi via its API
    try:
        r = requests.get('http://' + str(ip) + ':' + str(port) + '/LED/info')
        res_body = r.json()
    except Exception:
        return make_response(jsonify({
            'error': 'LED RPi service is unavailable. Please try again.'
        }), 503)

    # pass this response to the end user
    if r.status_code == requests.codes.ok:
        return make_response(jsonify(res_body), 201)
    else:
        return make_response(jsonify(res_body), 400)


@app.route("/LED", methods=['PUT'])
def led_put():
    # get the latest information about the LED RPi
    ip = listener.getIP()
    port = listener.getPort()
    colors_allowed = listener.getColors()

    # handle cases where LED RPi and its service is not available.
    if None not in (ip, port, colors_allowed):
        pass
    else:
        return make_response(jsonify({
            'error': 'LED RPi appears to be offline. Please try again.'
        }), 502)

    # at least one paramater is required
    status, color, intensity = getLEDParams(request.args, request.json)
    if status or color or intensity is not None:
        pass
    else:
        return make_response(jsonify({
            'error': '/LED requires at least one param.' +
            'See /LED/info'}), 400)

    # handle invalid user request params
    if status and status not in ("on", "off"):
        return make_response(jsonify({
            'error': '/LED \'status\' only accepts the following options: ' +
            '[\'on\', \'off\']'}), 400)

    if color and color not in colors_allowed:
        return make_response(jsonify({
            'error': '/LED \'color\' only accepts the following options: ' +
            str(colors_allowed)}), 400)

    try:
        if intensity is not None:
            intensity = int(intensity)
    except Exception:
        return make_response(jsonify({
            'error': '/LED \'intensity\' only accepts the following options: ' +
            'int(0 to 100)'}), 400)

    if intensity and intensity not in range(0, 101):
        return make_response(jsonify({
            'error': '/LED \'intensity\' only accepts the following options: ' +
            'int(0 to 100)'}), 400)

    # build the query string to be sent to the LED RPi
    queryString = "?"
    if status is not None:
        queryString += "status=" + str(status) + '&'
    if color is not None:
        queryString += "color=" + str(color) + '&'
    if intensity is not None:
        queryString += "intensity=" + str(intensity)

    # send our LED change request to the LED RPi
    try:
        r = requests.put(
            'http://' + str(ip) + ':' + str(port) +
            '/LED/change' + queryString)
        res_body = r.json()
    except Exception:
        return make_response(jsonify({
            'error': 'LED RPi service is unavailable. Please try again.'
        }), 503)

    # pass this response to the end user
    if r.status_code == requests.codes.ok:
        return make_response(jsonify(res_body), 201)
    else:
        return make_response(jsonify(res_body), 400)


# this is a helper function that extracts query params
# from the end user's request for clean forwarding to
# the LED RPi
def getLEDParams(args, json):
    status = None
    if not args or 'status' not in args:
        if not json or 'status' not in json:
            pass
        else:
            status = json['status']
    else:
        status = args['status']

    color = None
    if not args or 'color' not in args:
        if not json or 'color' not in json:
            pass
        else:
            color = json['color']
    else:
        color = args['color']

    intensity = None
    if not args or 'intensity' not in args:
        if not json or 'intensity' not in json:
            pass
        else:
            intensity = json['intensity']
    else:
        intensity = args['intensity']

    return status, color, intensity


# this is a helper function that handles blanket 404 errors
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({
        'error': 'Invalid route. ' +
        'See /info'
    }), 404)

def main(args):
	global IP
	global PORT
	IP = args.ip_address
	PORT = args.flask_port
	app.run(host='0.0.0.0', port=8080, debug=True)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Sends appropriate response to OutdoorPi given an image')
	
	parser.add_argument('--ip_address',
						'-ip',
						help="The IP address of the OutdoorPi",
						type=str)
						
	parser.add_argument('--flask_port',
						'-p',
						help="The port number of the Flask server hosted by the OutdoorPi",
						type=int)
						
	if len(sys.argv) != 5:
		print("Error: Too few arguments provided. Please see --help for more information.")
	else:
		main(parser.parse_args(sys.argv[1:]))