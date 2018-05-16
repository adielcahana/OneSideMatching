from data import Hospitals, StatisticsStudent
import matplotlib.pyplot as plt
from copy import deepcopy
import numpy as np
import assignments
import lpsolver
import csv
import random


def make_student_list(hospitals):
    student = StatisticsStudent(1)

    student.reported = student.priorities = hospitals.names
    student_list = list()
    student_list.append(student)
    for i in range(2, 639):
        # duplicate all fields like reported
        duplicate_student = deepcopy(student)
        # set another id
        duplicate_student.id = i
        student_list.append(duplicate_student)
    return student_list


# shuffle a random reported list for the first student and return the updated list
def shuffle_one_student(student_priorities):
     np.random.shuffle(student_priorities)
     return student_priorities


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
                rand_a = random.randint(0, len(priority_list) - 1)
                rand_b = random.randint(0, len(priority_list) - 1)
                swap(students[index].priorities, priority_list[rand_a], priority_list[rand_b])
    return students


def simulation_flips_changes(num_of_flips, students, hospitals, strategies):
    # students after the flips
    students = flip_priorities(students, num_of_flips, 0.5)
    # get the probs if everyone has the same reported priorities
    lottery_probs_same, order = make_lottery(students, hospitals)
    # happiness of everyone
    happiness = lpsolver.get_happiness_coeff(order, students)
    # happiness of the first student
    result_happiness = np.dot(happiness[0], lottery_probs_same[0])
    improvement_happiness = []
    tuple_improve = list()
    for i in range(len(strategies)):
        # set the priorities of the first student with the i strategy
        students[0].priorities = strategies[i]
        lottery_probs, o = make_lottery(students, hospitals)
        # multiple from the result from solve (dot) lottery_probs
        result_happiness_after = np.dot(happiness[0], lottery_probs[0])
        if result_happiness_after > result_happiness:
            improvement_happiness.append((students[0].priorities, result_happiness, result_happiness_after))
    # if improvement_happiness not empty print the details
    if improvement_happiness:
        with open('results/improvement_happiness' + str(num_of_flips) + '.csv', 'w') as resultFile:
            csv_out = csv.writer(resultFile)
            csv_out.writerow(['priorities', 'real happiness', 'after shuffle happiness'])
            for tup in improvement_happiness:
                csv_out.writerow(tup)
        tuple_improve.append((num_of_flips, len(improvement_happiness)))
    return tuple_improve


# all the students have the same priorities and we choose th first student and
# changing his priorities randomly and calculate his new happiness according
# of his new priorities
# it seems he always succeed to improve his happiness
def flip_simulation():
    tuple_improve = list()
    # hospitals have 2 fields : 1. names of hospitals, 2. num of seats to each hospital
    hospitals = Hospitals.from_csv("res/seats_2018.csv")
    # list of students with the same priorities
    students = make_student_list(hospitals)
    strategies = list()
    # student possible strategies (50 for now)
    for i in range(50):
        # get strategies
        strategies.append(shuffle_one_student(deepcopy(students[0].priorities)))
    # run the simulation for 25 times with the same strategies and the same priorities
    for i in range(60):
        tup = simulation_flips_changes(i, students, hospitals, strategies)
        if tup:
            tuple_improve.append(tup)
            print(tup)
            print(" ")
    print("tuple improve results list: ")
    print(tuple_improve)

    # ax = plt.subplot(111)
    # plt.title("flips improve")
    # # crush here
    # plt.bar([i[0] for i in tuple_improve], [j[1] for j in tuple_improve], align='center')
    # #######
    # plt.gca().set_xticks([i[0] for i in tuple_improve])
    # ax.set_xlabel("number of flips")
    # ax.set_ylabel("number of Improves strategies")
    # plt.show()


flip_simulation()
