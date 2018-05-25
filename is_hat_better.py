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

hospital_codes = data.get_hospital_codes()
students = data.get_all_students(hospital_codes)
temp = []

# trim students without reported priorities or result
for student in students:
    if student.reported is not None and student.real is not None and student.reported != student.real:
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

# happines of the students with real priorities and hat
happiness_before = np.zeros(len(students))
# happines of the students with reported priorities and our algorithm
happiness_after = np.zeros(len(students))

for simulation in range(num_of_simulations):
    # revert the random students to say the reported priorites
    for student in students:
        student.priorities = student.real

    probs = assignments.expected_hat(students, hospitals, order, 1000)
    coeff = lpsolver.get_happiness_coeff(order, students)

    for i in range(len(students)):
        happiness_before[i] += np.dot(np.asarray(coeff[i]), probs[i])

    for student in students:
        student.priorities = student.reported

    probs = assignments.expected_hat(students, hospitals, order, 1000)
    problem = lpsolver.Problem(probs, order, students)
    new_probs = problem.solve()

    for i in range(len(students)):
        happiness_after[i] += np.dot(np.asarray(coeff[i]), new_probs[i])


# average over number of simulations
avg_happiness_before = happiness_before / num_of_simulations
avg_happiness_after = happiness_after / num_of_simulations
students_x = np.arange(0, len(students))
p1, = plt.plot(students_x, avg_happiness_before)
p2, = plt.plot(students_x, avg_happiness_after)
plt.legend([p1, p2], ["real priorities\n and expected hat", "reported priorities\n and our algorithm"])
# plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
plt.xlabel("# of student")
plt.ylabel("happines")
plt.title("is hat better?\n N = " + str(len(students)) + "\n averaged over " + str(num_of_simulations) +" simulations")
plt.show()