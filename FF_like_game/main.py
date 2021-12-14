import pygame


pygame.init()


SCREEN_WIDTH = 1124
SCREEN_HEIGHT = SCREEN_WIDTH // (800/600)
BOTTOM_PANEL = SCREEN_HEIGHT - 725           # 118px

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Battle Time!')

background_img = pygame.image.load('img/cyberpunk-gf755e0a93_1280.png').convert_alpha()
panel_img = pygame.image.load('img/empty-blackboard.jpg').convert_alpha()

hp_hearts = {
    'full': pygame.image.load('img/icons/heart-sketch.png').convert_alpha(),
    'touched': pygame.image.load('img/icons/heart.png').convert_alpha(),
    'empty': pygame.image.load('img/icons/broken-heart.png').convert_alpha()
}


def draw_background():
    screen.blit(background_img, (0, 0))


def draw_panel():
    screen.blit(panel_img, (0, SCREEN_HEIGHT - BOTTOM_PANEL))


def draw_hp():
    pygame.draw.rect(screen, '#D5D9DC', (20, 750, 250, 50), border_radius=3)
    positions = [26, 64, 102, 140]
    hp_value = 2.5
    counter = 1
    for i in positions:
        if counter <= hp_value:
            screen.blit(hp_hearts['full'], (i, 762))
        elif 1 > hp_value - counter + 1 > 0:
            screen.blit(hp_hearts['touched'], (i, 762))
        else:
            screen.blit(hp_hearts['empty'], (i, 762))
        counter += 1


if __name__ == '__main__':
    pygame.display.set_caption('Battle Time!')
    run = True

    while run:

        draw_background()
        draw_panel()
        draw_hp()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()
