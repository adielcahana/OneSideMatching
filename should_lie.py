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
shouldnt_lie = np.zeros(len(not_lying_precentages))
should_lie = np.zeros(len(not_lying_precentages))

happiness_type = 'quadratic'
for simulation in range(num_of_simulations):
    for index, precentage in enumerate(not_lying_precentages):
        # select random students to say the truth
        real_students_indices = np.random.randint(0, len(students), not_lying_count[index])
        reported_students_indices = np.asarray(set(np.arange(len(students))) - set(real_students_indices))
        #happines of the students with reported priorities
        real_students_happiness_before = []
        # happines of the students with real priorities
        real_students_happiness_after = []

        # happines of the students with reported priorities
        reported_students_happiness_before = []
        # happines of the students with real priorities
        reported_students_happiness_after = []


        probs = assignments.expected_hat(students, hospitals, order, 1000)
        for i in real_students_indices:
            students[i].priorities = students[i].real

        coeff = lpsolver.get_happiness_coeff(order, students, happiness_type)
        problem = lpsolver.AssignmentProblem(probs, order, students, happiness_type)
        new_probs = problem.solve()
        for i in real_students_indices:
            real_students_happiness_before.append(np.dot(np.asarray(coeff[i]), new_probs[i]))
        for i in reported_students_indices:
            reported_students_happiness_before.append(np.dot(np.asarray(coeff[i]), new_probs[i]))

        problem = lpsolver.AssignmentProblem(probs, order, students, happiness_type)
        new_probs = problem.solve()
        for i in real_students_indices:
            real_students_happiness_after.append(np.dot(np.asarray(coeff[i]), new_probs[i]))
        for i in reported_students_indices:
            reported_students_happiness_after.append(np.dot(np.asarray(coeff[i]), new_probs[i]))

        for i in range(len(real_students_indices)):
            if real_students_happiness_after[i] > real_students_happiness_before[i]:
                shouldnt_lie[index] += 1
        for i in range(len(reported_students_indices)):
            if reported_students_happiness_after[i] > reported_students_happiness_before[i]:
                should_lie[index] += 1

        # revert the random students to say the reported priorites
        for i in real_students_indices:
            students[i].priorities = students[i].reported

# average over number of simulations
shouldnt_lie /= num_of_simulations
shouldnt_lie_precentage = shouldnt_lie / not_lying_count
should_lie_precentage = should_lie / (len(students) - not_lying_count)
# fix nan at first index
shouldnt_lie[0] = 0
p1, _ = plt.plot(not_lying_precentages, shouldnt_lie_precentage)
p2, _ = plt.plot(not_lying_precentages, should_lie_precentage)
plt.legend([p1, p2], ["students with real priorites","students with reported priorites"])
plt.xlabel("precentage of students with real priorites")
plt.ylabel("avarege precentage of the students\n with real priorites that profit from their strategy")
plt.title("is lying profitable?\n N = " + str(len(students)) + "\n averaged over " + str(num_of_simulations) +" simulations")
plt.show()