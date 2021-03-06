import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import data


# basic stat
def understanding_stat(students):
    understands = get_attribute_list(students, "understanding")
    answers = ["understand", "Understand in general", "Understand basics", "Do not understand", "unreported"]
    draw_hist(understands, answers, "Understand the System", -0.1, 0.7, "", "number Of students", 10)


# basic stat
def is_hat_better_stat(students):
    hat = get_attribute_list(students, "is_hat_better")
    answers = ["Yes", "Dont Know", "No", "unreported"]
    draw_hist(hat, answers, "Hat Better?", -0.1, 0.7, "", "number Of students", 10)


# basic stat
def university_stat(students):
    universities = get_attribute_list(students, "university")
    answers = ["Tel-Aviv", "Ben-Gurion", "Technion", "Hebrew", "Bar-Ilan"]
    draw_hist(universities, answers, "University", 0.85, 0.7, "university-name", "number Of students", 10)


# basic stat
def age_stat(students):
    ages = get_attribute_list(students, "age")
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


# basic stat
def all_reasons_stat(students):
    all_reason = get_all_reasons(students)
    answers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    draw_hist(all_reason, answers, "Reason", 0.9, 2.0, "answer id", "number Of students", 0)


# basic stat
def get_all_reasons(students):
    all_reasons_list = []
    for student in students:
        if student.all_reasons is not None:
            all_reasons_list += student.all_reasons
    return all_reasons_list


# basic stat
def gender_stat(students):
    gender_list = get_attribute_list(students, "gender")
    answers = ['male', "female", "unreported"]
    draw_hist(gender_list, answers, "Gender", 0.9, 2.5, "", "number Of students", 0)


# swap 2 items in current list
def swap(list_to_swap, index_a, index_b):
    list_to_swap[index_b], list_to_swap[index_a] = list_to_swap[index_a], list_to_swap[index_b]


# get real hospital votes - for each hospital separate
def single_real_hospital_votes():
    real_priority_list = get_attribute_list(students, "real")
    votes_result = count_hospitals_choices(real_priority_list)
    single_hospital_votes(votes_result, "real votes.png", "real")


# get reported hospital votes - for each hospital separate
def single_reported_hospital_votes():
    real_priority_list = get_attribute_list(students, "reported")
    votes_result = count_hospitals_choices(real_priority_list)
    single_hospital_votes(votes_result, "reported votes.png", "reported")


# get hospital votes - for each hospital separate (ministry data)
def single_ministry_of_health_data():
    votes_result = data.get_votes()
    single_hospital_votes(votes_result, "ministry data votes.png", "Ministry Of Health")


# plot the results of hospital votes - for each hospital
def single_hospital_votes(votes_result, file_name, title):
    for hospital, vote in votes_result[0].items():
        fig = plt.figure()
        ax = plt.subplot(111)
        plt.title(title + " votes for: " + hospital[::-1] + "\n" + "number of votes: " + str(votes_result[1]))
        plt.bar(list(range(1, 26)), vote,  align='center')
        plt.gca().set_xticks(list(range(1, 26)))
        # sometimes need to adjust the range numbers ( y axis range = 450?, jumps = 20?)
        plt.gca().set_yticks(list(range(0, 450, 20)))
        ax.set_xlabel("priority")
        ax.set_ylabel("number of votes")
        # plt.show()
        plt.savefig("plots/" + hospital + file_name)
        plt.close(fig)


# Generic draw hist
def draw_hist(list, label_names, title, x, y, x_name, y_name, rotate):
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


# Generic2 draw hist
def draw_hist2(students, list, label_names, title, x, y, x_name, y_name, rotate):
    ax = plt.subplot(111)
    plt.title(title)
    plt.bar(label_names, list,  align='center')
    plt.gca().set_xticks(label_names)
    ax.set_xlabel(x_name)
    ax.set_ylabel(y_name)
    plt.show()


# to get the votes results - count the times hospital was chosen at X position
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
    # return tne num of votes and the list of each hospital(dictionary)
    return d_name_to_list, legal_counter_votes


# real rating - according to the type of the happiness func(linear, quadratic, median)
def real_priority_hist(students, type):
    # get a list of the real priorities
    real_priority_list = get_attribute_list(students, "real")
    d_name_to_priority = dict()
    # initialize dictionary to key=name and value=priority list
    for hos_name in real_priority_list[0]:
        d_name_to_priority[hos_name] = np.zeros(len(real_priority_list[0]))
    # priority_counter - each hospital has a list of votes
    priority_counter, counter_legal_votes = count_hospitals_choices(real_priority_list)
    # plot results
    popular_hospitals_stat(priority_counter, counter_legal_votes, d_name_to_priority,
                           "Hospital rating by students real priority - " + type + " happiness", type)


