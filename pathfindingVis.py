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

    def draw(self, window_d, colour):
        pygame.draw.rect(window_d, colour, (self.x * box_width, self.y * box_height, box_width - 2, box_height - 2))


# Creating Grid
for i in range(columns):
    array = []
    for j in range(rows):
        array.append(Box(i, j))
    grid.append(array)


def main():
    while True:
        for event in pygame.event.get():
            #Quitting Window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        #Fills window with black
        window.fill((0, 0, 0))

        #applies function draw to each individual box
        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                box.draw(window, (50,50,50))

        #Updates Display
        pygame.display.flip()

main()