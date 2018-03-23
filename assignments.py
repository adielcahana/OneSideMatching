import numpy as np



def hat(students, hospitals):
    np.random.shuffle(students)
    for student in students:
        for choice in student.priorities:
            if hospitals[choice] > 0:
                student.assignment = hospitals[choice]
                hospitals[choice] -= 1
                break


def expected_hat(students, hospitals, iterate_num):
    shuffled_students = np.copy(students)
    probs = np.zeros((len(students), len(hospitals)))
    for i in range(iterate_num):
        hat(shuffled_students, hospitals)
        for j in range(len(students)):
            # get the second parameter of the tuple(the index of the hospital was assign to current student)
            hospital_index = hospitals[students[i].assignment][1]
            probs[j][hospital_index] += 1
