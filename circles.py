import pandas as pd

import data

hospital_codes = data.get_hospital_codes()
students = data.get_all_students(hospital_codes)
priority_type = 'real'

columns = dict()
for i in range(len(students[0].reported)):
    columns[priority_type + '_' + str(i)] = []
columns["id"] = []
columns["result"] = []
columns["result index"] = []


temp = []
results_before = []

# trim students without reported priorities or result
for student in students:
    if student.reported is not None and student.assignment is not "":
        temp.append(student)
        results_before.append(student.assignment)
        # add to file
        for i, priority in enumerate(student.__getattribute__(priority_type)):
            columns[priority_type + '_' + str(i)].append(priority)
        columns["id"].append(student.id)
        columns["result"].append(student.assignment)
        columns["result index"].append(student.__getattribute__(priority_type).index(student.assignment))


students = temp

swaps = 1
itetation = 0

while swaps != 0:
    itetation += 1
    swaps = 0
    swaps_id = [student.id for student in students]
    for i in range(len(students)):
        result_i = students[i].assignment
        for j in range(len(students)):
            result_j = students[j].assignment
            if students[i].is_preferred(result_j, priority_type) and students[j].is_preferred(result_i, priority_type):
                students[i].assignment = result_j
                students[j].assignment = result_i

                swaps_id[i], swaps_id[j] = swaps_id[j], swaps_id[i]
                swaps += 1

    if swaps != 0:
        swap_str = "swap_" + str(itetation)
        columns[swap_str + " ids"] = swaps_id
        columns[swap_str] = []
        columns[swap_str + " index"] = []
        for student in students:
            columns[swap_str].append(student.assignment)
            columns[swap_str + " index"].append(student.__getattribute__(priority_type).index(student.assignment))


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
