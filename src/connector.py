import json

import requests
import stomper
from requests.auth import HTTPBasicAuth
from websocket import create_connection, WebSocketConnectionClosedException

from models.person import Person


class Connector:
    last_interacting_person = None
    available_image_ids = []

    def __init__(self):
        self.build_available_image_ids()

    def build_available_image_ids(self):
        response = requests.get('http://localhost:8080/attendanceBoard/board/persons',
                                auth=HTTPBasicAuth('attendanceboard', 'attendanceboard20'))
        payload = json.loads(response.text)

        self.available_image_ids.clear()
        for person in payload:
            person = Person(json.dumps(person))
            if person.imagePresent:
                self.available_image_ids.append(person.objectGUID)

    def subscribe_person_update(self):
        try:
            ws = create_connection('ws://localhost:8080/attendanceBoard/websocket/none-sockjs')
            ws.send('CONNECT\naccept-version:1.0,1.1,2.0\n\n\x00\n')
            sub = stomper.subscribe('/topic/person-update', 1)
            ws.send(sub)

            print('Successfully connected to person-update topic \n')

            while True:
                try:
                    payload = stomper.unpack_frame(ws.recv())['body']
                    person = Person(payload)
                    self.last_interacting_person = person
                except json.decoder.JSONDecodeError:
                    print('Error while parsing JSON payload \n')
                except WebSocketConnectionClosedException:
                    print('Connection closed, trying to reconnect.. \n')
                    self.subscribe_person_update()
                    break

        except ConnectionRefusedError:
            self.subscribe_person_update()
