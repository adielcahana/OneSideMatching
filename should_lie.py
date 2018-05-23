import math
import time

import numpy as np

import assignments
import data
import lpsolver

np.random.seed(int(time.time()))
hospitals = data.Hospitals.from_csv("D:\Documents\לימודים\שנה ד\OneSideMatching\\res\seats_2018.csv")
order = assignments.get_hospitals_order(hospitals)

hospital_codes = data.get_hospital_codes()
students = data.get_all_students(hospital_codes)

temp = []

# trim students without reported priorities or result
for student in students:
    if student.reported is not None and student.real is not None and student.reported != student.real:
        student.priorities = student.reported
        temp.append(student)

students = temp

total_seats=0
for hospital, seats_count in hospitals:
    total_seats += seats_count

fixed_sesats_factor = math.ceil(total_seats/len(students))
for hospital, seats_count in hospitals:
    hospitals[hospital] = int(math.ceil(seats_count / fixed_sesats_factor))

total_seats=0
for hospital, seats_count in hospitals:
    total_seats += seats_count

if total_seats > len(students):
    for hospital in np.random.choice(hospitals.names, total_seats - len(students)):
        hospitals[hospital] -= 1

total_seats=0
for hospital, seats_count in hospitals:
    total_seats += seats_count


shouldnt_lie = 0
not_lying_precentage = 0.6
not_lying = int(len(students) * not_lying_precentage)

indices = np.random.randint(0, len(students), not_lying)
happiness_before = []
happiness_after = []

probs = assignments.expected_hat(students, hospitals, order, 1000)
for i in indices:
    students[i].priorities = students[i].real

coeff = lpsolver.get_happiness_coeff(order, students)
for i in indices:
    happiness_before.append(np.dot(np.asarray(coeff[i]), probs[i]))

problem = lpsolver.Problem(probs, order, students)
new_probs = problem.solve()

for i in indices:
    happiness_after.append(np.dot(np.asarray(coeff[i]), new_probs[i]))

for i in range(len(happiness_before)):
    if happiness_after[i] > happiness_before[i]:
        shouldnt_lie += 1


print("number of students: " + str(len(students)))
print("number of not lying students: " + str(not_lying))
print("number of student that should say truth: " + str(shouldnt_lie))