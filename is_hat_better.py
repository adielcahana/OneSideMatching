import math
import time

import numpy as np
from matplotlib import pyplot as plt

import assignments
import data
import lpsolver

np.random.seed(int(time.time()))
num_of_simulations = 10
hospitals = data.Hospitals.from_csv("D:\Documents\לימודים\שנה ד\OneSideMatching\\res\seats_2018.csv")
order = assignments.get_hospitals_order(hospitals)

hospital_codes = data.get_codes("res/hospitals codes.txt")
result_codes = data.get_codes("res/results codes.txt")
students = data.get_all_students(hospital_codes, result_codes)
temp = []

# trim students without reported priorities or result
for student in students:
    if student.reported is not None and student.real is not None and student.reported != student.real:
        student.priorities = student.real
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
total_seats = 0
for hospital, seats_count in hospitals:
    total_seats += seats_count
# reduce one seat from random hospitals so that the diffrenec between number of seats and number of students will be 0
if total_seats > len(students):
    for hospital in np.random.choice(hospitals.names, total_seats - len(students)):
        hospitals[hospital] -= 1

# happines of the students with real priorities and hat
happiness_real_expcted = np.zeros((num_of_simulations, len(students)))

happiness_reporteded_expcted = np.zeros((num_of_simulations, len(students)))
# happines of the students with reported priorities and our algorithm
happiness_real_alg = np.zeros((num_of_simulations, len(students)))

happiness_reported_alg = np.zeros((num_of_simulations, len(students)))

happiness_onereal_alg = np.zeros((num_of_simulations, len(students)))
happiness_onereal_expected = np.zeros((num_of_simulations, len(students)))

coeff = lpsolver.get_happiness_coeff(order, students, 'quadratic')
for simulation in range(num_of_simulations):
    # revert the random students to say the reported priorites
    for student in students:
        student.priorities = student.real
    # happiness with real priorities and expected hat
    probs = assignments.expected_hat(students, hospitals, order, 1000)
    for i in range(len(students)):
        happiness_real_expcted[simulation][i] += np.dot(np.asarray(coeff[i]), probs[i])

    # happiness with real priorities and our algorithm
    problem = lpsolver.AssignmentProblem(probs, order, students, 'quadratic')
    new_probs = problem.solve()
    for i in range(len(students)):
        happiness_real_alg[simulation][i] += np.dot(np.asarray(coeff[i]), new_probs[i])

    for student in students:
        student.priorities = student.reported

    # happiness with reported priorities and expected hat
    probs = assignments.expected_hat(students, hospitals, order, 1000)
    for i in range(len(students)):
        happiness_reporteded_expcted[simulation][i] += np.dot(np.asarray(coeff[i]), probs[i])

    # happiness with reported priorities and our algorithm
    problem = lpsolver.AssignmentProblem(probs, order, students, 'quadratic')
    new_probs = problem.solve()
    for i in range(len(students)):
        happiness_reported_alg[simulation][i] += np.dot(np.asarray(coeff[i]), new_probs[i])

    #one lie simulation
    for idx, student in enumerate(students):
        student.priorities = student.real

        probs = assignments.expected_hat(students, hospitals, order, 1000)
        happiness_onereal_expected[simulation][idx] = np.dot(np.asarray(coeff[idx]), probs[idx])

        problem = lpsolver.AssignmentProblem(probs, order, students, 'quadratic')
        new_probs = problem.solve()
        happiness_onereal_alg[simulation][idx] = np.dot(np.asarray(coeff[idx]), new_probs[idx])

        student.priorities = student.reported


np.savetxt("res/is hat better/quadratic/reaported_lp.csv", happiness_reported_alg, delimiter=",")
np.savetxt("res/is hat better/quadratic/reaported_hat.csv", happiness_reporteded_expcted, delimiter=",")
np.savetxt("res/is hat better/quadratic/real_hat.csv", happiness_real_expcted, delimiter=",")
np.savetxt("res/is hat better/quadratic/real_lp.csv", happiness_real_alg, delimiter=",")
np.savetxt("res/is hat better/quadratic/onelie_hat.csv", happiness_onereal_expected, delimiter=",")
np.savetxt("res/is hat better/quadratic/onelie_lp.csv", happiness_onereal_alg, delimiter=",")

students_x = np.arange(0, len(students))
p1 = plt.errorbar(students_x, np.average(happiness_real_expcted, axis=0), yerr=np.std(happiness_real_expcted, axis=0))
p2 = plt.errorbar(students_x, np.average(happiness_real_alg, axis=0), yerr=np.std(happiness_real_alg, axis=0))
p3 = plt.errorbar(students_x, np.average(happiness_reporteded_expcted, axis=0), yerr=np.std(happiness_reporteded_expcted, axis=0))
p4 = plt.errorbar(students_x, np.average(happiness_reported_alg, axis=0), yerr=np.std(happiness_reported_alg, axis=0))
p5 = plt.errorbar(students_x, np.average(happiness_onereal_expected, axis=0), yerr=np.std(happiness_onereal_expected, axis=0))
p6 = plt.errorbar(students_x, np.average(happiness_onereal_alg, axis=0), yerr=np.std(happiness_onereal_alg, axis=0))
plt.legend([p1, p2, p3, p4, p5, p6], ["real priorities\n and expected hat", "real priorities\n and lp",
                              "reported priorities\n and expected hat", "reported priorities\n and lp",
                                      "one real and expected hat", "one real and lp"])

plt.xlabel("# of student")
plt.ylabel("happines")
plt.title("is hat better?\n N = " + str(len(students)) + "\n averaged over " + str(num_of_simulations) +" simulations")
plt.show()