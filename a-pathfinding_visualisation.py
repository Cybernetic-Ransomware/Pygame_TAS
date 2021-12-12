import pygame
import math
from queue import PriorityQueue

WIDTH = 800
HEIGHT = WIDTH
ROWS = 40
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
        self.neighbors = []

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
        self.color = CLRS['WHITE']

    def make_start(self):
        self.color = CLRS['ORANGE']

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

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():    # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():                      # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():    # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():    # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float('inf') for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float('inf') for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        if current != start:
            current.make_closed()

    return False


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


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def main():
    grid = make_grid(ROWS, WIDTH)

    start = None
    end = None

    run = True
    started = False

    while run:
        draw(WIN, grid, ROWS, WIDTH)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:       # LPM
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, WIDTH)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()
                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot not in (end, start):
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:     # PPM
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, WIDTH)
                spot = grid[row][col]
                spot.reset()

                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    algorithm(lambda: draw(WIN, grid, ROWS, WIDTH), grid, start, end)
                    
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, WIDTH)

    pygame.quit()


if __name__ == '__main__':
    pygame.display.set_caption('A* Path Finding Algorithm')
    main()
