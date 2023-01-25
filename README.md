# Blurr Faces

This application will recognize faces in an image and blur them, via amazon rekognition. 

This application use ApiRest with flask and website.

## Will use the following AWS services:
- Rekognition (Face detection)

## Prerequisites
- Python 3.6 or later
- AWS CLI
- AWS Account

## Usage
- Clone the repository
- Create a virtual environment
- Install the requirements
    - `pip install -r requirements.txt`
- Run the application
- Open the browser and go to http://localhost:5000
- Upload an image and click on the button "Blur Faces"
- The application will blur the faces and will save the image in the folder "static/uploads"