import loader
import pandas as pd
from data import Hospitals
from copy import deepcopy
import numpy as np
import assignments
import lpsolver
import csv
import random


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


def swap(list, item_a, item_b):
    a, b = list.index(item_a), list.index(item_b)
    list[b], list[a] = list[a], list[b]


# change priorities in percentage chance
def flip_priorities(students, num_of_filps, percentage_chance):
    for index in range(len(students)):
        for i in range(num_of_filps):
            priority_list = students[index].priorities
            # percentage_chance to swap  2 items from the priority list
            if random.random() < percentage_chance:
                # swap 2 random items
                rand_a = random.randint(0, len(priority_list))
                rand_b = random.randint(0, len(priority_list))
                swap(students, priority_list.priorities[rand_a], priority_list.priorities[rand_b])
    return students


def sim_change_one_student(num_of_flips):
    hospitals = Hospitals.from_csv("res/seats_2018_test.csv")
    # the list of students with the same reported priorities
    students = make_student_list(hospitals)
    # students after the flips
    students = flip_priorities(students, num_of_flips)
    # get the probs if everyone has the same reported priorities
    lottery_probs_same, order = make_lottery(students, hospitals)
    # happiness of everyone
    happiness = lpsolver.get_happiness_coeff(order, students)
    # happiness of the first student
    result_happiness = np.dot(happiness[0], lottery_probs_same[0])
    improvement_happiness = []
    for i in range(30):
        # get the priorities of the first student after shuffle
        same_reported_first_shuffle = shuffle_one_student(deepcopy(students))
        lottery_probs, o = make_lottery(same_reported_first_shuffle, hospitals)
        # multiple from the result from solve (dot) lottery_probs
        result_happiness_after = np.dot(happiness[0], lottery_probs[0])
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
sim_change_one_student(0)


