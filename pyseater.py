import turtle
import csv
import random as rng


class Desk:
    def __init__(self, x, y) :
        self.x = x
        self.y = y


class Pupil:
    def __init__(self, name) :
        self.name = name


# Do we want to watch the turtle do the drawing?
do_animation = False

# Declare collections
desks = []
pupils = []

# CSV containing pupil data
datafile="data/pupils.csv"

# Desk a.k.a. square size
desk_size = 90

# Classroom a.k.a. grid dimensions
n_cols = 5
n_rows = 4

# Compute pen start position on screen
start_x = -(desk_size * (0.5 * n_cols))
start_y = (desk_size * (0.5 * n_rows))


def read_pupils(filename) :
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            pupil = Pupil(row[0])
            pupils.append(Pupil(row[0]))


def get_pupil(index) :
    pupil = pupils[index]
    del pupils[index]
    return pupil


def draw_classroom(pen, size, n_cols, n_rows):
    pen.goto(start_x, start_y)
    pen.pendown()
    for _ in range(0, n_rows):
        for _ in range(0, n_cols):
            for _ in range(0, 4):
                pen.forward(size)
                pen.right(90)
            pen.forward(size)
        pen.penup()
        pen.backward(size * n_cols)
        pen.right(90)
        pen.forward(size)
        pen.left(90)
        pen.pendown()
    pen.penup()


def draw_desk(turtle, size, color, desk):
    pen.goto(start_x + (desk.x * size), start_y - (desk.y * size))
    pen.pendown()
    turtle.fillcolor(color)
    turtle.begin_fill()
    for _ in range(4):
        turtle.forward(size)
        turtle.right(90)
    turtle.end_fill()
    pen.penup()


def assign_desk(pupil, desk) :
    pen.goto(start_x + (desk.x * desk_size) + (0.15 * desk_size), start_y - (desk.y * desk_size) - (0.5 * desk_size))
    pen.pendown()
    pen.pencolor("black")
    pen.write(pupil.name)
    pen.penup()


def draw_table() :
    draw_desk(pen, desk_size, "lightblue", desks[0])
    draw_desk(pen, desk_size, "lightblue", desks[1])
    draw_desk(pen, desk_size, "lightblue", desks[2])
    draw_desk(pen, desk_size, "lightblue", desks[3])
    draw_desk(pen, desk_size, "lightblue", desks[4])
    draw_desk(pen, desk_size, "lightblue", desks[5])


def do_random_assignment() :
    read_pupils(datafile)
    n_pupils = len(pupils)
    assert n_pupils <= len(desks), "There are not enough desks."

    for i in range(0, n_pupils) :
        pupil = get_pupil(rng.randint(0, len(pupils) - 1))
        assign_desk(pupil, desks[i])


def click_handler(x, y) :
    screen.onclick(None)
    draw_table()
    do_random_assignment()
    screen.onclick(click_handler)


# Create some desks
desks.append(Desk(1,1))
desks.append(Desk(1,2))
desks.append(Desk(2,1))
desks.append(Desk(2,2))
desks.append(Desk(3,1))
desks.append(Desk(3,2))


screen = turtle.Screen()
screen.setup(width=800, height=600)
turtle.title("pyseater")

pen = turtle.Turtle(visible=do_animation)
if do_animation ==  True:
    pen.speed(10)
else :
    screen.tracer(False)

pen.penup()

draw_classroom(pen, desk_size, n_cols, n_rows)
draw_table()
screen.onclick(click_handler)
pen.hideturtle()
screen.mainloop()
