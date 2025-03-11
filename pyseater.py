import turtle

def draw_grid(turtle, size, num_squares):
    for _ in range(num_squares):
        for _ in range(num_squares):
            for _ in range(4):
                turtle.forward(size)
                turtle.right(90)
            turtle.forward(size)
        turtle.penup()
        turtle.backward(size * num_squares)
        turtle.right(90)
        turtle.forward(size)
        turtle.left(90)
        turtle.pendown()

def fill_square(turtle, size, color):
    turtle.fillcolor(color)
    turtle.begin_fill()
    for _ in range(4):
        turtle.forward(size)
        turtle.right(90)
    turtle.end_fill()

def label_square(turtle) :
    turtle.pencolor("yellow")
    turtle.write("Horatio")


screen = turtle.Screen()
screen.setup(width=800, height=600)
turtle.title("pyseater")
pen = turtle.Turtle()


start_x = -130
start_y = 130

pen.speed(10)  # Set speed to fastest
pen.penup()
pen.goto(start_x, start_y)  # Adjust starting position if needed
pen.pendown()

grid_size = 60  # Size of each square
num_squares = 3
draw_grid(pen, grid_size, num_squares)

# Example of filling squares:
pen.penup()
pen.goto(start_x, start_y)  # Reset position to the beginning of the grid
pen.pendown()

for row in range(num_squares):
    for col in range(num_squares):
        if (row + col) % 2 == 0:  # Fill squares in a checkerboard pattern
            fill_square(pen, grid_size, "blue")
        else :
            fill_square(pen, grid_size, "red")
        pen.forward(grid_size)
    pen.penup()
    pen.backward(grid_size * num_squares)
    pen.right(90)
    pen.forward(grid_size)
    pen.left(90)
    pen.pendown()


# Try writing in the squares
pen.penup()
# pen.goto(-140, -175)  # Reset position to the beginning of the grid
pen.goto(start_x + 10, start_y - 25)


for row in range(num_squares):
    for col in range(num_squares):
        if (row + col) % 2 == 0:  # Fill squares in a checkerboard pattern
            pen.pendown()
            label_square(pen)
            pen.penup()
        pen.penup()
        pen.forward(grid_size)
    pen.penup()
    pen.backward(grid_size * num_squares)
    pen.right(90)
    pen.forward(grid_size)
    pen.left(90)
    pen.pendown()

screen.mainloop()
