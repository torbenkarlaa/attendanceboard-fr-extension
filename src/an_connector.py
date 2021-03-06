import json

import requests
import stomper
import yaml
from requests.auth import HTTPBasicAuth
from websocket import create_connection, WebSocketConnectionClosedException

from assets.messages import Messages
from models.person import Person

config = yaml.load(open('config.yml'), Loader=yaml.FullLoader).get('attendanceboard')


class ANConnector:
    WS_HEADER = 'CONNECT\naccept-version:1.0,1.1,2.0\n\n\x00\n'

    last_interacting_person = None
    persons = []

    def __init__(self):
        self.build_persons()

    def build_persons(self):
        response = requests.get(config.get('api') + '/board/persons',
                                auth=HTTPBasicAuth(config.get('auth').get('username'),
                                                   config.get('auth').get('password')))
        payload = json.loads(response.text)

        self.persons.clear()
        for person in payload:
            person = Person(json.dumps(person))
            self.persons.append(person)

    def subscribe_person_update(self):
        try:
            ws = create_connection(config.get('websocket-endpoint'))
            ws.send(self.WS_HEADER)
            sub = stomper.subscribe('/topic/person-update', 1)
            ws.send(sub)

            print(Messages.AN_CONNECTOR_CONNECTION_SUCCESSFUL)

            while True:
                try:
                    payload = stomper.unpack_frame(ws.recv())['body']
                    person = Person(payload)
                    self.last_interacting_person = person
                except json.decoder.JSONDecodeError:
                    print(Messages.AN_CONNECTOR_PAYLOAD_ERROR)
                except WebSocketConnectionClosedException:
                    print(Messages.AN_CONNECTOR_CONNECTION_CLOSED)
                    self.subscribe_person_update()
                    break

        except ConnectionRefusedError:
            self.subscribe_person_update()

    @staticmethod
    def set_absent(id_):
        ws = create_connection(config.get('websocket-endpoint'))
        ws.send(ANConnector.WS_HEADER)
        msg = stomper.send('/app/set-absent', id_)
        ws.send(msg)

    @staticmethod
    def set_present(id_):
        ws = create_connection(config.get('websocket-endpoint'))
        ws.send(ANConnector.WS_HEADER)
        msg = stomper.send('/app/set-present', id_)
        ws.send(msg)
