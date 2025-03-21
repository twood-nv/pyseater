import turtle
import csv
import time
import argparse
import random as rng
from enum import Enum


Divide = Enum('String', [('HORIZONTAL', 0), ('VERTICAL', 1)])
Orientate = Enum('String', [('NORTH', 0), ('EAST', 1), ('SOUTH', 2), ('WEST', 3)])


class Table :
    def __init__(self, x_length, y_length, divide) :
        self.x_length = x_length
        self.y_length = y_length
        self.divide = divide
        if divide == Divide.HORIZONTAL :
            assert(y_length == 2)
        else :
            assert(x_length == 2)
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
    def assign_student(self, student) :
        self.student = student


class Student :
    def __init__(self) :
        self.attributes = {}
    def set_attribute(self, key, value) :
        self.attributes[key] = value
    def get_attribute(self, key) :
        return self.attributes[key]
    

class Rule:
    def __init__(self, attribute, boolean) :
        self.attribute = attribute
        self.boolean = boolean



tables = []
n_places = 0
n_students = 0


def str2bool(str) :
  return str.lower() in ("t", "true", "1")


def parse_rule(rule_string):
    items = rule_string.split('=')
    key = items[0].strip() 
    if len(items) > 1:
        value = str2bool('='.join(items[1:]))
    return (key, value)


def parse_rules(rule_strings) :
    rules = []
    if rule_strings:
        for rule_string in rule_strings:
            attribute, boolean = parse_rule(rule_string)
            rules.append(Rule(attribute, boolean))
    return rules


