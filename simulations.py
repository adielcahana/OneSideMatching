from data import Hospitals, StatisticsStudent
import matplotlib.pyplot as plt
from copy import deepcopy
import numpy as np
import assignments
import lpsolver
import csv
import random
import pandas as pd
import collections
from matplotlib.ticker import MaxNLocator
import glob

def make_student_list(hospitals):
    student = StatisticsStudent(1)

    student.reported = student.priorities = hospitals.names
    student_list = list()
    student_list.append(student)
    for i in range(2, 639):
        # duplicate all fields like reported
        duplicate_student = deepcopy(student)
        # set another id
        duplicate_student.id = i
        student_list.append(duplicate_student)
    return student_list


# shuffle a random reported list for the first student and return the updated list
def shuffle_one_student(student_priorities):
     np.random.shuffle(student_priorities)
     return student_priorities


# after we got the same reported (except from  student[0])we make a lottery and check
# if student[0] have a better probs
def make_lottery(students, hospitals, num_of_iter):
    order = assignments.get_hospitals_order(hospitals)
    probs = assignments.expected_hat(students, hospitals, order, num_of_iter)
    problem = lpsolver.Problem(probs, order, students)
    new_probs = problem.solve()
    return new_probs, order


def swap(list, index_a, index_b):
    list[index_b], list[index_a] = list[index_a], list[index_b]


# change priorities in percentage chance
def flip_priorities(students, num_of_filps, percentage_chance):
    for index in range(len(students)):
        for i in range(num_of_filps):
            priority_list = students[index].priorities
            # percentage_chance to swap  2 items from the priority list
            if random.random() < percentage_chance:
                # swap 2 random items
                rand_a = random.randint(0, len(priority_list) - 1)
                rand_b = random.randint(0, len(priority_list) - 1)
                swap(students[index].priorities, rand_a, rand_b)
    return students


def fill_strategy(priorities_queue, strategy):
    for j in range(len(strategy)):
        next_item = priorities_queue.popleft()
        try:
            index = next(i for i, k in enumerate(strategy) if k == "")
            if next_item in strategy:
                continue
            else:
                strategy[index] = next_item
        except StopIteration:
            pass


def strategy1(priorities, strategy, top5, hospital_value):
    indices = [priorities.index(x) for x in top5]
    indices.sort()
    # fill strategies 1
    for i in indices:
        # same place as  at the priority list -> don`t move
        if i-1 < 0 or hospital_value[i] == priorities[i]:
            strategy[i] = priorities[i]
        # if the new position is already taken -> don`t move
        elif strategy[i-1] == "":
            strategy[i-1] = priorities[i]
        # check if valid move
        else:
            strategy[i] = priorities[i]
    return strategy


def strategy2(priorities, strategy, last5, hospital_value):
    indices = [priorities.index(x) for x in last5]
    indices.sort(reverse=True)

    for i in indices:
        # same place as the last 5 items at priority list -> don`t move
        if i+1 >= len(strategy) or hospital_value[i] == priorities[i]:
            strategy[i] = priorities[i]
        elif strategy[i+1] == "":
            strategy[i + 1] = priorities[i]
        # if the new position is already taken -> don`t move
        else:
            strategy[i] = priorities[i]
    return strategy


def strategy3(priorities, strategy, top3, hospital_value):
    indices = [priorities.index(x) for x in top3]
    indices.sort()
    # fill strategies 3
    for i in indices:
        # same place as  at the priority list -> don`t move
        if i-2 < 0 or hospital_value[i] == priorities[i]:
            strategy[i] = priorities[i]
        # if the new position is already taken -> don`t move
        elif strategy[i-2] == "":
            strategy[i-2] = priorities[i]
        # check if valid move
        elif [i-1] == "":
            strategy[i-1] = priorities[i]
        else:
            strategy[i] = priorities[i]
    return strategy


def strategy4(priorities, strategy, last3, hospital_value):
    indices = [priorities.index(x) for x in last3]
    indices.sort(reverse=True)

    for i in indices:
        # same place as the last 5 items at priority list -> don`t move
        if i+2 >= len(strategy) or hospital_value[i] == priorities[i]:
            strategy[i] = priorities[i]
        elif strategy[i+2] == "":
            strategy[i + 2] = priorities[i]
        # if the new position is already taken -> don`t move
        elif strategy[i+1] == "":
            strategy[i+1] = priorities[i]
        else:
            strategy[i] = priorities[i]
    return strategy


def strategy5(priorities, strategy, last3, top3, hospital_value):
    indices_top = [priorities.index(x) for x in top3]
    indices_top.sort()

    for i in indices_top:
        # same place as  at the priority list -> don`t move
        if i-1 < 0 or hospital_value[i] == priorities[i]:
            strategy[i] = priorities[i]
        # if the new position is already taken -> don`t move
        elif strategy[i-1] == "":
            strategy[i-1] = priorities[i]
        # check if valid move
        else:
            strategy[i] = priorities[i]

    indices_last = [priorities.index(x) for x in last3]
    indices_last.sort(reverse=True)

    for i in indices_last:
        # same place as the last 5 items at priority list -> don`t move
        if i+1 >= len(strategy) or hospital_value[i] == priorities[i]:
            strategy[i] = priorities[i]
        elif strategy[i+1] == "":
            strategy[i + 1] = priorities[i]
        # if the new position is already taken -> don`t move
        else:
            strategy[i] = priorities[i]
    return strategy


