import json


class Person(object):
    id: str
    objectGUID: str
    name: str
    surname: str
    room: int
    telephone: int
    present: bool
    imagePresent: bool
    firstAider: bool
    alarmArea: str

    def __init__(self, json_string):
        try:
            self.__dict__ = json.loads(json_string)
        except TypeError:
            print("Couldn't build person object from JSON string")
