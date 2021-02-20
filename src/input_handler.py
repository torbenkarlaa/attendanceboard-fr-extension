import cv2

from connector import Connector


class InputHandler:
    last_predict = None
    recognized_faces = {}

    def start(self):
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        connector = Connector()
        capture = cv2.VideoCapture(0)

        recognizer.read('train-dump.yml')

        print('Watching for video input changes.. \n')

        while True:
            ret, frame = capture.read()
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.5, minNeighbors=5)

            for (x, y, w, h) in faces:

                roi = gray_frame[y: y + h, x: x + w]
                id_, conf = recognizer.predict(roi)

                self.handle_predict(id_, conf)

                if conf <= 0 and id_ != self.last_predict:
                    cv2.putText(frame, connector.available_image_ids[id_], (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (255, 255, 255), 1, cv2.LINE_AA)
                    self.last_predict = id_
                    # TODO: Login

                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            cv2.imshow('frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        print(self.recognized_faces)
        capture.release()
        cv2.destroyAllWindows()

    def handle_predict(self, id_, conf):
        if self.recognized_faces.get(id_) is None or self.recognized_faces.get(id_) > conf:
            self.recognized_faces[id_] = conf
