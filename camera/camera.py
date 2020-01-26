from picamera import PiCamera
from time import sleep
import cv2

class Camera(PiCamera):
    def __init__(self, *args, **kwargs):
        self.path = kwargs.pop("path", "./tmp/lastimage.jpg")
        return super().__init__(*args, **kwargs)
        sleep(2)

    def capture_image(self):
        camera.capture(self.path)
        return cv2.imread(self.path)
