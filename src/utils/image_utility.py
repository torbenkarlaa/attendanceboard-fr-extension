import pickle

import cv2
import numpy as np
from bson import Binary
from keras_preprocessing.image import img_to_array
from tensorflow.python.keras.applications.mobilenet_v2 import preprocess_input


class ImageUtility:
    FACE_CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')
    SCALE_FACTOR = 1.1
    IMG_SIZE = 224

    @staticmethod
    def img_to_bin(image):
        image_grey = image.convert('L')
        image_arr = np.array(image_grey, 'uint8')

        faces = ImageUtility.FACE_CASCADE.detectMultiScale(image_arr, scaleFactor=ImageUtility.SCALE_FACTOR,
                                                           minNeighbors=5)

        roi = []

        for (x, y, w, h) in faces:
            roi.append(np.array(image, 'uint8')[y:y + h, x:x + w])

            if len(roi) == 1:
                roi = ImageUtility.resize_roi(image, x, y, w, h)
                roi = preprocess_input(roi)
                return Binary(pickle.dumps(roi, protocol=2), subtype=128)

        if len(roi) == 0:
            return None

    @staticmethod
    def bin_to_np_arr(binary):
        return pickle.loads(binary)

    @staticmethod
    def resize_roi(image, x, y, w, h):
        img_w, img_h = image.size
        if w != h:
            return []
        if w > ImageUtility.IMG_SIZE:
            x = int(x + ((w - ImageUtility.IMG_SIZE) / 2))
            y = int(y + ((h - ImageUtility.IMG_SIZE) / 2))

            if x + ImageUtility.IMG_SIZE > img_w:
                x = img_w - ImageUtility.IMG_SIZE
            if y + ImageUtility.IMG_SIZE > img_h:
                y = img_h - ImageUtility.IMG_SIZE
        if w < ImageUtility.IMG_SIZE:
            x = int(x - ((ImageUtility.IMG_SIZE - w) / 2))
            y = int(y - ((ImageUtility.IMG_SIZE - h) / 2))

            if x < 0:
                x = 0
            if y < 0:
                y = 0

        w, h = ImageUtility.IMG_SIZE, ImageUtility.IMG_SIZE
        image_arr = img_to_array(image)
        return image_arr[y:y + h, x:x + w]
