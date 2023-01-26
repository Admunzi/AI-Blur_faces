from PIL import Image, ImageFilter
import credentials


def blur_faces(filename, faces_detected):
    image = Image.open(credentials.PATH_UPLOADS_FILES + filename)

    for face in faces_detected['FaceDetails']:
        create_blured_box(face, image)

    image.save(credentials.PATH_UPLOADS_FILES + filename)
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
