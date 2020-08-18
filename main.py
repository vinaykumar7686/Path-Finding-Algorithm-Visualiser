import pygame
import time
from queue import PriorityQueue

try:
    ROWS = int(input("Enter the size of grid (e.g., 25)"))
except Exception:
    print('Due to invalid input recieved, the number of rows has been set as 50')
    ROWS = 50

try:
    algo = int(input("Enter 1 For Dijkstra's Algorithm, 2 for A* Algorithm"))
except:
    print('Due to invalid input recieved A* Algorithm will be implemented as Default.')
    algo = 2

WIDTH = 800
GAP = 800//ROWS

WIN = pygame.display.set_mode((WIDTH, WIDTH))

pygame.display.set_caption("Path Finding Algorithm Visualiser")

RED = (255,0,0)
WAYS = (217, 252, 152)
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
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == WAYS

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
        self.color = WAYS

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
        # Down Test
        if self.row<self.total_rows-1 and not grid[self.row+1][self.col].is_barrier():
            self.neighbors.append(grid[self.row+1][self.col])
        
        # Up Test
        if self.row>0 and not grid[self.row-1][self.col].is_barrier():
            self.neighbors.append(grid[self.row-1][self.col])

        # Left Test
        if self.col>0 and not grid[self.row][self.col-1].is_barrier():
            self.neighbors.append(grid[self.row][self.col-1])

        # Right Test
        if self.col<self.total_rows-1 and not grid[self.row][self.col+1].is_barrier():
            self.neighbors.append(grid[self.row][self.col+1])

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

    for i in range(0, rows):
        grid.append([])
        for j in range(0, rows):
            grid[i].append((Spot(i, j, GAP, rows)))


    return grid

def draw_grid(win, rows, width):

    # Draw Horizontal Lines
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i*GAP), (width, i*GAP))

        # Draw Vertical Lines
        for j in range(rows):
            pygame.draw.line(win, GREY, (j*GAP, 0), (j*GAP, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)
    
    draw_grid(win, rows, width)

    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    '''
    Takes the ciurrent position of mouse, number of rows and width of frame and returns the index of grid element to which the mouse is pointing.
    '''
    x, y = pos

    row = x // GAP
    col = y // GAP

    return row, col

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def a_star_algorithm(draw, grid, start, end):
    pygame.display.set_caption("A* Path Finding Algorithm Visualiser")
    # count variable is used in case of conflict when two values in priority queue have same priority
    count = 0
    # Defined a Priority Queue
    open_set = PriorityQueue()

    # Added start position to the Queue
    open_set.put((0, count, start))
    # To keep track of path
    came_from = {}

    # Initialising G-Score (Distance Travelled to reach that spot)
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0

    # Initialising F-Score (Total Distance to be travelled from starting to end through this spot to reach destination)
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    # A set to keep track whether or not a given value exists in Priority Queue (Used a set here as PriorityQueue doest support testing presence.)
    open_set_hash = {start}

    while not open_set.empty():
        
        # In case user wanys to exit while the algorith is running.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True
        
        for neighbor in current.neighbors:
            temp_g_score = g_score[current]+1

            # If the new gscore of neighbors of current is less than the score that was before.
            if temp_g_score<g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())

                if neighbor not in open_set_hash:
                    count+=1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()
        
        if current!=start:
            current.make_closed()

    return False

def dijkstra_algorithm(draw, grid, start, end):
    pygame.display.set_caption("Dijkstra's Path Finding Algorithm Visualiser")
    # count variable is used in case of conflict when two values in priority queue have same priority
    count = 0
    # Defined a Priority Queue
    open_set = PriorityQueue()

    # Added start position to the Queue
    open_set.put((0, count, start))
    # To keep track of path
    came_from = {}

    # Initialising G-Score (Distance Travelled to reach that spot)
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0

    # A set to keep track whether or not a given value exists in Priority Queue (Used a set here as PriorityQueue doest support testing presence.)
    open_set_hash = {start}

    while not open_set.empty():
        
        # In case user wanys to exit while the algorith is running.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True
        
        for neighbor in current.neighbors:
            temp_g_score = g_score[current]+1

            # If the new gscore of neighbors of current is less than the score that was before.
            if temp_g_score<g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score

                if neighbor not in open_set_hash:
                    count+=1
                    open_set.put((g_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()
        
        if current!=start:
            current.make_closed()

    return False

def main(win, width):
    #ROWS = 50#int(input("Enter the size of grid: "))

    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # If algorithm has started then user can't edit grid or do anything else, other than exiting.
            if started:
                continue
            
            # Left Mouse Button
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]

                # If start is not defined and the point clicked is not equal to end the make the point as start
                if not start and spot!=end:
                    spot.make_start()
                    start = spot

                # If start is defined and end is not defined and the point clicked is not equal to start the make the point as end
                elif not end and spot!=start:
                    spot.make_end()
                    end = spot
                # if start and end have beend defined and the spot is not equal to start or end then define the spot as barrier
                elif spot!=start and spot!=end:
                    spot.make_barrier()

            # Right Mouse Button
            if pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]

                spot.reset()

                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            # Event to trigger Algorithm
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    if algo == 1:
                        dijkstra_algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    elif algo ==2:
                        a_star_algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
                
                if event.key == pygame.K_ESCAPE:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()

main(WIN, 800)
