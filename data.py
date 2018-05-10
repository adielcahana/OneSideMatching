import re

import numpy as np
import pandas as pd


class Student:
    def __init__(self, id, priorities=None):
        self.id = id
        self.priorities = priorities
        self.assignment = ''


class StatisticsStudent(Student):
    def __init__(self, id):
        Student.__init__(self, id)
        self.reported = None
        self.real = None
        self.age = None
        self.gender = None
        self.university = None
        self.course = None
        self.city = None
        self.pair = None
        self.manipulate = None
        self.all_reasons = None
        self.exchange = None
        self.is_hat_better = None
        self.understanding = None


class Hospitals:
    """
    a class that represents the number of seats for each hospital
    """
    def __init__(self):
        self.seats = dict()

    def __setitem__(self, key, value):
        self.seats[key] = value

    def __getitem__(self, item):
        return self.seats[item]

    def __iter__(self):
        return iter(self.seats.items())

    def __len__(self):
        return len(self.seats)

    @staticmethod
    def from_excel(path):
        hospital_list = pd.read_excel(path).as_matrix()
        hospitals = Hospitals()
        for hospital in hospital_list:
            hospitals[hospital[0]] = hospital[1]
        return hospitals

    @staticmethod
    def from_csv(path):
        """
        read data from excel file (hospital list)
        :param path: file path of seats (seats_2018.csv for example)
        :return: Hospitals seats
        """
        data = pd.read_csv(path, encoding='iso-8859-8')
        hospitals = Hospitals()
        hospital_name = data['Hospital'].tolist()
        hospital_seats = data['seats'].tolist()
        for i in range(len(hospital_name)):
            hospitals[hospital_name[i]] = hospital_seats[i]
        return hospitals

    @staticmethod
    def copy(hospitals):
        new_hospitals = Hospitals()
        for key, value in hospitals:
            new_hospitals[key] = value
        return new_hospitals

    @property
    def names(self):
        return list(self.seats.keys())


def get_student(id, row, hospital_codes):
    """
    extract student data from the questionnaire
    :param id: student id (currently using the row number)
    :param row: pandas row from the questionnaire results
    :param hospital_codes: mapping from int to hospital name (defined in the questionnaire)
    :return: StatisticStudent as appeared in the row
    """
    student = StatisticsStudent(id)
    student.reported = get_priorities(row, 'reported', hospital_codes)
    student.real = get_priorities(row, 'real', hospital_codes)
    student.age = int(row['Age'])
    student.gender = int(row['Gender'])
    student.university = int(row['University'])
    student.course = int(row['Course'])
    student.city = int(row['City'])
    student.pair = row['Pair?']
    student.assignment = row['Result']
    student.manipulate = row['Did you manipulate?']
    all_resons_str = row['All reasons']
    if not isinstance(all_resons_str, float):
        student.all_reasons = list(map(int, all_resons_str.split(',')))
    student.exchange = row['Exchange?']
    student.is_hat_better = row['IsHatBetter?']
    student.understanding = row['Understanding']
    return student


def get_priorities(row, type, hospital_codes):
    """
    extract student priorities from the questionnaire
    :param row: pandas row from the questionnaire
    :param type: 'real' or 'reported' priorities to extract
    :param hospital_codes: mapping from int to hospital name (defined in the questionnaire)
    :return: list of hospital names in priorities order
    """
    if type == 'real':
        col_name = 'Real_'
    else:  # type == 'reported'
        col_name = 'Reported_'
        priorities = parse_reported_raw(row)
        if priorities is not None:
            return priorities

    priorities = []
    for i in range(1, len(hospital_codes) + 1):
        code = row[col_name + str(i)]
        if code is np.nan:
            return None
        priorities.append(hospital_codes[int(code)])
    return priorities


def parse_reported_raw(row):
    """parse Reported Raw column in the questionnaire result"""
    priorities = []
    if type(row["Reported Raw"]) is float:
        return None
    for element in row["Reported Raw"].split():
        hospital = element.split('.')[1]
        if re.match("^[^0-9]+$", hospital) is None:
            raise Exception('illegal hospital name: ' + hospital)
        priorities.append(hospital)
    return priorities


def get_votes():
    """
    load votes for each hospital from reported votes of 2018
    :return: tuple -
    dictionary of votes for each hospital,
    and number of students that participated in the lottery
    """
    data = pd.read_csv("res/פירוט העדפות.csv")
    hospital_votes = dict()
    for i in range(0, 25):
        row = data.iloc[i]
        name = row['Hospital']
        votes = []
        for j in range(1, 26):
            count = row['Reported_' + str(j)]
            if np.isnan(count):
                votes.append(0)
            else:
                votes.append(int(count))
            hospital_votes[name] = votes
    return hospital_votes, 638


def get_hospital_codes():
    """
    get a mapping from hospital code to hospital name
    :return: hospital codes map
    """
    hospital_codes = {}
    with open("res/hospitals codes.txt", encoding='utf8') as f:
        for line in f:
            val, key = line.split(",")
            hospital_codes[int(key)] = val
    return hospital_codes
