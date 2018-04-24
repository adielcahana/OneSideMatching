import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import loader


def gender_stat(students):
    gender_list = get_gender(students)
    gender = ['male', "female", "unreported"]
    ax = plt.subplot(111)
    plt.title("Gender")
    labels, counts = np.unique(gender_list, return_counts=True)
    plt.bar(labels, counts,  align='center')
    plt.gca().set_xticks(labels)
    for i, v in enumerate(counts):
        ax.text(i + 0.9, v + 2.5, str(v), color='blue', fontweight='bold')
    ax.set_xticklabels(gender, rotation=0, rotation_mode="anchor", ha="center")
    plt.show()


def all_reasons_stat(students):
    all_reason = get_all_reasons(students)
    ax = plt.subplot(111)
    plt.title("Reason")
    labels, counts = np.unique(all_reason, return_counts=True)
    plt.bar(labels, counts,  align='center')
    plt.gca().set_xticks(labels)
    for i, v in enumerate(counts):
        ax.text(i + 0.9, v + 2.0, str(v), color='blue', fontweight='bold')
    plt.show()


def get_all_reasons(students):
    all_reasons_list = []
    for student in students:
        if student._all_reasons is not None:
            all_reasons_list += student._all_reasons
    return all_reasons_list

def get_gender(students):
    gender_list = []
    for student in students:
        gender_list.append(student._gender)
    return gender_list


if __name__ == "__main__":
    hospital_codes = {}
    with open("res/hospitals codes.txt", encoding='utf8') as f:
        for line in f:
            val, key = line.split(",")
            hospital_codes[int(key)] = val

    data = pd.read_csv("res//Internship Lottery_April 8, 2018_11.54.csv")
    students = []
    for i in range(2, 241):
        student = loader.get_student(i + 2, data.iloc[i], hospital_codes)
        if student is not None:
            students.append(student)

    real = 0
    reported = 0
    overlap = 0
    for student in students:
        if student.reported_priorities is not None:
            reported += 1
        if student.real_priorities is not None:
            real += 1
        if student.reported_priorities is not None and student.real_priorities is not None:
            overlap += 1

    # statistics
    #gender_stat(students)
    all_reasons_stat(students)

    print("real len: {}".format(real))
    print("reported len: {}".format(reported))
    print("overlap is: {}".format(overlap))