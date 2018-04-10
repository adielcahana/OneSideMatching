import numpy as np
from birkhoff import birkhoff_von_neumann_decomposition

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


def birkhoff_normalize(probs_matrix, hospitals):
    hospital_names = hospitals.names
    # initialize
    c = probs_matrix[:, 0] / hospitals[hospital_names[0]]
    result = (np.ones((hospitals[hospital_names[0]], 1))*c).transpose()
    # duplicate the columns, probs_matrix.shape()[0] = the number of columns
    column_size = probs_matrix.shape[1]
    for i in range(1, column_size):
        c = probs_matrix[:, i] / hospitals[hospital_names[i]]
        duplicate_column = (np.ones((hospitals[hospital_names[i]], 1))*c).transpose()
        result = np.column_stack((result, duplicate_column))
    return result


def birkhoff_decoposition(probs):
    result = birkhoff_von_neumann_decomposition(probs)
    coefficients, permutations = zip(*result)
    return coefficients, permutations


def birkhoff_lottery(coefficients, permutations):
    return np.random.choice(a=permutations, p=coefficients)


