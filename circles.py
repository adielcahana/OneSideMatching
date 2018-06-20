import numpy as np
import pandas as pd
from pulp import *

import data
from assignments import get_hospitals_order


class SwapProblem:
    def __init__(self, seats, hospitals_order, students):
        self._students = students
        self._order = hospitals_order

        students_size = len(students)
        hospital_size = len(hospitals_order)

        self._assginments = LpVariable.dicts(name='assginments', indexs=((i, j) for i in range(students_size) for j in range(hospital_size)),
                              lowBound=0.0, upBound=1.0, cat='Continuous')
        self._problem = LpProblem('students allocation swaps', LpMaximize)

        # normalization constraint
        for row in range(students_size):
            self._problem += lpSum(self._assginments[(row, j)] for j in range(hospital_size)) == 1.0

        # seats constraints
        order = sorted(hospitals_order.items(), key=lambda x: x[1])
        for col in range(hospital_size):
            self._problem += lpSum(self._assginments[(i, col)] for i in range(students_size)) == seats[order[col][0]]

        # objective function
        coeff = self.get_happiness_coeff(hospitals_order, students)
        self._problem += lpSum(
            self._assginments[(i, j)] * coeff[i][j] for i in range(students_size) for j in range(hospital_size))

    def get_happiness_coeff(self, hospitals_order, students):
        """
        create the matrix of each student profit from each priroty
        :param hospitals_order: the order of the hospitals in the matrix
        :param students: the students list
        :return: value of each priority for each student. coeff_mat[i][j] is the profit from assigning the Jth hospital
        (in the hospitals_order) to th Ith student
        """
        coeff_mat = np.zeros((len(students), len(hospitals_order)))
        for i, student in enumerate(students):
            assignment_idx = student.priorities.index(student.assignment)

            for j, priority in enumerate(student.priorities):
                # coefficient of priorities better then the current assginment will be 1
                if j < assignment_idx:
                    coeff = 1
                # coefficient of the current assginment will be 0
                elif j == assignment_idx:
                    coeff = 0
                # coefficient of priorities worse then the current assginment will be -infinity
                else:
                    coeff = -9999
                # assign the coefficient to the correct column
                coeff_mat[i][hospitals_order[priority]] = coeff
        return coeff_mat

    def solve(self):
        self._problem.solve()

        if self._problem.status == LpStatusOptimal:
            order = sorted(self._order.items(), key=lambda x: x[1])
            for i, student in enumerate(self._students):
                for j in range(len(order)):
                    if self._assginments[(i, j)].varValue == 1:
                        student.assignment = order[j][0]
            return self._students

        raise Exception("no solution")


def preprocess(students, priority_type):
    """
    prepare the data for processing.
    filter students without the desired priority_type, initialize csv columns, load the hospital seats etc.
    :param students: list of all of the students from the questionnaire
    :param priority_type: which priorities to load as main priorites - 'real' or 'reported'
    :return: students - extracted list of students, columns - dict of list for csv writing,
    results_before - list of each student assignment, seats - Hospitals class loaded from seats_2018.csv
    """
    seats = data.Hospitals()
    columns = dict()
    for i in range(len(students[0].reported)):
        columns[priority_type + '_' + str(i)] = []
    columns["id"] = []
    columns["result"] = []
    columns["result index"] = []

    temp = []
    results_before = []

    # trim students without reported priorities or result
    for student in students:
        if student.__getattribute__(priority_type) is not None and student.assignment is not "":
            student.priorities = student.__getattribute__(priority_type)
            temp.append(student)
            results_before.append(student.assignment)
            try:
                seats[student.assignment] += 1
            except:
                seats[student.assignment] = 1
            # add to file
            for i, priority in enumerate(student.__getattribute__(priority_type)):
                columns[priority_type + '_' + str(i)].append(priority)
            columns["id"].append(student.id)
            columns["result"].append(student.assignment)
            columns["result index"].append(student.__getattribute__(priority_type).index(student.assignment))

    students = temp
    return students, columns, results_before, seats


def find_simple_swaps(students, priority_type, columns):
    """
    for each student, go over all of the other student, and check if you can swap places with him.
    do this iterativley until you can't improve the students assignments anymore
    :param students: list of all of the students from the questionnaire
    :param priority_type: which priorities to load as main priorites - 'real' or 'reported'
    :param columns: dict of list for csv writing
    :return: students with new assignments
    """
    # number of swaps in each iteration
    swaps = 1
    # number of iterations
    itetation = 0

    # while there is still swaps
    while swaps != 0:
        itetation += 1
        swaps = 0
        # save each students id so we can track the swaps
        swaps_id = [student.id for student in students]
        for i in range(len(students)):
            result_i = students[i].assignment
            # go over all the students and check if the student can improve his seat priority
            for j in range(len(students)):
                result_j = students[j].assignment
                if students[i].is_preferred(result_j, priority_type) and students[j].is_preferred(result_i, priority_type):
                    students[i].assignment = result_j
                    students[j].assignment = result_i
                    # swap the ids of the students so we can track each seat origins
                    swaps_id[i], swaps_id[j] = swaps_id[j], swaps_id[i]
                    swaps += 1

        # write results of the iteration into the csv columns
        if swaps != 0:
            swap_str = "swap_" + str(itetation)
            columns[swap_str + " ids"] = swaps_id
            columns[swap_str] = []
            columns[swap_str + " index"] = []
            for student in students:
                columns[swap_str].append(student.assignment)
                columns[swap_str + " index"].append(student.__getattribute__(priority_type).index(student.assignment))

    return students


if __name__ == "__main__":
    hospital_codes = data.get_codes("res/hospitals codes.txt")
    results_codes = data.get_codes("res/results codes.txt")
    students = data.get_all_students(hospital_codes, results_codes)
    priority_type = 'real'

    students, columns, results_before, seats = preprocess(students, priority_type)

    for name in hospital_codes.values():
        if name not in set(seats.names):
            seats[name] = 0
    order = get_hospitals_order(seats)

    # uncomment this to activate the linear programing solver
    # students = SwapProblem(seats, order, students).solve()

    students = find_simple_swaps(students, priority_type, columns)
    results_after = []
    # uncomment this to activate the linear programing solver
    # result_after_index = []
    for student in students:
        results_after.append(student.assignment)
        # uncomment this to activate the linear programing solver
        # result_after_index.append(student.priorities.index(student.assignment))

    # uncomment this to activate the linear programing solver
    # columns["results after"] = results_after
    # columns["results after idx"] = result_after_index

    trades = 0
    for result in zip(results_before, results_after):
        if result[0] != result[1]:
            trades += 1

    print("number of swaps: " + str(trades))
    pd.DataFrame(columns).to_csv("res/simple_circles_result.csv")