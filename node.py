import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)     # start
PURPLE = (128, 0, 128)     # goal
RED = (255, 0, 0)          # closed set
GREEN = (0, 255, 0)        # path
BLUE = (0, 0, 255)         # current agent position
CYAN = (0, 255, 255)       # open set
GREY = (128, 128, 128)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.width = width
        self.total_rows = total_rows

        # Standard convention:
        # x increases to the right (col), y increases downward (row)
        self.x = col * width
        self.y = row * width

        self.color = WHITE
        self.neighbors = []

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == CYAN

    def is_wall(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == PURPLE

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = CYAN

    def make_wall(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = PURPLE

    def make_path(self):
        self.color = GREEN

    def make_current(self):
        self.color = BLUE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        r, c = self.row, self.col

        # Down
        if r < self.total_rows - 1 and not grid[r + 1][c].is_wall():
            self.neighbors.append(grid[r + 1][c])
        # Up
        if r > 0 and not grid[r - 1][c].is_wall():
            self.neighbors.append(grid[r - 1][c])
        # Right
        if c < self.total_rows - 1 and not grid[r][c + 1].is_wall():
            self.neighbors.append(grid[r][c + 1])
        # Left
        if c > 0 and not grid[r][c - 1].is_wall():
            self.neighbors.append(grid[r][c - 1])

    def __lt__(self, other):
        return False
