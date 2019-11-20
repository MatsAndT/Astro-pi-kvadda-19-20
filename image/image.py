import cv2
import numpy

class Image:
    def __init__(self, image):
        if not isinstance(image, numpy.ndarray):
            raise TypeError('Expected image, not {}'.format(type(image)))
        self.original = image

    @property
    def ndvi(self):
        b, _, nir = cv2.split(self.original) 

        bottom = nir.astype(float) + b.astype(float)
        bottom[bottom == 0] = 0.0000000000000001

        top = nir.astype(float) - b
        
        return top / bottom

