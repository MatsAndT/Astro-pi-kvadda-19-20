from time import sleep

import os
import cv2
import numpy
import logging
from logging import handlers
from picamera import PiCamera

picam = PiCamera()
picam.resolution = (2592, 1944)
path = "./data/"
sleep(2)  # Pause to give the camera time to adjust

id = 0

filename = "log.log"

# if the logging is imported the root will be file name
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# How the logs are going to look
formatter = logging.Formatter(
    '%(levelname)s:%(asctime)s:%(name)s:%(funcName)s:%(message)s')


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
        if id is None:
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

        if self._ndvi is not None:
            return self._ndvi

        # Get each color of the image
        blue, _, near_ir = cv2.split(self.original)

        bottom = near_ir.astype(float) + blue.astype(float)
        # Replace zeroes with near zero value
        bottom[bottom == 0] = 0.0000000000000001

        top = near_ir.astype(float) - blue.astype(float)

        self._ndvi = top / bottom

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

        # TODO: log brightness and average ndvi for debug

        score = round(brightness)

        if -0.2 < ndvi_average < 0:  # Likely ocean
            score = round(score / 2)

        if 200 < brightness:  # Clouds
            score = round(score / 4)

        logger.debug('function score end')
        return max(0, score)

    @property
    def id(self):
        logger.debug('function score start')

        # ID is read only, unless it havent been set
        logger.debug('function score end')
        return self._id

    @id.setter
    def id_setter(self, value):
        logger.debug('function id_setter start')

        if self._id is None:
            self._id = value
            return

        raise AttributeError("ID can only be set once")
        logger.debug('function id_setter end')

    @property
    def path(self):
        logger.debug('function path start and end')
        return os.path.abspath("{}{}.jpg".format(path, self.id))

    @property
    def name(self):
        logger.debug('function name start and end')
        return "{self.id}.jpg"

    @classmethod
    def capture_image(cls):
        logger.debug('function capture_image start')

        picam.capture("{}{}.jpg".format(path, id + 1))

        logger.debug('function score end')
        return cls(cv2.imread(path))