# reported rating - according to the type of the happiness func(linear, quadratic, median)
def reported_priority_hist(students, type):
    # get a list of the real priorities
    real_priority_list = get_attribute_list(students, "reported")
    d_name_to_priority = dict()
    # initialize dictionary to key=name and value=priority list
    for hos_name in real_priority_list[0]:
        d_name_to_priority[hos_name] = np.zeros(len(real_priority_list[0]))
    # priority_counter - each hospital has a list of votes
    priority_counter, counter_legal_votes = count_hospitals_choices(real_priority_list)
    # plot results
    popular_hospitals_stat(priority_counter, counter_legal_votes, d_name_to_priority,
                           "Hospital rating by students reported priority - " + type + " happiness", type)


#  ministry of health rating - according to the type of the happiness func(linear, quadratic, median)
def ministry_of_health_data(type):
    priority_dict, num_of_students = data.get_votes()
    d_name_to_priority = dict()
    # initialize dictionary to key=name and value=priority list
    for hos_name in list(priority_dict.keys()):
        d_name_to_priority[hos_name] = np.zeros(len(priority_dict.keys()))
        # plot results
    popular_hospitals_stat(priority_dict, num_of_students, d_name_to_priority,
                           "Hospital priority - Ministry Of Health data - " + type + " happiness", type)


# plot according to the type of the happiness func
def popular_hospitals_stat(priority_counter, counter_legal_votes, d_name_to_priority, title,
                           happiness_type="quadratic"):
    list_size = len(priority_counter)
    coefficient_vector = np.zeros(list_size)
    if happiness_type == 'quadratic':
        for i in range(list_size):
            coefficient_vector[i] = (list_size - i)**2
    elif happiness_type == 'linear':
        for i in range(list_size):
            coefficient_vector[i] = list_size - i
    elif happiness_type == 'median':
        middle = list_size // 2
        for i in range(list_size):
            if i <= middle:
                coefficient_vector[i] = (list_size - i - middle)**2
            else:
                coefficient_vector[i] = -((list_size - i - middle)**2)
        coefficient_vector += abs(min(coefficient_vector))
    for name, priority in priority_counter.items():
        d_name_to_priority[name] = np.dot(coefficient_vector, priority)
    ax = plt.subplot(111)
    plt.title(title)
    li = list(d_name_to_priority.items())
    li = sorted(li, key=lambda x: x[1])
    x = [e[0] for e in li]
    # normalization
    if happiness_type == 'linear':
        y = [e[1]/1000 for e in li]
    else:
        y = [e[1]/1000 for e in li]

    plt.bar(x, y,  align='center')
    plt.gca().set_xticks(list(d_name_to_priority.keys()))

    name_reverse = []
    for name in d_name_to_priority.keys():
        name_reverse.append(name[::-1])
    ax.set_xticklabels(name_reverse, rotation=90, rotation_mode="anchor", ha="right")
    if happiness_type == 'linear':
        ax.set_ylabel("Hospital priority (x10^4)")
    else:
        ax.set_ylabel("Hospital priority (x10^5)")
    plt.xlabel("students votes: " + str(counter_legal_votes))
    plt.show()


# the data of the health ministry - with 3 different happiness functions in one graph.
def ministry_of_health_data_all():
    priority_dict, num_of_students = data.get_votes()
    d_name_to_priority = dict()
    # initialize dictionary to key=name and value=priority list
    for hos_name in list(priority_dict.keys()):
        d_name_to_priority[hos_name] = np.zeros(len(priority_dict.keys()))
    # plot results
    popular_hospitals_stat_all(priority_dict, num_of_students,
                               "Hospital priority - Ministry Of Health data - happiness results")


