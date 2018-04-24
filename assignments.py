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


def birkhoff_normalize(probs_matrix, hospitals, order):
    # create mapping from column index to hospital name
    rev_order = {v: k for k, v in order.items()}
    # initialize
    c = probs_matrix[:, 0] / hospitals[rev_order[0]]
    result = (np.ones((hospitals[rev_order[0]], 1))*c).transpose()
    birkhoff_order = dict()
    birkhoff_order[rev_order[0]] = 0
    # duplicate the columns, probs_matrix.shape()[0] = the number of columns
    column_size = probs_matrix.shape[1]
    count = hospitals[rev_order[0]]
    # birkhoff order is a mapping from hospital name to his start column in the bi-stochastic matrix
    for i in range(1, column_size):
        birkhoff_order[rev_order[i]] = count
        c = probs_matrix[:, i] / hospitals[rev_order[i]]
        duplicate_column = (np.ones((hospitals[rev_order[i]], 1))*c).transpose()
        result = np.column_stack((result, duplicate_column))
        count += hospitals[rev_order[i]]
    return result, birkhoff_order


def birkhoff_decoposition(probs):
    result = birkhoff_von_neumann_decomposition(probs)
    coefficients, permutations = zip(*result)
    return coefficients, permutations


def birkhoff_lottery(coefficients, permutations):
    return np.random.choice(a=permutations, p=coefficients)


def set_assignments(students, birkhoff_order, permutation):
    # sort the birkhoff_order by column number
    order_list = sorted(birkhoff_order.items(), key=lambda x: x[1])
    for i in range(len(students)):
        index = np.where(permutation[i] == 1)[0]
        for hospital, col in order_list:
            if col > index:
                students[i].assignment = hospital
                break


def do_lottery(students, hospitals, num_of_iteration):
    order = get_hospitals_order(hospitals)
    probs = expected_hat(students, hospitals, order, num_of_iteration)
    normalize_probs, birkhoff_order = birkhoff_normalize(probs, hospitals, order)
    coefficients, permutations = birkhoff_decoposition(normalize_probs)
    assginment = birkhoff_lottery(coefficients, permutations)
    set_assignments(students, birkhoff_order, assginment)
    return students