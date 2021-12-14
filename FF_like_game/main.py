import pygame


pygame.init()


SCREEN_WIDTH = 1124
SCREEN_HEIGHT = SCREEN_WIDTH // (800/600)
BOTTOM_PANEL = SCREEN_HEIGHT - 725

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Battle Time!')

background_img = pygame.image.load('img/cyberpunk-gf755e0a93_1280.png').convert_alpha()


def draw_background():
    screen.blit(background_img, (0, 0))


if __name__ == '__main__':
    pygame.display.set_caption('Battle Time!')
    run = True

    while run:

        draw_background()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()
