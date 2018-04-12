import pandas as pd
from data import Student
import pandas as pd

from data import Student


def get_student(row):
    for j in range(1, len(hospital_codes) + 1):
        code = int(data.iloc[i]['Real_' + str(j)])
        if code is None:
            raise ValueError
        real_priorities.append(hospital_codes[code])
        code = int(data.iloc[i]['Reported_' + str(j)])
        if code is None:
            students_real.append(Student(i, real_priorities))
            raise ValueError
        reported_priorities.append(hospital_codes[code])

def get_priorites(row, type, codes):
    if type == 'real':
        col_name = 'Real_'
    else:
        col_name = 'Reported_'
        priorities = parse_reported_raw(row)
        if priorities is not None:
            return priorities

    priorities = []
    for i in range(1, len(codes) + 1):
        code = int(row[col_name + str(j)])
        if code == np.nan:
            return None
        priorities.append(hospital_codes[code])
    return priorities

def parse_reported_raw(row, codes):
    priorities = []
    hospital = str()
    last_word = False
    for element in str(row["Reported Raw"]).split():
        if element[-1] == '.':
            last_word = False
            if len(hospital) > 0:
                priorities.append(hospital)
                hospital = str()
        else:
            if last_word is True:
                hospital += " " + element
            else:
                hospital = element
                last_word = True
    print(priorities)


hospital_codes = {}

with open("res/hospitals codes.txt", encoding='utf8') as f:
    for line in f:
        val, key = line.split(",")
        hospital_codes[int(key)] = val

data = pd.read_csv("res//Internship Lottery_April 8, 2018_11.54.csv")
parse_reported_raw(data.iloc[10], hospital_codes)

# students_real = []
# students_reported = []
# overlap = 0
# for i in range(4, 241):
#     real_priorities = []
#     reported_priorities = []
#     try:
#         for j in range(1, len(hospital_codes) + 1):
#             code = int(data.iloc[i]['Real_' + str(j)])
#             if code is None:
#                 raise ValueError
#             real_priorities.append(hospital_codes[code])
#             code = int(data.iloc[i]['Reported_' + str(j)])
#             if code is None:
#                 students_real.append(Student(i, real_priorities))
#                 raise ValueError
#             reported_priorities.append(hospital_codes[code])
#         overlap += 1
#         students_real.append(Student(i, real_priorities))
#         students_reported.append(Student(i, reported_priorities))
#     except ValueError:
#         continue
#
# print("real len: {}".format(len(students_real)))
# print("reported len: {}".format(len(students_reported)))
# print("overlap is: {}".format(overlap))
