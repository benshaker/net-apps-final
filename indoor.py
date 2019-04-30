#!/usr/bin/env python3
# indoor.py

from indoor_keys import CloudVisionKey
import requests

# example request below
#   note that content must be a base64 string
#   starting with /9j/ or whatever

# {
#   "requests":[
#     {
#       "image":{
#         "content":"/9j/7QBEUGhvdG9...image contents...eYxxxzj/Coa6Bax//Z"
#       },
#       "features":[
#         {
#           "type":"LABEL_DETECTION",
#           "maxResults":1
#         }
#       ]
#     }
#   ]
# }

r = requests.post(
    'https://vision.googleapis.com/v1/images:annotate?key='
     + CloudVisionKey,
    json=dataz)
json_res = r.json()
responses = json_res['responses']
annotations = responses[0]['labelAnnotations']

for annote in annotations:
    print(annote['description'], annote['score'])
