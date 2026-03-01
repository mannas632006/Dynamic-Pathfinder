import pygame

# Colors for Visualization
WHITE = (255, 255, 255)  # Empty
BLACK = (0, 0, 0)        # Wall
GREEN = (0, 255, 0)      # Path
RED = (255, 0, 0)        # Visited
YELLOW = (255, 255, 0)   # Frontier (Priority Queue)
ORANGE = (255, 165, 0)   # Start
PURPLE = (128, 0, 128)   # Goal
GREY = (128, 128, 128)   # Grid lines

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_wall(self):
        return self.color == BLACK

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_wall(self):
        self.color = BLACK

    def make_goal(self):
        self.color = PURPLE

    def make_visited(self):
        if self.color not in [ORANGE, PURPLE]:
            self.color = RED

    def make_frontier(self):
        if self.color not in [ORANGE, PURPLE]:
            self.color = YELLOW

    def make_path(self):
        if self.color not in [ORANGE, PURPLE]:
            self.color = GREEN

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        # Check Down, Up, Right, Left
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall():
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_wall():
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_wall():
            self.neighbors.append(grid[self.row][self.col - 1])
