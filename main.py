import credentials
import uuid
from flask import Flask, request, render_template
from rekognition import detect_faces_local_file
from blur import blur_faces


app = Flask(__name__)
# app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
# app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png']
# app.config['UPLOAD_PATH'] = 'static/uploads/'


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/process', methods=['POST'])
def process():
    list_images = []
    for uploaded_file in request.files.getlist('image'):
        if uploaded_file.filename != '':
            unique_name_img = create_unique_name(uploaded_file)
            list_images.append(unique_name_img)
            uploaded_file.save(credentials.PATH_UPLOADS_FILES + unique_name_img)
            minor_blur = request.form.get('minor_blur')

            faces_detected = detect_faces_local_file(unique_name_img, minor_blur)
            blur_faces(unique_name_img, faces_detected)

    return render_template("index.html", list_images=list_images)


def create_unique_name(uploaded_file):
    return uuid.uuid4().hex + "." + uploaded_file.filename.split(".")[-1]


if __name__ == '__main__':
    app.run(debug=True)
