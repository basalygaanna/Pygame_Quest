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
        self.snake_size = 40
        screen_size = pygame.display.get_surface().get_size()
        self.screen_size = (
            screen_size[0] // self.snake_size * self.snake_size,
            screen_size[1] // self.snake_size * self.snake_size,
        )
        self.status = Status.START
        self.fps = 50
        self.direction = (0, 1)
        self.count = 0
        self.snakes = pygame.sprite.Group()
        self.candies = pygame.sprite.Group()
        for i in range(3):
            snake = pygame.sprite.Sprite(self.snakes)
            if i == 2:
                snake.image = pygame.image.load('pictures/snake_head.png')
            else:
                snake.image = pygame.image.load('pictures/snake_body.png')
            snake.rect = snake.image.get_rect()
            snake.rect.x = self.screen_size[0] // self.snake_size // 2 * self.snake_size
            snake.rect.y = self.screen_size[1] // self.snake_size // 2 * self.snake_size + \
                           i * self.snake_size
            if i == 2:
                self.head_x, self.head_y = snake.rect.x, snake.rect.y
        self.create_candy()

    def create_candy(self):
        candy = pygame.sprite.Sprite(self.candies)
        candy.image = pygame.image.load('pictures/candy.png')
        candy.rect = candy.image.get_rect()
        candy.rect.x, candy.rect.y = self.choose_place_of_candy()
        if pygame.sprite.spritecollideany(candy, self.snakes):
            for sprite in self.candies:
                sprite.kill()
            self.create_candy()

    def choose_place_of_candy(self):
        return randint(1, self.screen_size[0] // self.snake_size - 1) * self.snake_size, \
               randint(1, self.screen_size[1] // self.snake_size - 1) * self.snake_size

    def move(self):
        self.head_x += self.direction[0] * self.snake_size
        self.head_y += self.direction[1] * self.snake_size
        snake = pygame.sprite.Sprite()
        snake.image = pygame.image.load('pictures/snake_head.png')
        snake.rect = snake.image.get_rect()
        snake.rect.x = self.head_x
        snake.rect.y = self.head_y
        if pygame.sprite.spritecollideany(snake, self.candies):
            for sprite in self.candies:
                sprite.kill()
            self.create_candy()
            self.count += 1
        else:
            self.snakes.sprites()[0].kill()
        self.from_head_to_body()
        if pygame.sprite.spritecollideany(snake, self.snakes):
            self.status = Status.FINISH
            return False
        self.snakes.add(snake)
        if not 0 <= self.head_x <= self.screen_size[0] - 1 or \
                not 0 <= self.head_y <= self.screen_size[1] - 1:
            self.status = Status.FINISH
            return False
        return True

    def from_head_to_body(self):
        body = pygame.sprite.Sprite()
        body.image = pygame.image.load('pictures/snake_body.png')
        body.rect = body.image.get_rect()
        body.rect.x = self.snakes.sprites()[-1].rect.x
        body.rect.y = self.snakes.sprites()[-1].rect.y
        self.snakes.sprites()[-1].kill()
        self.snakes.add(body)

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
        fon = pygame.transform.scale(pygame.image.load('pictures/snake_gameover.jpeg'), self.screen_size)
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
