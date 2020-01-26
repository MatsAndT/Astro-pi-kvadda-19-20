import cv2
import numpy

class Image:
    _ndvi = None

    def __init__(self, image):

        # Check if image is numpy.ndarray
        if not isinstance(image, numpy.ndarray):
            raise TypeError('Expected image, not {}'.format(type(image)))

        self.original = image

    @property
    def ndvi(self):
        """
        Calculates NDVI values for each pixel (NDVI = (NIR + B) / (NIR - B))
        :return: numpy.ndarray NDVI image
        """

        if self._ndvi is not None:
            return self._ndvi

        # Get each color of the image
        blue, _, near_ir = cv2.split(self.original) 

        bottom = near_ir.astype(float) + blue.astype(float)
        bottom[bottom == 0] = 0.0000000000000001 # Replace zeroes with near zero value

        top = near_ir.astype(float) - blue.astype(float)
        
        self._ndvi = top / bottom
        return self._ndvi
