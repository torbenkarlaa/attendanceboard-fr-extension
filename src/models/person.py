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
        self.__dict__ = json.loads(json_string)
