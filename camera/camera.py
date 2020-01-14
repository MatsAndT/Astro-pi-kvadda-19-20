from picamera import PiCamera
from time import sleep
import cv2

path = "./tmp/lastimage.jpg"

camera = PiCamera()
sleep(2)

def capture_image():
    camera.capture(path)
    return cv2.imread(path)