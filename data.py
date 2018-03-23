import pandas as pd
import xlrd

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
        self._index = dict()
        self._seats = dict()

    def __setitem__(self, key, value):
        if key not in self._seats:
            self._index[key] = len(self._seats)
        self._seats[key] = value

    # return tuple of seats and index mapping
    def __getitem__(self, item):
        return self._seats[item], self._index[item]

    def __iter__(self):
        return iter(self._seats)

    def __len__(self):
        return len(self._seats)

    # read data from excel file (hospital list)
    @staticmethod
    def from_excel(path):
        hospital_list = pd.read_excel(path)
        hospital_list = hospital_list.as_matrix()
        hospitals = Hospitals()
        for hospital in hospital_list:
            hospitals[hospital[0]] = hospital[1]
        return hospitals

    @staticmethod
    def copy(hospitals):
        new_hospitals = Hospitals()
        for key, value in hospitals:
            new_hospitals[key] = value
        return new_hospitals

    @property
    def names(self):
        return list(self._seats.keys())
