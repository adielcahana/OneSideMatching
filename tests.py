from data import Hospitals
import numpy as np
import randomizer
import assignments

hospitals = Hospitals.from_excel("res\\hospital_list_test.xlsx")
students = randomizer.create_random_students(500, hospitals.names)
probs = assignments.expected_hat(students, hospitals, 100)


columns_sum = np.sum(probs, axis=0)
for name in hospitals.names:
    if columns_sum[hospitals[name][1]] != hospitals[name][0]*100:
        print(columns_sum)
