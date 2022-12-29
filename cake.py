import pygame
import sys

pygame.init()
size = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(size)
load_image = pygame.image.load
FPS = 50
pictures = ['cake1', 'cake2', 'cake3']
cake_height = 50
cake_width = 5


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
        string_rendered = font.render(line, False, pygame.Color('black'))
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


class Cake:
    def __init__(self, x, y, size_cake, picture):
        self.cake1 = pygame.sprite.Group()
        self.flag = 0
        self.status = True
        for i in range(size_cake // 5):
            cake1 = pygame.sprite.Sprite(self.cake1)
            cake1.image = load_image(f'pictures/{picture}.png')
            cake1.rect = cake1.image.get_rect()
            cake1.rect.x = x + i * 5
            cake1.rect.y = y

    def change_status(self):
        self.status = False
        if cakes:
            for piece in self.cake1:
                if piece.rect.x < cakes[-1].cake1.sprites()[0].rect.x:
                    piece.kill()
                if piece.rect.x > cakes[-1].cake1.sprites()[-1].rect.x:
                    piece.kill()

    def draw(self, screen):
        self.cake1.draw(screen)
        if self.status:
            self.move()

    def move(self):
        if self.cake1.sprites()[-1].rect.x + 10 > 800:
            self.flag = 1
        elif self.cake1.sprites()[0].rect.x - 5 < 0:
            self.flag = 0
        for i in self.cake1:
            if self.flag == 0:
                i.rect.x += 5
            else:
                i.rect.x -= 5
        if count_cakes != 0:
            self.count_height(count_cakes)

    def shift_down(self):
        for piece in self.cake1:
            piece.rect.y += 50

    def count_height(self, count_cakes):
        font = pygame.font.Font(None, 50)
        text = font.render(str(count_cakes), True, (0, 0, 0))
        text_x = 350
        text_y = 0
        screen.blit(text, (text_x, text_y))


size_cake = 200
cake_number = 0
active_cake = Cake(0, 550, size_cake, pictures[cake_number])
cakes = []
tower_height = 0
start_screen()
clock = pygame.time.Clock()
running = True
fps = 30
moving = 10
pos = (390, 380)
count_cakes = 0
while running:
    screen.fill((255, 255, 255))
    for cake in cakes:
        cake.draw(screen)
    active_cake.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                active_cake.change_status()
                cakes.append(active_cake)
                if cakes[-1].cake1:
                    size_cake = cakes[-1].cake1.sprites()[-1].rect.x + 5 - cakes[-1].cake1.sprites()[
                        0].rect.x
                    count_cakes += 1
                    active_cake.count_height(count_cakes)
                if not cakes[-1].cake1:
                    print('Game over')
                    exit(0)
                if tower_height >= 7:
                    cakes.pop(0)
                    for cake in cakes:
                        cake.shift_down()
                else:
                    tower_height += 1
                cake_number += 1
                active_cake = Cake(0, 550 - tower_height * 50, size_cake, pictures[cake_number % 3])
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                active_cake.change_status()
                cakes.append(active_cake)
                if cakes[-1].cake1:
                    size_cake = cakes[-1].cake1.sprites()[-1].rect.x + 5 - cakes[-1].cake1.sprites()[
                        0].rect.x
                if not cakes[-1].cake1:
                    print('Game over')
                    exit(0)
                if tower_height >= 7:
                    cakes.pop(0)
                    for cake in cakes:
                        cake.shift_down()
                else:
                    tower_height += 1
                cake_number += 1
                active_cake = Cake(0, 550 - tower_height * 50, size_cake, pictures[cake_number % 3])

    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
