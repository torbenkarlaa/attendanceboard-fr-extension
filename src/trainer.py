import pickle
import urllib.request

import cv2
import numpy as np
import yaml
from PIL import Image
from bson import Binary

from an_connector import ANConnector
from assets.messages import Messages
from database_connector import DatabaseConnector

an_connector = ANConnector()
config = yaml.load(open('config.yml'), Loader=yaml.FullLoader).get('attendanceboard')
database_connector = DatabaseConnector()


class Trainer:
    FACE_CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')
    DATA_FILE = 'train-dump.yml'
    SCALE_FACTOR = 1.1

    def train(self):
        print(Messages.TRAINER_START)

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        data_arr = []
        id_arr = []

        Trainer.insert_base_images()

        for person in an_connector.persons:
            for entry in database_connector.get(person.objectGUID):
                arr = Trainer.bin_to_np_arr(entry['data'])
                data_arr.append(arr)
                id_arr.append(an_connector.persons.index(person))

        recognizer.train(data_arr, np.array(id_arr))
        recognizer.save(self.DATA_FILE)
        print(Messages.TRAINER_FINISH)

    @staticmethod
    def insert_base_images():
        for person in an_connector.persons:
            if person.imagePresent and database_connector.count(person.objectGUID) == 0:
                url = config.get('api') + '/person-images/' + person.objectGUID + '.jpg'
                image = Image.open(urllib.request.urlopen(url))
                binary = Trainer.img_to_bin(image)

                if binary is not None:
                    database_connector.insert({'guid': person.objectGUID, 'data': binary})

    @staticmethod
    def img_to_bin(image):
        image = image.convert('L')
        image_arr = np.array(image, 'uint8')

        faces = Trainer.FACE_CASCADE.detectMultiScale(image_arr, scaleFactor=Trainer.SCALE_FACTOR, minNeighbors=5)

        roi = []

        for (x, y, w, h) in faces:
            roi.append(image_arr[y:y + h, x:x + w])

        if len(roi) == 0:
            return None

        return Binary(pickle.dumps(roi[0], protocol=2), subtype=128)

    @staticmethod
    def bin_to_np_arr(binary):
        return pickle.loads(binary)
