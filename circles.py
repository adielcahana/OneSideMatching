import pandas as pd

import data

hospital_codes = data.get_hospital_codes()
students = data.get_all_students(hospital_codes)


columns = dict()
for i in range(len(students[0].reported)):
    columns['priority_' + str(i)] = []
columns["id"] = []
columns["result"] = []


temp = []
results_before = []

# trim students without reported priorities or result
for student in students:
    if student.reported is not None and student.assignment is not "":
        temp.append(student)
        results_before.append(student.assignment)
        # add to file
        for i, priority in enumerate(student.reported):
            columns['priority_' + str(i)].append(priority)
        columns["id"].append(student.id)
        columns["result"].append(student.assignment)


students = temp

swaps = 1
itetation = 0

while swaps != 0:
    itetation += 1
    swaps = 0
    for i in range(len(students)):
        result_i = students[i].assignment

        for j in range(len(students)):
            result_j = students[j].assignment
            if students[i].is_preferred(result_j) and students[j].is_preferred(result_i):
                students[i].assignment = result_j
                students[j].assignment = result_i
                swaps += 1
    if swaps != 0:
        columns["swap_" + str(itetation)] = []
        for student in students:
            columns["swap_" + str(itetation)].append(student.assignment)


results_after = []
for student in students:
    results_after.append(student.assignment)

trades = 0
for result in zip(results_before, results_after):
    if result[0] != result[1]:
        trades += 1

pd.DataFrame(columns).to_csv("circles_result.csv")
print("num of trades: " + str(trades))
print("num of iteration: " + str(itetation))
