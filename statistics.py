import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import loader


def single_real_hospital_votes():
    real_priority_list = get_attribute_list(students, "_real")
    votes_result = count_hospitals_choices(real_priority_list)
    ax = plt.subplot(111)

    for hospital, vote in votes_result[0].items():
        plt.title("votes for: " + hospital[::-1] + "\n" + "number of votes: " + str(votes_result[1]))
        plt.bar(list(range(1, 26)), vote,  align='center')
        plt.gca().set_xticks(list(range(1, 26)))
        ax.set_xticklabels((list(map(str, range(1, 26)))), rotation=0, rotation_mode="anchor", ha="center")
        ax.set_xlabel("priority")
        ax.set_ylabel("number of votes")
        plt.show()


def draw_hist(students, list, label_names, title, x, y, x_name, y_name, rotate):
    ax = plt.subplot(111)
    plt.title(title)
    labels, counts = np.unique(list, return_counts=True)
    plt.bar(labels, counts,  align='center')
    plt.gca().set_xticks(labels)
    for i, v in enumerate(counts):
        ax.text(i + x, v + y, str(v), color='blue', fontweight='bold')
    ax.set_xticklabels(label_names, rotation=rotate, rotation_mode="anchor", ha="center")
    ax.set_xlabel(x_name)
    ax.set_ylabel(y_name)
    plt.show()


def count_hospitals_choices(real_priority_list):
    d_name_to_list = dict()
    legal_counter_votes = 0
    for hos_name in real_priority_list[0]:
        d_name_to_list[hos_name] = np.zeros(len(real_priority_list[0]))
    for ls in real_priority_list:
        if ls is None:
            continue
        legal_counter_votes += 1
        for index_name in range(len(ls)):
            d_name_to_list[ls[index_name]][index_name] += 1
    return d_name_to_list, legal_counter_votes


def real_priority_hist(students):
    popular_hospitals_stat(students, "_real", "Hospital rating by students real priority")


def reported_priority_hist(students):
    popular_hospitals_stat(students, "_reported", "Hospital rating by students reported priority")


def popular_hospitals_stat(students, attr, title):
    # get a list of the real priorities
    real_priority_list = get_attribute_list(students, attr)
    d_name_to_priority = dict()
    # initialize dictionary to key=name and value=priority list
    for hos_name in real_priority_list[0]:
        d_name_to_priority[hos_name] = np.zeros(len(real_priority_list[0]))
    # priority_counter - each hospital has a list of votes
    priority_counter, counter_legal_votes = count_hospitals_choices(real_priority_list)
    num = len(real_priority_list[0])
    coefficient_vector = np.zeros(num)
    for i in range(len(real_priority_list[0])):
        coefficient_vector[i] = (num - i)**2
    for name, priority in priority_counter.items():
        d_name_to_priority[name] = np.dot(coefficient_vector, priority)
    ax = plt.subplot(111)
    plt.title(title)
    li = list(d_name_to_priority.items())
    li = sorted(li, key=lambda x: x[1])
    x = [e[0] for e in li]
    y = [e[1]/10000 for e in li]
    plt.bar(x, y,  align='center')
    plt.gca().set_xticks(list(d_name_to_priority.keys()))

    name_reverse = []
    for name in d_name_to_priority.keys():
        name_reverse.append(name[::-1])
    ax.set_xticklabels(name_reverse, rotation=90, rotation_mode="anchor", ha="right")
    ax.set_ylabel("Hospital priority (x10^5)")
    plt.xlabel("students votes: " + str(counter_legal_votes))
    plt.show()


def pair_stat(students):
    pairs = get_attribute_list(students, "_pair")
    answers = ["Yes", "No", "unreported"]
    draw_hist(students, pairs, answers, "Pair ?", -0.1, 0.7, "", "number Of students", 10)


def get_attribute_list(students, attribute):
    list = []
    for student in students:
        list.append(getattr(student, attribute))
    return list


def understanding_stat(students):
    understands = get_attribute_list(students, "_understanding")
    answers = ["understand", "Understand in general", "Understand basics", "Do not understand", "unreported"]
    draw_hist(students, understands, answers, "Understand the System", -0.1, 0.7, "", "number Of students", 10)


def is_hat_better_stat(students):
    hat = get_attribute_list(students, "_is_hat_better")
    answers = ["Yes", "Dont Know", "No", "unreported"]
    draw_hist(students, hat, answers, "Hat Better?", -0.1, 0.7, "", "number Of students", 10)


def university_stat(students):
    universities = get_attribute_list(students, "_university")
    answers = ["Tel-Aviv", "Ben-Gurion", "Technion", "Hebrew", "Bar-Ilan"]
    draw_hist(students, universities, answers, "University", 0.85, 0.7, "university-name", "number Of students", 10)


def age_stat(students):
    ages = get_attribute_list(students, "_age")
    ages.remove(1)
    ax = plt.subplot(111)
    plt.title("Age")
    labels, counts = np.unique(ages, return_counts=True)
    plt.bar(labels, counts,  align='center')
    plt.gca().set_xticks(labels)
    for i, v in enumerate(counts):
        if i == (len(counts)-1):
            i += 1
        ax.text(i + 22.7, v + 0.7, str(v), color='blue', fontweight='bold')
    ax.set_xlabel('student age')
    ax.set_ylabel('number Of students')
    plt.show()


# all reasons hist
def all_reasons_stat(students):
    all_reason = get_all_reasons(students)
    answers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    draw_hist(students, all_reason, answers, "Reason", 0.9, 2.0, "answer id", "number Of students", 0)


def get_all_reasons(students):
    all_reasons_list = []
    for student in students:
        if student._all_reasons is not None:
            all_reasons_list += student._all_reasons
    return all_reasons_list


# gender hist
def gender_stat(students):
    gender_list = get_attribute_list(students, "_gender")
    answers = ['male', "female", "unreported"]
    draw_hist(students, gender_list, answers, "Gender", 0.9, 2.5, "", "number Of students", 0)


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
    #all_reasons_stat(students)
    #age_stat(students)
    #university_stat(students)
    #is_hat_better_stat(students)
    #understanding_stat(students)
    #pair_stat(students)
    #popular_hospitals_stat(students)
    #real_priority_hist(students)
    #reported_priority_hist(students)
    single_real_hospital_votes()

    print("real len: {}".format(real))
    print("reported len: {}".format(reported))
    print("overlap is: {}".format(overlap))