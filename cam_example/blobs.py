import sensor
import image
import time
import math
import pyb
from pyb import UART
from pyb import Pin
import omv
import rpc

try:
    with open('thresholds.txt') as file:
        thresholds = file.read()
    thresholds = eval(thresholds)
except Exception:
    thresholds = [
        [0, 100, -128, 127, -128, 127],
        [0, 100, -128, 127, -128, 127],
        [0, 100, -128, 127, -128, 127],
        [0, 100, -128, 127, -128, 127],
        [0, 100, -128, 127, -128, 127],
    ]

yellow_thr = thresholds[0]
blue_thr = thresholds[1]
obst_thr = thresholds[2]

SCREEN_CENTER = (160, 120)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)

sensor.skip_frames(time = 2000)

import connect_to_kostyli
usb_vbus = Pin("USB_VBUS", Pin.IN, Pin.PULL_DOWN)
if(usb_vbus.value()):
    #pyb.LED(2).on()
    connect_to_kostyli.connect_to_comp()
    pass

clock = time.clock()

uart = UART(3, 115200)

while True:
    clock.tick()
    img = sensor.snapshot()

    img.draw_circle(*SCREEN_CENTER, 5, color=(255, 0, 0), fill=True)

    for blob in img.find_blobs([blue_thr], pixels_threshold=50, area_threshold=50):
        if blob.roundness() > 0:
            img.draw_edges(blob.corners(), color=(255, 0, 0))

    for blob in img.find_blobs([yellow_thr], pixels_threshold=50, area_threshold=50):
        if blob.roundness() > 0:
            img.draw_edges(blob.corners(), color=(255, 0, 0))

    print(clock.fps())
