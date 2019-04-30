#!/usr/bin/env python3
# outdoor.py

import cv2
import picamera
from flask import Flask, send_file, requests
from six import StringIO

@app.route("/camera")
def camera_stuff():
	cam = cv2.VideoCapture(0)
	global CUR_IMG, PATH_TO_ENDPOINT
	
	PATH_TO_ENDPOINT = ""
	
	while True:
		if not cam.isOpened():
			cam = cv2.VideoCapture(0)
			
		ret, frame = cam.read()
		cv2.imshow('frame', frame)
		frame_im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		pil_im = Image.fromarray(frame_im)
		stream = StringIO()
		pil_im.save(stream, format="JPEG")
		stream.seek(0)
		CUR_IMG = stream.read()
		files = {'image': CUR_IMG}
		response = requests.post(
			url = PATH_TO_ENDPOINT,
			files=files
		)
		
	
	
	
