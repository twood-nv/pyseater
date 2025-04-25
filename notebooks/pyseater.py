from enum import Enum
import csv
import time
import random as rng
from datetime import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.patches as mpatch
plt.rcParams['figure.figsize'] = [8, 8] # adjust this to get a good fig size depending on the display you're using...

# tables = []
# n_places = 0
# n_students = 0


Divide = Enum('Divide', [('HORIZONTAL', 0), ('VERTICAL', 1)])
Orientate = Enum('Orientate', [('NORTH', 0), ('EAST', 1), ('SOUTH', 2), ('WEST', 3)])


class Table :
    def __init__(self, x_length, y_length, divide) :
        self.x_length = x_length
        self.y_length = y_length
        self.divide = divide
        if divide == Divide.HORIZONTAL : assert(y_length == 2)
        else : assert(x_length == 2)
        self.places = []
        self.fitness = 0
    def add_place(self, place) :
        self.places.append(place)


class Place:
    def __init__(self, x, y, orientate) :
        self.x = x
        self.y = y
        self.orientate = orientate
        self.student = 0
        self.adjacent = 0
        self.opposite = 0
    def assign_student(self, student) :
        self.student = student
    def set_adjacent(self, adjacent) :
        self.adjacent = adjacent
    def set_opposite(self, opposite) :
        self.opposite = opposite
        

class Student :
    def __init__(self) :
        self.attributes = {}
    def set_attribute(self, key, value) :
        self.attributes[key] = value
    def get_attribute(self, key) :
        return self.attributes[key]


class Rule :
    def __init__(self, attribute, boolean) :
        self.attribute = attribute
        self.boolean = boolean


class Parameters : 
    def __init__(self) :
        self.seed = None
        self.font_size = 8
        self.n_rows = 10
        self.n_cols = 10
        self.max_iterations = 1000000
        self.target_fitness = 100.
        self.student_file = "../data/students.csv"
        self.migration_interval = 5
        self.batch_size = 0
        self.log_level = 1  
        

class Pyseater :
    def __init__(self, n_rows, n_cols) : 
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.classroom = [[0 for i in range(n_cols)] for j in range(n_rows)]
        self.n_places = 0
        self.n_students = 0
        self.tables = []
        self.adj_rules = []
        self.ops_rules = []
        # self.max_iterations = 0

    def solve(self, args) :
        iterations = 0
        perfect_fitness = self.n_places * (len(self.adj_rules) + len(self.ops_rules))
        best_fitness = 0
        solution_found = False    
        start_time = time.time()

        while iterations < args.max_iterations :
            # Apply rules and do swaps
            for table in self.tables :
                process_table(self, table)        

            # Compute table fitness
            for table in self.tables :
                compute_table_fitness(self, table)

            # Compute solution fitness
            solution_fitness = 0
            for table in self.tables :
                solution_fitness = solution_fitness + table.fitness

            if(args.log_level > 1) : 
                if solution_fitness > best_fitness: best_fitness = solution_fitness
                print_progress_bar(solution_fitness, args.target_fitness, best_fitness, length = 50)
            
            # Check fitness
            if solution_fitness >= args.target_fitness :
                solution_found = True
                exec_time = (time.time() - start_time)
                break
            else :
                if iterations % args.migration_interval == 0 :
                    student_swap_table_random(self.tables)

            iterations = iterations + 1

        # End, do reporting
        if (iterations == args.max_iterations) or (solution_found == True) :
            exec_time = (time.time() - start_time)
            if (solution_found == True) and (args.log_level > 0) :
                percentage_fitness = (solution_fitness / perfect_fitness) * 100
                print("\nSUCCESS, " + str(round(percentage_fitness, 2)) + "% after " + str(iterations) + " iterations, in " +str(round(exec_time, 2)) + " seconds. Throughput: " + str(round(iterations / exec_time, 2)))
                # screen.update()
            elif (solution_found == False) and (args.log_level > 0) :
                print("\nFAIL, no solution after " + str(iterations) + " iterations, in " +str(round(exec_time, 2)) + " seconds. Throughput: " + str(round(iterations / exec_time, 2)))
                
        if args.log_level == 0 : print(str(solution_found) + "," + str(iterations) + "," + str(round(iterations / exec_time, 2)) +"," + str(exec_time))
        

def find_adjacent(myseater, place) :
    if place.orientate in (Orientate.NORTH, Orientate.SOUTH) :
        if (place.x - 1 != -1) and (myseater.classroom[place.x -1][place.y] != 0) :
            return myseater.classroom[place.x - 1][place.y]
        elif (place.x + 1 != myseater.n_cols) and (myseater.classroom[place.x + 1][place.y] != 0) :
            return myseater.classroom[place.x + 1][place.y]
    elif place.orientate in (Orientate.EAST, Orientate.WEST) :
        if (place.y - 1 != -1) and (myseater.classroom[place.x][place.y - 1] != 0) :
            return myseater.classroom[place.x][place.y - 1]
        elif (place.y + 1 != myseater.n_cols) and (myseater.classroom[place.x][place.y + 1] != 0) :
            return myseater.classroom[place.x][place.y + 1]


