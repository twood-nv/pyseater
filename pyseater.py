#!/usr/bin/python3
import turtle
import csv
import time
import random as rng
from enum import Enum


Divide = Enum('String', [('HORIZONTAL', 0), ('VERTICAL', 1)])
Orientate = Enum('String', [('NORTH', 0), ('EAST', 1), ('SOUTH', 2), ('WEST', 3)])


class Pupil:
    def __init__(self, name, gender) :
        self.name = name
        self.gender = gender


class Desk:
    def __init__(self, x, y, orientate) :
        self.x = x
        self.y = y
        self.orientate = orientate
        self.pupil = Pupil("","M")

    def assign_pupil(self, pupil) :
        self.pupil = pupil


class Table :
    def __init__(self, x_length, y_length, divide) :
        self.x_length = x_length
        self.y_length = y_length
        self.divide = divide
        if divide == Divide.HORIZONTAL :
            assert(y_length == 2)
        else :
            assert(x_length == 2)
        self.desks = []
        self.fitness = 0

    def add_desk(self, desk) :
        self.desks.append(desk)


# Declare collections
tables = []

# Desk a.k.a. square size
desk_size = 50

# Classroom a.k.a. grid dimensions
n_cols = 10
n_rows = 10

n_desks = 0
n_pupils = 0

classroom = [[0 for i in range(n_cols)] for j in range(n_rows)]

# Compute pen start position on screen
start_x = -(desk_size * (0.5 * n_cols))
start_y = (desk_size * (0.5 * n_rows))


def read_pupils() :
    with open("data/pupils.csv", 'r') as file:
        reader = csv.reader(file)
        pupils = []
        for row in reader :
            pupils.append(Pupil(row[0].strip(), row[1].strip()))
    global n_pupils
    n_pupils = len(pupils)
    return pupils


def draw_classroom(n_cols, n_rows):
    turtle.penup()
    turtle.goto(start_x, start_y)
    turtle.pendown()
    for row in range(0, n_rows):
        for col in range(0, n_cols):
            for _ in range(0, 4):
                turtle.forward(desk_size)
                turtle.right(90)
            turtle.forward(desk_size)
        turtle.penup()
        turtle.backward(desk_size * n_cols)
        turtle.right(90)
        turtle.forward(desk_size)
        turtle.left(90)
        turtle.pendown()
    turtle.penup()


def assign_desk(desk) :
    turtle.goto(start_x + (desk.x * desk_size) + (0.10 * desk_size), start_y - (desk.y * desk_size) - (0.5 * desk_size))
    turtle.pendown()
    turtle.pencolor("black")
    turtle.write(desk.pupil.name)
    turtle.penup()


def draw_desk(desk):
    turtle.penup()
    turtle.goto(start_x + (desk.x * desk_size), start_y - (desk.y * desk_size))
    turtle.pendown()
    if desk.pupil.gender == "M" :
        turtle.fillcolor("lightblue")
    else :
        turtle.fillcolor("lightpink")
    turtle.begin_fill()
    for side in range(4):
        if side == desk.orientate.value :
            turtle.forward(0.5 * desk_size)
            turtle.right(60)
            turtle.forward(0.2 * desk_size)
            turtle.right(120)
            turtle.forward(0.2 * desk_size)
            turtle.right(120)
            turtle.forward(0.2 * desk_size)
            turtle.right(60)
            turtle.forward(0.5 * desk_size)
        else :
            turtle.forward(desk_size)
        turtle.right(90)
    turtle.end_fill()
    turtle.penup()
    if desk.pupil != 0 :
        assign_desk(desk)


def draw_floorplan() :
    for x in range(0, n_rows) : 
        for y in range(0, n_cols) :
            if classroom[x][y] != 0 :
                draw_desk(classroom[x][y])


def add_table(x_start, y_start, table) :
    tables.append(table)
    for x in range(x_start, x_start + table.x_length) :
        for y in range(y_start, y_start + table.y_length) :
            if table.divide == Divide.HORIZONTAL :
                orientate = (Orientate.SOUTH if y == y_start  else Orientate.NORTH)
            else :
                orientate = (Orientate.EAST if x == x_start  else Orientate.WEST)
            desk = Desk(x, y, orientate)
            global n_desks
            n_desks = n_desks + 1
            classroom[x][y] = desk
            table.add_desk(desk)


def do_random_assignment() :
    pupils = read_pupils()
    assert n_pupils <= n_desks, "There are not enough desks."
    for t in range(0, len(tables)) :
        table = tables[t]
        for d in range(0, len(table.desks)) :
            desk = table.desks[d]
            index = rng.randint(0, len(pupils) - 1)
            pupil = pupils[index]
            del pupils[index]
            desk.pupil = pupil
            draw_desk(desk)


def swap_pupils(desk_a, desk_b) :
    pupil_temp = desk_a.pupil
    desk_a.assign_pupil(desk_b.pupil)
    desk_b.assign_pupil(pupil_temp)
    draw_desk(desk_a)
    draw_desk(desk_b)


def pupil_swap_table(table_a, table_b) :
    desk_a = table_a.desks[rng.randint(0, (table_a.x_length * table_a.y_length) - 1)]
    desk_b = table_b.desks[rng.randint(0, (table_b.x_length * table_b.y_length) - 1)]
    swap_pupils(desk_a, desk_b)


def pupil_swap_table_random(tables) :
    for i in range(0, len(tables)) :
        a = i
        b = i + 1 if i != len(tables) - 1 else 0
        pupil_swap_table(tables[a], tables[b])


