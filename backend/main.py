from flask import Flask, send_file
from flask_cors import CORS
from flask import request
from algo import workflow
import cv2
import numpy as np
import base64
import os
app = Flask(__name__)
CORS(app)
img_dir = "images"
file_dir = os.path.join(os.getcwd(), img_dir)

def create_dir():
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)

@app.route("/post/image", methods=["POST"])
def hello_world():
    if request.method == "POST":
        f = request.files['file']
        f_name = f.filename
        base = os.path.splitext(f_name)[0]
        f_name = base+".jpg"
        f_path = os.path.join(file_dir, f_name)
        f.save(f_path)
        workflow(f_path)
        return send_file(f_path, mimetype='image/jpg')


@app.route("/ping", methods=["GET"])
def ping():
    return "pong"


if __name__ == "__main__":
    create_dir()
    app.run(host="0.0.0.0", port=8888)