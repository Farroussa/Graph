from tabulate import tabulate
import copy


def clear():
    for i in range(20):
        print("\n")


def run():
    print("\n\n")
    a = int(input("Which table do you want to work on :\n\nType your answer : "))
    matrix = read_one_text(a)
    p_matrix = copy.deepcopy(matrix)
    clear()
    print("Here the constraint table n°", a, "\n")
    transform_pretty_table(p_matrix)
    running = True
    menu(matrix)
    while running:
        stop = int(input("\nDo you want to exit ?\n\n1 - Yes\n2 - No\n\nType your answer : "))
        clear()
        if stop == 1:
            running = False
        elif stop == 2:
            ans = int(input("Do you want to work on another constraint table ?\n\n1 - Yes"
                            "\n2 - No\n\nType your answer : "))
            clear()
            if ans == 1:
                a = int(input("Which table do you want to work on :\n\nType your answer : "))
                matrix = read_one_text(a)
                p_matrix = copy.deepcopy(matrix)
                clear()
                print("Here the constraint table n°", a, "\n")
                transform_pretty_table(p_matrix)
                menu(matrix)

            elif ans == 2:
                print("Here the constraint table n°", a, "\n")
                transform_pretty_table(p_matrix)
                menu(matrix)
            running = True


def menu(matrix):
    b = int(input("\nWhat do you want to do ?\n\n1 - Is there negative arcs\n2 - Is there a cycle"
                  "\n3 - Computations\n4 - Print the value matrix\n\nType your answer : "))
    if b == 1:
        clear()
        negative_arcs(matrix)
    elif b == 2:
        clear()
        is_acyclic(matrix)
    elif b == 3:
        if is_acyclic(matrix) and not negative_arcs(matrix):
            clear()
            print("\033[92mThe graph is acyclic and contains non negative arcs, we can process computations\033[0m\n")
            task_matrix_earliest_dates = calculate_earliest_dates(tasks_matrix)

            task_matrix_sucessors = create_successor(task_matrix_earliest_dates)

            task_matrix_latest_dates = calculate_latest_dates(task_matrix_sucessors)
            p_tasks_matrix_latest_dates = copy.deepcopy(task_matrix_latest_dates)
            transform_pretty_table2(p_tasks_matrix_latest_dates)
            c = int(input("\n\nDo you want to compute the Total Float : \n\n1 - Yes\n2 - No\n\nType your answer : "))
            if c == 1:
                clear()
                task_matrix_total_float = find_total_float(task_matrix_latest_dates)
                p_task_matrix_total_float = copy.deepcopy(task_matrix_total_float)
                transform_pretty_table2(p_task_matrix_total_float)
                critical_path(task_matrix_total_float)
    elif b == 4:
        clear()
        print("Value matrix \n")


def read_one_text(index):
    file = open('Constraint_Tables/' + str(index) + '.txt')
    data = []
    for row in file:
        data.append([str(x) for x in row.split()])
    return data


def transform_pretty_table(matrice):
    a = len(matrice[0])
    if a == 3 and matrice[0][0] != 'Task':
        matrice.insert(0, ['Task', 'Duration', 'Predecessors'])
    print(tabulate(matrice, headers='firstrow', tablefmt='fancy_grid'))


def negative_arcs(matrice):
    cpt = 1
    for i in range(len(matrice)):
        if '-' in matrice[i][1]:
            cpt = -1

    if cpt == -1:
        print("\033[91mThis problem contains negative arcs\033[0m\n\n")
        return True
    else:
        print("\033[92mNo negative arcs\033[0m\n")
        return False


