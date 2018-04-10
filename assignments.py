import numpy as np

from data import Hospitals


def get_hospitals_order(hospitals):
    order = dict()
    i = 0
    for name in hospitals.names:
        order[name] = i
        i += 1
    return order


def hat(students, hospitals, order):
    indexes = np.arange(len(students), dtype=np.int16)
    np.random.shuffle(indexes)
    seats = Hospitals.copy(hospitals)
    assignments = np.zeros((len(students), len(hospitals)), dtype=np.float64)

    for i in range(len(students)):
        for choice in students[indexes[i]].priorities:
            if seats[choice] > 0:
                assignments[indexes[i]][order[choice]] = 1.0
                seats[choice] -= 1
                break

    return assignments


def expected_hat(students, hospitals, order, iterate_num):
    probs = np.zeros((len(students), len(hospitals)), dtype=np.float64)
    for i in range(iterate_num):
        probs += hat(students, hospitals, order)
    return probs / iterate_num