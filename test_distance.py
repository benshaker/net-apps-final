#!/usr/bin/python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

# Port Vslues
rTRIG = 8
lTRIG = 10
rECHO = 16
lECHO = ?

GPIO.setup(rTRIG, GPIO.OUT)
GPIO.setup(rECHO, GPIO.IN)
GPIO.setup(lTRIG, GPIO.OUT)
GPIO.setup(lECHO, GPIO.IN)
GPIO.output(rTRIG, GPIO.LOW)
GPIO.output(lTRIG, GPIO.LOW)

def getDist(TRIG, ECHO):
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG, GPIO.LOW)

    while GPIO.input(ECHO)==0:
        pulse_start_time = time.time()
    while GPIO.input(ECHO)==1:
        pulse_end_time = time.time()

    pulse_duration = pulse_end_time - pulse_start_time
    Dist = round(pulse_duration * 17150, 2)

    return Dist

for x in range(20):
    print getDist(rTRIG, rECHO)
    print getDist(lTRIG, lECHO)
