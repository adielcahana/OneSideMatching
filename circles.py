import loader
import randomizer

hospital_codes = loader.get_hopital_codes()
# students = loader.get_all_students(hospital_codes)
students = randomizer.create_random_statistic_students(638, )

temp = []
results_before = []
# trim students without reported priorities or result
for student in students:
    if student.reported is not None and student._result is not None:
        temp.append(student)
        results_before.append(student._result)

students = temp

swaps = 1
itetation = 0

while swaps != 0:
    itetation += 1
    swaps = 0
    for i in range(len(students)):
        result_i = students[i]._result

        for j in range(len(students)):
            result_j = students[j]._result
            if students[i].is_preferred(result_j) and students[j].is_preferred(result_i):
                students[i]._result = result_j
                students[j]._result = result_i
                swaps += 1

results_after = []
for student in students:
    results_after.append(student._result)

trades = 0
for result in zip(results_before, results_after):
    if result[0] != result[1]:
        trades += 1

print("num of trades: " + str(trades))
print("num of iteration: " + str(itetation))
