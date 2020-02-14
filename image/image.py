import logging
import os
from time import sleep

import cv2
import numpy

from picamera import PiCamera

picam = PiCamera()
picam.resolution = (2592, 1944)
path = "./data/"
sleep(2)  # Pause to give the camera time to adjust

id = 0

logger = logging.getLogger('astro')

class Image:
    _ndvi = None
    _score = None
    _id = None

    def __init__(self, image, id_=None):
        logger.info('Image init')

        # Check if image is numpy.ndarray
        if not isinstance(image, numpy.ndarray):
            raise TypeError('Expected image, not {}'.format(type(image)))

        self.original = image
        global id
        if id_ is None:
            self.id = id
            id += 1
        else:
            self.id = id_

        logger.debug('function __init__ end')

    @property
    def ndvi(self):
        """
        Calculates NDVI values for each pixel (NDVI = (NIR + B) / (NIR - B))
        :return: numpy.ndarray NDVI image
        """
        logger.debug('function ndvi start')

        # Check if result has been stored earlier
        if self._ndvi is not None:
            return self._ndvi

        # Get each color of the image
        blue, _, near_ir = cv2.split(self.original)

        bottom = near_ir.astype(float) + blue.astype(float)
        # Replace zeroes with near zero value
        bottom[bottom == 0] = 0.0000000000000001

        top = near_ir.astype(float) - blue.astype(float)

        self._ndvi = top / bottom # Store result

        logger.debug('function ndvi end')
        return self._ndvi

    @property
    def score(self):
        """
        Calculates the score based on average NDVI value and average brightness.
        :return: int score
        """
        logger.debug('function score start')

        if self._score is not None:
            return self._score

        # Get average brightness from grayscale of original
        brightness = cv2.mean(cv2.cvtColor(
            self.original, cv2.COLOR_BGR2GRAY))[0]
        ndvi_average = cv2.mean(self.ndvi)[0]

        logger.debug('Image brightness: {}, ndvi_average: {}'.format(brightness, ndvi_average))

        score = round(brightness)

        if -0.2 < ndvi_average < 0:  # Likely ocean
            score = round(score / 2)

        if 200 < brightness:  # Clouds
            score = round(score / 4)

        logger.debug('function score end')
        return max(0, score) # return positive score

    @property
    def id(self):
        logger.debug('function score start')

        # ID is read only, unless it havent been set
        logger.debug('function score end')
        return self._id

    @id.setter
    def id(self, value):
        logger.debug('function id_setter start')

        if self._id is None:
            self._id = value
            return

        logger.debug('function id_setter end')
        raise AttributeError("ID can only be set once")

    @property
    def path(self):
        '''Returns the absolute path of the image'''
        logger.debug('function path start and end')
        return os.path.abspath("{}{}.jpg".format(path, self.id))

    @property
    def name(self):
        '''Returns the image name'''
        logger.debug('function name start and end')
        return "{}.jpg".format(self.id)

    @classmethod
    def capture_image(cls):
        logger.debug('function capture_image start')

        picam.capture("{}{}.jpg".format(path, id))

        logger.debug('function capture_image end')
        return cls(cv2.imread("{}{}.jpg".format(path, id)))
