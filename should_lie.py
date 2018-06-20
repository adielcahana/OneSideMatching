import math
import time

import numpy as np
from matplotlib import pyplot as plt

import assignments
import data
import lpsolver

np.random.seed(int(time.time()))
num_of_simulations = 100
hospitals = data.Hospitals.from_csv("D:\Documents\לימודים\שנה ד\OneSideMatching\\res\seats_2018.csv")
order = assignments.get_hospitals_order(hospitals)

hospital_codes = data.get_codes("res/hospitals codes.txt")
result_codes = data.get_codes("res/results codes.txt")
students = data.get_all_students(hospital_codes, result_codes)
temp = []

# trim students without reported priorities or result
for student in students:
    if student.reported is not None and student.real is not None and student.reported != student.real:
        student.priorities = student.reported
        temp.append(student)
students = temp

# normalize the number of seats in each hospital to fit the num of students
# count the total amount of seats
total_seats = 0
for hospital, seats_count in hospitals:
    total_seats += seats_count

# divide each hospital seats by factor of total_seats/number_of_students
fixed_sesats_factor = math.ceil(total_seats/len(students))
for hospital, seats_count in hospitals:
    hospitals[hospital] = int(math.ceil(seats_count / fixed_sesats_factor))

# count the total amount of seats count again to check if the number of seats equals to num of students
total_seats=0
for hospital, seats_count in hospitals:
    total_seats += seats_count
# reduce one seat from random hospitals so that the diffrenec between number of seats and number of students will be 0
if total_seats > len(students):
    for hospital in np.random.choice(hospitals.names, total_seats - len(students)):
        hospitals[hospital] -= 1

# precantage of students that will say the truth
not_lying_precentages = np.arange(0, 1.1, 0.1)
# number of students that will say the truth
not_lying_count = np.asarray(not_lying_precentages * len(students), dtype=np.int64)
# counter of number of students that profit from not lying in each precentage
shouldnt_lie = np.zeros((num_of_simulations, len(not_lying_precentages)))
should_lie = np.zeros((num_of_simulations, len(not_lying_precentages)))

happiness_type = 'median'
for simulation in range(num_of_simulations):
    print("simulation num: " + str(simulation))
    for index, precentage in enumerate(not_lying_precentages):
        # select random students to say the truth
        indices = np.arange(len(students))
        np.random.shuffle(indices)
        real_students_indices = indices[0:not_lying_count[index]]
        reported_students_indices = np.asarray(list(set(indices) - set(real_students_indices)))
        # happiness of the students with reported priorities
        real_students_happiness_before = []
        # happiness of the students with real priorities
        real_students_happiness_after = []

        # happiness of the rest of students before and after some of them are telling the truth
        reported_students_happiness_before = []
        reported_students_happiness_after = []

        probs = assignments.expected_hat(students, hospitals, order, 1000)
        problem = lpsolver.AssignmentProblem(probs, order, students, happiness_type)
        new_probs = problem.solve()

        for i in real_students_indices:
            students[i].priorities = students[i].real
        coeff = lpsolver.get_happiness_coeff(order, students, happiness_type)

        for i in real_students_indices:
            real_students_happiness_before.append(np.dot(coeff[i], new_probs[i]))
        for i in reported_students_indices:
            reported_students_happiness_before.append(np.dot(coeff[i], new_probs[i]))

        probs = assignments.expected_hat(students, hospitals, order, 1000)
        problem = lpsolver.AssignmentProblem(probs, order, students, happiness_type)
        new_probs = problem.solve()
        for i in real_students_indices:
            real_students_happiness_after.append(np.dot(coeff[i], new_probs[i]))
        for i in reported_students_indices:
            reported_students_happiness_after.append(np.dot(coeff[i], new_probs[i]))

        for i in range(len(real_students_indices)):
            if real_students_happiness_after[i] > real_students_happiness_before[i]:
                shouldnt_lie[simulation][index] += 1
        for i in range(len(reported_students_indices)):
            if reported_students_happiness_after[i] > reported_students_happiness_before[i]:
                should_lie[simulation][index] += 1

        # revert the random students to say the reported priorites
        for i in real_students_indices:
            students[i].priorities = students[i].reported


for row in shouldnt_lie:
    row /= not_lying_count
    row[0] = 0
lying_count = len(students) - not_lying_count
for row in should_lie:
    row /= lying_count
    row[-1] = 0

plt.errorbar(not_lying_precentages, np.average(shouldnt_lie, axis=0),
         yerr=np.std(shouldnt_lie, axis=0), label="students with real priorities")
plt.errorbar(not_lying_precentages, np.average(should_lie, axis=0),
         yerr=np.std(should_lie, axis=0), label="students with reported priorities")
plt.legend(loc='upper right')
plt.xlabel("precentage of students with real priorites")
plt.ylabel("avarege precentage of the students\n with real priorites that profit from their strategy")
plt.title("is lying profitable?\n N = " + str(len(students)) + "\naveraged over " + str(num_of_simulations) +" simulations\nwith " + happiness_type + " happinees function")
plt.show()
