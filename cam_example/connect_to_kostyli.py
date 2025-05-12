import pyb
import sensor
import image
import time
import math
from pyb import UART
from pyb import Pin
import omv
import rpc


def connect_to_comp():
    omv.disable_fb(True)

    interface = rpc.rpc_usb_vcp_slave()

    def stream_generator_cb():
        img = sensor.snapshot()
        img.to_jpeg(quality=90)
        try:
            with open("thresholds.txt") as file:
                thr = file.read()
        except Exception:
            thr = [[0, 100, -127, 127, -127, 127],
                    [0, 100, -127, 127, -127, 127],
                    [0, 100, -127, 127, -127, 127],
                    [0, 100, -127, 127, -127, 127],
                    [0, 100, -127, 127, -127, 127],]

        thr_bt = bytearray(str(thr), 'utf8')
        thr_bt += bytearray([0] * (300 - len(thr_bt)))

        bt = thr_bt + img.bytearray()

        return bt

    def jpeg_image_stream_cb():
        interface.stream_writer(stream_generator_cb)

    def save_thresholds(thr):
        with open("thresholds.txt", 'w') as file:
            file.write(thr)
        interface.schedule_callback(jpeg_image_stream_cb)
        return bytes()

    def jpeg_image_stream(data):
        params = bytes(data).decode().split(";")
        sensor.set_pixformat(eval(params[0]))
        sensor.set_framesize(eval(params[1]))
        interface.schedule_callback(jpeg_image_stream_cb)
        return bytes()

    JPEG_IMAGE_STREAM_CALLBACK = 48
    SAVE_THRESHOLDS_CALLBACK = 96

    interface.register_callback(jpeg_image_stream)
    interface.register_callback(save_thresholds)

    interface.loop()

