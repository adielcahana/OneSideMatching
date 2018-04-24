import numpy as np
import pandas as pd

from data import Student


class StatisticsStudent(Student):

    def __init__(self, id):
        Student.__init__(self, id)
        self._reported = None
        self._real_priorities = None
        self._age = None
        self._gender = None
        self._university = None
        self._course = None
        self._city = None
        self._pair = None
        self._result = None
        self._manipulate = None
        self._all_reasons = None
        self._exchange = None
        self._is_hat_better = None
        self._understanding = None

    @property
    def real_priorities(self):
        return self._real_priorities

    @real_priorities.setter
    def real_priorities(self, real_priorities):
        self._real_priorities = real_priorities

    @property
    def reported_priorities(self):
        return self._priorities

    @reported_priorities.setter
    def reported_priorities(self, priorities):
        self._priorities = priorities


def get_student(id, row, codes):
    student = StatisticsStudent(id)
    student._reported = get_priorites(row, 'reported', codes)
    student._real = get_priorites(row, 'real', codes)
    student._age = int(row['Age'])
    student._gender = int(row['Gender'])
    student._university = int(row['University'])
    student._course = int(row['Course'])
    student._city = int(row['City'])
    student._pair = row['Pair?']
    student._result = row['Result']
    student._manipulate = row['Did you manipulate?']
    all_resons_str = row['All reasons']
    print(all_resons_str)
    if not isinstance(all_resons_str, float):
        student._all_reasons = list(map(int, all_resons_str.split(',')))
    student._exchange = row['Exchange?']
    student._is_hat_better = row['IsHatBetter?']
    student._understanding = row['Understanding']
    return student


def get_priorites(row, type, codes):
    if type == 'real':
        col_name = 'Real_'
    else:  # type == 'reported'
        col_name = 'Reported_'
        priorities = parse_reported_raw(row)
        if priorities is not None:
            return priorities

    priorities = []
    for i in range(1, len(codes) + 1):
        code = row[col_name + str(i)]
        if code is np.nan:
            return None
        priorities.append(hospital_codes[int(code)])
    return priorities


def parse_reported_raw(row):
    priorities = []
    hospital = str()
    last_word = False
    if type(row["Reported Raw"]) is float:
        return None
    for element in row["Reported Raw"].split():
        if element[-1] == ".":
            last_word = False
            if len(hospital) > 0:
                priorities.append(hospital)
                hospital = str()
        else:
            if last_word is True:
                hospital += " " + element
            else:
                hospital = element
                last_word = True
    priorities.append(hospital)
    return priorities