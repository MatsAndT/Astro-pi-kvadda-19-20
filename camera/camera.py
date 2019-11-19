import time
import cv2

from io import BytesIO
from picamera import PiCamera
from picamera.array import PiRGBArray

camera = PiCamera()
raw_capture = PiRGBArray(camera)
time.sleep(0.3) # Camera warmup

def capture_image():
    camera.capture(raw_capture, format="bgr")
    return raw_capture.array