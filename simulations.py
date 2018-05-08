import loader
import pandas as pd
from data import Hospitals
from copy import deepcopy
import numpy as np
import assignments
import lpsolver
import csv


def make_student_list(hospitals):
    student = loader.StatisticsStudent(1)
    student._reported = hospitals.names
    student_list = []
    student_list.append(student)
    for i in range(2, 83):
        # duplicate all fields like reported
        duplicate_student = deepcopy(student)
        # set another id
        duplicate_student.id = i
        student_list.append(duplicate_student)
    return student_list


# shuffle a random reported list for the first student and return the updated list
def shuffle_one_student(students_reported):
    np.random.shuffle(students_reported[0].reported_priorities)
    return students_reported


# after we got the same reported (except from  student[0])we make a lottery and check
# if student[0] have a better probs
def make_lottery(students, hospitals):
    order = assignments.get_hospitals_order(hospitals)
    probs = assignments.expected_hat(students, hospitals, order, 50)
    problem = lpsolver.Problem(probs, order, students)
    new_probs = problem.solve()
    return new_probs, order


def sim1_change_one_student():
    hospitals = Hospitals.from_csv("res/seats_2018_test.csv")
    # the list of students with the same reported priorities
    students_same_reported = make_student_list(hospitals)
    # get the probs if everyone has the same reported priorities
    lottery_probs_same, order = make_lottery(students_same_reported, hospitals)
    # happiness of everyone
    happiness = lpsolver.get_happiness_coeff(order, students_same_reported)
    # happiness of the first student
    result_happiness = np.dot(happiness[0], lottery_probs_same[0])
    improvement_happiness = []
    for i in range(30):
        # get the priorities of the first student after shuffle
        same_reported_first_shuffle = shuffle_one_student(deepcopy(students_same_reported))
        lottery_probs, o = make_lottery(same_reported_first_shuffle, hospitals)
        happiness_after = lpsolver.get_happiness_coeff(order, same_reported_first_shuffle)
        # multiple from the result from solve (dot) lottery_probs
        result_happiness_after = np.dot(happiness_after[0], lottery_probs[0])
        if result_happiness_after > result_happiness:
            improvement_happiness.append((same_reported_first_shuffle[0].priorities, result_happiness, result_happiness_after))

    with open('improvement_happiness.csv', 'w') as resultFile:
        csv_out = csv.writer(resultFile)
        csv_out.writerow(['priorities', 'real happiness', 'after shuffle happiness'])
        for tup in improvement_happiness:
            csv_out.writerow(tup)

# all the students have the same priorities and we choose th first student and
# changing his priorities randomly and calculate his new happiness according
# of his new priorities
# it seems he always succeed to improve his happiness
sim1_change_one_student()