def read_students() :
    with open(args.student_file, 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        keys = next(reader)
        students = []
        for row in reader :
            s = Student()
            for i in range(len(row)) :
                s.set_attribute(keys[i], row[i])
            students.append(s)
    global n_students
    n_students = len(students)
    return students


def draw_classroom(n_cols, n_rows):
    turtle.penup()
    turtle.goto(START_X, START_Y)
    turtle.pendown()
    for row in range(n_rows):
        for col in range(n_cols):
            for _ in range(4):
                turtle.forward(args.place_size)
                turtle.right(90)
            turtle.forward(args.place_size)
        turtle.penup()
        turtle.backward(args.place_size * n_cols)
        turtle.right(90)
        turtle.forward(args.place_size)
        turtle.left(90)
        turtle.pendown()
    turtle.penup()


def assign_place(place) :
    turtle.goto(START_X + (place.x * args.place_size) + (0.2 * args.place_size), START_Y - (place.y * args.place_size) - (0.75 * args.place_size))
    turtle.pendown()
    turtle.pencolor("black")
    turtle.write(str(place.student.get_attribute("name")) + "\n" + str(place.student.get_attribute("language")) + "\n" + str(place.student.get_attribute("game")))
    turtle.penup()


def draw_place(place):
    turtle.penup()
    turtle.goto(START_X + (place.x * args.place_size), START_Y - (place.y * args.place_size))
    turtle.pendown()
    if place.student == 0 :
        turtle.fillcolor("lightblue")
    elif place.student.get_attribute("gender") == "M" :
        turtle.fillcolor("lightblue")
    else :
        turtle.fillcolor("lightpink")
    turtle.begin_fill()
    for side in range(4):
        if side == place.orientate.value :
            turtle.forward(0.5 * args.place_size)
            turtle.right(60)
            turtle.forward(0.2 * args.place_size)
            turtle.right(120)
            turtle.forward(0.2 * args.place_size)
            turtle.right(120)
            turtle.forward(0.2 * args.place_size)
            turtle.right(60)
            turtle.forward(0.5 * args.place_size)
        else :
            turtle.forward(args.place_size)
        turtle.right(90)
    turtle.end_fill()
    turtle.penup()
    if place.student != 0 :
        assign_place(place)


def draw_floorplan() :
    for x in range(args.n_rows) : 
        for y in range(args.n_cols) :
            if classroom[x][y] != 0 :
                draw_place(classroom[x][y])


def add_table(x_start, y_start, table) :
    tables.append(table)
    for x in range(x_start, x_start + table.x_length) :
        for y in range(y_start, y_start + table.y_length) :
            if table.divide == Divide.HORIZONTAL :
                orientate = (Orientate.SOUTH if y == y_start  else Orientate.NORTH)
            else :
                orientate = (Orientate.EAST if x == x_start  else Orientate.WEST)
            place = Place(x, y, orientate)
            global n_places
            n_places = n_places + 1
            classroom[x][y] = place
            table.add_place(place)


def do_random_assignment() :
    students = read_students()
    assert n_places == n_students
    for table in tables :
        for place in table.places :
            index = rng.randint(0, len(students) - 1)
            student = students[index]
            del students[index]
            place.student = student


def swap_students(place_a, place_b) :
    student_temp = place_a.student
    place_a.assign_student(place_b.student)
    place_b.assign_student(student_temp)
    if args.show == True :
        draw_place(place_a)
        draw_place(place_b)


def student_swap_table(table_a, table_b) :
    place_a = table_a.places[rng.randint(0, (table_a.x_length * table_a.y_length) - 1)]
    place_b = table_b.places[rng.randint(0, (table_b.x_length * table_b.y_length) - 1)]
    swap_students(place_a, place_b)


def student_swap_table_random(tables) :
    for i in range(0, len(tables)) :
        a = i
        b = i + 1 if i != len(tables) - 1 else 0
        student_swap_table(tables[a], tables[b])


def appy_rules(rules, student_a, student_b) :
    for rule in rules :        
        if rule.boolean != (student_a.get_attribute(rule.attribute) == student_b.get_attribute(rule.attribute)) :
            return False


def compute_table_fitness(rules, table) :
    table.fitness = 0
    for place in table.places :
        adjacent = find_adjacent(place)
        for rule in rules :
            if rule.boolean == (place.student.get_attribute(rule.attribute) == adjacent.student.get_attribute(rule.attribute)) :
                table.fitness = table.fitness + 1


def find_adjacent(place) :
    if place.orientate in (Orientate.NORTH, Orientate.SOUTH) :
        if (place.x - 1 != -1) and (classroom[place.x -1][place.y] != 0) :
            return classroom[place.x - 1][place.y]
        elif (place.x + 1 != args.n_cols) and (classroom[place.x + 1][place.y] != 0) :
            return classroom[place.x + 1][place.y]
    elif place.orientate in (Orientate.EAST, Orientate.WEST) :
        if (place.y - 1 != -1) and (classroom[place.x][place.y - 1] != 0) :
            return classroom[place.x][place.y - 1]
        elif (place.y + 1 != args.n_cols) and (classroom[place.x][place.y + 1] != 0) :
            return classroom[place.x][place.y + 1]


def solve(rules) :
    iterations = 0
    max_fitness = n_places * len(rules) 
    start_time = time.time()
    while iterations < args.max_iterations :
        # apply rules and do swaps
        for table in tables :
            table.fitness = 0
            for place in table.places :
                adjacent = find_adjacent(place)
                if appy_rules(rules, place.student, adjacent.student) == False :
                    if (table.x_length > 2) or (table.y_length > 2) :
                        coin = rng.randint(0, 2)
                        if coin == 0 :
                            student_swap_opposite(place)
                        elif coin == 1 :
                            student_swap_adjacent(place)
                        else :
                            student_swap_random(table, place)
                    else :
                        student_swap_opposite(place)
                    if args.show == True :
                        screen.update()
                        time.sleep(args.frame_delay)
                    break
        # compute table fitness
        for table in tables :
            compute_table_fitness(rules, table)

        # find unfit tables 
        unfit = []
        solution_fitness = 0
        for table in tables :
            solution_fitness = solution_fitness + table.fitness
            if table.fitness != (len(table.places) * len(rules)) :                
                unfit.append(table)
        if args.show == True :
            solution_fitness = float(solution_fitness) / max_fitness
            print(str(iterations) + ": Solution fitness = " + "{:.2%}".format(solution_fitness))

        if solution_fitness >= args.target_fitness :
            exec_time = (time.time() - start_time)
            print("Solved after " + str(iterations) + " iterations, in " +str(round(exec_time, 2)) + " seconds. Throughput: " + str(round(iterations / exec_time, 2)))
            solution_fitness = float(solution_fitness) / float(max_fitness)
            print(str(iterations) + ": Solution fitness = " + "{:.2%}".format(solution_fitness))
            screen.update()
            break
        else :
            if iterations % args.migration_interval == 0 :
                student_swap_table_random(tables)

        iterations = iterations + 1
        if (iterations % 50 == 0) and (len(tables) == 1) :
            print("No solution after " + str(iterations) + " shuffling table.")
            for i in range(0, len(unfit)) :
                rng.shuffle(unfit[i].desks)
    if iterations == args.max_iterations :
        print("No solution found after max ietarions: " + str(args.max_iterations))

def student_swap_random(table, place) :
    index = rng.randint(0, len(table.places) - 1)
    swap_students(place, table.places[index])


def student_swap_opposite(desk) :
    if desk.orientate == Orientate.NORTH :
        swap_students(desk, classroom[desk.x][desk.y - 1])
    elif desk.orientate == Orientate.EAST : 
        swap_students(desk, classroom[desk.x + 1][desk.y])
    elif desk.orientate == Orientate.SOUTH : 
        swap_students(desk, classroom[desk.x][desk.y + 1])
    elif desk.orientate == Orientate.WEST : 
        swap_students(desk, classroom[desk.x - 1][desk.y])


def student_swap_adjacent(desk) :
    if desk.orientate in (Orientate.NORTH, Orientate.SOUTH) :
        if (desk.x - 1 != -1) and (classroom[desk.x -1][desk.y] != 0) :
            swap_students(desk, classroom[desk.x -1][desk.y]) 
        elif (desk.x + 1 != args.n_cols) and (classroom[desk.x + 1][desk.y] != 0) :
            swap_students(desk, classroom[desk.x + 1][desk.y])
    elif desk.orientate in (Orientate.EAST, Orientate.WEST) :
        if (desk.y - 1 != -1) and (classroom[desk.x][desk.y - 1] != 0) :
            swap_students(desk, classroom[desk.x][desk.y - 1])
        elif (desk.y + 1 != args.n_rows) and (classroom[desk.x][desk.y + 1] != 0) :
            swap_students(desk, classroom[desk.x][desk.y + 1])


def click_handler(x, y) :
    do_random_assignment()
    draw_floorplan()
    screen.update()
    solve(rules)
    draw_floorplan()
    screen.update()
    screen.onclick(click_handler)


parser = argparse.ArgumentParser(description="pyseater - generate classroom seating plans according to some rules")
parser.add_argument("--rules", metavar="ATTRIBUTE=BOOL", nargs='+', help="specify a list of rules as key=value pairs, e.g. language=false.")
parser.add_argument("--seed", help="provide a random seed to get deterministic behaviour", type=int)
parser.add_argument("--show", help="show the evolution of the seating plan, can be very slow", action='store_true')
parser.add_argument("--frame_delay", help="delay after each refresh, only relevant when --show is set", default=0.05, type=float)
parser.add_argument("--place_size", help="size in pixels of a seating place, i.e. one square on the grid", default=70, type=int)
parser.add_argument("--n_rows", help="the number of rows in the floorplan", default=10, type=int)
parser.add_argument("--n_cols", help="the number of columns in the floorplan", default=10, type=int)
parser.add_argument("--max_iterations", help="maximum solver iterations before giving up", default=1000000, type=int)
parser.add_argument("--target_fitness", help="target solution fitness as a percentage, e.g 95", default=100, type=float)
parser.add_argument("--student_file", help="csv file containing student data", default="data/students.csv")
parser.add_argument("--migration_interval", help="number of iterations between random student table migrations", default=5, type=int)
parser.add_argument("--canvas_width", help="width of the display canvas in pixels", default=800, type=int)
parser.add_argument("--canvas_height", help="height of the display canvas in pixels", default=800, type=int)
parser.add_argument("--batch", help="generate <batch size> seating plans, ", default=0, type=int)


args = parser.parse_args()
rules = parse_rules(args.rules)

if len(rules) == 0 :
    rules.append(Rule("gender", False))
    rules.append(Rule("language", False))
    rules.append(Rule("game", False))

print("Applying rules:")
for rule in rules :
    print(str(rule.attribute) + " = " + str(rule.boolean))

if args.seed :
    print("Seed will be set to " + str(args.seed))
    rng.seed(args.seed)

START_X = -(args.place_size * (0.5 * args.n_cols))
START_Y = (args.place_size * (0.5 * args.n_rows))

classroom = [[0 for i in range(args.n_cols)] for j in range(args.n_rows)]

add_table(0, 2, Table(2, 2, Divide.HORIZONTAL))
add_table(4, 2, Table(2, 2, Divide.VERTICAL))
add_table(8, 6, Table(2, 2, Divide.HORIZONTAL))
add_table(4, 6, Table(2, 3, Divide.VERTICAL))
add_table(0, 6, Table(2, 2, Divide.HORIZONTAL))

if args.target_fitness :
    print("Target fitness set to " + str(args.target_fitness) + "%")
args.target_fitness = (args.target_fitness / 100) * (len(rules) * n_places)

screen = turtle.Screen()
screen.setup(width=args.canvas_width, height=args.canvas_height)
turtle.title("pyseater")
turtle.Turtle(visible=False)
screen.tracer(False)
turtle.penup()
draw_classroom(args.n_cols, args.n_rows)
draw_floorplan()

if args.batch != 0 :
    for _ in range(args.batch) :
        click_handler(0, 0)

else:
    screen.onclick(click_handler)
    turtle.hideturtle()
    screen.mainloop()