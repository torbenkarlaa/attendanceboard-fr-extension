import threading
from operator import itemgetter

import cv2
import numpy as np
from keras_preprocessing.image import img_to_array
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.python.keras.models import load_model

from an_connector import ANConnector
from assets.messages import Messages
from database_connector import DatabaseConnector
from utils.average_utility import AverageUtility
from utils.benchmark_utility import BenchmarkUtility
from utils.image_utility import ImageUtility

an_connector = ANConnector()
average_utility = AverageUtility()
benchmark_utility = BenchmarkUtility()
database_connector = DatabaseConnector()
listener_thread = threading.Thread(target=an_connector.subscribe_person_update, daemon=True)


class InputHandler:
    last_predict = None
    benchmark_mode_activated = False
    frame_rescaling_activated = False
    frame_width = 0
    frame_height = 0

    def __init__(self):
        self.activate_benchmark_mode()
        self.activate_frame_rescaling()
        listener_thread.start()

    def activate_benchmark_mode(self):
        print(Messages.INPUT_HANDLER_BENCHMARK_MODE)

        input_ = input().lower()
        if input_ == 'y':
            self.benchmark_mode_activated = True
            print()
        elif input_ == 'n':
            self.benchmark_mode_activated = False
            print()
        else:
            self.activate_benchmark_mode()

    def activate_frame_rescaling(self):
        print(Messages.INPUT_HANDLER_FRAME_RESCALING)

        input_ = input().lower()
        if input_ == 'y':
            self.frame_rescaling_activated = True
            print()
        elif input_ == 'n':
            self.frame_rescaling_activated = False
            print()
        else:
            self.activate_frame_rescaling()

    def start(self):
        print('Loading model for detection ... ')
        prototxt_path = 'deploy.prototxt'
        weights_path = 'res.caffemodel'
        facenet = cv2.dnn.readNet(prototxt_path, weights_path)
        net = load_model('mask_detector.model')

        # Param may need to be changed, depending on your video input
        capture = cv2.VideoCapture(2)

        print(Messages.INPUT_HANDLER_START)

        success, frame = capture.read()
        self.crop_frame(frame)

        if self.benchmark_mode_activated:
            benchmark_utility.scale_factor = ImageUtility.SCALE_FACTOR
            benchmark_utility.frame_width = self.frame_width
            benchmark_utility.frame_height = self.frame_height

        while success:
            frame = cv2.resize(frame, (self.frame_width, self.frame_height))
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            (h, w) = frame.shape[:2]
            blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))

            facenet.setInput(blob)
            detections = facenet.forward()

            faces = []
            locs = []
            preds = []

            for i in range(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]

                if confidence > 0:
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype('int')

                    (startX, startY) = (max(0, startX), max(0, startY))
                    (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

                    face = image[startY:endY, startX:endX]

                    if face.size != 0:
                        face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
                        face = cv2.resize(face, (224, 224))
                        face = img_to_array(face)
                        face = preprocess_input(face)

                        faces.append(face)
                        locs.append((startX, startY, endX, endY))

            if len(faces) > 0:
                faces = np.array(faces, dtype='float32')
                preds = net.predict(faces, batch_size=32)

            for (box, pred) in zip(locs, preds):
                (startX, startY, endX, endY) = box
                confs = zip(an_connector.persons, pred)
                label = max(confs, key=itemgetter(1))[0].surname
                print(label)

                # cv2.putText(frame, label, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                # cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)

            cv2.imshow('FR-Extension', frame)
            success, frame = capture.read()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        print(Messages.INPUT_HANDLER_CLOSE)
        capture.release()
        cv2.destroyAllWindows()
        cv2.waitKey(1)

        if self.benchmark_mode_activated:
            average_utility.print_averages()
            benchmark_utility.print_benchmarks()

    def crop_frame(self, frame):
        height, width, layers = frame.shape

        if width * height >= 921_600:
            self.frame_width = int(width / 2)
            self.frame_height = int(height / 2)
            print(Messages.INPUT_HANDLER_CROP_FRAME.format(width, height, self.frame_width, self.frame_height))
