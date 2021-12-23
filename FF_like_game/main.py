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


def draw_hp(enemy: bool, hp_value: float, max_hp: int, offset: int):

    # not sure if loading files by every frame isn't right for efficiency
    hp_hearts = {
        'full': pygame.image.load('img/icons/heart-sketch.png').convert_alpha(),
        'touched': pygame.image.load('img/icons/heart.png').convert_alpha(),
        'empty': pygame.image.load('img/icons/broken-heart.png').convert_alpha()
    }

    if enemy:
        pygame.draw.rect(screen, '#D5D9DC', (SCREEN_WIDTH - 20 - INDENT - 250, 770 + offset, 250, 50), border_radius=3)
        positions = [SCREEN_WIDTH - x - INDENT - 25 for x in [26, 64, 102, 140, 178, 216]][:max_hp]
    else:
        pygame.draw.rect(screen, '#D5D9DC', (INDENT + 20, 770 + offset, 250, 50), border_radius=3)
        positions = [x + INDENT for x in [26, 64, 102, 140, 178, 216]][:max_hp]

    counter = 1
    for i in positions:
        if counter <= hp_value:
            screen.blit(hp_hearts['full'], (i, 782 + offset))
        elif 1 > hp_value - counter + 1 > 0:
            screen.blit(hp_hearts['touched'], (i, 782 + offset))
        else:
            screen.blit(hp_hearts['empty'], (i, 782 + offset))
        counter += 1


class Character():
    def __init__(self, x, y, sprite, max_hp, strength, med_packs, reverse=False):
        self.sprite = sprite
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_med_packs = med_packs
        self.med_packs = med_packs
        self.alive = True
        img = pygame.image\
            .load(f'img/characters/{self.sprite}/idle/cultist_priest_idle_1.png')\
            .convert_alpha()
        img = pygame.transform.scale(img, (img.get_width() * 1.5, img.get_height() * 1.5))
        if reverse:
            img.set_alpha(200)
            img = pygame.transform.flip(img, True, False)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        screen.blit(self.image, self.rect)


if __name__ == '__main__':
    pygame.display.set_caption('Battle Time!')
    run = True

    cultist = Character(200, 600, 'cultist', 4, 16, 3, reverse=False)
    ghost_01 = Character(800, 600, 'cultist', 3, 8, 2, reverse=True)
    ghost_02 = Character(1000, 600, 'cultist', 3, 10, 1, reverse=True)
    enemy_list = [ghost_01, ghost_02]

    while run:

        clock.tick(FPS)

        draw_background()
        draw_panel()
        draw_hp(enemy=False, hp_value=3.5, max_hp=cultist.max_hp, offset=0)
        draw_hp(enemy=True, hp_value=1.5, max_hp=ghost_01.max_hp, offset=0)
        draw_hp(enemy=True, hp_value=2, max_hp=ghost_02.max_hp, offset=55)

        cultist.draw()
        ghost_01.draw()
        ghost_02.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()
