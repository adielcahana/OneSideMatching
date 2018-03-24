import numpy as np

from data import Hospitals


def hat(students, hospitals):
    np.random.shuffle(students)
    for student in students:
        for choice in student.priorities:
            if hospitals[choice] > 0:
                student.assignment = choice
                hospitals[choice] -= 1
                break


def expected_hat(students, hospitals, iterate_num):
    hospitals_order = dict()
    i = 0
    for name in hospitals.names:
        hospitals_order[name] = i
        i += 1
    probs = np.zeros((len(students), len(hospitals)))
    shuffled_students = np.copy(students)

    for i in range(iterate_num):
        seats = Hospitals.copy(hospitals)
        hat(shuffled_students, seats)
        for j in range(len(students)):
            hospital_index = hospitals_order[students[j].assignment]
            probs[j][hospital_index] += 1

    probs /= iterate_num
    return probs, hospitals_order
