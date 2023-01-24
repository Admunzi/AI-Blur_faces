"""
This application will recognize faces via amazon rekognition and will blur the faces.
The web app will be hosted on localhost:5000
With a form to upload one or more images and return the images with the faces blurred.

Author: Daniel Ayala Cantador

"""
import uuid

from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import boto3
from PIL import Image, ImageFilter

APP = Flask(__name__)
APP.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
# APP.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png']
APP.config['UPLOAD_PATH'] = 'static/uploads/'

CLIENT_REKOGNITION = boto3.client('rekognition', region_name='us-east-1')


@APP.route('/')
def index():
    return render_template("index.html")


def detect_faces_local_file(name_img):
    with open(APP.config['UPLOAD_PATH'] + name_img, 'rb') as image:
        response = CLIENT_REKOGNITION.detect_faces(Image={
            'Bytes': image.read()
        },
            Attributes=['ALL', ])

    return response


def blur_faces(filename, faces_detected, minor_blur):
    image = Image.open(APP.config['UPLOAD_PATH'] + filename)

    for face in faces_detected['FaceDetails']:
        if minor_blur and face['AgeRange']['Low'] < 18:
            create_blured_box(face, image)

        if not minor_blur:
            create_blured_box(face, image)

    image.save(APP.config['UPLOAD_PATH'] + filename)
    return filename


def create_blured_box(face, image):
    box = face['BoundingBox']
    x = image.size[0] * box['Left']
    y = image.size[1] * box['Top']
    w = image.size[0] * box['Width']
    h = image.size[1] * box['Height']
    region = image.crop((x, y, x + w, y + h))
    region = region.filter(ImageFilter.GaussianBlur(25))
    image.paste(region, (int(x), int(y)))


@APP.route('/process', methods=['POST'])
def process():
    list_images = []
    for uploaded_file in request.files.getlist('image'):
        if uploaded_file.filename != '':
            unique_name_img = uuid.uuid4().hex + "." + uploaded_file.filename.split(".")[-1]
            list_images.append(unique_name_img)
            uploaded_file.save(APP.config['UPLOAD_PATH'] + unique_name_img)
            minor_blur = request.form.get('minor_blur')

            faces_detected = detect_faces_local_file(unique_name_img)
            blur_faces(unique_name_img, faces_detected, minor_blur)

    return render_template("index.html", list_images=list_images)


if __name__ == '__main__':
    APP.run(debug=True)
