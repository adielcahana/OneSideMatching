import numpy as np
from pulp import *


class Problem:
    def __init__(self, probs, hospitals_order, students):
        self._students = students
        self._order = hospitals_order
        shape = probs.shape
        self._P = LpVariable.dicts(name='P', indexs=((i, j) for i in range(shape[0]) for j in range(shape[1])),
                              lowBound=0.0, upBound=1.0, cat='Continuous')
        self._problem = LpProblem('students allocation', LpMaximize)

        # normalization constraint
        for row in range(shape[0]):
            self._problem += lpSum(self._P[(row, j)] for j in range(shape[1])) <= 1.0

        # seats constraints
        columns_sum = np.sum(probs, axis=0)
        for col in range(shape[1]):
            self._problem += lpSum(self._P[(i, col)] for i in range(shape[0])) <= columns_sum[col]

        # happiness constraint
        coeff = get_happiness_coeff(hospitals_order, students)
        happiness = [np.dot(probs[i], coeff[i]) for i in range(shape[0])]
        for row in range(shape[0]):
            self._problem += lpSum(self._P[(row, j)] * coeff[row][j] for j in range(shape[1])) >= happiness[row]

        # objective function
        coeff = get_happiness_coeff(self._order, self._students)
        self._problem += lpSum(
            self._P[(i, j)] * coeff[i][j] for i in range(len(self._students)) for j in range(len(self._order)))

    # def set_objective_func(self , objective_func):
    #     self._problem += objective_func

    def solve(self):
        self._problem.solve()

        if self._problem.status == LpStatusOptimal:
            # status = LpStatus[self._problem.status]
            # after = pulp.value(self._problem.objective)
            new_probs = np.zeros((len(self._students), len(self._order)))
            for i in range(len(self._students)):
                for j in range(len(self._order)):
                    new_probs[i][j] = self._P[(i, j)].varValue
            return new_probs

        return "no solution"


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


