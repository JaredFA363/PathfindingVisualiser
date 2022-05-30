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

class Box:
    def __init__(self, i, j):
        # identifies each box
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.target = False

    def draw(self, window_d, colour):
        # - 2 on box width and height inorder to show border
        pygame.draw.rect(window_d, colour, (self.x * box_width, self.y * box_height, box_width - 2, box_height - 2))


# Creating Grid
for i in range(columns):
    array = []
    for j in range(rows):
        array.append(Box(i, j))
    grid.append(array)

# Start of grid is top left corner
start_grid = grid[0][0]
start_grid.start = False

def main():
    begin_search = False
    target_box_set = False
    target_box = None

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

        #Fills window with black
        window.fill((0, 0, 0))

        #applies function draw to each individual box
        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                box.draw(window, (50,50,50))
                if box.start:
                    box.draw(window, (0,200,200))
                if box.wall:
                    box.draw(window, (90,90,90))
                if box.target:
                    box.draw(window, (200,200,0))

        #Updates Display
        pygame.display.flip()

main()