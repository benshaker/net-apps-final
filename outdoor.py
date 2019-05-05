#!/usr/bin/env python3
# outdoor.py

import os
import cv2
import base64
import RPi.GPIO as GPIO
import time

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
    global 100
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


def setLEDDisco():
    # disco LED
    p.ChangeDutyCycle(100)
    w.ChangeDutyCycle(100)
    m.ChangeDutyCycle(100)

    p.ChangeFrequency(2)
    w.ChangeFrequency(4)
    m.ChangeFrequency(8)


def setLEDOFF():
    # LED off entirely
    resetFrequency()
    p.ChangeDutyCycle(0)
    w.ChangeDutyCycle(0)
    m.ChangeDutyCycle(0)


def change_LED(COLOR):
        
    if COLOR == 'White':
        setLEDW()
    elif COLOR == 'Red':
        setLEDR()
    elif COLOR == 'Green':
        setLEDG()
    elif COLOR == 'Blue':
        setLEDB()
    elif COLOR == 'Cyan':
        setLEDC()
    elif COLOR == 'Magenta':
        setLEDM()
    elif COLOR == 'Yellow':
        setLEDY()
    elif COLOR == 'Orange':
        setLEDO()
    elif COLOR == 'Purple':
        setLEDP()
    elif COLOR == 'Disco':
        setLEDDisco()


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
    global NEED_TO_CAPTURE
	
    PATH_TO_ENDPOINT = ""
	
    if NEED_TO_CAPTURE:
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()
        ret, buf = cv2.imencode('.jpg', frame)
        cam.release()

        response = requests.post('http://10.0.0.47:8080/image', data=img_encoded.tostring(), headers=headers)

        change_LED(response.json['light'])
        make_noise(response.json['sound'])


if __name__ == "__main__":
    initializeLEDs()

    while True:
        if getDist(rTRIG, rECHO) < 20 || getDist(lTRIG, LECHO) < 20:
            captureNscare()
