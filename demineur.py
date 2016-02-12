#!/usr/bin/python
""" implements the game demineur """

import pygame
from pygame.locals import *
import numpy as np
import copy
from operator import add

size_cell = 50
cells_by_side = 10
nb_fps = 30
side_win = size_cell*cells_by_side
nb_mines = 90

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
boom = import_img('boom.png')
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

for x in range(0, cells_by_side):
    for y in range(0, cells_by_side):
        create_brick(hidden, x, y)

# refresh screen
pygame.display.flip()


# create matrix with random mines (create 2 extra rows 
# and columns to be able to count the number of neighbours
# later
grid = np.zeros((cells_by_side+2, cells_by_side+2))

# place mines randomly
# don't allow to place mine at the border of the field
for i in range(0, nb_mines):
   a = np.random.randint(1, cells_by_side+1)
   b = np.random.randint(1, cells_by_side+1)
   
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

print(number_neighbours(1, 8, grid))

def discover_brick(x, y):
    """ function that discover the brick at location (x, y)"""
    
    # coordinate to be passed to the function create_brick
    xx = x-1
    yy = y-1

    if grid[x, y] == 1:
        for i in range(cells_by_side+2):
            for j in range(cells_by_side+2):
                if grid[i, j] == 1:
                    create_brick(boom, i-1, j-1)
        print('You lost!')

    if grid[x, y] == 0:
        if number_neighbours(x, y, grid) == 0:
            create_brick(empty, xx, yy) 
        if number_neighbours(x, y, grid) == 1:
            create_brick(one, xx, yy)
        if number_neighbours(x, y, grid) == 2:
            create_brick(two, xx, yy)
        if number_neighbours(x, y, grid) == 3:
            create_brick(three, xx, yy)
        if number_neighbours(x, y, grid) == 4:
            create_brick(four,xx , yy)
        if number_neighbours(x, y, grid) == 5:
            create_brick(five, xx, yy)
        if number_neighbours(x, y, grid) == 6:
            create_brick(six, xx, yy)
        if number_neighbours(x, y, grid) == 7:
            create_brick(seven, xx, yy)
        if number_neighbours(x, y, grid) == 8:
            create_brick(eight, xx, yy)

def click_brick():
    """ function that returns the brick location (x, y) of the click """ 
    x = 0
    y = 0
    
    for i in range(0, cells_by_side):
        if event.pos[0] > size_cell*i:
            if event.pos[0] < size_cell*(i+1):
                x = i

    for i in range(0, cells_by_side):
        if event.pos[1] > size_cell*i:
            if event.pos[1] < size_cell*(i+1):
                y = i
    
    return (x, y)

def place_flag(x, y):
    """ function that places a green flag at location (x, y)"""     
    # coordinate to be passed to the function create_brick
    xx = x-1
    yy = y-1

    create_brick(flag, xx, yy)


run_game = 1
while run_game:

    pygame.time.Clock().tick(nb_fps)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            run_game = 0
        if event.type == KEYDOWN and event.key == K_SPACE:
            run_game = 0
    if event.type == MOUSEBUTTONDOWN:
        x, y = click_brick()
        # update indices to account for extra row and column
        x = x+1
        y = y+1
        print(x, y)

        # # implement a counter to decide when you win

        if event.button == 1:
            discover_brick(x, y)
            
        elif event.button == 3:
            place_flag(x, y)
             
        pygame.display.flip()