def find_opposite(myseater, place) :
    if place.orientate == Orientate.NORTH :
        return myseater.classroom[place.x][place.y - 1]
    elif place.orientate == Orientate.EAST : 
        return myseater.classroom[place.x + 1][place.y]
    elif place.orientate == Orientate.SOUTH : 
        return myseater.classroom[place.x][place.y + 1]
    elif place.orientate == Orientate.WEST : 
        return myseater.classroom[place.x - 1][place.y]


def add_table(myseater, x_start, y_start, table) :
    myseater.tables.append(table)
    for x in range(x_start, x_start + table.x_length) :
        for y in range(y_start, y_start + table.y_length) :
            if table.divide == Divide.HORIZONTAL :
                orientate = (Orientate.SOUTH if y == y_start  else Orientate.NORTH)
            else :
                orientate = (Orientate.EAST if x == x_start  else Orientate.WEST)
            place = Place(x, y, orientate)
            # global n_places
            myseater.n_places = myseater.n_places + 1
            myseater.classroom[x][y] = place
            table.add_place(place)
    for place in table.places :
        place.set_adjacent(find_adjacent(myseater, place))
        place.set_opposite(find_opposite(myseater, place))


def process_table(myseater, table) :
    for place in table.places :
        # apply multiple rulsets here!
        fit = apply_ruleset(myseater.adj_rules, place.student, place.adjacent.student)
        fit = apply_ruleset(myseater.ops_rules, place.student, place.opposite.student)
        if fit == False :
            if (table.x_length > 2) or (table.y_length > 2) :
                coin = rng.randint(0, 2)
                if coin == 0 : swap_students(place, place.opposite)
                elif coin == 1 : swap_students(place, place.adjacent)
                else : student_swap_random(table, place)
            else : swap_students(place, place.opposite)
            return


def compute_table_fitness(myseater, table) :
    table.fitness = 0
    for place in table.places :
        for rule in myseater.adj_rules :
            table.fitness = table.fitness + apply_rule(rule, place.student, place.adjacent.student)
        for rule in myseater.ops_rules :
            table.fitness = table.fitness + apply_rule(rule, place.student, place.opposite.student)


def apply_ruleset(ruleset, student_a, student_b) :
    for rule in ruleset :        
        if apply_rule(rule, student_a, student_b) == 0 : return False


def apply_rule(rule, student_a, student_b) :
    return 0 if rule.boolean != (student_a.get_attribute(rule.attribute) == student_b.get_attribute(rule.attribute)) else 1


def student_swap_random(table, place) :
    index = rng.randint(0, len(table.places) - 1)
    swap_students(place, table.places[index])


def student_swap_table_random(tables) :
    for i in range(0, len(tables)) :
        a = i
        b = i + 1 if i != len(tables) - 1 else 0
        if tables[a] == tables[b] : rng.shuffle(tables[a].desks)
        else : student_swap_table(tables[a], tables[b])


def student_swap_table(table_a, table_b) :
    place_a = table_a.places[rng.randint(0, (table_a.x_length * table_a.y_length) - 1)]
    place_b = table_b.places[rng.randint(0, (table_b.x_length * table_b.y_length) - 1)]
    swap_students(place_a, place_b)


def swap_students(place_a, place_b) :
    student_temp = place_a.student
    place_a.assign_student(place_b.student)
    place_b.assign_student(student_temp)


