# noinspection PyUnresolvedReferences
from assets.messages import Messages


class AverageUtility:
    persons = {}

    def add(self, person, conf):
        confs = self.persons.get(person)
        if confs is None:
            confs = []

        confs.append(conf)
        self.persons[person] = confs

    def print_averages(self):
        print(Messages.DASH_LINE)
        print(Messages.AVERAGE_UTILITIES_HEADER)

        for person in self.persons:
            avg = sum(self.persons.get(person)) / len(self.persons.get(person))
            print(person.surname + ' - ' + str(avg))

        print(Messages.LINE_BREAK)
