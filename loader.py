import numpy as np
import pandas as pd

from data import Student


class StatisticsStudent(Student):
    def __init__(self, id, reported_priorities, real_priorities):
        Student.__init__(self, id, reported_priorities)
        self._real_priorities = real_priorities

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
    reported = get_priorites(row, 'reported', codes)
    real = get_priorites(row, 'real', codes)
    if real is None and reported is None:
        return None
    return StatisticsStudent(id, reported, real)


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


if __name__ == "__main__":
    hospital_codes = {}
    with open("res/hospitals codes.txt", encoding='utf8') as f:
        for line in f:
            val, key = line.split(",")
            hospital_codes[int(key)] = val

    data = pd.read_csv("res//Internship Lottery_April 8, 2018_11.54.csv")
    students = []
    for i in range(2, 241):
        student = get_student(i + 2, data.iloc[i], hospital_codes)
        if student is not None:
            students.append(student)

    real = 0
    reported = 0
    overlap = 0
    for student in students:
        if student.reported_priorities is not None:
            reported += 1
        if student.real_priorities is not None:
            real += 1
        if student.reported_priorities is not None and student.real_priorities is not None:
            overlap += 1

    print("real len: {}".format(real))
    print("reported len: {}".format(reported))
    print("overlap is: {}".format(overlap))