def is_acyclic(matrix):
    rows_to_remove = []
    succ = []
    cycle = []
    rien = True
    while rien and matrix:

        for i, row in enumerate(matrix):
            if 'none' in row:
                rows_to_remove.append(i)
                succ.append(row[0])

        for index in sorted(rows_to_remove, reverse=True):
            del matrix[index]

        rows_to_remove.clear()

        for i in range(len(matrix)):
            if ',' in matrix[i][2]:
                mot = if_virgule(matrix[i][2])
                mot = supprimer(succ, mot)
                mot2 = ','.join(mot)
                matrix[i][2] = mot2

            elif ',' not in matrix[i][2] and matrix[i][2] in succ:
                matrix[i][2] = 'none'

        succ.clear()
        for row in matrix:
            if 'none' in row:
                rien = True
                break
        else:
            rien = False
    if matrix:
        for row in matrix:
            cycle.append(row[0])
        print("\033[91mThe graph contains a cycle\033[0m", cycle)
        return False
    else:
        print("\033[92mThe graph is acyclic\033[0m")
        return True


def if_virgule(string):
    result = string.split(',')
    return result


def supprimer(list1, list2):
    for item in list1:
        if item in list2:
            list2.remove(item)
    return list2


tasks_matrix = [['A', '1', '2', '4', '3', '6', '5', '7', '8', '9', '10', 'W'],
                ['0', '1', '2', '2', '3', '4', '4', '4', '5', '6', '7', '8'],
                ['0', '7', '3', '8', '1', '1', '2', '1', '3', '2', '1', '0'],
                ['--', 'A', '1', '1', '2', '3,4', '3,4', '3,4', '6', '8', '5,7,9', '10']]


def calculate_earliest_dates(tasks_matrix):
    durations = list(map(int, tasks_matrix[2]))

    earliest_dates = [0] * len(tasks_matrix[0])

    # Create a dictionary to map task names to their indices
    task_indices = {task: i for i, task in enumerate(tasks_matrix[0])}

    # Iterate through tasks to calculate earliest start dates
    for i in range(len(tasks_matrix[0])):
        predecessors = tasks_matrix[3][i].split(',')

        # If task has predecessors, calculate earliest start date
        if predecessors[0] != '--':
            max_completion_date = max(
                [earliest_dates[task_indices[predecessor]] + durations[task_indices[predecessor]] for predecessor in
                 predecessors])
            earliest_dates[i] = max_completion_date

    tasks_matrix.append(list(map(str, earliest_dates)))
    return tasks_matrix


def create_successor(tasks_matrix):
    task = tasks_matrix[0]
    predecessors = tasks_matrix[3]

    successor_row = []

    for i in range(len(task)):
        successor_list = []
        for j in range(len(predecessors)):
            if task[i] in predecessors[j].split(','):
                successor_list.append(task[j])
        if not successor_list:
            successor_row.append('--')
        else:
            successor_row.append(','.join(successor_list))

    tasks_matrix.append(successor_row)
    return tasks_matrix


def calculate_latest_dates(tasks_matrix):
    task_ids = tasks_matrix[0]
    durations = list(map(int, tasks_matrix[2]))
    successors = tasks_matrix[-1]

    latest_dates = [0] * len(task_ids)

    # Find the index of the task 'W'
    w_index = task_ids.index('W')

    # Set the latest date for 'W' to its earliest date
    latest_dates[w_index] = tasks_matrix[-2][w_index]

    # Iterate through tasks from right to left
    for i in range(len(task_ids) - 2, -1, -1):
        if successors[i] == 'W':
            latest_dates[i] = int(latest_dates[-1]) - durations[i]
            continue

        successor_indices = [int(successor) for successor in successors[i].split(',')]
        min_successor_latest_date = find_latest_dates(tasks_matrix, successor_indices, latest_dates)

        latest_dates[i] = int(min_successor_latest_date) - durations[i]

    tasks_matrix.append(list(map(str, latest_dates)))
    return tasks_matrix


def find_latest_dates(matrice, sucessor_indices, latest_dates):
    task = matrice[0]
    latest_date_values = []
    for i in range(1, len(task)-1):
        for j in range(len(sucessor_indices)):
            if int(task[i]) == int(sucessor_indices[j]):
                latest_date_values.append(latest_dates[i])
    return min(latest_date_values)


def find_total_float(tasks_matrix):
    earliest_dates = tasks_matrix[4]
    latest_dates = tasks_matrix[6]
    total_float = []
    for i in range(len(earliest_dates)):
        total_float.append(int(latest_dates[i]) - int(earliest_dates[i]))

    tasks_matrix.append(list(map(str, total_float)))
    return tasks_matrix


