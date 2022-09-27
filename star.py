from tempfile import SpooledTemporaryFile
import pygame
import math
from queue import PriorityQueue

from sklearn import gaussian_process
from sympy import Lambda

# Pygame Basics - (Window Display Size / Window Title)

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("Pathfinder A*")

# Color Display

RED=(255, 0, 0)
GREEN=(0,255,0)
BLUE=(0,255,0)
YELLOW=(255,255,0)
WHITE=(255,255,255)
BLACK=(0,0,0)
PURPLE=(128,0,128)
ORANGE=(255,165,0)
GREY=(128,128,128)
TURQUOISE=(64,224,208)

# Keeps track of colors and location of different nodes across the grid panel

class Node:
    def __intit__(self,row,col,width,total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE # Starting Color for Grid
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
    
    # Getter Function for Node Position
    
    def pos_get(self):
        return self.row, self.col 
    
    # Highlights the purpose of each individual color (e.g. If Node is taken then the color is assigned RED)
    
    def closed_spot(self):
        return self.color == RED 
    
    def open_spot(self):
        return self.color == GREEN
    
    def is_wall(self):
        return self.color == BLACK
    
    def is_start(self):
        return self. color == ORANGE
    
    def is_end(self):
        return self.color == TURQUOISE
    
    def reset(self):
        self.color = WHITE
    
    def make_start(self):
        self.color = ORANGE
    
    def make_closed(self):
        self.color = RED
    
    def make_open(self):
        self.color = GREEN
    
    def make_wall(self):
        self.color = BLACK
    
    def make_end(self):
        self.color = TURQUOISE
    
    # Creates edges of rectangle and sets boundaries
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.width))
    
    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # Moving down
            self.neighbors.append(grid[self.rows + 1][self.col]) 
        
        if self.row > 0 and not grid[self.row + 1][self.col].is_barrier(): # Moving up
            self.neighbors.append(grid[self.rows - 1][self.col]) 
        
        if self.col < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # Moving right
            self.neighbors.append(grid[self.rows ][self.col + 1]) 
        
        if self.row > 0 and not grid[self.row][self.col - 1].is_barrier(): # Moving left
            self.neighbors.append(grid[self.rows ][self.col  - 1]) #

    def __lt__(self, other):
        return False
    
    # Algorithm Function - Finds Distance through Manhattan Format (Heuristic)
    
    # Manhattan Distance - Distance between two points in a N dimensional vector space

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs(y1-y2)

# Current starts at end node and traverses back to start node

# Current is equal to last node and adds it to path (allowing for path creation)

def new_path(original, current, draw):
    while current in original:
        current == original[current]
        current.make_path()
        draw()


def algorithm(draw, grid, start, end):
    counterd = 0
    set_open = PriorityQueue() # Ensures minimal element is given from f-score
    set_open.put((0, counterd, start)) # Add to PriorityQueue (Add Start Node to F Score)
    original = {} # Keeps track of path as a dict
    g_score = {spot: float("inf") for row in grid for spot in row} # KeyList for every spot from float("inf")
    g_score[start] = 0

    f_score = {spot: float("inf") for row in grid for spot in row} # Keeps track of predicted distance from Node to End Node
    f_score[start] = h(start.get_pos(), end.get_pos()) # Huerestic Distance (Start to 0)

    open_hash = {start} # Checks if there is a value in Queue and keeps track of values in PriorityQueue

    while not open_hash.empty():
        for event in pygame.event.get(): # Condition to Quit Loop
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = set_open.get()[2] # Recieves popped node from Queue and synchronizes it with hash (Protects Duplicate Errors)
        set_open.remove(current)

        if current == end: # Makes shortest path option
            new_path(original, end, draw)
            return True
        
        for neighbor in current.neighbors: # Considers all neighbors
            temporary = g_score[current] + 1 # Assume edges are 1 and adds one to move nodes

            if temporary < g_score[neighbor]: # Reminds program to update optimal path if a lesser distance is found
                original[neighbor] = current
                g_score[neighbor] = temporary
                f_score[neighbor] = temporary + h(neighbor.get_pos(), end.get_pos()) # Updates f - score

                if neighbor not in open_hash: # Adds to openset hash
                    count += 1
                    set_open.put((f_score[neighbor], count, neighbor)) # Makes current neighbor open
                    set_open.add(neighbor)
                    neighbor.make_open()
        
        draw()

        if current != start: # If current isnt start = make node closed (RED / Considered in Set)
            current.make_closed()
    
    return False # Path wasn't found
    
def make_grid(rows, width):
    grid = []
    gap = width // rows

# Appends spot in grid row "i" and creates multiple lists to store multiple Nodes

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Node(i, j, gap, rows)
            grid[i].append(spot) 

    return grid

# Draws the gridline by drawing horizontal lines (Up to Down)

def grid_draw(win, rows, width):
    hole = width // rows

    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * hole), (width, i * hole))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * hole, 0), (j * hole, width))

# Fills screen with WHITE and then draws colors / grid lines 

def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)
    
    grid_draw(win, rows, width)
    pygame.display.update()

def clicked_pos(pos, rows, width):
    hole = width // rows
    y, x = pos

    row = y // hole
    col = x // hole

    return row, col

# Main Loop

def main(win, width):
    ROWS = 60
    grid = make_grid(ROWS, width)

    # Defines start and end positions / Defines algorithm start

    start = None
    end = None

    run = True
    
    # Checks for events in pygame and user input (e.g. spacebar)

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            # Blocks users from changing obstacles (nodes)

            if pygame.mouse.get_pressed()[0]: #Left Side of Mouse Action
                pos = pygame.mouse.get_pos()
                row, col = clicked_pos(pos, ROWS, width) # Gives row / column of user click
                spot = grid[row][col]
                
                # Forces user so first click if not already clicked is the start or end click

                if not start and spot != end:
                    start = spot
                    start.make_start()
                
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                
                # Error checks if user clicks a random spot (Not Start or End)
                
                elif spot != end and spot != start:
                    spot.make_barrier()
                
            elif pygame.mouse.get_pressed()[2]: # Right Side of Mouse Action
                pos = pygame.mouse.get_pos()
                row, col = clicked_pos(pos, ROWS, width) # Gives row / column of user click
                spot = grid[row][col]
                spot.reset()

                if spot == start:
                    start == None
                
                elif spot == end:
                    end == None

            # If spacebar is pressed and program has not started, then update neighbors for all rows in grid / spots in row
            # Call Algorithm

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.type == pygame.K_c: #Clears Screen for New Path
                    start = None
                    end =  None
                    grid = make_grid(ROWS, width) # Remakes entire grid for board reset

    
    pygame.quit()

main(WIN, WIDTH) # Main Element
