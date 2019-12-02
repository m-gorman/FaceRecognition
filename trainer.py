import numpy as np
import cv2
from PIL import Image
import time
import glob
from os import path
from random import randint
import sys

face_detector = cv2.CascadeClassifier('cascade/haarcascade_frontalface_default.xml')

name = raw_input("Enter name: ")

img_dir = path.join('faces', name)
for im_path in glob.glob('training/*.jpg'):

	#img_numpy = np.array(PIL_img,'uint8')


    window = cv2.namedWindow('x', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('x', 900,900)
    
    img = cv2.imread(im_path)
    height, width = img.shape[:2]

	#image = cv2.resize(image,(240,240))
	
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        #cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 10)

        print x,y,w,h

        x_left = -30
        y_left = -30
        x_right = 30
        y_right = 30

        if x + x_left < 0:
            x_left = 0
        if y + y_left < 0:
            y_left = 0
        if x + w + x_right > width:
            x_right = 0
        if y + h + y_right > height:
            y_right = 0

        cv2.imshow('x', img[y+y_left:y+h+y_right,x+x_left:x+w+x_right])


        i = cv2.waitKey(0)

        if i == 121:
            img_path = path.join(img_dir, str(randint(0,10000)) + ".jpg")
            print "SAVING to " + img_path
            cv2.imwrite(img_path, img[y+y_left:y+h+y_right,x+x_left:x+w+x_right])

        if i == 110:
            print "Ignoring"

        if i == 133:
            print "Quitting..."
            break
