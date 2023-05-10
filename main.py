from hcsr04 import HCSR04
from time import sleep
from machine import Pin

import time
import network

ssid = 'Your network name'
password = 'Your password'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Wait for connect or fail
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )


led_r = Pin(15, Pin.OUT)
led_y = Pin(14, Pin.OUT)
led_g = Pin(13, Pin.OUT)

sensor = HCSR04(trigger_pin=19, echo_pin=18, echo_timeout_us=10000)

def red():
    led_g.off()
    led_y.off()
    led_r.on()
    
def yellow():
    led_g.off()
    led_y.on()
    led_r.off()

def green():
    led_g.on()
    led_y.off()
    led_r.off()
    
def leds_off():
    led_g.off()
    led_y.off()
    led_r.off()

def flash_red():
    red()
    sleep(.1)
    leds_off()
    sleep(.1)
    print(distance)

while True:
    distance = sensor.distance_cm()
    if distance < 3:
        while distance < 3:
            flash_red()
    elif distance > 0 and distance < 10:
        red()
        print(distance)
    elif distance >= 10 and distance < 20:
        yellow()
        print(distance)
    elif distance >= 20 and distance < 30:
        green()
        print(distance)
    else:
        print(distance)
        leds_off()
    sleep(.1)