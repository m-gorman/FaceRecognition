#!flask/bin/python
from flask import Flask
from flask import request
import json
import FaceRec

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/GetFaces')
def GetFaces():
    images = request.args.get('images')
    images = json.loads(images)

    names = []
    has_faces_count = 0

    for image in images:
        has_faces, names = FaceRec.get_faces(image)
        if has_faces:
            has_faces_count += 1

    return json.dumps([has_faces_count, len(images), names])

if __name__ == '__main__':
    app.run(port='80')