def read_students(myseater, student_file) :
    with open(student_file, 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(filter(lambda row: row[0]!='#', file))
        keys = next(reader)
        students = []
        for row in reader :
            s = Student()
            for i in range(len(row)) :
                s.set_attribute(keys[i], row[i])
            students.append(s)
            if(len(students) == myseater.n_places) :
                break
        # myseater.n_students = len(students)
        # print("n_places: " + str(n_places) + " n_students: " + str(n_students))
    return students


def print_progress_bar (current_fitness, target_fitness, best_fitness, decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    current_percent = ("{0:." + str(decimals) + "f}").format(100 * (current_fitness / float(target_fitness)))
    best_percent = ("{0:." + str(decimals) + "f}").format(100 * (best_fitness / float(target_fitness)))
    filledLength = int(length * current_fitness // target_fitness)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{"Current: "} |{bar}| {current_percent}% {"Best: "} {best_percent}%', end = printEnd)


def get_place_text(place) :
    values = list(place.student.attributes.values())
    n_items =  min(3, len(values))
    adjust_vertical = n_items * 0.3
    label = ""
    for i in range(0, n_items) :
        label += values[i] + "\n"
    return label


def draw_floorplan(myseater) :
    
    fig, ax = plt.subplots()
    rectangles = {}
    count = 0       
    for x in range(myseater.n_rows) : 
        for y in range(myseater.n_cols) :
            if myseater.classroom[x][y] != 0 :
                colour = "darkgray"
                if myseater.classroom[x][y].student != 0 :
                    label = get_place_text(myseater.classroom[x][y])  
                    if "colour" in myseater.classroom[x][y].student.attributes : 
                        colour = myseater.classroom[x][y].student.get_attribute("colour")
                else :
                    label = count
                rectangles[label] = mpatch.Rectangle((x, y), 1, 1, facecolor=colour, edgecolor='black')
                count = count + 1  
        

    for r in rectangles:
        ax.add_patch(rectangles[r])
        rx, ry = rectangles[r].get_xy()

        # print(str(rx) + " " + str(ry) + " " + str(myseater.classroom[rx][ry].orientate))

        x = rx
        y = ry

        # North
        if myseater.classroom[rx][ry].orientate == Orientate.NORTH :          
            ax.add_patch(mpatch.Polygon([[x + 0.5, y],[x + 0.4, y + 0.2],[x + 0.6, y + 0.2]], closed=True,fill=True, color="white"))
        
        # South
        elif myseater.classroom[rx][ry].orientate == Orientate.SOUTH :
            ax.add_patch(mpatch.Polygon([[x + 0.5, y + 1],[x + 0.4, y + 0.8],[x + 0.6, y + 0.8]], closed=True,fill=True, color="white"))
        
        #East
        elif myseater.classroom[rx][ry].orientate == Orientate.EAST :
            ax.add_patch(mpatch.Polygon([[x + 1, y + 0.5],[x + 0.8, y + 0.4],[x + 0.8, y + 0.6]], closed=True,fill=True, color="white"))
        
        #West
        elif myseater.classroom[rx][ry].orientate == Orientate.WEST :
            ax.add_patch(mpatch.Polygon([[x, y + 0.5],[x + 0.2, y + 0.4],[x + 0.2, y + 0.6]], closed=True,fill=True, color="white"))

        
        cx = rx + rectangles[r].get_width() / 2.0
        cy = ry + rectangles[r].get_height() / 2.0
        ax.annotate(r, (cx, cy), color='black', weight='normal', fontsize=8, ha='center', va='center')
    
    ax.set_xlim((0, myseater.n_rows))
    ax.set_ylim((0, myseater.n_cols))
    ax.set_aspect('equal')
    # ax.axis('off')  # hide the surrounding axes
    plt.show()


def save_figure(figname, fig) :
    dtnow = dt.now()
    dtstr = dtnow.strftime("%d-%m-%Y_%H:%M:%S_")
    filename = dtstr + figname + ".svg"
    print("saving: " + figname + " as " + filename)
    fig.savefig(filename)


def generate_random_floorplan(myseater) :
    for x in range(0, myseater.n_cols) :
        for y in range(0, myseater.n_rows) :       
            table = generate_random_table()
            if check_boundary(x, y, table, myseater) != False :
                if space_is_empty(x, y, table, myseater) != False :
                    add_table(myseater, x, y, table)
    # if(args.log_level > 1) : 
    # if(args.log_level > 1) : 
    print("Table count = " + str(len(myseater.tables)))
    print("Place count = " + str(myseater.n_places))


def generate_random_table() :
    coin = rng.randint(0, 1)
    if coin == 0 :
        divide = Divide.HORIZONTAL 
        x_length = rng.randint(2, 4)
        y_length = 2
    else :
        divide = Divide.VERTICAL
        x_length = 2
        y_length = rng.randint(2, 4)
    return Table(x_length, y_length, divide)


def check_boundary(x, y, table, myseater) :
    if (x == 0 or x + table.x_length == myseater.n_cols +1) and table.divide == Divide.VERTICAL : return False
    if (y == 0 or y + table.y_length == myseater.n_rows + 1) and table.divide == Divide.HORIZONTAL : return False
    if (x + table.x_length < myseater.n_cols) and (y + table.y_length < myseater.n_rows) : return True
    else : return False


def space_is_empty(x, y, table, myseater) : 
    for i in range(x, x + table.x_length + 1) :
        for j in range(y, y + table.y_length + 1) :
            # print("i: " + str(i) + " j: " + str(j))
            if myseater.classroom[i][j] != 0 : return False
            if myseater.classroom[i - 1][j] != 0 : return False
            if myseater.classroom[i][j - 1] != 0 : return False
            if myseater.classroom[i - i][j - 1] != 0 : return False
            if j + 1 != myseater.n_cols :
                if myseater.classroom[i][j + 1] != 0 : return False
                if myseater.classroom[i - 1][j + 1] != 0 : return False
            if i + 1 != myseater.n_rows :
                if myseater.classroom[i + 1][j] != 0 : return False


def do_random_assignment(myseater, args) :
    students = read_students(myseater, args.student_file)
    # global n_students
    myseater.n_students = len(students)
    # print("n_places: " + str(myseater.n_places) + " n_students: " + str(myseater.n_students))
    assert myseater.n_places == myseater.n_students
    for table in myseater.tables :
        for place in table.places :
            index = rng.randint(0, len(students) - 1)
            student = students[index]
            del students[index]
            place.student = student