# plot 3 different happiness functions in one graph
def popular_hospitals_stat_all(priority_counter, counter_legal_votes, title):
    # signs: Q = quadratic, L = linear, M = median
    list_size = len(priority_counter)
    d_name_to_priorityQ = dict()
    d_name_to_priorityL = dict()
    d_name_to_priorityM = dict()
    coefficient_vectorQ = np.zeros(list_size)
    coefficient_vectorL = np.zeros(list_size)
    coefficient_vectorM = np.zeros(list_size)

    middle = list_size // 2
    for i in range(list_size):
        coefficient_vectorQ[i] = (list_size - i)**2
        coefficient_vectorL[i] = list_size - i
        if i <= middle:
            coefficient_vectorM[i] = (list_size - i - middle)**2
        else:
            coefficient_vectorM[i] = -((list_size - i - middle)**2)
        coefficient_vectorM += abs(min(coefficient_vectorM))
    for name, priority in priority_counter.items():
        d_name_to_priorityQ[name] = np.dot(coefficient_vectorQ, priority)
        d_name_to_priorityL[name] = np.dot(coefficient_vectorL, priority)
        d_name_to_priorityM[name] = np.dot(coefficient_vectorM, priority)

    ax = plt.subplot(111)
    plt.title(title)
    liQ = list(d_name_to_priorityQ.items())
    liQ = sorted(liQ, key=lambda x: x[1])

    liL = list(d_name_to_priorityL.items())
    liL = sorted(liL, key=lambda x: x[1])

    liM = list(d_name_to_priorityM.items())
    liM = sorted(liM, key=lambda x: x[1])

    # To be with equal arrangement -
    # we make swaps of items in liM and liL according to the sort of liQ results.
    swap(liL, 3, 4)
    swap(liM, 2, 3)
    swap(liM, 3, 4)
    swap(liM, 11, 12)
    swap(liM, 13, 14)
    swap(liM, 14, 15)
    swap(liM, 15, 16)

    xQ = [e[0] for e in liQ]
    yQ = [e[1]/1000 for e in liQ]
    yL = [e[1]/1000 for e in liL]

    # to make the graph look better
    yL = [e*5 for e in yL]
    yM = [e[1]/1000 for e in liM]

    name_reverse = []
    for name in xQ:
        name_reverse.append(name[::-1])
    ax.set_xticklabels(name_reverse, rotation=90, rotation_mode="anchor", ha="right")
    ax.set_ylabel("Hospital priority (x10^4)")
    plt.xlabel("students votes: " + str(counter_legal_votes))

    plt.plot(name_reverse, yQ)
    plt.plot(name_reverse, yL)
    plt.plot(name_reverse, yM)

    plt.legend(['y = Quadratic', 'y = Linear', 'y = Median'], loc='upper left')
    plt.show()


# basic plot
def pair_stat(students):
    pairs = get_attribute_list(students, "pair")
    answers = ["Yes", "No", "unreported"]
    draw_hist(pairs, answers, "Pair ?", -0.1, 0.7, "", "number Of students", 10)


# get desirable attribute from each student
def get_attribute_list(students, attribute):
    attribute_list = []
    if attribute == "result":
        for student in students:
            attribute_list.append(student.assignment)
    else:
        for student in students:
            attribute_list.append(getattr(student, attribute))
    return attribute_list


# count how many students got one of their top 5 real priorities
# (return the counter and their indexes)
def got_result_from_range():
    real_priority_list = get_attribute_list(students, "real")
    result_list = get_attribute_list(students, "result")
    i = 0
    top5_counter = 0
    five_ten_counter = 0
    ten_fif_counter = 0
    fif_twenty_counter = 0
    last5_counter = 0
    for student_list in real_priority_list:
        if student_list:
            top5 = student_list[:5]
            five_ten = student_list[5:10]
            ten_fif = student_list[10:15]
            fif_twenty = student_list[15:20]
            last5 = student_list[20:25]
            if not pd.isnull(result_list[i]):
                if result_list[i] in top5:
                    top5_counter += 1
                if result_list[i] in five_ten:
                    five_ten_counter += 1
                if result_list[i] in ten_fif:
                    ten_fif_counter += 1
                if result_list[i] in fif_twenty:
                    fif_twenty_counter += 1
                if result_list[i] in last5:
                    last5_counter += 1
        i += 1
    num_of_participants = top5_counter+five_ten_counter+ten_fif_counter+fif_twenty_counter+last5_counter
    draw_hist2(students, [top5_counter, five_ten_counter, ten_fif_counter, fif_twenty_counter, last5_counter],
               ['1-5', '6-10', '11-15', '16-20', '21-25'],
               "Placement of the final results according to the students' real choice ", 0.9, 2.0,
               "Final placement range \n participants:" + str(num_of_participants),
               "number Of students", 0)

if __name__ == "__main__":
    # get data
    hospital_codes = data.get_codes("res/hospitals codes.txt")
    result_codes = data.get_codes("res/results codes.txt")
    students = data.get_all_students(hospital_codes, result_codes)

    # statistics functions : to activate just uncomment the desirable line ->

    # gender_stat(students)
    # all_reasons_stat(students)
    # age_stat(students)
    # university_stat(students)
    # is_hat_better_stat(students)
    # understanding_stat(students)
    # pair_stat(students)
    # popular_hospitals_stat(students)

    # real_priority_hist(students, 'quadratic')
    # real_priority_hist(students, 'linear')
    # real_priority_hist(students, 'median')

    # reported_priority_hist(students, 'quadratic')
    # reported_priority_hist(students, 'linear')
    # reported_priority_hist(students, 'median')

    # single_real_hospital_votes()
    # single_reported_hospital_votes()
    # single_ministry_of_health_data()

    # the data of the health ministry - with 3 different happiness functions in one graph.

    # -> current active func <-
    ministry_of_health_data_all()

    # ministry_of_health_data('quadratic')
    # ministry_of_health_data('linear')
    # ministry_of_health_data('median')

    # got_result_from_range()

