import pickle
import threading

import cv2
from bson import Binary

from ldap_connector import LDAPConnector
from database_connector import DatabaseConnector
from trainer import Trainer

ldap_connector = LDAPConnector()
database_connector = DatabaseConnector()
listener_thread = threading.Thread(target=ldap_connector.subscribe_person_update)


class InputHandler:
    last_predict = None
    recognized_faces = {}

    def __init__(self):
        listener_thread.start()

    def start(self):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        capture = cv2.VideoCapture(2)

        recognizer.read('train-dump.yml')

        print('Watching for video input changes ... \n')

        while True:
            ret, frame = capture.read()
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = Trainer.FACE_CASCADE.detectMultiScale(image, scaleFactor=1.5, minNeighbors=5)

            for (x, y, w, h) in faces:
                roi = image[y: y + h, x: x + w]
                id_, conf = recognizer.predict(roi)
                p_id = ldap_connector.persons[id_].id

                if conf <= 10:
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    text_width = cv2.getTextSize(p_id, font, 1, 2)[0][0]
                    offset = int((w - text_width) / 2)

                    cv2.putText(frame, p_id, (x + offset, y - 10), font, 1, (255, 255, 255), 1, cv2.LINE_AA)

                    if id_ != self.last_predict:
                        print('Recognized ' + p_id + ' - changing present state')
                        self.last_predict = id_

                        if ldap_connector.persons[id_].present:
                            LDAPConnector.set_absent(p_id)
                        else:
                            LDAPConnector.set_present(p_id)

                elif ldap_connector.last_interacting_person is not None:
                    print('Persisting sample data for ' + p_id)

                    binary = Binary(pickle.dumps(roi, protocol=2), subtype=128)
                    database_connector.insert(
                        {'guid': ldap_connector.last_interacting_person.objectGUID, 'data': binary})

                    ldap_connector.last_interacting_person = None

                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            cv2.imshow('frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        capture.release()
        cv2.destroyAllWindows()
