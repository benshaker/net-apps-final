#!/usr/bin/python
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Port Vslues
rTRIG = 8
rECHO = 10
lTRIG = 16
lECHO = 18

GPIO.setup(rTRIG, GPIO.OUT)
GPIO.setup(rECHO, GPIO.IN)
GPIO.setup(lTRIG, GPIO.OUT)
GPIO.setup(lECHO, GPIO.IN)
GPIO.output(rTRIG, GPIO.LOW)
GPIO.output(lTRIG, GPIO.LOW)

time.sleep(2)

def getDist(TRIG, ECHO):
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

while True:
    print(getDist(rTRIG, rECHO))
    print(getDist(lTRIG, lECHO))
    # getDist(rTRIG, rECHO)
