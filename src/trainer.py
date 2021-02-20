import os
import urllib.request

import cv2
import numpy as np
from PIL import Image

from connector import Connector

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, 'images')
BASE_URL = 'http://localhost:8080/attendanceBoard/person-images/'


class Trainer:

    @staticmethod
    def load_images():
        connector = Connector()

        for available_id in connector.available_image_ids:
            img_dir = os.path.join(IMAGE_DIR, available_id)
            if not os.path.exists(img_dir):
                os.mkdir(img_dir)

            urllib.request.urlretrieve(BASE_URL + available_id + '.jpg', img_dir + '/base.jpg')

    @staticmethod
    def train():
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')
        roi_arr = []
        label_ids = []
        recognizer = cv2.face.LBPHFaceRecognizer_create()

        for root, dirs, files in os.walk(IMAGE_DIR):
            for file in files:
                if file.endswith('png') or file.endswith('jpg'):
                    path = os.path.join(root, file)

                    image = Image.open(path).convert('L')
                    image_arr = np.array(image, 'uint8')

                    faces = face_cascade.detectMultiScale(image_arr, scaleFactor=1.5, minNeighbors=5)

                    for (x, y, w, h) in faces:
                        roi_arr.append(image_arr[y: y + h, x: x + w])
                        label_ids.append(1)

        recognizer.train(roi_arr, np.array(label_ids))
        recognizer.save('train-dump.yml')


Trainer.train()
