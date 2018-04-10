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
    for student in students:
        m = len(hospitals_order)
        j = 0
        for priority in student.priorities:
            coeff[i][hospitals_order[priority]] = (m - j)**2
            j += 1
        i += 1
    return coeff



