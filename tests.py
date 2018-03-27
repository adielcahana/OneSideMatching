import time

import numpy as np

import assignments
import randomizer
from data import Hospitals
from lpsolver import solve

np.random.seed(1)
hospitals = Hospitals.from_excel("res/hospital_list_test.xlsx")
students = randomizer.create_random_students(500, hospitals.names)
start = time.time()
probs, order = assignments.expected_hat(students, hospitals, 100000)
solution = solve(probs, order, students)

print(time.time() - start)

columns_sum = np.sum(solution, axis=0)
for name in hospitals.names:
    if columns_sum[order[name]] - hospitals[name] >= 0.0001:
        print('error')

rows_sum = np.sum(solution, axis=1)
for i in range(len(rows_sum)):
    if rows_sum[i] - 1.0 >= 0.000001:
        print('error')
