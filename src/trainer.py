import urllib.request

import cv2
import numpy as np
import yaml
from PIL import Image

from an_connector import ANConnector
from assets.messages import Messages
from database_connector import DatabaseConnector
from utils.image_utility import ImageUtility

an_connector = ANConnector()
config = yaml.load(open('config.yml'), Loader=yaml.FullLoader).get('attendanceboard')
database_connector = DatabaseConnector()


class Trainer:
    DATA_FILE = 'train-dump.yml'

    @staticmethod
    def train():
        print(Messages.TRAINER_START)

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        data = []
        labels = []

        Trainer.insert_base_images()

        for person in an_connector.persons:
            for entry in database_connector.get(person.objectGUID):
                image = ImageUtility.bin_to_np_arr(entry['data'])
                data.append(image)
                labels.append(an_connector.persons.index(person))

        recognizer.train(data, np.array(labels))
        recognizer.save(Trainer.DATA_FILE)
        print(Messages.TRAINER_FINISH)

    @staticmethod
    def insert_base_images():
        for person in an_connector.persons:
            if person.imagePresent and database_connector.count(person.objectGUID) == 0:
                url = config.get('api') + '/person-images/' + person.objectGUID + '.jpg'
                image = Image.open(urllib.request.urlopen(url))

                # w, h = image.size
                # image = image.crop((w - h, 0, w, h))
                binary = ImageUtility.img_to_bin(image)

                if binary is not None:
                    database_connector.insert({'guid': person.objectGUID, 'data': binary})
