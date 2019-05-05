#!/usr/bin/env python3
# outdoor.py

import os
import cv2
import base64
import numpy as np
import RPi.GPIO as GPIO
import time
import requests

# Suppress Warnings
GPIO.setwarnings(False)

# Ports used for proximity sensors
rTRIG = 8
rECHO = 10
lTRIG = 16
lECHO = 18

# setup pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(rTRIG, GPIO.OUT)
GPIO.setup(rECHO, GPIO.IN)
GPIO.setup(lTRIG, GPIO.OUT)
GPIO.setup(lECHO, GPIO.IN)
GPIO.setup(11, GPIO.OUT)  # Red
GPIO.setup(13, GPIO.OUT)  # Green
GPIO.setup(15, GPIO.OUT)  # Blue
GPIO.output(rTRIG, GPIO.LOW)
GPIO.output(lTRIG, GPIO.LOW)
p = GPIO.PWM(11, 100)
w = GPIO.PWM(13, 100)
m = GPIO.PWM(15, 100)

# prepare headers for http request
content_type = 'image/jpeg'
headers = {'content-type': content_type}

def initializeLEDs():
    p.start(0)
    w.start(0)
    m.start(0)


def resetFrequency():
    p.ChangeFrequency(100)
    w.ChangeFrequency(100)
    m.ChangeFrequency(100)


def setLEDW():
    # white LED - Waiting for command
    resetFrequency()
    p.ChangeDutyCycle(100)
    w.ChangeDutyCycle(100)
    m.ChangeDutyCycle(100)


def setLEDR():
    # red LED
    resetFrequency()
    p.ChangeDutyCycle(100)
    w.ChangeDutyCycle(0)
    m.ChangeDutyCycle(0)


def setLEDG():
    # green LED
    resetFrequency()
    p.ChangeDutyCycle(0)
    w.ChangeDutyCycle(100)
    m.ChangeDutyCycle(0)


def setLEDB():
    # blue LED
    resetFrequency()
    p.ChangeDutyCycle(0)
    w.ChangeDutyCycle(0)
    m.ChangeDutyCycle(100)


def setLEDM():
    # magenta LED
    resetFrequency()
    p.ChangeDutyCycle(100)
    w.ChangeDutyCycle(0)
    m.ChangeDutyCycle(100)


def setLEDC():
    # cyan LED
    resetFrequency()
    p.ChangeDutyCycle(0)
    w.ChangeDutyCycle(100)
    m.ChangeDutyCycle(100)


def setLEDY():
    # yellow LED
    resetFrequency()
    p.ChangeDutyCycle(100)
    w.ChangeDutyCycle(100)
    m.ChangeDutyCycle(0)


def setLEDO():
    # orange LED
    resetFrequency()
    p.ChangeDutyCycle(100)
    w.ChangeDutyCycle(25)
    m.ChangeDutyCycle(0)


def setLEDP():
    # purple LED
    resetFrequency()
    p.ChangeDutyCycle(33)
    w.ChangeDutyCycle(0)
    m.ChangeDutyCycle(100)


def setLEDOFF():
    # LED off entirely
    resetFrequency()
    p.ChangeDutyCycle(0)
    w.ChangeDutyCycle(0)
    m.ChangeDutyCycle(0)


def change_LED(COLOR):

    if COLOR == 'white':
        setLEDW()
    elif COLOR == 'red':
        setLEDR()
    elif COLOR == 'green':
        setLEDG()
    elif COLOR == 'blue':
        setLEDB()
    elif COLOR == 'cyan':
        setLEDC()
    elif COLOR == 'magenta':
        setLEDM()
    elif COLOR == 'yellow':
        setLEDY()
    elif COLOR == 'orange':
        setLEDO()
    elif COLOR == 'purple':
        setLEDP()


def make_noise(SOUND):

    if SOUND != None:
        os.system('aplay -q -D bluealsa:HCI=hci0,DEV=FC:58:FA:A6:22:95,PROFILE=a2dp ' + SOUND)


def getDist(TRIG, ECHO):
    # Repsonse of 10000 means the sensor did not read correctly
    # Occurs when the pulse returns before the echo is read

    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG, GPIO.LOW)

    start_time = time.time()

    while GPIO.input(ECHO)==0:
        pulse_start_time = time.time()
        if pulse_start_time - start_time > 1:
            return 10000

    while GPIO.input(ECHO)==1:
        pulse_end_time = time.time()
        if pulse_end_time - pulse_start_time > 1:
            return 10000
    try:
         pulse_duration = pulse_end_time - pulse_start_time
    except:
         return 10000
    Dist = round(pulse_duration * 17150, 2)

    return Dist


def captureNscare():
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()
        ret, img_encoded = cv2.imencode('.jpg', frame)
        cam.release()

        response = requests.post('http://10.0.0.47:8080/image', data=img_encoded.tostring(), headers=headers)

        change_LED(response.json()['light'])
        make_noise(response.json()['sound'])


if __name__ == "__main__":
    initializeLEDs()
    prevTime = time.time() - 5

    while True:
        curTime = time.time()
        if curTime - prevTime > 5 and (getDist(rTRIG, rECHO) < 20 or getDist(lTRIG, lECHO) < 20):
            prevTime = time.time()
            captureNscare()
