# implements the game demineur

import pygame
from pygame.locals import *
import numpy as np
import copy
from operator import add

size_cell = 50
cells_by_side = 10
nb_fps = 30
side_win = size_cell*cells_by_side
nb_mines = 10

pygame.init()

# open windows
window = pygame.display.set_mode((side_win, side_win))

def import_img(png_file):
    """ import and scale image in png_file and return the brick """
    brick_name = pygame.image.load(png_file)
    brick_name = pygame.transform.scale(brick_name, (size_cell, size_cell))
    return brick_name

mine = import_img('mine.png')
empty = import_img('empty.png')
unit_grid = import_img('grid.png')
flag = import_img('flag.png')
hidden = import_img('hidden.png')
one = import_img('1.png')
two = import_img('2.png')
three = import_img('3.png')
four = import_img('4.png')
five = import_img('5.png')
six = import_img('6.png')
seven = import_img('7.png')
eight = import_img('8.png')


def create_brick(brick, x, y):
    """ place brick at location (x, y) """
    window.blit(brick, (size_cell*x, size_cell*y))

# create matrix containing the number of neighbouring mines
grid = np.zeros((cells_by_side+1, cells_by_side+1))

# create grid with random mines
for i in range(nb_mines):
   a = np.random.randint(1, cells_by_side-1)
   b = np.random.randint(1, cells_by_side-1)
   
   grid[a, b] = 1

print(np.transpose(grid))

def number_neighbours(x, y, grid):
    """ return number of neighbourghs for the cell (x, y) in grid """
    n = 0
    if grid[x+1, y] == 1:
        n = n+1
    if grid[x+1, y+1] == 1:
        n = n+1
    if grid[x, y+1] == 1:
        n = n+1
    if grid[x-1, y+1] == 1:
        n = n+1
    if grid[x-1, y] == 1:
        n = n+1
    if grid[x-1, y-1] == 1:
        n = n+1
    if grid[x, y-1] == 1:
        n = n+1
    if grid[x+1, y-1] == 1:
        n = n+1    
    return n

for x in range(1, cells_by_side-1):
    for y in range(1, cells_by_side-1):
        create_brick(hidden, x, y)

def discover_brick(x, y):
    """ function that discover the brick at location (x, y)"""

    if grid[x, y] == 1:
        create_brick(mine, x, y)

    if grid[x, y] == 0:
        if x != 0:
            if y != 0:     
                if number_neighbours(x, y, grid) == 0:
                    create_brick(empty, x, y) 
                if number_neighbours(x, y, grid) == 1:
                    create_brick(one, x, y)
                if number_neighbours(x, y, grid) == 2:
                    create_brick(two, x, y)
                if number_neighbours(x, y, grid) == 3:
                    create_brick(three, x, y)
                if number_neighbours(x, y, grid) == 4:
                    create_brick(four, x, y)
                if number_neighbours(x, y, grid) == 5:
                    create_brick(five, x, y)
                if number_neighbours(x, y, grid) == 6:
                    create_brick(six, x, y)
                if number_neighbours(x, y, grid) == 7:
                    create_brick(seven, x, y)
                if number_neighbours(x, y, grid) == 8:
                    create_brick(eight, x, y)

def click_brick():
    """ function that returns the brick location (x, y) of the click """ 
    x = 0
    y = 0
    
    if event.type == MOUSEBUTTONDOWN:
        if event.button == 1:

            for i in range(1, cells_by_side-1):
                if event.pos[0] > size_cell*i:
                    if event.pos[0] < size_cell*(i+1):
                        x = i

            for i in range(1, cells_by_side-1):
                if event.pos[1] > size_cell*i:
                    if event.pos[1] < size_cell*(i+1):
                        y = i
    return (x, y)


# refresh screen
pygame.display.flip()

run_game = 1
while run_game:

    pygame.time.Clock().tick(nb_fps)
	
    for event in pygame.event.get():
        if event.type == QUIT:
            run_game = 0
        if event.type == KEYDOWN and event.key == K_SPACE:
            run_game = 0

        x, y = click_brick()
        discover_brick(x, y)
        
        # create green flag if even.button == 2 at location x, y
        


    pygame.display.flip()

