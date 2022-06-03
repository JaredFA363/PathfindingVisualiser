#PathFinding Algorithm with Dijkstra Algorithm
from tkinter import messagebox, Tk
import pygame
import sys

w_width = 500
w_height = 500

window = pygame.display.set_mode((w_width, w_height))

columns = 25
rows = 25

box_width = w_width // columns
box_height = w_height // rows

# stores all the indicies in the window
grid = []
queue = []
path = []


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
        self.neighbours = []
        #box before end node
        self.prior = None

    def draw(self, win, color):
        # - 2 on box width and height inorder to show border
        pygame.draw.rect(win, color, (self.x * box_width, self.y * box_height, box_width-2, box_height-2))

    def set_neighbours(self):
        # Horizontal Neighbours
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y])
        if self.x < columns - 1:
            self.neighbours.append(grid[self.x + 1][self.y])
        # Vertical Neighbours
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbours.append(grid[self.x][self.y + 1])


# Creating Grid
for i in range(columns):
    array_ = []
    for j in range(rows):
        array_.append(Box(i, j))
    grid.append(array_)

# Set Neighbours
for i in range(columns):
    for j in range(rows):
        grid[i][j].set_neighbours()

# Start of grid is top left corner
start_of_grid = grid[0][0]
start_of_grid.start = True
start_of_grid.visited = True
# First box will be in queue
queue.append(start_of_grid)


def main():
    begin_search = False
    target_box_set = False
    searching = True
    target_box = None

    while True:
        for event in pygame.event.get():
            # Quitting Window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Mouse Controls
            elif event.type == pygame.MOUSEMOTION:
                #captures mouse position
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                # Draw Wall
                if event.buttons[0]:
                    i = x // box_width
                    j = y // box_height
                    grid[i][j].wall = True
                # Set Target
                if event.buttons[2] and not target_box_set:
                    i = x // box_width
                    j = y // box_height
                    target_box = grid[i][j]
                    target_box.target = True
                    target_box_set = True
            # Start Algo
            if event.type == pygame.KEYDOWN and target_box_set:
                begin_search = True

        if begin_search:
            if len(queue) > 0 and searching:
                current_box = queue.pop(0)
                current_box.visited = True
                if current_box == target_box:
                    searching = False
                    # Draws Path
                    while current_box.prior != start_of_grid:
                        #iterates through end points and its priors until it reaches start
                        path.append(current_box.prior)
                        current_box = current_box.prior
                else:
                    #iterates between all neighbours in currentbos
                    for neighbour in current_box.neighbours:
                        if not neighbour.queued and not neighbour.wall:
                            neighbour.queued = True
                            neighbour.prior = current_box
                            queue.append(neighbour)
            else:
                #if no solution
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution", "There is no solution!")
                    searching = False

        #Fills grid black
        window.fill((0, 0, 0))

        #applies function draw to each individual box
        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                box.draw(window, (50,50,50))

                if box.queued:
                    box.draw(window, (255,0,255))
                if box.visited:
                    box.draw(window, (0,200,0))
                if box in path:
                    box.draw(window, (0,0,200))

                if box.start:
                    box.draw(window, (0,200,200))
                if box.wall:
                    box.draw(window, (90,90,90))
                if box.target:
                    box.draw(window, (255,0,0))

        #Updates Window
        pygame.display.flip()

main()
