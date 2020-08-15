import pygame
import time
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))

pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)

GREY = (210,210,210)
VIOLET = (148, 0, 211) 
INDIGO = (75, 0, 130)
YELLOW = (255, 255, 0)
ORANGE = (255, 127, 0)


class Spot:
    def __init__(self, row, col, width, total_rows):

        self.row = row
        self.col = col
        self.x = width * row
        self.y = width * col
        self.color = WHITE
        self.neighbor = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_barrier(self):
        return self.color == BLACK
    
    def is_open(self):
        return self.color == GREEN

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == VIOLET



    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED

    def make_barrier(self):
        self.color = BLACK
    
    def make_open(self):
        self.color = GREEN

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = VIOLET

    def make_path(self):
        self.color = YELLOW


    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        pass

    def __lt__(self, other):
        return False



def h(p1, p2):
    '''
    This functions is used to return the manhattan distance between two points passed as arguments
    '''
    x1, y1 = p1
    x2, y2 = p2

    return abs(x2-x1)+abs(y2-y1)

def make_grid(rows, width):
    '''
    This Functions defined rows*rows number of Spots and adds the into a grid (a nested list) and return it.
    '''
    grid = []

    gap = width//rows

    for i in range(0, rows):
        grid.append([])
        for j in range(0, rows):
            grid[i].append((Spot(i, j, gap, rows)))


    return grid

def draw_grid(win, rows, width):
    gap =  width // rows

    # Draw Horizontal Lines
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i*gap), (width, i*gap))

        # Draw Vertical Lines
        for j in range(rows):
            pygame.draw.line(win, GREY, (j*gap, 0), (j*gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)
    
    draw_grid(win, rows, width)

    pygame.display.update()


