# USAGE
# python pi_face_recognition.py --cascade haarcascade_frontalface_default.xml --encodings encodings.pickle

# import the necessary packages
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
import base64
import numpy as np

seen_dict = {}
conseq_frames = {}


# load the known faces and embeddings along with OpenCV's Haar
# cascade for face detection
print("[INFO] loading cascade...")
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

# start the FPS counter
fps = FPS().start()

# loop over frames from the video file stream
while True:
	# grab the frame from the threaded video stream and resize it
	# to 500px (to speedup processing)
	frame = vs.read()
	frame = imutils.resize(frame, width=500)

	retval, buff = cv2.imencode(".jpg", frame)
	jpg_as_text = base64.b64encode(buff)
	print(jpg_as_text)

	1/0
	
	# convert the input frame from (1) BGR to grayscale (for face
	# detection) and (2) from BGR to RGB (for face recognition)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

	# detect faces in the grayscale frame
	rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
		minNeighbors=5, minSize=(30, 30),
		flags=cv2.CASCADE_SCALE_IMAGE)

	# OpenCV returns bounding box coordinates in (x, y, w, h) order
	# but we need them in (top, right, bottom, left) order, so we
	# need to do a bit of reordering
	boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

	# loop over the recognized faces
	for (top, right, bottom, left) in boxes:
		# draw the predicted face name on the image
		cv2.rectangle(frame, (left, top), (right, bottom),
			(0, 255, 0), 2)

		print top, bottom, left, right
		cropped_face = frame[top:bottom, left:right]
		retval, buff = cv2.imencode(".jpg", cropped_face)
		jpg_as_text = base64.b64encode(buff)
		print(jpg_as_text)

		jpg_as_np = np.frombuffer(base64.b64decode(jpg_as_text), dtype=np.uint8)
		image_buffer = cv2.imdecode(jpg_as_np, flags=1)
		cv2.imshow("decoded", image_buffer)

	# display the image to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

	# update the FPS counter
	fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()