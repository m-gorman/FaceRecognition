import numpy as np
import base64
import cv2
import pickle
import face_recognition

face_data = pickle.loads(open("encodings.pickle", "rb").read())
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

def get_faces(b64_image):
    jpg_as_np = np.frombuffer(base64.b64decode(b64_image), dtype=np.uint8)
    image_buffer = cv2.imdecode(jpg_as_np, flags=1)

    gray = cv2.cvtColor(image_buffer, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(image_buffer, cv2.COLOR_BGR2RGB)

    rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
        minNeighbors=5, minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE)

    boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

    encodings = face_recognition.face_encodings(rgb, boxes)
    names = []

    for encoding in encodings:
        matches = face_recognition.compare_faces(face_data["encodings"],
            encoding)
        name = "Unknown"

        if True in matches:
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}
            for i in matchedIdxs:
                name = face_data["names"][i]
                counts[name] = counts.get(name, 0) + 1

            name = max(counts, key=counts.get)
            names.append(name)

    has_faces = len(encodings) > 0
    return has_faces, names