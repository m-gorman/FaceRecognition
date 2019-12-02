import requests
import json
from imutils.video import VideoStream
import time
import imutils
import cv2
import base64
import MotionDetection
from Timer import Timer
from collections import Counter
import pygame
from pygame import mixer

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=1).start()
time.sleep(2.0)

frame = vs.read()
frame = imutils.resize(frame, width=500)

motion_detector = MotionDetection.MotionDetector(frame)

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


motion_timer = Timer(5)
# we will wait this long until we start detecting motion again after a face id request
motion_cooldown = 1

names = []

while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=500)

    if motion_timer.elapsed() > motion_cooldown and motion_detector.Detect_Motion(frame):
        print "Detection motion"
        # take photo every 0.2 seconds for 2 seconds
        frames = []
        timer = Timer()
        while len(frames) < 10:
            cv2.imwrite(str(time.time()) + ".jpg", frame)
            frame = vs.read()
            frame = imutils.resize(frame, width=500)
            frames.append(frame)
            time.sleep(0.3)
        print "Making request"
        names = Make_Face_Request(frames)
        counted = Counter(names)
        names = [n for n in counted if counted[n] > 6]
        motion_timer = Timer()

    print names
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                Doorbell(names)