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

