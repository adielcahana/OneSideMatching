class Student:
    def __init__(self, id):
        self._id = id
        self._priorities = []
        self._assignment =''

    def get_priorities(self):
        return self._priorities

    def set_priorities(self, priorities):
        self._priorities = priorities

    def assign(self, hospital):
        self._assignment = hospital


class Hospitals:
    def __init__(self):
        self._seats = dict()

    def __setitem__(self, key, value):
        self._seats[key] = value

    def __getitem__(self, item):
        return self._seats[item]
