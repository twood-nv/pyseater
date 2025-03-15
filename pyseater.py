#!/usr/bin/python3

import turtle
import csv
import random as rng
from enum import Enum

# tables have a dividing line over which children face each other
Divide = Enum('String', [('HORIZONTAL', 0), ('VERTICAL', 1)])

# desks have an orientation depending on diviision of the table and their position
Orientate = Enum('String', [('NORTH', 0), ('EAST', 1), ('SOUTH', 2), ('WEST', 3)])


class Desk:
    def __init__(self, x, y, orientate) :
        self.x = x
        self.y = y
        self.colour = "lightblue"
        self.orientate = orientate
        self.pupil = 0


class Table :
    def __init__(self, x_length, y_length, divide) :
        self.x_length = x_length
        self.y_length = y_length
        self.divide = divide
        if divide == Divide.HORIZONTAL :
            assert(y_length == 2)
        else :
            assert(x_length == 2)


class Pupil:
    def __init__(self, name, gender) :
        self.name = name
        self.gender = gender


# Declare collections
desks = []
pupils = []

# CSV containing pupil data
datafile="data/pupils.csv"

# Desk a.k.a. square size
desk_size = 50

# Classroom a.k.a. grid dimensions
n_cols = 10
n_rows = 10

# 2D array representing classroom 
floorplan = [[0 for i in range(n_cols)] for j in range(n_rows)]

# Compute pen start position on screen
start_x = -(desk_size * (0.5 * n_cols))
start_y = (desk_size * (0.5 * n_rows))


def read_pupils(filename) :
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader :
            pupils.append(Pupil(row[0].strip(), row[1].strip()))


def get_pupil(index) :
    pupil = pupils[index]
    del pupils[index]
    return pupil


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
    pen.goto(start_x + (desk.x * desk_size) + (0.10 * desk_size), start_y - (desk.y * desk_size) - (0.5 * desk_size))
    pen.pendown()
    pen.pencolor("black")
    pen.write(desk.pupil.name)
    pen.penup()


def draw_desk(desk):
    turtle.penup()
    turtle.goto(start_x + (desk.x * desk_size), start_y - (desk.y * desk_size))
    turtle.pendown()
    turtle.fillcolor(desk.colour)
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


def add_table(x_start, y_start, table) :
    for x in range(x_start, x_start + table.x_length) :
        for y in range(y_start, y_start + table.y_length) :

            if table.divide == Divide.HORIZONTAL :
                orientate = (Orientate.SOUTH if y == y_start  else Orientate.NORTH)

            else :
                orientate = (Orientate.EAST if x == x_start  else Orientate.WEST)

            desk = Desk(x, y, orientate)            
            floorplan[x][y] = desk
            desks.append(desk)


def do_random_assignment() :
    read_pupils(datafile)
    n_pupils = len(pupils)
    assert n_pupils <= len(desks), "There are not enough desks."
    for i in range(0, n_pupils) :
        pupil = get_pupil(rng.randint(0, len(pupils) - 1))
        desks[i].pupil = pupil
        if pupil.gender == "M" :
            desks[i].colour = "lightblue"
        else :
            desks[i].colour = "lightpink"
        draw_desk(desks[i])


def click_handler(x, y) :
    screen.onclick(None)
    do_random_assignment()
    screen.onclick(click_handler)


add_table(0, 2, Table(2, 2, Divide.HORIZONTAL))
add_table(4, 2, Table(2, 2, Divide.VERTICAL))
add_table(0, 6, Table(2, 2, Divide.HORIZONTAL))
add_table(4, 6, Table(2, 3, Divide.VERTICAL))
add_table(8, 6, Table(2, 2, Divide.HORIZONTAL))

# for i in range(0, n_rows) : 
#     for j in range(0, n_cols) :
#         if floorplan[i][j] == 0 :
#             print(str(i) + ":" + str(j) + " is empty")
#         else :
#             print(str(i) + ":" + str(j) + " has a " + str(floorplan[i][j].orientate) + " desk.")

# Render
screen = turtle.Screen()
screen.setup(width=800, height=600)
turtle.title("pyseater")

pen = turtle.Turtle(visible=False)
screen.tracer(False)
pen.penup()

draw_classroom(n_cols, n_rows)

for x in range(0, n_rows) : 
    for y in range(0, n_cols) :
        if floorplan[x][y] != 0 :
            draw_desk(floorplan[x][y])

screen.onclick(click_handler)
pen.hideturtle()
screen.mainloop()