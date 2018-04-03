import time

import numpy as np

import assignments
import randomizer
from data import Hospitals
from lpsolver import solve, normalize_new_probs, birkhoff_algo, lottery

np.random.seed(1)
hospitals = Hospitals.from_excel("res/hospital_list_test1.xlsx")
students = randomizer.create_random_students(10, hospitals.names)
start = time.time()
probs, order = assignments.expected_hat(students, hospitals, 20)
solution = solve(probs, order, students)
d = normalize_new_probs(solution, hospitals._seats, hospitals.names, order)
birkhoff_list = birkhoff_algo(d)
choice = lottery(birkhoff_list)
print("\n\nwe choose: \n", birkhoff_list[choice[0]][1])


print(time.time() - start)

columns_sum = np.sum(solution, axis=0)
for name in hospitals.names:
    if columns_sum[order[name]] - hospitals[name] >= 0.0001:
        print('error')

rows_sum = np.sum(solution, axis=1)
for i in range(len(rows_sum)):
    if rows_sum[i] - 1.0 >= 0.000001:
        print('error')
