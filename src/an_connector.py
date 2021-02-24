import json
import requests
import stomper

from requests.auth import HTTPBasicAuth
from websocket import create_connection, WebSocketConnectionClosedException

from models.person import Person


class ANConnector:
    CONNECTION_ENDPOINT = 'ws://localhost:8080/attendanceBoard/websocket/none-sockjs'
    WS_HEADER = 'CONNECT\naccept-version:1.0,1.1,2.0\n\n\x00\n'

    last_interacting_person = None
    persons = []

    def __init__(self):
        self.build_persons()

    def build_persons(self):
        response = requests.get('http://localhost:8080/attendanceBoard/board/persons',
                                auth=HTTPBasicAuth('attendanceboard', 'attendanceboard20'))
        payload = json.loads(response.text)

        self.persons.clear()
        for person in payload:
            person = Person(json.dumps(person))
            self.persons.append(person)

    def subscribe_person_update(self):
        try:
            ws = create_connection(self.CONNECTION_ENDPOINT)
            ws.send(self.WS_HEADER)
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

    @staticmethod
    def set_absent(id_):
        ws = create_connection(ANConnector.CONNECTION_ENDPOINT)
        ws.send(ANConnector.WS_HEADER)
        msg = stomper.send('/app/set-absent', id_)
        ws.send(msg)

    @staticmethod
    def set_present(id_):
        ws = create_connection(ANConnector.CONNECTION_ENDPOINT)
        ws.send(ANConnector.WS_HEADER)
        msg = stomper.send('/app/set-present', id_)
        ws.send(msg)
