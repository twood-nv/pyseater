from enum import Enum
import csv

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


class Rule:
    def __init__(self, attribute, boolean) :
        self.attribute = attribute
        self.boolean = boolean
        

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

    