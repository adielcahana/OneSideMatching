import time

import numpy as np

import assignments
import randomizer
from data import Hospitals
from lpsolver import solve


def timeit(func, *args):
    start = time.time()
    ret = func(*args)
    print(func.__name__ + " time is: " + str(time.time() - start) + " sec")
    return ret


def double_equality(a, b, epsilon):
    return abs(a - b) <= epsilon


def sainity_test():
    epsilon = 0.0001

    # test column normalization to number of seats
    def column_test(mat, var_name):
        columns_sum = np.sum(mat, axis=0)
        for name in hospitals.names:
            if not double_equality(columns_sum[order[name]], hospitals[name], epsilon):
                print('error in ' + var_name + ' column sum')
                break

    # test rows normalization to 1
    def rows_test(mat, var_name):
        rows_sum = np.sum(mat, axis=1)
        for i in range(len(rows_sum)):
            if not double_equality(rows_sum[i], 1.0, epsilon):
                print('error in ' + var_name + ' rows sum')
                break

    # test probs
    column_test(probs, 'probs')
    rows_test(probs, 'probs')
    #test solution
    column_test(solution, 'solution')
    rows_test(solution, 'solution')
    # test birkhoff matrix
    # column_test(new_probs, 'birkhoff')
    rows_test(new_probs, 'birkhoff')


def time_test():
    global probs, solution, new_probs
    probs = timeit(assignments.expected_hat, students, hospitals, order, 100)
    solution = timeit(solve, probs, order, students)
    new_probs, birkhoff_order = timeit(assignments.birkhoff_normalize, solution, hospitals, order)
    coefficients, permutations = timeit(assignments.birkhoff_decoposition, new_probs)
    result = timeit(assignments.birkhoff_lottery, coefficients, permutations)
    print(result)


if __name__ == "__main__":
    np.random.seed(1)
    hospitals = Hospitals.from_excel("res/hospital_list_test.xlsx")
    students = randomizer.create_random_students(500, hospitals.names)
    order = assignments.get_hospitals_order(hospitals)

    probs = None
    solution = None
    new_probs = None

    time_test()
    sainity_test()