def strategy6(priorities, strategy, five_better_last5, hospital_value):
    indices = [priorities.index(x) for x in five_better_last5]
    indices.sort(reverse=True)

    for i in indices:
        # same place as the last 5 items at priority list -> don`t move
        if i-1 < 0 or hospital_value[i] == priorities[i]:
            strategy[i] = priorities[i]
        elif strategy[i-1] == "":
            strategy[i - 1] = priorities[i]
        else:
            strategy[i] = priorities[i]
    return strategy


# def strategy7(priorities, strategy, hospital_value):
#     return hospital_value


# def strategy8(priorities, strategy, rate_20, hospital_value):
#     strategy[4] = rate_20
#     return strategy


def strategy9(priorities, strategy, top5):
    indices = [priorities.index(x) for x in top5]
    indices.sort(reverse=True)

    for i in indices:
        # same place as the last 5 items at priority list -> don`t move
        if i+1 >= len(strategy):
            strategy[i] = priorities[i]
        elif strategy[i+1] == "":
            strategy[i + 1] = priorities[i]
        else:
            strategy[i] = priorities[i]
    return strategy


def strategy10(priorities, strategy, last5):
    indices = [priorities.index(x) for x in last5]
    indices.sort()

    for i in indices:
        # same place as the last 5 items at priority list -> don`t move
        if i-1 < 0:
            strategy[i] = priorities[i]
        elif strategy[i-1] == "":
            strategy[i - 1] = priorities[i]
        else:
            strategy[i] = priorities[i]
    return strategy


def get_strategies(hospital_value: list(), priorities):
    # initialize list of lists of strategies
    strategies = [["" for x in range(len(priorities))] for i in range(10)]
    # queue with all the priorities by order
    priorities_queue = collections.deque()
    [priorities_queue.append(i) for i in priorities]

    # strategy 1: one place up - top 5 from hospital_value
    # indices of top5 in priorities
    top5 = hospital_value[:5]
    # fill with top5
    strategies[0] = strategy1(priorities, strategies[0], top5, hospital_value)
    # fill the rest places of the strategy according to the real priorities
    fill_strategy(priorities_queue.copy(), strategies[0])

    # strategy 2: one place down - last 5 from hospital_value
    # indices of last5 in priorities
    last5 = hospital_value[-5:]
    # fill with last5
    strategies[1] = strategy2(priorities, strategies[1], last5, hospital_value)
    # fill the rest places of the strategy according to the real priorities
    fill_strategy(priorities_queue.copy(), strategies[1])

    # strategy 3: two place up - top 3 from hospital_value
    # indices of top3 in priorities
    top3 = hospital_value[:3]
    # fill with top3
    strategies[2] = strategy3(priorities, strategies[2], top3, hospital_value)
    # fill the rest places of the strategy according to the real priorities
    fill_strategy(priorities_queue.copy(), strategies[2])

    # strategy 4: two place down - last 3 from hospital_value
    # indices of last3 in priorities
    last3 = hospital_value[-3:]
    # fill with last5
    strategies[3] = strategy4(priorities, strategies[3], last3, hospital_value)
    # fill the rest places of the strategy according to the real priorities
    fill_strategy(priorities_queue.copy(), strategies[3])

    # strategy 5: top3 - one up, last3 - one down, from hospital_value
    # last3 and top3 in hospital_value
    last3 = hospital_value[-3:]
    top3 = hospital_value[:3]
    # fill with last5
    strategies[4] = strategy5(priorities, strategies[4], last3, top3, hospital_value)
    # fill the rest places of the strategy according to the real priorities
    fill_strategy(priorities_queue.copy(), strategies[4])

    # strategy 6: positions of 15-19 - one up
    before_last5 = hospital_value[15:20:1]
    # fill with last5
    strategies[5] = strategy6(priorities, strategies[5], before_last5, hospital_value)
    # fill the rest places of the strategy according to the real priorities
    fill_strategy(priorities_queue.copy(), strategies[5])

    # strategy 7: same priorities as hospital values
    strategies[6] = hospital_value

    # strategy 8: move item rated 20(hospital value) to position 5 of priorities
    strategies[7][4] = hospital_value[20]
    # fill the rest places of the strategy according to the real priorities
    fill_strategy(priorities_queue.copy(), strategies[7])

    # strategy 9: positions of top5 - one down
    strategies[8] = strategy9(priorities, strategies[8], top5)
    # fill the rest places of the strategy according to the real priorities
    fill_strategy(priorities_queue.copy(), strategies[8])

    # strategy 10: positions of top5 - one down
    strategies[9] = strategy10(priorities, strategies[9], last5)
    # fill the rest places of the strategy according to the real priorities
    fill_strategy(priorities_queue.copy(), strategies[9])

    return strategies


