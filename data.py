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
        self._index[key] = len(self._seats)
        self._seats[key] = value

    # return tuple of seats and index mapping
    def __getitem__(self, item):
        return self._seats[item], self._index

    # read data from excel file (hospital list)
    # "D:\\Users\\Admin\\OneSideMatching\\res\\hospital_list_test.xlsx"
    def from_excel(self, path):
        hospital_list = pd.read_excel(path)
        hospital_list = hospital_list.as_matrix()
        return hospital_list
