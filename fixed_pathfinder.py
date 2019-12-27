# Elias Mäkelä 22.12.2019
# Finds shortest path in matrix between two points using A* algorithm
import math
from tkinter import *

SIZE = 50
PIXELS = 8


class Pathfinder:
    def __init__(self):
        self.__window = Tk()
        self.__window.title("Pathfinder")
        self.__white = PhotoImage(file="white.gif")
        self.__black = PhotoImage(file="black.gif")
        self.__green = PhotoImage(file="green.gif")
        self.__red = PhotoImage(file="red.gif")
        self.__grid = []
        self.__button = []
        self.__click = "normal"

        self.goal = None
        self.start = None
        self.path = None

        for i in range(SIZE):
            self.__row = []
            self.__grid_row = []
            for j in range(SIZE):
                new_button = Button(self.__window, borderwidth=0)
                new_button.config(image=self.__white)
                new_button.bind('<Button-1>', self.press_button)
                new_button.bind("<B1-Motion>", self.press_button)
                new_button.location = [j, i]
                new_button.grid(row=i, column=j)
                grid = Nodes(None, [j, i], "normal")
                self.__row.append(new_button)
                self.__grid_row.append(grid)
            self.__button.append(self.__row)
            self.__grid.append(self.__grid_row)

        self.__start_button = Button(self.__window, text="set starting point", command=self.start_command)
        self.__start_button.grid(row=0, column=SIZE, rowspan=4, sticky=N+E+W)
        self.__goal_button = Button(self.__window, text="set goal", command=self.goal_command)
        self.__goal_button.grid(row=4, column=SIZE, rowspan=4, sticky=N+E+W)

        self.__test_button = Button(self.__window, text="COCK", command=self.test)
        self.__test_button.grid(row=10, column=SIZE, rowspan=4, sticky=N+E+W)

        self.__window.mainloop()

    def press_button(self, event):
        button = event.widget
        start_x, start_y = button.location
        x = start_x + math.floor(event.x/PIXELS)
        y = start_y + math.floor(event.y/PIXELS)
        try:
            if self.__click == "normal":
                self.__button[y][x].config(image=self.__black)
                self.__grid[y][x].mode = "wall"
            elif self.__click == "start" and self.__grid[y][x].mode == "normal":
                self.__button[y][x].config(image=self.__green)
                self.__click = "normal"
                self.__grid[y][x].mode = "start"
                if self.start:
                    self.__button[self.start.location[1]][self.start.location[0]].config(image=self.__white)
                    self.start.mode = "normal"
                self.start = self.__grid[y][x]

            elif self.__click == "goal" and self.__grid[y][x].mode == "normal":
                self.__button[y][x].config(image=self.__red)
                self.__click = "normal"
                self.__grid[y][x].mode = "goal"
                if self.goal:
                    self.__button[self.goal.location[1]][self.goal.location[0]].config(image=self.__white)
                    self.goal.mode = "normal"
                self.goal = self.__grid[y][x]
        except IndexError:
            pass

    def distance_to_goal(self, start):
        return math.sqrt((self.goal.location[0] - start[0]) ** 2 + (self.goal.location[1] - start[1]) ** 2)

    def start_command(self):
        self.__click = "start"

    def goal_command(self):
        self.__click = "goal"

    def test(self):
        pass

    def path(self):
        if self.goal and self.start:
            if self.a_star(self.start, self.goal):
                self.create_path()
            else:
                print("No path possible")
        else:
            print("set start and goal")

    def create_path(self):
        pass

    def a_star(self, start, goal):
        # TODO: find a way to calculate steps
        start.h = self.distance_to_goal(start)
        start.g = 0
        start.f = start.h + start.g
        open_list = [start]
        closed_list = []
        steps = 0
        while len(open_list) != 0:
            steps += 1
            smallest_f = open_list[0].f
            for i in open_list:
                if i.f < smallest_f:
                    smallest_f = i
            closed_list.append(smallest_f)
            open_list.remove(smallest_f)

            for i in range(3):
                for j in range(3):
                    x = closed_list[-1][0] - 1 + i
                    y = closed_list[-1][1] - 1 + j
                    try:
                        child = self.__grid[y][x]
                        if self.__grid[y][x].mode == "normal" and child != closed_list:
                            open_list.append(child)
                            child.parent = closed_list[-1]
                            child.h = self.distance_to_goal(child.location)
                            child.g = steps
                            child.f = child.h + child.g
                        elif child in closed_list and child.g > steps:
                            child.parent = closed_list[-1]
                            child.h = self.distance_to_goal(child.location)
                            child.g = steps
                            child.f = child.h + child.g
                    except IndexError:
                        pass
            if closed_list[-1] == goal:
                self.path = closed_list
                return True
        return False


class Nodes:
    def __init__(self, parent=None, location=None, mode=None):
        self.g = 0
        self.h = 0
        self.f = 0
        self.location = location
        self.parent = parent
        self.mode = mode


def main():
    Pathfinder()


main()
