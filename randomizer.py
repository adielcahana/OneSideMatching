import numpy as np

from data import Student
from loader import StatisticsStudent


class RandomStudent(Student):
    def __init__(self, id, hospitals):
        Student.__init__(self, id)
        np.random.shuffle(hospitals)
        self.priorities = np.copy(hospitals)


class RandomStatisticsStudent(StatisticsStudent):
    def __init__(self, id, hospitals):
        StatisticsStudent.__init__(self, id)
        np.random.shuffle(hospitals)
        self._priorities = self._reported = np.copy(hospitals)


def create_random_students(size, hospitals):
    students = list()
    for i in range(size):
        students.append(RandomStudent(i, hospitals))
    return students

def create_random_statistic_students(size, hospitals):
    students = list()
    for i in range(size):
        students.append(RandomStatisticsStudent(i, hospitals))
    return students
