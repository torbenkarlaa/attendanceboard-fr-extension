import pickle
import urllib.request
import cv2
import numpy as np

from PIL import Image
from bson import Binary

from ldap_connector import LDAPConnector
from database_connector import DatabaseConnector

BASE_URL = 'http://localhost:8080/attendanceBoard/person-images/'


class Trainer:
    FACE_CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')
    SCALE_SIZE = (500, 500)

    ldap_connector = LDAPConnector()
    database_connector = DatabaseConnector()

    def train(self):
        print('Starting training ...')

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        data_arr = []
        id_arr = []

        self.insert_base_images()

        for person in self.ldap_connector.persons:
            for entry in self.database_connector.get(person.objectGUID):
                arr = Trainer.bin_to_np_arr(entry['data'])
                data_arr.append(arr)
                id_arr.append(self.ldap_connector.persons.index(person))

        recognizer.train(data_arr, np.array(id_arr))
        recognizer.save('train-dump.yml')
        print('Training finished \n')

    def insert_base_images(self):
        for person in self.ldap_connector.persons:
            if person.imagePresent and self.database_connector.count(person.objectGUID) == 0:
                image = Image.open(urllib.request.urlopen(BASE_URL + person.objectGUID + '.jpg'))
                binary = Trainer.img_to_bin(image)

                if binary is not None:
                    self.database_connector.insert({'guid': person.objectGUID, 'data': binary})

    @staticmethod
    def img_to_bin(image):
        image = image.convert('L')
        image_arr = np.array(image, 'uint8')

        faces = Trainer.FACE_CASCADE.detectMultiScale(image_arr, scaleFactor=1.5, minNeighbors=5)

        roi = []

        for (x, y, w, h) in faces:
            roi.append(image_arr[y: y + h, x: x + w])

        if len(roi) == 0:
            return None

        return Binary(pickle.dumps(roi[0], protocol=2), subtype=128)

    @staticmethod
    def bin_to_np_arr(binary):
        return pickle.loads(binary)