def compare_pupil_attribute(a, b) :
    return True if a == b else False


def find_adjacent(desk) :
    if desk.orientate in (Orientate.NORTH, Orientate.SOUTH) :
        if (desk.x - 1 != -1) and (classroom[desk.x -1][desk.y] != 0) :
            return classroom[desk.x - 1][desk.y]
        elif (desk.x + 1 != n_cols) and (classroom[desk.x + 1][desk.y] != 0) :
            return classroom[desk.x + 1][desk.y]
    elif desk.orientate in (Orientate.EAST, Orientate.WEST) :
        if (desk.y - 1 != -1) and (classroom[desk.x][desk.y - 1] != 0) :
            return classroom[desk.x][desk.y - 1]
        elif (desk.y + 1 != n_rows) and (classroom[desk.x][desk.y + 1] != 0) :
            return classroom[desk.x][desk.y + 1]


def solve() :
    iterations = 0
    wait  = 0.1
    show_evolution = False
    start_time = time.time()
    while True :
        for i in range(0, len(tables)) :
            table = tables[i]
            table.fitness = 0
            for j in range(0, len(table.desks)) :
                desk = table.desks[j]
                adjacent = find_adjacent(desk)
                # for each desk test rule, do swaps if necessary
                if compare_pupil_attribute(desk.pupil.gender, adjacent.pupil.gender) == True :
                    if (table.x_length > 2) or (table.y_length > 2) :
                        coin = rng.randint(0, 2)
                        if coin == 0 :
                            pupil_swap_opposite(desk)
                        elif coin == 1 :
                            pupil_swap_adjacent(desk)
                        else :
                            pupil_swap_random(table, desk)
                    else :
                        pupil_swap_opposite(desk)

                    if show_evolution == True :
                        screen.update()
                        time.sleep(wait)
                    break            
            # for each table compute fitness
            for j in range(0, len(table.desks)) :
                desk = table.desks[j]
                adjacent = find_adjacent(desk)
                same = compare_pupil_attribute(desk.pupil.gender, adjacent.pupil.gender)
                if same == False :
                    table.fitness = table.fitness + 1
        # find unfit tables 
        unfit = []
        for i in range(0, len(tables)) :
            # health = float(table.fitness) / float(len(table.desks)) * 100.
            # print("Table " + str(i) + " fitness = %.1f" % health)
            if tables[i].fitness != len(tables[i].desks) :                
                unfit.append(tables[i])

        if len(unfit) == 0 :
            exec_time = (time.time() - start_time)
            print("Solved after " + str(iterations) + " iterations, in " +str(round(exec_time, 2)) + " seconds. Throughput: " + str(round(iterations / exec_time, 2)))
            screen.update()
            break
        else :
            if iterations % 5 == 0 :
                pupil_swap_table_random(tables)

        iterations = iterations + 1
        if (iterations % 50 == 0) and (len(tables) == 1) :
            print("No solution after " + str(iterations) + " shuffling table.")
            for i in range(0, len(unfit)) :
                rng.shuffle(unfit[i].desks)


def pupil_swap_random(table, desk) :
    index = rng.randint(0, len(table.desks) - 1)
    swap_pupils(desk, table.desks[index])


def pupil_swap_opposite(desk) :
    match desk.orientate :
        case Orientate.NORTH :
            swap_pupils(desk, classroom[desk.x][desk.y - 1])
        case Orientate.EAST : 
            swap_pupils(desk, classroom[desk.x + 1][desk.y])
        case Orientate.SOUTH : 
            swap_pupils(desk, classroom[desk.x][desk.y + 1])
        case Orientate.WEST : 
            swap_pupils(desk, classroom[desk.x - 1][desk.y])


def pupil_swap_adjacent(desk) :
    if desk.orientate in (Orientate.NORTH, Orientate.SOUTH) :
        if (desk.x - 1 != -1) and (classroom[desk.x -1][desk.y] != 0) :
            swap_pupils(desk, classroom[desk.x -1][desk.y]) 
        elif (desk.x + 1 != n_cols) and (classroom[desk.x + 1][desk.y] != 0) :
            swap_pupils(desk, classroom[desk.x + 1][desk.y])
    elif desk.orientate in (Orientate.EAST, Orientate.WEST) :
        if (desk.y - 1 != -1) and (classroom[desk.x][desk.y - 1] != 0) :
            swap_pupils(desk, classroom[desk.x][desk.y - 1])
        elif (desk.y + 1 != n_rows) and (classroom[desk.x][desk.y + 1] != 0) :
            swap_pupils(desk, classroom[desk.x][desk.y + 1])


def click_handler(x, y) :
    do_random_assignment()
    draw_floorplan()
    screen.update()
    solve()
    draw_floorplan()
    screen.update()
    screen.onclick(click_handler)


add_table(0, 2, Table(2, 2, Divide.HORIZONTAL))
add_table(4, 2, Table(2, 2, Divide.VERTICAL))
add_table(8, 6, Table(2, 2, Divide.HORIZONTAL))
add_table(4, 6, Table(2, 3, Divide.VERTICAL))
add_table(0, 6, Table(2, 2, Divide.HORIZONTAL))

screen = turtle.Screen()
screen.setup(width=800, height=600)
turtle.title("pyseater")
turtle.Turtle(visible=False)
screen.tracer(False)
turtle.penup()
draw_classroom(n_cols, n_rows)
draw_floorplan()
screen.onclick(click_handler)
turtle.hideturtle()
screen.mainloop()