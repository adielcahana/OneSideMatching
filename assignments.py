import numpy as np


def hat(students, hospitals):
    np.random.shuffle(students)
    for student in students:
        for choice in student.get_priorities():
            if hospitals[choice] > 0:
                student.assign(hospitals[choice])
                hospitals[choice] -= 1

    return students

def expected_hat(students, hospitals):
    probs = np.zeros((len(students), len(hospitals)))
