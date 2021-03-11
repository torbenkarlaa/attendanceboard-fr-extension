import pickle
import threading

import cv2
from bson import Binary

from an_connector import ANConnector
from assets.messages import Messages
from database_connector import DatabaseConnector
from trainer import Trainer
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
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(Trainer.DATA_FILE)

        # Param may need to be changed, depending on your video input
        capture = cv2.VideoCapture(2)

        print(Messages.INPUT_HANDLER_START)

        prev_pos_x = None
        prev_pos_y = None
        frame_offset = 75
        frames_counter = 0

        success, frame = capture.read()
        self.crop_frame(frame)

        if self.benchmark_mode_activated:
            benchmark_utility.scale_factor = ImageUtility.SCALE_FACTOR
            benchmark_utility.frame_width = self.frame_width
            benchmark_utility.frame_height = self.frame_height

        while success:
            frame = cv2.resize(frame, (self.frame_width, self.frame_height))

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if prev_pos_x is not None and prev_pos_y is not None:
                image = image[prev_pos_y[0] - frame_offset:prev_pos_y[1] + frame_offset,
                        prev_pos_x[0] - frame_offset:prev_pos_x[1] + frame_offset]

            faces = ImageUtility.FACE_CASCADE.detectMultiScale(image, scaleFactor=ImageUtility.SCALE_FACTOR,
                                                               minNeighbors=5)

            if faces == ():
                frames_counter += 1

                if self.benchmark_mode_activated:
                    benchmark_utility.measure(False, False)

                if frames_counter >= 10:
                    frames_counter = 0
                    prev_pos_x = None
                    prev_pos_y = None

            for (x, y, w, h) in faces:
                roi = image[y:y + h, x:x + w]

                if prev_pos_x is not None and prev_pos_y is not None:
                    x += prev_pos_x[0] - frame_offset
                    y += prev_pos_y[0] - frame_offset

                if self.frame_rescaling_activated:
                    prev_pos_x = (x, x + w)
                    prev_pos_y = (y, y + h)

                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                id_, conf = recognizer.predict(roi)
                p_id = an_connector.persons[id_].id

                if self.benchmark_mode_activated:
                    average_utility.add(an_connector.persons[id_], conf)
                    benchmark_utility.measure(True, conf <= 10)

                if conf <= 10:
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    text_width = cv2.getTextSize(p_id, font, 1, 2)[0][0]
                    offset = int((w - text_width) / 2)

                    cv2.putText(frame, p_id, (x + offset, y - 10), font, 1, (255, 255, 255), 1, cv2.LINE_AA)

                    if id_ != self.last_predict:
                        print(Messages.INPUT_HANDLER_IDENTIFICATION.format(p_id))
                        self.last_predict = id_

                        if an_connector.persons[id_].present:
                            ANConnector.set_absent(p_id)
                        else:
                            ANConnector.set_present(p_id)

                elif an_connector.last_interacting_person is not None:
                    print(Messages.INPUT_HANDLER_SAMPLE_DATA.format(p_id))

                    binary = Binary(pickle.dumps(roi, protocol=2), subtype=128)
                    database_connector.insert(
                        {'guid': an_connector.last_interacting_person.objectGUID, 'data': binary})

                    an_connector.last_interacting_person = None

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
