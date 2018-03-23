class Student:
    def __init__(self, id):
        self._id = id
        self._priorities = []
        self._assignment = ''

    @property
    def id(self):
        return id

    @property
    def priorities(self):
        return self._priorities

    @priorities.setter
    def priorities(self, priorities):
        self._priorities = priorities

    @property
    def assignment(self):
        return self._assignment

    @assignment.setter
    def assignment(self, hospital):
        self._assignment = hospital


class Hospitals:
    def __init__(self):
        self._seats = dict()

    def __setitem__(self, key, value):
        self._seats[key] = value

    def __getitem__(self, item):
        return self._seats[item]
