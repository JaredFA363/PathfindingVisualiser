from tkinter import messagebox, Tk
from numpy import array
import pygame
import sys

w_width = 500
w_height = 500

window = pygame.display.set_mode((w_width, w_height))

columns = 25
rows = 25

box_width = w_width//columns
box_height = w_height//rows

# stores all the indicies in the window
grid = []
queue = []

class Box:
    def __init__(self, i, j):
        # identifies each box
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.target = False
        #Flags for Dijkstra's Algorithm
        self.queued = False
        self.visited = False
        self.neighbour = []

    def draw(self, window_d, colour):
        # - 2 on box width and height inorder to show border
        pygame.draw.rect(window_d, colour, (self.x * box_width, self.y * box_height, box_width - 2, box_height - 2))

    def set_neighbour(self):
        # Horizontal Neighbours
        if self.x > 0:
            self.neighbour.append(grid[self.x - 1][self.y])
        if self.x < columns - 1:
            self.neighbour.append(grid[self.x + 1][self.y])
        # Vertical Neighbours
        if self.y > 0:
            self.neighbour.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbour.append(grid[self.x][self.y + 1])



# Creating Grid
for i in range(columns):
    array = []
    for j in range(rows):
        array.append(Box(i, j))
    grid.append(array)

# Set Neighbours
for i in range(columns):
    for j in range(rows):
        grid[i][j].set_neighbour()

# Start of grid is top left corner
start_grid = grid[0][0]
start_grid.start = True
start_grid.visited = True
# First box will be in queue
queue.append(start_grid)

def main():
    begin_search = False
    target_box_set = False
    target_box = None
    searching = True

    while True:
        for event in pygame.event.get():
            #Quitting Window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #Mouse Controls
            elif event.type == pygame.MOUSEMOTION:
                #captures mouse position
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                #Draws Wall
                if event.buttons[0]:
                    i = x // box_width
                    j = y // box_height
                    grid[i][j].wall = True
                #Set Target
                if event.buttons[2] and not target_box_set:
                    i = x // box_width
                    j = y // box_height
                    target_box = grid[i][j]
                    target_box.target = True
                    target_box_set = True
        #Start Algo
            if event.type == pygame.KEYDOWN and target_box_set:
                begin_search = True

        if begin_search:
            if len(queue) > 0 and searching:
                current_box = queue.pop(0)
                current_box.visited = True
                if current_box == target_box:
                    searching = False
                else:
                    #iterates between all neighbours in currentbos
                    for neighbour in current_box.neighbour:
                        if not neighbour.queued and not neighbour.wall:
                            neighbour.queued = True
                            queue.append(neighbour)
        #if no solution
            else:
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution", "There is No Solution")
                    searching = False

        #Fills window with black
        window.fill((0, 0, 0))

        #applies function draw to each individual box
        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                box.draw(window, (50,50,50))

                if box.queued:
                    box.draw(window, (200,0,0))
                if box.visited:
                    box.draw(window, (0,200,0))

                if box.start:
                    box.draw(window, (0,200,200))
                if box.wall:
                    box.draw(window, (90,90,90))
                if box.target:
                    box.draw(window, (200,200,0))

        #Updates Display
        pygame.display.flip()

main()
