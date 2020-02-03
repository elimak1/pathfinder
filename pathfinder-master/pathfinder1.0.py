# Elias Mäkelä 22.12.2019
# Finds shortest path in matrix between two points using A* algorithm
import math
from tkinter import *
# TODO: make useless curves straight
SIZE = 50
# picture side is 6 and frame 2 pixels
PIXELS = 8


class Pathfinder:
    def __init__(self):
        self.__window = Tk()
        self.__window.title("Pathfinder")
        self.__window.wm_minsize(550, 410)
        self.__white = PhotoImage(file="white.gif")
        self.__black = PhotoImage(file="black.gif")
        self.__green = PhotoImage(file="green.gif")
        self.__red = PhotoImage(file="red.gif")
        self.__blue = PhotoImage(file="blue.gif")
        self.__grid = []
        self.__button = []
        self.__click = "normal"
        self.__drawing = "on"
        self.__search = False

        self.goal = None
        self.start = None

        # Creates buttons in the grid
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
                # Every button has creature in same position in a grid
                grid = Nodes(None, [j, i], "normal")
                self.__row.append(new_button)
                self.__grid_row.append(grid)
            self.__button.append(self.__row)
            self.__grid.append(self.__grid_row)

        self.__start_button = Button(self.__window, text="set starting point",
                                     command=self.start_command)
        self.__start_button.grid(row=0, column=SIZE, rowspan=4, sticky=N+E+W)
        self.__goal_button = Button(self.__window, text="set goal",
                                    command=self.goal_command)
        self.__goal_button.grid(row=4, column=SIZE, rowspan=4, sticky=N+E+W)

        self.__test_button = Button(self.__window, text="find path",
                                    command=self.no_visual)
        self.__test_button.grid(row=10, column=SIZE, rowspan=4, sticky=N+E+W)

        self.__clear_button = Button(self.__window, text="clear",
                                     command=self.clear)
        self.__clear_button.grid(row=13, column=SIZE, rowspan=4, sticky=N+E+W)

        self.__draw_button = Button(self.__window, text="visual path find",
                                    command=self.visual)
        self.__draw_button.grid(row=16, column=SIZE, rowspan=4, sticky=N+E+W)

        self.__info_label = Label(self.__window, text="")
        self.__info_label.grid(row=19, column=SIZE, rowspan=4, columnspan=5,
                               sticky=N+E+W)

        self.__window.mainloop()

    def press_button(self, event):
        """ Updates buttons in the grid
        :param event: mouse 1 press or hold (event)"""
        button = event.widget
        start_x, start_y = button.location
        x = start_x + math.floor(event.x/PIXELS)
        y = start_y + math.floor(event.y/PIXELS)
        if self.__drawing == "on":
            # Ignores input if it's not on the grid
            try:
                # Changes node into wall
                if self.__click == "normal" and\
                        self.__grid[y][x].mode == "normal":
                    self.__button[y][x].config(image=self.__black)
                    self.__grid[y][x].mode = "wall"
                # Changes node into start node
                elif self.__click == "start" and\
                        self.__grid[y][x].mode == "normal":
                    self.__button[y][x].config(image=self.__green)
                    self.__click = "normal"
                    self.__grid[y][x].mode = "start"
                    # Makes previous start into normal node
                    if self.start:
                        self.__button[self.start.location[1]][
                            self.start.location[0]].config(image=self.__white)
                        self.start.mode = "normal"
                    self.start = self.__grid[y][x]
                # Changes node into goal node
                elif self.__click == "goal" and\
                        self.__grid[y][x].mode == "normal":
                    self.__button[y][x].config(image=self.__red)
                    self.__click = "normal"
                    self.__grid[y][x].mode = "goal"
                    # Makes previous goal into normal node
                    if self.goal:
                        self.__button[self.goal.location[1]][
                            self.goal.location[0]].config(image=self.__white)
                        self.goal.mode = "normal"
                    self.goal = self.__grid[y][x]
            except IndexError:
                pass

    def distance_to_goal(self, start):
        """Calculates distance from node to goal using pythagoras equation
        :param start: node that needs distance to goal (object)
        :return distance from node to goal"""
        return math.sqrt((self.goal.location[0] - start.location[0]) ** 2 +
                         (self.goal.location[1] - start.location[1]) ** 2)

    def start_command(self):
        """Next click will set start node"""
        self.__click = "start"

    def goal_command(self):
        """Next click will set goal node"""
        self.__click = "goal"

    def visual(self):
        """ Draws visual representation of A*"""
        self.__search = True
        self.path()

    def no_visual(self):
        """ Draws only the path"""
        self.__search = False
        self.path()

    def path(self):
        """Calls A* algorithm if user has set goal and start nodes"""
        if self.goal and self.start:
            self.a_star(self.start, self.goal)
        else:
            self.__info_label.configure(text="Please set start and goal")

    def create_path(self):
        """ Draws shortest path between nodes backtracking from goal node using
        parents"""
        # Can't keep drawing after path is created
        self.__drawing = "off"
        node = self.goal.parent
        while node.mode != "start" and node != node.parent:
            self.__button[node.location[1]][node.location[0]]\
                .config(image=self.__blue)
            node = node.parent

    def a_star(self, start, goal):
        """ Finds shortest path between start and goal nodes using A* algorithm
        :param start: starting node (object)
        :param goal: target node (object)"""
        start.h = self.distance_to_goal(start)
        start.g = 0
        start.f = start.h + start.g
        open_list = [start]
        closed_list = []
        goal_reached = False
        # Loop stops if there is no possible path
        while len(open_list) != 0:
            # Adds best possible node from open_list to closed_list
            smallest_f = open_list[0].f
            smallest = open_list[0]
            for i in open_list:
                if i.f < smallest_f:
                    smallest_f = i.f
                    smallest = i
            closed_list.append(smallest)
            open_list.remove(smallest)
            # Draws considered node if visual mode is on
            if self.__search:
                self.__button[smallest.location[1]][smallest.location[0]]\
                    .configure(image=self.__green)
            # Goal is reached
            if closed_list[-1] == goal:
                self.create_path()
                goal_reached = True
                break

            # Considers all nodes around current node and adds possible
            # next nodes to open list
            for i in range(3):
                for j in range(3):
                    x = closed_list[-1].location[0] - 1 + i
                    y = closed_list[-1].location[1] - 1 + j
                    if 0 <= x <= 49 and 0 <= y <= 49:
                        child = self.__grid[y][x]
                        if (child.mode == "normal" or child.mode == "goal") \
                                and child not in closed_list and\
                                child not in open_list:
                            open_list.append(child)
                            child.parent = closed_list[-1]
                            child.h = self.distance_to_goal(child)
                            child.g = self.count_steps(child)
                            child.f = child.h + child.g
                            # Draws visual for possible next node
                            if self.__search:
                                self.__button[y][x].configure(image=self.__red)
                        # Updates node if shorter path to it is found
                        elif child in open_list and child.g >\
                                self.count_steps(child):
                            child.parent = closed_list[-1]
                            child.h = self.distance_to_goal(child)
                            child.g = self.count_steps(child)
                            child.f = child.h + child.g

        if goal_reached:
            self.__info_label.configure(text="Here is the calculated path")
        else:
            self.__info_label.configure(text="No path possible")

    def count_steps(self, node):
        """Counts steps needed to reach current node from start
        :param node: current node (object)
        :return number of steps (int)"""
        steps = 0
        while node.parent:
            steps += 1
            node = node.parent
        return steps

    def clear(self):
        """ Resets grid"""
        self.__drawing = "on"
        self.goal = None
        self.start = None
        for row in self.__grid:
            for node in row:
                node.g = 0
                node.h = 0
                node.f = 0
                node.parent = None
                node.mode = "normal"
                try:
                    self.__button[node.location[1]][node.location[0]].config(
                        image=self.__white)
                except ValueError:
                    pass


class Nodes:
    def __init__(self, parent=None, location=None, mode=None):
        """ Every button has a corresponding object in grid"""
        # Steps to reach node
        self.g = 0
        # Distance from node to goal
        self.h = 0
        # g+h
        self.f = 0
        # Nodes location
        self.location = location
        # Parent is node where this node is reached
        self.parent = parent
        # Mode could be normal, wall, start, or goal
        self.mode = mode


def main():
    Pathfinder()


main()
