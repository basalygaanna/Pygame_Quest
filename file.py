import pygame
import sys

pygame.init()
size = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(size)
load_image = pygame.image.load
FPS = 50
pictures = ['cake1', 'cake2', 'cake3']


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Чем выше, тем лучше!"]

    fon = pygame.transform.scale(load_image('pictures/fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    clock = pygame.time.Clock()
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def render(self, pos):
        screen.blit(load_image('data/mar.png'), pos)
        self.rect.x, self.rect.y = pos

    def check(self, pos):
        self.rect.x, self.rect.y = pos
def show_pic():


start_screen()
clock = pygame.time.Clock()
running = True
fps = 30
moving = 10
pos = (390, 380)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.type == pygame.KEYDOWN:
                if event.key == 3:
                    show_pic()
    screen.fill((0, 0, 0))
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
