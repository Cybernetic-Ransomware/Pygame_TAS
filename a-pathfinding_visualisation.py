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





if __name__ == '__main__':
    pygame.display.set_caption('A* Path Finding Algorithm')
