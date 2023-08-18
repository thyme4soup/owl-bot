import RPi.GPIO as GPIO
from RPi.GPIO import BOARD, HIGH, LOW, OUT
import time
import random
import math

#  ---2-
# 6    7
# |    |
#  --5-
# |    |
# 3    1
# ---4-  [0]

SEGMENTS = 8
OPEN = [HIGH, LOW, LOW, LOW, LOW, HIGH, LOW, LOW]
CLOSED = [HIGH, HIGH, HIGH, HIGH, HIGH, LOW, HIGH, HIGH]
TEST = [HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, LOW]

ser = 7
srck = 29
srclr_bar = 26
rck = 31
gbar = 24

#GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(ser, OUT)
GPIO.setup(srck, OUT)
GPIO.setup(srclr_bar, OUT)
GPIO.setup(rck, OUT)
GPIO.setup(gbar, OUT)

def get_blink_s(expected):
    lambd = 1.0 / expected # lambda -- expected strikes per period time i.e. lambda = 0.5 -> 1 strike expected every 2 seconds
    r = random.random()
    x = (-1.0 / lambd) * math.log(1 - r) # transform uniform var on (0,1) to exponential distribution
    return x # return in ms

def clk(pin):
    GPIO.output(pin, HIGH);
    GPIO.output(pin, LOW);

def send_data(data):
    GPIO.output(gbar, LOW)
    GPIO.output(srclr_bar, HIGH)
    GPIO.output(srck, LOW)
    GPIO.output(rck, LOW)
    for datum in data:
        GPIO.output(ser, datum)
        clk(srck)
    clk(rck)

def set_eyes(data):
    send_data(data)
    send_data(data)

while True:
    set_eyes(OPEN)
    blink_s = get_blink_s(3.0)
    print(f'sleeping {blink_s} seconds')
    time.sleep(blink_s)
    set_eyes(CLOSED)
    time.sleep(0.2)
