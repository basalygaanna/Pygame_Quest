import pygame
import sys
from random import choice
from enum import Enum


def terminate():
    pygame.quit()
    sys.exit()


class Status(Enum):
    START = 1
    RUN = 2
    FINISH = 3
    RESTART = 4
    QUIT = 5


class Button:
    def __init__(self, x, y, status, text='', color='white'):
        self.x = x
        self.y = y
        self.switch_status = status
        self.text = text
        self.default_color = color
        self.color = color
        self.rect = None

    def draw(self, screen):
        self.rect = pygame.draw.rect(screen, self.color, (self.x, self.y, 300, 100), 0)
        self.color = self.default_color
        font = pygame.font.SysFont("chiller", 80)
        string_rendered = font.render(self.text, False, pygame.Color('purple'))
        text_rect = string_rendered.get_rect()
        text_rect.x = self.rect.x + (self.rect.width - text_rect.width) // 2
        text_rect.y = self.rect.y
        screen.blit(string_rendered, text_rect)

    def on_hoover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.color = '#666666'
            # 'pressed': '#333333',
            return True
        return False

    def pressed(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed():
            return True, self.switch_status
        return False, False


class Cake:
    def __init__(self, screen_size, tower_height, cake_size, picture):
        self.screen_size = screen_size
        self.cake_height = 50
        self.cake_width = 5
        self.cake1 = pygame.sprite.Group()
        self.flag = 0
        self.active = True
        for i in range(cake_size // self.cake_width):
            cake1 = pygame.sprite.Sprite(self.cake1)
            cake1.image = pygame.image.load(f'pictures/{picture}.png')
            cake1.rect = cake1.image.get_rect()
            cake1.rect.x = i * self.cake_width
            cake1.rect.y = screen_size[1] - (tower_height + 1) * self.cake_height

    def change_status(self, cakes):
        self.active = False
        if cakes:
            for piece in self.cake1:
                if piece.rect.x < cakes[-1].cake1.sprites()[0].rect.x:
                    piece.kill()
                if piece.rect.x > cakes[-1].cake1.sprites()[-1].rect.x:
                    piece.kill()

    def draw(self, screen):
        self.cake1.draw(screen)
        if self.active:
            self.move()

    def move(self):
        if self.cake1.sprites()[-1].rect.x + 10 > self.screen_size[0]:
            self.flag = 1
        elif self.cake1.sprites()[0].rect.x - 3 < 0:
            self.flag = 0
        for i in self.cake1:
            if self.flag == 0:
                i.rect.x += 3
            else:
                i.rect.x -= 3

    def shift_down(self):
        for piece in self.cake1:
            piece.rect.y += self.cake_height


class CakeGame:
    @staticmethod
    def get_picture():
        return choice(['cake1', 'cake2', 'cake3'])

    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.screen_size = pygame.display.get_surface().get_size()
        self.cake_size = 200
        self.tower_height = 0
        self.active_cake = Cake(
            self.screen_size,
            self.tower_height,
            self.cake_size,
            self.get_picture()
        )
        self.cakes = []
        self.status = Status.START
        self.count_cakes = 0
        self.fps = 50

    def start_screen(self):
        intro_text = ["Чем выше, тем лучше!"]
        fon = pygame.transform.scale(pygame.image.load('pictures/fon.jpg'), self.screen_size)
        self.screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 40)
        clock = pygame.time.Clock()
        for line in intro_text:
            string_rendered = font.render(line, False, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            intro_rect.x = 40
            intro_rect.y = self.screen_size[1] // 8
            self.screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    self.status = Status.RUN
                    return  # начинаем игру
            pygame.display.flip()
            clock.tick(self.fps)

    def count_height(self):
        font = pygame.font.Font(None, 50)
        text = font.render(str(self.count_cakes), True, (0, 0, 0))
        text_x = 350
        text_y = 0
        self.screen.blit(text, (text_x, text_y))

    def draw(self):
        clock = pygame.time.Clock()
        while True:
            self.screen.fill((255, 255, 255))
            for cake in self.cakes:
                cake.draw(self.screen)
            self.active_cake.draw(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or \
                        (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                    self.active_cake.change_status(self.cakes)
                    self.cakes.append(self.active_cake)
                    if self.cakes[-1].cake1:
                        self.cake_size = self.cakes[-1].cake1.sprites()[-1].rect.x + 5 - \
                                         self.cakes[-1].cake1.sprites()[
                                             0].rect.x
                        self.count_cakes += 1
                        self.count_height()
                    if not self.cakes[-1].cake1:
                        self.status = Status.FINISH
                        return

                    if self.tower_height >= self.screen_size[1] // 100:
                        self.cakes.pop(0)
                        for cake in self.cakes:
                            cake.shift_down()
                    else:
                        self.tower_height += 1
                    self.active_cake = Cake(
                        self.screen_size,
                        self.tower_height,
                        self.cake_size,
                        self.get_picture()
                    )
            pygame.display.flip()
            clock.tick(self.fps)

    def finish_screen(self):
        buttons = [
            Button(
                (self.screen_size[0] - 600) // 4,
                self.screen_size[1] - 150,
                Status.RESTART,
                'Play again',
            ),
            Button(
                (self.screen_size[0] - 600) // 4 * 3 + 300,
                self.screen_size[1] - 150,
                Status.QUIT,
                'Exit',
            )
        ]
        intro_text = [f'{self.count_cakes}', 'Game over']
        fon = pygame.transform.scale(pygame.image.load('pictures/gameover.jpg'), self.screen_size)
        self.screen.blit(fon, (0, 0))
        font = pygame.font.SysFont("chiller", 130)
        clock = pygame.time.Clock()
        text_coord_y = 0
        for line in intro_text:
            string_rendered = font.render(line, False, pygame.Color('purple'))
            intro_rect = string_rendered.get_rect()
            intro_rect.x = (self.screen_size[0] - intro_rect.width) // 2
            intro_rect.y = self.screen_size[1] // 6 + text_coord_y
            self.screen.blit(string_rendered, intro_rect)
            text_coord_y += 150
        for button in buttons:
            button.draw(self.screen)
        while True:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        pressed, status = button.pressed(mouse_pos)
                        if pressed:
                            self.status = status
                            return
                        # button.draw(self.screen)
            for button in buttons:
                button.on_hoover(mouse_pos)
                button.draw(self.screen)

            pygame.display.flip()
            clock.tick(self.fps)

    def run(self):
        while True:
            if self.status == Status.START:
                self.start_screen()
            elif self.status == Status.RUN:
                self.draw()
            elif self.status == Status.FINISH:
                self.finish_screen()
            elif self.status == Status.RESTART:
                self.__init__()
            else:
                return


def main():
    pygame.init()
    size = 800, 600
    pygame.display.set_mode(size)
    game = CakeGame()
    game.run()
    pygame.quit()


if __name__ == '__main__':
    main()
