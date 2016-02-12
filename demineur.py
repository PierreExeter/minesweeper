#!/usr/bin/python
""" implements the game minesweeper """

import pygame
from pygame.locals import *
import numpy as np
import copy
from operator import add

# initialise game

# def initialise_parameter(prompt_text, min, max):
    # """ 
    # initialise the variable x by prompting the user with the 
    # string prompt_text and allow only integer values between 
    # min and max 
    # """
    # x = 0 
    # while True:
        # try:
            # x = int(raw_input(prompt_text))

        # except ValueError:
            # print('Oops, that\'s not an integer!')
        # else:
            # if min <= x <= max:
                # break
            # else:
                # print('Out of range. Try again')
    # return x   

while True:
    try:
        cells_by_side = int(raw_input('Enter the size of the mine field (5 - 12): ') )
    except ValueError:
        print('Oops, that\'s not an integer!')
    else:
        if 5 <= cells_by_side <= 12:
            break
        else:
            print('Out of range. Try again.')

 # cells_by_side = 10

while True:
    try:
        nb_mines = int(raw_input('Enter the number of mines (min 3): ') )
    except ValueError:
        print('Oops, that\'s not an integer!')
    else:
        if nb_mines <= 3:
            print('Not enough mines...')
        elif nb_mines >= cells_by_side**2-1:
            print('Too many mines for the size of the mine field!')
        else:
            break

# nb_mines = 90

size_cell = 50
nb_fps = 30
side_win = size_cell*cells_by_side

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

def discover_brick(x, y, xx, yy):
    """ function that discovers the brick at location (x, y)"""
    
    if grid[xx, yy] == 1:
        for i in range(cells_by_side+2):
            for j in range(cells_by_side+2):
                if grid[i, j] == 1:
                    create_brick(boom, i-1, j-1)
        print('You lost!')

    if grid[xx, yy] == 0:
        if number_neighbours(xx, yy, grid) == 0:
            create_brick(empty, x, y) 
        if number_neighbours(xx, yy, grid) == 1:
            create_brick(one, x, y)
        if number_neighbours(xx, yy, grid) == 2:
            create_brick(two, x, y)
        if number_neighbours(xx, yy, grid) == 3:
            create_brick(three, x, y)
        if number_neighbours(xx, yy, grid) == 4:
            create_brick(four,x , y)
        if number_neighbours(xx, yy, grid) == 5:
            create_brick(five, x, y)
        if number_neighbours(xx, yy, grid) == 6:
            create_brick(six, x, y)
        if number_neighbours(xx, yy, grid) == 7:
            create_brick(seven, x, y)
        if number_neighbours(xx, yy, grid) == 8:
            create_brick(eight, x, y)

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
        print(x, y)
        
        # corresponding grid coordinates
        xx = x+1
        yy = y+1

        # # implement a counter to decide when you win

        if event.button == 1:
            discover_brick(x, y, xx, yy)
            
        if event.button == 3:
            create_brick(flag, x, y)
             
        pygame.display.flip()

