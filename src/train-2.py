import cv2
import numpy as np
import requests
from PIL import Image

from connector import Connector

BASE_URL = 'http://localhost:8080/attendanceBoard/person-images/'
FACE_CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')
RECOGNIZER = cv2.face.LBPHFaceRecognizer_create()


def build_dump():
    connector = Connector()
    roi_arr = []
    id_arr = []

    for guid in connector.available_image_ids:
        image = Image.open(requests.get(BASE_URL + guid + '.jpg', stream=True).raw).convert('L')
        image_arr = np.array(image, 'uint8')

        faces = FACE_CASCADE.detectMultiScale(image_arr, scaleFactor=1.5, minNeighbors=5)

        for (x, y, w, h) in faces:
            roi_arr.append(image_arr[y: y + h, x: x + w])
            id_arr.append(connector.available_image_ids.index(guid))

    RECOGNIZER.train(roi_arr, np.array(id_arr))
    RECOGNIZER.save('train-dump.yml')