def critical_path(tasks_matrix):
    tasks = tasks_matrix[0]
    total_float = tasks_matrix[-1]
    path = []
    for i in range(len(tasks)):
        if int(total_float[i]) == 0:
            path.append(tasks[i])
    print("\nThe critical path is : \n")
    for j in range(len(path)):
        print(" --> \033[91m", path[j], "\033[0m", end='')

    print()


def transform_pretty_table2(matrice):
    a = len(matrice)

    new_column = ['Task', 'Rank', 'Duration', 'Predecessors', 'Earliest Date',
                  'Successors', 'Latest Date', 'Total Float']

    if a == 2:
        for i in range(len(matrice)):
            matrice[i].insert(0, new_column[i])
    elif a == 3:
        for i in range(len(matrice)):
            matrice[i].insert(0, new_column[i])
    elif a == 4:
        for i in range(len(matrice)):
            matrice[i].insert(0, new_column[i])
    elif a == 5:
        for i in range(len(matrice)):
            matrice[i].insert(0, new_column[i])
    elif a == 6:
        for i in range(len(matrice)):
            matrice[i].insert(0, new_column[i])
    elif a == 7:
        for i in range(len(matrice)):
            matrice[i].insert(0, new_column[i])
            transform_blue(matrice)
    elif a == 8:
        for i in range(len(matrice)):
            zeros_in_red(matrice)
            matrice[i].insert(0, new_column[i])

    print(tabulate(matrice, headers='firstrow', tablefmt='fancy_grid'))


def zeros_in_red(matrix):
    task = matrix[0]
    total_float = matrix[-1]
    for i in range(len(total_float)):
        if total_float[i] == '0':
            total_float[i] = '\033[91m' + total_float[i] + '\033[0m'
            task[i] = '\033[91m' + task[i] + '\033[0m'


def transform_blue(matrix):
    ligne_verte = matrix[4]
    ligne_verte2 = matrix[-1]
    for i in range(len(ligne_verte)):
        ligne_verte[i] = '\033[94m' + ligne_verte[i] + '\033[0m'
    for j in range(len(ligne_verte2)):
        ligne_verte2[j] = '\033[94m' + ligne_verte2[j] + '\033[0m'



def rank_func (M):
    constraint_matrix = copy.deepcopy(M)
    rank = []
    long = len(constraint_matrix)
    p = False
    old_car = []
    n = 0
    while long > 0:
        if p:
            for i in rank[n]:
                for e in range (len(constraint_matrix)):
                    if i in constraint_matrix[e][2]:
                        list = [int(x) for x in constraint_matrix[e][2].split(',')]
                        list.remove(int(i))
                        if len(list) == 0:
                            constraint_matrix[e][2] = "none"
                        else:
                            constraint_matrix[e][2] = ",".join(map(str, list))
            n += 1

        new_list = []
        for e in constraint_matrix:
            if e[2] == "none" and e[0] not in old_car:
                new_list.append(e[0])
                long -= 1
                old_car.append(e[0])
        rank.append(new_list)

        p = True
    
    rank.insert(0, ["A"])
    rank.append(["W"])


    final_matrix = []
    number_matrix = []
    rank_matrix = []
    incr = 0
    for e in rank:
        for i in e:
            number_matrix.append(i)
            rank_matrix.append(incr)
        incr += 1
    
    final_matrix.append(number_matrix)
    final_matrix.append(rank_matrix)

    return final_matrix



def duration(matrix, constraint_table):    

    duration_matrix = ['0']
    for e in matrix[0]:
        for i in constraint_table:
            if e[0] == i[0]:
                duration_matrix.append(i[1])

    duration_matrix.append('0')
    matrix.append(duration_matrix)



def predecessor (matrix, constraint_table):

    predecessor_matrix = ['--']
    predecessor_matrix.append('A')
    for e in matrix[0][2:-1]:
        for i in constraint_table:
            if int(e) == int(i[0]):
                predecessor_matrix.append(i[2])
    
    predecessor_matrix.append(constraint_table[-1][0])
    
    matrix.append(predecessor_matrix)