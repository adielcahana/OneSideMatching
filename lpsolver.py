from birkhoff import birkhoff_von_neumann_decomposition
import numpy as np
from pulp import *

before = 0
after = 0
status = None



def solve(probs, hospitals_order, students):
    global before, after, status
    shape = probs.shape
    P = LpVariable.dicts(name='P', indexs=((i, j) for i in range(shape[0]) for j in range(shape[1])),
                          lowBound=0.0, upBound=1.0, cat='Continuous')
    problem = LpProblem('students allocation', LpMaximize)
    # normalization constraint
    for row in range(shape[0]):
        problem += lpSum(P[(row, j)] for j in range(shape[1])) <= 1.0
    # seats constraints
    columns_sum = np.sum(probs, axis=0)
    for col in range(shape[1]):
        problem += lpSum(P[(i, col)] for i in range(shape[0])) <= columns_sum[col]
    # happiness constraint
    coeff = get_happiness_coeff(hospitals_order, students)
    happiness = [np.dot(probs[i], coeff[i]) for i in range(shape[0])]
    before = np.sum(happiness)
    for row in range(shape[0]):
        problem += lpSum(P[(row, j)] * coeff[row][j] for j in range(shape[1])) >= happiness[row]
    # objective function
    problem += lpSum(P[(i, j)] * coeff[i][j] for i in range(shape[0]) for j in range(shape[1]))

    problem.solve()

    if problem.status == LpStatusOptimal:
        status = LpStatus[problem.status]
        after = pulp.value(problem.objective)
        new_probs = np.zeros((len(students), len(hospitals_order)))
        for i in range(shape[0]):
            for j in range(shape[1]):
                new_probs[i][j] = P[(i, j)].varValue
        return new_probs


def get_happiness_coeff(hospitals_order, students):
    coeff = np.zeros((len(students), len(hospitals_order)))
    i = 0
    m = len(hospitals_order)
    for student in students:
        j = 0
        for priority in student.priorities:
            coeff[i][hospitals_order[priority]] = (m - j)**2
            j += 1
        i += 1
    return coeff


#################### new ##################
def normalize_new_probs(probs_matrix, hospital_seats, hospital_names, order):
    # initialize
    c = probs_matrix[:, 0]
    c = c/hospital_seats[hospital_names[0]]
    result = (np.ones((hospital_seats[hospital_names[0]], 1))*c).transpose()
    # duplicate the columns, probs_matrix.shape()[0] = the number of columns
    column_size = probs_matrix.shape[1]
    for i in range(1, column_size):
        c = probs_matrix[:, i]
        c = c/hospital_seats[hospital_names[i]]
        duplicate_column = (np.ones((hospital_seats[hospital_names[i]], 1))*c).transpose()
        result = np.column_stack((result, duplicate_column))
    print(result)
    return result


def birkhoff_algo(d):
    print("\n\n\n\n")
    res = birkhoff_von_neumann_decomposition(d)
    for coefficient, permutation_matrix in res:
        print('coefficient:', coefficient)
        print('permutation matrix:\n', permutation_matrix)
    return res


def lottery(res):
    p = []
    size = len(res)
    for i in range(0, size):
        p.append(res[i][0])
    choice = np.random.choice(size, 1, p)
    return choice
