import pygame
import sys
from random import randint, choice
from enum import Enum


def terminate():
    pygame.quit()
    sys.exit()


class Status(Enum):
    START = 1
    RUN = 2
    FINISH = 3


class QuestGame:
    def __init__(self, fon, pictures, ids):
        self.status = Status.RUN
        self.clues = pygame.sprite.Group()
        self.clothes = pygame.sprite.Group()
        self.screen = pygame.display.get_surface()
        self.screen_size = pygame.display.get_surface().get_size()
        self.fon = pygame.transform.scale(pygame.image.load(fon),
                                          self.screen_size)
        self.pictures = pictures
        self.clues_dct = ids
        self.found_clues = []
        self.cl_id_dct = {}
        for pic in self.clues_dct:
            clue = pygame.sprite.Sprite(self.clues)
            clue.image = pygame.image.load(pic)
            clue.rect = clue.image.get_rect()
            clue.rect.x = randint(0, self.screen_size[0] - clue.rect.width)
            clue.rect.y = randint(0, self.screen_size[1] - clue.rect.height)
            self.cl_id_dct[clue] = self.clues_dct[pic]
            pic = choice(pictures)
            cloth = pygame.sprite.Sprite(self.clothes)
            cloth.image = pygame.image.load(pic)
            cloth.rect = cloth.image.get_rect()
            cloth.rect.center = clue.rect.center
        for i in range(15):
            pic = choice(pictures)
            cloth = pygame.sprite.Sprite(self.clothes)
            cloth.image = pygame.image.load(pic)
            cloth.rect = cloth.image.get_rect()
            cloth.rect.x = randint(0, self.screen_size[0] - cloth.rect.width)
            cloth.rect.y = randint(0, self.screen_size[1] - cloth.rect.height)

    def find_sprite(self, mouse_pos):
        for i in range(len(self.clothes) - 1, -1, -1):
            if self.clothes.sprites()[i].rect.collidepoint(mouse_pos):
                return self.clothes.sprites()[i]

    def clue_pressed(self, mouse_pos):
        for clue in self.clues:
            if clue.rect.collidepoint(mouse_pos):
                return clue

    def draw(self):
        clock = pygame.time.Clock()
        moving = False
        while True:
            self.screen.blit(self.fon, (0, 0))
            self.clues.draw(self.screen)
            self.clothes.draw(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos
                    sprite = self.find_sprite(mouse_pos)
                    if sprite:
                        moving = True
                    else:
                        if self.clue_pressed(mouse_pos):
                            clue = self.clue_pressed(mouse_pos)
                            self.found_clues.append(self.cl_id_dct[clue])
                            clue.kill()
                            if len(self.found_clues) == len(self.clues_dct):
                                self.status = Status.FINISH
                                return
                if event.type == pygame.MOUSEMOTION:
                    if moving:
                        sprite.rect.center = event.pos
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    moving = False
            pygame.display.flip()
            # pygame.time.wait(500)
            # if not self.move():
            #     return
            # clock.tick(self.fps)

    def run(self):
        while True:
            if self.status == Status.RUN:
                self.draw()
            elif self.status == Status.FINISH:
                return


def main():
    pygame.init()
    size = 800, 600
    pygame.display.set_mode(size)
    game = QuestGame('pictures/basket_fon.jpg',
                     ['pictures/ert.jpg.png', 'pictures/ert.png', 'pictures/rty.png'],
                     {'pictures/wer.png': 1})
    game.run()
    pygame.quit()


if __name__ == '__main__':
    main()
