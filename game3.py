import pygame
import sys
from random import randint
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
        font = pygame.font.Font(None, 80)
        string_rendered = font.render(self.text, False, pygame.Color('black'))
        text_rect = string_rendered.get_rect()
        text_rect.x = self.rect.x + (self.rect.width - text_rect.width) // 2
        text_rect.y = self.rect.y + (self.rect.height - text_rect.height) // 2
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


class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.screen_size = pygame.display.get_surface().get_size()

    def move(self):
        pass

    def start_screen(self):
        intro_text = ["Съешь как можно больше конфет!"]
        fon = pygame.transform.scale(pygame.image.load('pictures/snake_fon.jpg'), self.screen_size)
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

    def draw(self):
        clock = pygame.time.Clock()
        while True:
            self.screen.fill((168, 182, 227))
            self.snakes.draw(self.screen)
            self.candies.draw(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    delta = 0
                    if event.key == pygame.K_RIGHT:
                        delta = self.direction[0] - self.direction[1]
                    elif event.key == pygame.K_LEFT:
                        delta = self.direction[1] - self.direction[0]
                    self.direction = (
                        (self.direction[0] + delta) * ((self.direction[0] + delta) % 2),
                        (self.direction[1] + delta) * ((self.direction[1] + delta) % 2),
                    )

            pygame.display.flip()
            pygame.time.wait(500)
            if not self.move():
                return
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
        intro_text = [f'{self.count}', 'Game over']
        fon = pygame.transform.scale(pygame.image.load('pictures/snake_gameover.jpeg'),
                                     self.screen_size)
        self.screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 130)
        clock = pygame.time.Clock()
        text_coord_y = 0
        for line in intro_text:
            string_rendered = font.render(line, False, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            intro_rect.x = (self.screen_size[0] - intro_rect.width) // 2
            intro_rect.y = self.screen_size[1] // 8 + text_coord_y
            self.screen.blit(string_rendered, intro_rect)
            text_coord_y += 130
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
    game = SnakeGame()
    game.run()
    pygame.quit()


if __name__ == '__main__':
    main()
