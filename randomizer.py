import numpy as np

from data import Student, Hospitals


class RandomStudent(Student):
    def __init__(self, id, hospitals):
        Student.__init__(self, id)
        np.random.shuffle(hospitals)
        self._priorities = hospitals

class LyingStudent(Student):
    def __init__(self, student, precentage):
        Student.__init__(self, student.id)
        self._student = student
        self._real_priorities = np.copy(student.priorities)
        # randomize the priorities according to the lying precentage
        size = int(precentage * len(student.priorities))
        start = np.random.randint(0, len(student.priorities))
        # selecet random elements to shuffle
        if start + size > len(student.priorities):
            remaining = size - (len(student.priorities) - start)
            shuffled = self._real_priorities[start: len(student.priorities)] + \
                        self._real_priorities[0: remaining]
            np.random.shuffle(shuffled)
            self._real_priorities[start: len(student.priorities)] = shuffled[0 : len(student.priorities) - start]
            self._real_priorities[0: remaining] = shuffled[len(student.priorities) - start:]
        else:
            shuffled = self._real_priorities[start: start + size]
            np.random.shuffle(shuffled)
            self._real_priorities[start: start + size] = shuffled

    @property
    def id(self):
        return self._student.id

    @property
    def priorities(self):
        return self._student.priorities

    @priorities.setter
    def priorities(self, priorities):
        self._student.priorities = priorities

    @property
    def assignment(self):
        return self._student.assignment

    @assignment.setter
    def assignment(self, hospital):
        self._student._assignment = hospital

def create_random_students(size, hospitals):
    students = list()
    for i in range(size):
        students.append(RandomStudent(i, hospitals))
    return students

def create_random_lying_students(size, hospitals, num_of_lying , lying_precentage):
    students = []
    for i in range(num_of_lying):
        students[i] = LyingStudent(RandomStudent(i, hospitals), lying_precentage)
    for i in range(num_of_lying, size):
        students[i] = LyingStudent(RandomStudent(i, hospitals), lying_precentage)
    return students
