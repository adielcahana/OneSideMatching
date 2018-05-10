import numpy as np

from data import Student


class RandomStudent(Student):
    def __init__(self, id, hospitals):
        Student.__init__(self, id)
        np.random.shuffle(hospitals)
        self.priorities = np.copy(hospitals)


def create_random_students(size, hospitals):
    students = list()
    for i in range(size):
        students.append(RandomStudent(i, hospitals))
    return students
