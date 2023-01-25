import boto3
import credentials

CLIENT_REKOGNITION = boto3.client(
    'rekognition',
    aws_access_key_id=credentials.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=credentials.AWS_SECRET_ACCESS_KEY,
    aws_session_token=credentials.AWS_SESSION_TOKEN,
    region_name='us-east-1'
)


def detect_faces_local_file(name_img, minor_blur):
    with open(credentials.PATH_UPLOADS_FILES + name_img, 'rb') as image:
        response = CLIENT_REKOGNITION.detect_faces(Image={
            'Bytes': image.read()
        },
            Attributes=['ALL', ])

    if minor_blur:
        response['FaceDetails'] = json_without_older_18(response)

    return response


def json_without_older_18(response):
    return [face for face in response['FaceDetails'] if face['AgeRange']['Low'] < 18]

