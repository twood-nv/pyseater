import turtle
import csv
import random as rng


class Desk:
    def __init__(self, x, y) :
        self.x = x
        self.y = y
        self.colour = "lightblue"


class Pupil:
    def __init__(self, name, gender) :
        self.name = name
        self.gender = gender


# Do we want to watch the turtle do the drawing?
# It's really slow, probably remove this soon ...
do_animation = False

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
    for _ in range(0, n_rows):
        for _ in range(0, n_cols):
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


def assign_desk(pupil, desk) :
    pen.goto(start_x + (desk.x * desk_size) + (0.10 * desk_size), start_y - (desk.y * desk_size) - (0.5 * desk_size))
    pen.pendown()
    pen.pencolor("black")
    pen.write(pupil.name)
    pen.penup()


def draw_desk(desk):
    turtle.penup()
    turtle.goto(start_x + (desk.x * desk_size), start_y - (desk.y * desk_size))
    turtle.pendown()
    turtle.fillcolor(desk.colour)
    turtle.begin_fill()
    for _ in range(4):
        turtle.forward(desk_size)
        turtle.right(90)
    turtle.end_fill()
    turtle.penup()


def draw_table(x_start, x_length, y_start, y_length) :
    for i in range(x_start, x_start + x_length) :
        for j in range(y_start, y_start + y_length) :
            desk = Desk(i, j)
            desks.append(desk)
            draw_desk(desk)


def do_random_assignment() :
    read_pupils(datafile)
    n_pupils = len(pupils)
    assert n_pupils <= len(desks), "There are not enough desks."

    for i in range(0, n_pupils) :
        pupil = get_pupil(rng.randint(0, len(pupils) - 1))
        if pupil.gender == "M" :
            desks[i].colour = "lightblue"
        else :
            desks[i].colour = "lightpink"
        draw_desk(desks[i])
        assign_desk(pupil, desks[i])


def click_handler(x, y) :
    screen.onclick(None)
    do_random_assignment()
    screen.onclick(click_handler)


screen = turtle.Screen()
screen.setup(width=800, height=600)
turtle.title("pyseater")

pen = turtle.Turtle(visible=do_animation)
if do_animation ==  True:
    pen.speed(10)
else :
    screen.tracer(False)

pen.penup()

draw_classroom(n_cols, n_rows)
draw_table(0, 2, 2, 2)
draw_table(4, 2, 2, 2)
draw_table(0, 2, 6, 2)
draw_table(4, 2, 6, 3)
draw_table(8, 2, 6, 2)

screen.onclick(click_handler)
pen.hideturtle()
screen.mainloop()
