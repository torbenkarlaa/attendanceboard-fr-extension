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

    def __init__(self, j):
        self.__dict__ = json.loads(j)
