import time

import assignments
import randomizer
from data import Hospitals

hospitals = Hospitals.from_excel("res/hospital_list_test.xlsx")
students = randomizer.create_random_students(500, hospitals.names)
start = time.time()
probs, order = assignments.expected_hat(students, hospitals, 100)
print(time.time() - start)
# columns_sum = np.sum(probs, axis=0)
# for name in hospitals.names:
#     if columns_sum[order[name]] != hospitals[name] * 100:
#         print('error')

# rows_sum = np.sum(probs, axis=1)
# for i in range(len(rows_sum)):
#     if rows_sum[i] - 1.0 >= 0.000001:
#         print('error')
