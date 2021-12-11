import pygame
import math
from queue import PriorityQueue

WIDTH = 800
HEIGHT = WIDTH
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

CLRS = {
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'BLUE': (0, 0, 255),
    'YELLOW': (255, 255, 0),
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'PURPLE': (128, 0, 128),
    'ORANGE': (255, 165, 0),
    'GREY': (128, 128, 128),
    'TURQUOISE': (64, 224, 208)
}


class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = CLRS['WHITE']
        self.width = width
        self.height = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == CLRS['RED']

    def is_open(self):
        return self.color == CLRS['GREEN']

    def is_barrier(self):
        return self.color == CLRS['BLACK']

    def is_start(self):
        return self.color == CLRS['ORANGE']

    def is_end(self):
        return self.color == CLRS['TURQUOISE']

    def reset(self):
        return self.color == CLRS['WHITE']

    def make_closed(self):
        self.color = CLRS['RED']

    def make_open(self):
        self.color = CLRS['GREEN']

    def make_barrier(self):
        self.color = CLRS['BLACK']

    def make_end(self):
        self.color = CLRS['TURQUOISE']

    def make_path(self):
        self.color = CLRS['PURPLE']

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

    def update_neighbors(self):
        pass

    def __lt__(self, other):
        return False


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, CLRS['GREY'], (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, CLRS['GREY'], (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(CLRS['WHITE'])

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


if __name__ == '__main__':
    pygame.display.set_caption('A* Path Finding Algorithm')
