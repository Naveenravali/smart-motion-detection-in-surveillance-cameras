import cv2
import numpy


def crop_image(img: numpy.ndarray, x, y, h, w) -> numpy.ndarray:
    """
    this method will crop the image. \n
    1. img is numpy.ndarray \n
    2. x is the starting x co-ordinate \n
    3. y is the starting y co-ordinate \n
    4. h is the height \n
    5. w is the width
    """
    return img[y:y + h, x:x + w]


def get_height_and_width(frame: numpy.ndarray) -> tuple:
    """ This will return the 'Height' and 'Width' of the image """
    # h, w = len(frame), len(frame[0])      # getting height and width through length of rows and columns.
    h, w = frame.shape[:2]
    return h, w


def image_preprocess(frame: numpy.ndarray) -> numpy.ndarray:
    """This will return an image that was converted to Grayscale and then gaussian blur applied"""
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (5, 5), 0.5)
    return img

