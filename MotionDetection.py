import cv2
import numpy as np
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2
import os
from pygame import mixer
import random

class MotionDetector():
    def __init__(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        self.last_frame = gray

        # dimensions of the image * 255
        self.max_diff = 375 * 500 * 255
        self.avg = None

    # returns true if motion detected since last call
    def Detect_Motion(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # if the average frame is None, initialize it
        if self.avg is None:
            print("[INFO] starting background model...")
            self.avg = gray.copy().astype("float")



        cv2.accumulateWeighted(gray, self.avg, 0.01)

        diff = cv2.absdiff(gray, cv2.convertScaleAbs(self.avg))
        thresh = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=5)

        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        biggest = max([cv2.contourArea(c) for c in cnts]) if cnts else 0
        rects = []
        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < 4000:
                continue


            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)

            #frame[y:y+h,x:x+w] = [random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)]

            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            rects.append(img[y:y+h,x:x+w])

        cv2.imshow("tresh", thresh)

        cv2.imshow("avg", cv2.convertScaleAbs(self.avg))

        cv2.imshow("test", img)
        
        # display the image to our screen
        key = cv2.waitKey(1) & 0xFF

        return rects