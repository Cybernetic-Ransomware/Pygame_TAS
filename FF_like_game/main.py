import pygame
import yaml


pygame.init()

# SETUP
with open('config.yml', 'r') as f:
    parse_config = yaml.safe_load(f)

SCREEN_WIDTH = parse_config['SCREEN_WIDTH']
SCREEN_HEIGHT = parse_config['SCREEN_HEIGHT']
BOTTOM_PANEL = SCREEN_HEIGHT - 725 - 29
INDENT = (SCREEN_WIDTH - 1122) // 2

FPS = parse_config['FPS']
clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Battle Time!')

background_img = pygame.image.load('img/cyberpunk-gf755e0a93_1280.png').convert_alpha()
panel_img = pygame.image.load('img/empty-blackboard.jpg').convert_alpha()


def draw_background():
    screen.blit(background_img, (INDENT, 29))


def draw_panel():
    screen.blit(panel_img, (INDENT, SCREEN_HEIGHT - BOTTOM_PANEL))


def draw_hp(enemy: bool, hp_value: float, max_hp: int):

    # not sure if loading files by every frame isn't right for efficiency
    hp_hearts = {
        'full': pygame.image.load('img/icons/heart-sketch.png').convert_alpha(),
        'touched': pygame.image.load('img/icons/heart.png').convert_alpha(),
        'empty': pygame.image.load('img/icons/broken-heart.png').convert_alpha()
    }

    if enemy:
        pygame.draw.rect(screen, '#D5D9DC', (SCREEN_WIDTH - 20 - INDENT - 250, 780, 250, 50), border_radius=3)
        positions = [SCREEN_WIDTH - x - INDENT - 25 for x in [26, 64, 102, 140, 178, 216]][:max_hp]
    else:
        pygame.draw.rect(screen, '#D5D9DC', (INDENT + 20, 780, 250, 50), border_radius=3)
        positions = [x + INDENT for x in [26, 64, 102, 140, 178, 216]][:max_hp]

    counter = 1
    for i in positions:
        if counter <= hp_value:
            screen.blit(hp_hearts['full'], (i, 792))
        elif 1 > hp_value - counter + 1 > 0:
            screen.blit(hp_hearts['touched'], (i, 792))
        else:
            screen.blit(hp_hearts['empty'], (i, 792))
        counter += 1


if __name__ == '__main__':
    pygame.display.set_caption('Battle Time!')
    run = True

    while run:

        clock.tick(FPS)

        draw_background()
        draw_panel()
        draw_hp(enemy=False, hp_value=3.5, max_hp=6)
        draw_hp(enemy=True, hp_value=1.5, max_hp=3)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()
