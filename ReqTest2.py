import requests
import json
from imutils.video import VideoStream
import time
import imutils
import cv2
import base64
from Timer import Timer
from collections import Counter
import pygame
from pygame import mixer
from MotionDetection import MotionDetector

def Make_Face_Request(frames):

    encoded_frames = []
    for frame in frames:
        retval, buff = cv2.imencode(".jpg", frame)
        encoded = base64.b64encode(buff)
        encoded_frames.append(encoded)

    # defining a params dict for the parameters to be sent to the API 
    PARAMS = {'images':json.dumps(encoded_frames)}
  
    # sending get request and saving the response as response object 
    r = requests.get(url = "http://127.0.0.1:80/GetFaces", params = PARAMS) 
  
    # extracting data in json format 
    return r.json()

# make noise depending on who's there
def Doorbell(names):
    if len(names) == 0:
        mixer.init()
        mixer.music.load('sounds/ding_dong.mp3')
        mixer.music.play()
        return

    if len(names) > 1:
        joined = " and ".join(names)
        say = "Welcome ", joined
        os.system("echo \"%s\" | espeak" % say)
        return

    name = names[0]

    if (name == "Michael"):
        mixer.init()
        mixer.music.load('sounds/oh_ah_ah.mp3')
        mixer.music.play()

    if (name == "Dan"):
        mixer.init()
        mixer.music.load('sounds/aha_aha.mp3')
        mixer.music.play()

pygame.init()
pygame.display.set_mode()

cap = cv2.VideoCapture("vids/2.mp4")
ret, frame = cap.read()
d = MotionDetector(frame)

frame_hist = []

while cap.isOpened():
    ret, frame = cap.read()
    cv2.imshow("view", frame)
    key = cv2.waitKey(1) & 0xFF

    movement_frames = d.Detect_Motion(frame)

    curr_sec = int(time.time())

    for frame in movement_frames:
        frame_hist.append([frame, time.time()])

    frame_hist = [f for f in frame_hist if f[1] > time.time() - 10]


    #print names

    #if len(frame_hist) > 15:
    #    frames = [f[0] for f in frame_hist]
    #    names = Make_Face_Request(frames)
    #    print names
        #Doorbell(names)