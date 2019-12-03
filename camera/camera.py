import time
import cv2
import atexit

capture = cv2.VideoCapture(0)
capture.set(3, 2592)
capture.set(4, 1944)
capture.set(5, 10)
atexit.register(capture.release)
time.sleep(1) # Camera warmup

def capture_image():
    _, frame = capture.read()
    return frame