def simulation_flips_changes(num_of_flips, students, hospitals, sim_number):
    # students after the flips
    students = flip_priorities(students, num_of_flips, 0.5)
    # get the probs if everyone has the same reported priorities
    lottery_probs_same, order = make_lottery(students, hospitals, 100)
    # happiness of everyone
    happiness = lpsolver.get_happiness_coeff(order, students)
    # happiness of the first student
    result_happiness = np.dot(happiness[0], lottery_probs_same[0])
    print("before......:", result_happiness)

    improvement_happiness = []
    tuple_improve = list()

    hospital_value = hospitals.values

    strategies = get_strategies(hospital_value, deepcopy(students[0].priorities))

    for i in range(len(strategies)):
        # set the priorities of the first student with the i strategy
        students[0].priorities = strategies[i]
        lottery_probs, o = make_lottery(students, hospitals, 100)
        # multiple from the result from solve (dot) lottery_probs
        result_happiness_after = np.dot(happiness[0], lottery_probs[0])
        print("after:", result_happiness_after)
        #TODO add range of mistake (like 5.0) result_happiness_after - 5.0 > result_happiness
        if result_happiness_after > result_happiness:
            improvement_happiness.append((students[0].priorities, result_happiness, result_happiness_after, i, num_of_flips))
    # if improvement_happiness not empty print the details
    if improvement_happiness or num_of_flips == 0:
        with open('results/improvement_happiness' + str(sim_number) + '.csv', 'a', newline='') as resultFile:
            csv_out = csv.writer(resultFile)
            if num_of_flips == 0:
                csv_out.writerow(['priorities','real_happiness','after_strategy_happiness','strategy_id','num_of_flips'])
            for tup in improvement_happiness:
                csv_out.writerow(tup)
        tuple_improve.append((num_of_flips, len(improvement_happiness)))
    return tuple_improve


# all the students have the same priorities and we choose th first student and
# changing his priorities randomly and calculate his new happiness according
# of his new priorities
# it seems he always succeed to improve his happiness
def flip_simulation(sim_number):
    tuple_improve = list()
    # hospitals have 2 fields : 1. names of hospitals, 2. num of seats to each hospital
    hospitals = Hospitals.from_csv("res/seats_2018.csv")
    # list of students with the same priorities
    students = make_student_list(hospitals)

    # run the simulation for 25 times with the same strategies and the same priorities
    num_of_flips = 20
    for i in range(num_of_flips):
        tup = simulation_flips_changes(i, students, hospitals, sim_number)
        if tup:
            tuple_improve.append(tup)
            print(tup)
            print(" ")
    print("tuple improve results list: ")
    print(tuple_improve)


def graph_flip_succeed_example():
    # open and read the file results
    result_file = open('results/improvement_happiness0.csv')
    df = pd.read_csv(result_file)

    # draw graph1 - improvement happiness by number of flips.
    flips_column = df['num_of_flips'].real
    num_of_flips, succeed_counter = np.unique(flips_column, return_counts=True)
    fig, ax = plt.subplots()
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.plot(num_of_flips, succeed_counter)
    ax.set(xlabel='number of flips', ylabel='improvements counter', title='improvements by flips number one_simulation')
    ax.grid()
    fig.savefig("results/flips_improvements_counter_one_simulation.png")
    plt.show()


def graph_flips_average_sum():
    improvements_counter = np.zeros(1)
    files_counter = 0
    for result_file in glob.glob('results/*.csv'):
        files_counter += 1
        # open and read the file results
        result = open(result_file)
        df = pd.read_csv(result)

        # draw graph2 - improvement happiness by number of flips.
        flips_column = df['num_of_flips'].real
        improvements_counter = np.append(improvements_counter, flips_column)
    num_of_flips, succeed_counter = np.unique(improvements_counter, return_counts=True)
    succeed_counter = np.divide(succeed_counter, files_counter)
    fig, ax = plt.subplots()
    # ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.plot(num_of_flips, succeed_counter)
    ax.set(xlabel='number of flips', ylabel='improvements counter', title='Improvements by flips - Average')
    ax.grid()
    fig.savefig("results/flips_improvements_average_results.png")
    plt.show()


def processing_results():
    # full graph description (average sum of the improvements according to flips)
    graph_flips_average_sum()

    # graph of one simulation from one csv file
    # graph_flip_succeed_example()


# active flips simulation:
# num of flips get higher every iteration
# student[0] is the trickster - he have 10 strategies - trying to improve his condition
def run_flips_simulations():
    number_of_sim = 300
    for sim_num in range(number_of_sim):
        flip_simulation(sim_num)

# run sim1
run_flips_simulations()
# process the results the of flips simulation
processing_results()


