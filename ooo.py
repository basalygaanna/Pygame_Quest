import pygame, random, sqlite3, sys
from enum import Enum
from cake import CakeGame
from snake import SnakeGame
from cake import Button


r = 1

class Status(Enum):
    START = 1
    RUN = 2
    LIST = 6
    CONT = 3
    SETTS = 4
    QUIT = 5

def start_game():
    intro_text = ['Заставка', '',
                  'Правила игры',
                  'Если в правилах несколько строк',
                  'прихется выводить их построчно']
    fon = pygame.transform.scale(pygame.image.load('pictures/strt_screen.png'))
    screen.blit(fon, (0, 0))
def List():
    screen.fill((255, 255, 255))
    intro_text = ['Список.', '',
                  'Короче змейка, ',
                  '1 фритайм,',
                  'Помочь Даше с тортом,',
                  '2 фритайм ',
                  'Принести все табуретки',
                  '3 фритайм,',
                  '4 фритайм.',
                  ]
    #fon = pygame.transform.scale(pygame.image.load('pictures/strt_screen.png'), (width, height))
    #screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    board.status = Status.RUN
                    return

        pygame.display.flip()
        clock.tick(FPS)
def load_image(im):
    return pygame.image.load(f'pictures/{im}')
def terminate():
    pygame.quit()
    sys.exit()


class Chara:
    def __init__(self):
        self.cr = 7
    def generate_friends(self, filename):
        chars = ['с', 'р', 'а', 'к', 'е', 'п', 'м', 'о', 'д']
        if player.lil_lock == 0:
            sl = ((3, 16), (3, 15), (24, 27), (8, 13), (8, 14), (11, 19), (18, 20), (3, 24), (18, 19))
        elif player.lil_lock == 1:
            sl = ((3, 16), (3, 15), (24, 27), (10, 13), (9, 15), (10, 19), (18, 20), (3, 24), (18, 19))
        elif player.lil_lock == 2:
            sl = ((3, 16), (3, 15), (24, 27), (10, 13), (9, 15), (10, 19), (18, 20), (3, 24), (18, 19))
        elif player.lil_lock == 3:
            sl = ((3, 16), (3, 15), (24, 27), (10, 13), (9, 15), (10, 19), (18, 20), (3, 24), (18, 19))
        elif player.lil_lock == 4:
            sl = ((3, 16), (3, 15), (24, 27), (10, 13), (9, 15), (10, 19), (0, 0), (3, 24), (18, 19))
        elif player.lil_lock == 5:
            sl = ((3, 16), (3, 15), (24, 27), (10, 13), (9, 15), (0, 0), (18, 20), (3, 24), (18, 19))
        with open((filename + '1'), 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        print(level_map)
        for i in range(len(chars)):
            print(sl[i][0], sl[i][1])
            print(level_map[sl[i][0]])
            print(chars[i])
            print(level_map[sl[i][0]][8])
            if sl[i] != (0, 0):
                level_map[sl[i][0]] = ''.join([level_map[sl[i][0]][:sl[i][1] -1], chars[i], level_map[sl[i][0]][sl[i][1]:]])
            print(level_map)
        with open(filename, 'w') as mapFile:
            for i in level_map:
                mapFile.write(i)
                mapFile.write('\n')





class Board:
    # создание поля
    def __init__(self, width, height):

        self.width = width

        self.height = height

        self.board = [[0] * width for _ in range(height)]

        self.board_condition = [[0] * width for _ in range(height)]

        # значения по умолчанию

        self.left = 0

        self.top = 0

        self.cell_size = 35

        self.x = 0
        self.y = 0

        self.status = Status.START
        self.carp2 = pygame.transform.scale(pygame.image.load('pictures/Ковер2.png'),
                                            (self.cell_size, self.cell_size))
        self.carp1 = pygame.transform.scale(pygame.image.load('pictures/Ковер1.png'),
                                            (self.cell_size, self.cell_size))
        self.floor1 = pygame.transform.scale(pygame.image.load('pictures/Пол1.png'),
                                             (self.cell_size, self.cell_size))
        self.floor2 = pygame.transform.scale(pygame.image.load('pictures/Пол2.png'),
                                             (self.cell_size, self.cell_size))
        self.carp3 = pygame.transform.scale(pygame.image.load('pictures/Ковер3.png'),
                                            (self.cell_size, self.cell_size))
        self.wall1 = pygame.transform.scale(pygame.image.load('pictures/Стена1.png'),
                                            (self.cell_size, 2 * self.cell_size))
        self.door1 = pygame.transform.scale(pygame.image.load('pictures/Дверь1.png'),
                                            (self.cell_size, 2 * self.cell_size))
        self.table1 = pygame.transform.scale(pygame.image.load('pictures/Стол1.png'),
                                             (self.cell_size, round(2.5 * self.cell_size)))
        self.table2 = pygame.transform.scale(pygame.image.load('pictures/Стол2.png'),
                                             (self.cell_size, round(1.5 * self.cell_size)))
        self.table3 = pygame.transform.scale(pygame.image.load('pictures/Стол3.png'),
                                             (3 * self.cell_size, 2 * self.cell_size))
        self.tabretk1 = pygame.transform.scale(pygame.image.load('pictures/Табуретка1.png'),
                                               (self.cell_size, round(1.5 * self.cell_size)))
        self.sofa1 = pygame.transform.scale(pygame.image.load('pictures/Диван1.png'),
                                            (5 * self.cell_size, round(2.5 * self.cell_size)))
        self.bed2 = pygame.transform.scale(pygame.image.load('pictures/Кровать2.png'),
                                           (self.cell_size, 2 * self.cell_size))
        self.bed1 = pygame.transform.scale(pygame.image.load('pictures/Кровать1.png'),
                                           (self.cell_size, round(2.125 * self.cell_size)))
        self.bed3 = pygame.transform.scale(pygame.image.load('pictures/Кровать3.png'),
                                           (2 * self.cell_size, round(1.25 * self.cell_size)))
        self.tmbk1 = pygame.transform.scale(pygame.image.load('pictures/Тумбочка1.png'),
                                            (self.cell_size, self.cell_size))
        self.chair1 = pygame.transform.scale(pygame.image.load('pictures/Стул1.png'),
                                             (self.cell_size, round(1.6 * self.cell_size)))
        self.chair2 = pygame.transform.scale(pygame.image.load('pictures/Стул2.png'),
                                             (self.cell_size, round(1.6 * self.cell_size)))
        self.chair3 = pygame.transform.scale(pygame.image.load('pictures/Стул3.png'),
                                             (self.cell_size, round(1.6 * self.cell_size)))
        self.ciniy = pygame.transform.scale(pygame.image.load('pictures/чел5.png'),
                                             (round(1.2 * self.cell_size), round(1.6 * self.cell_size)))
        self.Polly = pygame.transform.scale(pygame.image.load('pictures/чел14.png'),
                                             (self.cell_size, round(1.6 * self.cell_size)))
        self.Alice = pygame.transform.scale(pygame.image.load('pictures/чел7.png'),
                                            (self.cell_size, round(1.6 * self.cell_size)))
        self.Ketrin = pygame.transform.scale(pygame.image.load('pictures/чел8.png'),
                                            (self.cell_size, round(1.6 * self.cell_size)))
        self.Dasha = pygame.transform.scale(pygame.image.load('pictures/чел9.png'),
                                             (self.cell_size, round(1.6 * self.cell_size)))
        self.Egorik = pygame.transform.scale(pygame.image.load('pictures/чел10.png'),
                                            (self.cell_size, round(1.6 * self.cell_size)))
        self.Masha = pygame.transform.scale(pygame.image.load('pictures/чел11.png'),
                                             (self.cell_size, round(1.6 * self.cell_size)))
        self.Andrew = pygame.transform.scale(pygame.image.load('pictures/чел12.png'),
                                            (self.cell_size, round(1.6 * self.cell_size)))
        self.Roma = pygame.transform.scale(pygame.image.load('pictures/чел13.png'),
                                             (self.cell_size, round(1.6 * self.cell_size)))
        self.Mari = pygame.transform.scale(pygame.image.load('pictures/чел1.png'),
                                             (self.cell_size, round(1.6 * self.cell_size)))
        self.Mari2 = pygame.transform.scale(pygame.image.load('pictures/чел2.png'),
                                             (self.cell_size, round(1.6 * self.cell_size)))
        self.Mari3 = pygame.transform.scale(pygame.image.load('pictures/чел3.png'),
                                             (self.cell_size, round(1.6 * self.cell_size)))
        self.Mari4 = pygame.transform.scale(pygame.image.load('pictures/чел4.png'),
                                             (self.cell_size, round(1.6 * self.cell_size)))
    # настройка внешнего вида

    def draw(self, level):
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    wall1 = pygame.transform.scale(pygame.image.load('pictures/Ковер2.png'),
                                                    (board.cell_size, 1.5 * board.cell_size))
                    screen.blit(wall1, (x * self.cell_size, y * self.cell_size))




    def start_screen(self):
        name = []
        intro_text = ["                 Rhfcysq ntrcn", "",
                      "Раз, два три",
                      "Пять, скоро будем мы играть,"]

        fon = pygame.transform.scale(load_image('strt_screen.png'), (width, height))
        screen.blit(fon, (0, 0))
        i = 0
        fonti = pygame.font.Font(None, 120)
        font = pygame.font.Font(None, 50)
        text_coord = 50
        for line in intro_text:
            if i == 0:
                string_rendered = fonti.render(line, 1, pygame.Color('red'))
            else:
                string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            i += 1
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        buttons = [
            Button(
                (width - 300) // 2,
                height - 700,
                Status.RUN,
                'Новая игра',
            ),
            Button(
                (width - 300) // 2,
                height - 550,
                Status.CONT,
                'Продолжить игру',
            ),
            Button(
                (width - 300) // 2,
                height - 400,
                Status.SETTS,
                'Настройки',
            ),
            Button(
                (width - 300) // 2,
                height - 250,
                Status.QUIT,
                'Выйти',
            )
        ]
        for button in buttons:
            button.draw(screen)
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
                            if self.status == Status.RUN:
                                self.start_log()
                            return
                        # button.draw(self.screen)
            for button in buttons:
                button.on_hoover(mouse_pos)
                button.draw(screen)

            pygame.display.flip()
            clock.tick(FPS)

    def start_log(self):
        con = sqlite3.connect('log_base')
        cur = con.cursor()
        f = cur.execute(f'''SELECT logs FROM logs where id = 1''').fetchall()
        font = pygame.font.Font(None, 50)
        f = f[0][0]
        '''try:
            f = f[0][0].split('\n')[self.dg]
        except Exception:
            print(3)
            return
        if self.step >= 50:
            return
        self.step = self.step + 1
        print(f[0][0])
        text = font.render(f[:self.step], True, (100, 255, 100))'''
        print(f)
        text = font.render(f, True, (100, 255, 100))
        x = 680
        pygame.draw.rect(screen, (255, 255, 255), ((0, x - 2), (width, height - x)), 5)
        pygame.draw.rect(screen, (0, 0, 0), ((0 + 2, x), (width - 5, height - x - 5)))
        screen.blit(text, (60, x + 40))
        pygame.display.flip()

        while pygame.event.wait().type != pygame.KEYDOWN:
            pass

    def set_view(self, left, top, cell_size):
        self.left = left

        self.top = top

        self.cell_size = cell_size

    def render(self, screen, pos):


        # pygame.draw.circle(screen, (255, 255, 0), 70, 80)
        level = self.load_level(player.cur_pol)
        for y in range(self.height):

            for x in range(self.width):
                coord = (pos[0], pos[1], player.cs * 2, player.cs)

                if self.board[y][x] == 1:
                    pygame.draw.rect(screen, (0, 255, 0), coord)

                elif self.board[y][x] == 2:
                    pygame.draw.rect(screen, (255, 255, 0), coord)

                elif self.board[y][x] == 3:
                    pygame.draw.rect(screen, (0, 255, 255), coord)

                elif self.board[y][x] == 4:
                    pygame.draw.rect(screen, (255, 255, 255), coord)

                elif self.board[y][x] == 5:
                    pygame.draw.rect(screen, (0, 0, 255), coord)

                elif self.board[y][x] == 6:
                    pygame.draw.rect(screen, (255, 0, 255), coord)

                else:
                    pygame.draw.rect(screen, (255, 255, 255), coord, 1)
                try:
                    if level[y][x] == '.':
                        screen.blit(self.carp2, (x * self.cell_size, y * self.cell_size))
                    elif level[y][x] == ',':
                        screen.blit(self.carp1, (x * self.cell_size, y * self.cell_size))
                    elif level[y][x] == '^':
                        screen.blit(self.floor1, (x * self.cell_size, y * self.cell_size))
                    elif level[y][x] == '>':
                        screen.blit(self.floor2, (x * self.cell_size, y * self.cell_size))
                    elif level[y][x] == '*':
                        screen.blit(self.carp3, (x * self.cell_size, y * self.cell_size))
                except Exception:
                    pass

    def draw_level(self, level, pos):
        x, y = None, None
        for y in range(len(level)):
            for x in range(len(level[y])):
                try:
                    coord = (pos[0], pos[1], player.cs * 2, player.cs)

                    if player.get_go() == 's':
                        screen.blit(self.Mari, (coord[0], coord[1] - board.cell_size))
                    elif player.get_go() == 'w':
                        screen.blit(self.Mari2, (coord[0], coord[1] - board.cell_size))
                    elif player.get_go() == 'a':
                        screen.blit(self.Mari3, (coord[0], coord[1] - board.cell_size))
                    elif player.get_go() == 'd':
                        screen.blit(self.Mari4, (coord[0], coord[1] - board.cell_size))
                    else:
                        screen.blit(self.Mari, (coord[0], coord[1] - board.cell_size))
                    coord = (
                    self.left + x * self.cell_size, self.top + y * self.cell_size, self.cell_size, self.cell_size)
                    if level[y][x] == '@':
                        screen.blit(self.wall1, (x * self.cell_size, y * self.cell_size))
                    elif level[y][x] == 'd' and (not self.board_condition[y + 1][x] or self.board[y + 1][x] != 5):
                        screen.blit(self.door1, (x * self.cell_size, y * self.cell_size))
                    elif level[y][x] == 'C':
                        screen.blit(self.table1, (x * self.cell_size, (y - 0.5) * self.cell_size))
                    elif level[y][x] == 'c':
                        screen.blit(self.table2, (x * self.cell_size, (y + 0.5) * self.cell_size))
                    elif level[y][x] == 'o':
                        screen.blit(self.table3, (x * self.cell_size, (y  ) * self.cell_size))
                    elif level[y][x] == 't':
                        screen.blit(self.tabretk1, (x * self.cell_size, (y + 0.5) * self.cell_size))
                    elif level[y][x] == 'i':
                        screen.blit(self.sofa1, (x * self.cell_size, (y + 0.25) * self.cell_size))
                    elif level[y][x] == 'a':
                        screen.blit(self.bed2, (x * self.cell_size, y * self.cell_size))
                    elif level[y][x] == 'r':
                        screen.blit(self.bed1, (x * self.cell_size, (y - 0.125) * self.cell_size))
                    elif level[y][x] == 'v':
                        screen.blit(self.bed3, (x * self.cell_size, (y + 0.75) * self.cell_size))
                    elif level[y][x] == 'b':
                        screen.blit(self.tmbk1, (x * self.cell_size, (y + 1) * self.cell_size))
                    elif level[y][x] == 'e':
                        screen.blit(self.chair1, (x * self.cell_size, (y + 0.4) * self.cell_size))
                    elif level[y][x] == 'u':
                        screen.blit(self.chair2, (x * self.cell_size, (y + 0.8) * self.cell_size))
                    elif level[y][x] == 'w':
                        screen.blit(self.chair3, (x * self.cell_size, (y + 1.2) * self.cell_size))
                    elif level[y][x] == 'с':
                        screen.blit(self.ciniy, (x * self.cell_size, (y - 1) * self.cell_size))
                    elif level[y][x] == 'р':
                        screen.blit(self.Polly, (x * self.cell_size, (y - 1) * self.cell_size))
                    elif level[y][x] == 'а':
                        screen.blit(self.Alice, (x * self.cell_size, (y - 1) * self.cell_size))
                    elif level[y][x] == 'к':
                        screen.blit(self.Ketrin, (x * self.cell_size, (y - 1) * self.cell_size))
                    elif level[y][x] == 'е':
                        screen.blit(self.Egorik, (x * self.cell_size, (y - 1) * self.cell_size))
                    elif level[y][x] == 'п':
                        screen.blit(self.Andrew, (x * self.cell_size, (y - 1) * self.cell_size))
                    elif level[y][x] == 'м':
                        screen.blit(self.Masha, (x * self.cell_size, (y - 1) * self.cell_size))
                    elif level[y][x] == 'о':
                        screen.blit(self.Roma, (x * self.cell_size, (y - 1) * self.cell_size))
                    elif level[y][x] == 'д':
                        screen.blit(self.Dasha, (x * self.cell_size, (y - 1) * self.cell_size))
                    elif player.get_go() == 's' and level[y][x] == coord:
                        screen.blit(self.Mari, (coord[0], coord[1] - board.cell_size))
                    elif player.get_go() == 'w' and level[y][x] == coord:
                        screen.blit(self.Mari2, (coord[0], coord[1] - board.cell_size))
                    elif player.get_go() == 'a' and level[y][x] == coord:
                        screen.blit(self.Mari3, (coord[0], coord[1] - board.cell_size))
                    elif player.get_go() == 'd' and level[y][x] == coord:
                        screen.blit(self.Mari4, (coord[0], coord[1] - board.cell_size))
                    elif player.get_go() != 'd' and level[y][x] == coord:
                        screen.blit(self.Mari, (coord[0], coord[1] - board.cell_size))


                except Exception:
                    print('lo')


    def get_cell(self, coord):
        x, y = coord[0] - self.left, coord[1] - self.top

        if self.width * self.cell_size > x >= 0 and self.height * self.cell_size > y >= 0:

            x, y = x // self.cell_size, y // self.cell_size

            self.board[y][x] = (self.board[y][x] + 1) % 7

        else:
            print(None)

    def get_col(self, coord):

        x, y = coord[0] - self.left, coord[1] - self.top

        x, y = x // self.cell_size, y // self.cell_size
        self.cake = 0

        if player.get_go() == 'a':
            x -= 1

        elif player.get_go() == 's':
            y += 1

        elif player.get_go() == 'd':
            x += 1

        else:
            y -= 1
        print('get_col')

        print('lllol')
        self.add_cake = self.board_condition[y][x]
        print('adcac', self.add_cake)

        print(self.add_cake)
        if self.board[y][x]:
            print('cake')

            if self.board[y][x] == 2:
                self.cake = 2
                print('cake2')

            elif self.board[y][x] == 3:
                self.cake = 3

            elif self.board[y][x] == 4:
                self.cake = 4

            elif self.board[y][x] == 5:
                self.cake = 5

            elif self.board[y][x] == 6:
                self.cake = 6

            elif self.board[y][x] == 7:
                self.cake = 7

            elif self.board[y][x] == 8:
                self.cake = 8

            else:
                self.cake = 1
            print(self.cake)
            print(board.cake)

            self.x = x
            self.y = y

            return True

        else:
            print(False)
            self.x = x
            self.y = y
            return False


    def load_level(self, filename):

        # читаем уровень, убирая символы перевода строки
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

            # и подсчитываем максимальную длину
        max_width = max(map(len, level_map))

            # дополняем каждую строку пустыми клетками ('.')
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))
    def generate_level(self, level):
        item = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        chars = ['с', 'р', 'а', 'к', 'е', 'п', 'м', 'о', 'д']
        x, y = None, None
        for y in range(len(level)):
            for x in range(len(level[y])):
                try:
                    self.board_condition[y][x] = 0
                    if level[y][x] == '.':
                        self.board[y][x] = 0
                    elif level[y][x] in item:
                        self.board[y][x] = 2
                        self.board_condition[y][x] = level[y][x]
                        print(self.board_condition)
                    elif level[y][x] == '@':
                        self.board[y][x] = 1
                    elif level[y][x] == 's':
                        self.board[y][x] = 3
                    elif level[y][x] == '!':
                        self.board[y][x] = 4
                    elif level[y][x] == 'd':
                        self.board[y][x] = 5
                    elif level[y][x] == 'l':
                        self.board[y][x] = 6
                    elif level[y][x] in chars:
                        self.board[y][x] = 2
                        self.board_condition[y][x] = level[y][x]
                        print(level[y][x])
                except Exception:
                    print('lo')
        # вернем игрока, а также размер поля в клетках
        return x, y


def draw(screen):
    screen.fill((0, 0, 0))


class Arrow:
    def __init__(self, pos):
        self.cur_level = 'map'
        self.cur_texture = 'maptexturka'
        self.cur_pol = 'mappol'
        self.s = 0
        self.cs = 15
        self.timer = 0
        coord = (pos[0], pos[1], self.cs * 2, self.cs)
        pygame.draw.rect(screen, (25-5, 0, 0), coord)
        self.dg = 0
        self.lil_lock = 0
        self.big_lock = 0


    def get_go(self):
        if go[0]:
            return 's'

        if go[1]:
            return 'w'

        if go[2]:
            return 'a'

        if go[3]:
            return 'd'

    def render(self, pos):
        coord = (pos[0], pos[1], self.cs * 2, self.cs)

        if self.get_go() == 's':
            pygame.draw.rect(screen, (255, 0, 0), coord)


        elif self.get_go() == 'w':
            pygame.draw.rect(screen, (255, 255, 0), coord)

        elif self.get_go() == 'a':
            pygame.draw.rect(screen, (255, 0, 255), coord)

        elif self.get_go() == 'd':
            pygame.draw.rect(screen, (0, 255, 255), coord)

        else:
            pygame.draw.rect(screen, (0, 0, 255), coord)

    def do(self, screen, coord):
        print('do')

        if board.get_col(coord) and board.cake == 2:
            print('cool')
            if self.s:
                self.timerEvent()
                return
            self.i_can_speak(screen)

        elif board.get_col(coord) and board.cake == 3:
            print('coolest')
            self.SAVE()

        elif board.get_col(coord) and board.cake == 5:
            print('cooler')
            lx = []
            self.open_the_door(board.x, board.y, lx, lx)

        elif board.get_col(coord) and board.cake == 6:
            print('coolsta')
            self.oh_no_not_the_Stairs()

        else:
            print('notcool')


    def oh_no_not_the_Stairs(self):
        print('ayo the pizza here')
        if self.get_go() == 'd' and self.cur_level == 'map-1':
            board.generate_level(board.load_level('map'))
            self.cur_level = 'map'
            self.cur_texture = 'maptexturka'
            self.cur_pol = 'mappol'
        elif self.get_go() == 'd' and self.cur_level == 'map':
            board.generate_level(board.load_level('map-1'))
            self.cur_level = 'map-1'
            self.cur_texture = 'maptexturka-1'
            self.cur_pol = 'mappol-1'
        elif self.get_go() == 'w' and self.cur_level == 'map':
            board.generate_level(board.load_level('map2'))
            self.cur_level = 'map2'
            self.cur_texture = 'maptexturka2'
            self.cur_pol = 'mappol2'
        elif self.get_go() == 'w' and self.cur_level == 'map2':
            board.generate_level(board.load_level('map'))
            self.cur_level = 'map'
            self.cur_texture = 'maptexturka'
            self.cur_pol = 'mappol'




    def open_the_door(self, x, y, lx, ly):

        lx.append(x)
        ly.append(y)
        print(lx)
        print(board.add_cake)
        board.add_cake = not board.add_cake
        print(board.board_condition)
        board.board_condition[y][x] = not board.board_condition[y][x]
        if board.board[y][x - 1] == 5 and (y not in ly or x - 1 not in lx):
            print('wha?')
            self.open_the_door(x - 1, y, lx, ly)
        if board.board[y][x + 1] == 5 and (y not in ly or x + 1 not in lx):
            print('wha?')
            self.open_the_door(x + 1, y, lx, ly)
        if board.board[y - 1][x] == 5 and (y - 1 not in ly or x not in lx):
            print('wha?')
            self.open_the_door(x, y - 1, lx, ly)
        if board.board[y + 1][x] == 5 and (y + 1 not in ly or x not in lx):
            print('wha?')
            self.open_the_door(x, y + 1, lx, ly)

        print(board.add_cake)



    def terminate(self):
        pygame.quit()
        sys.exit()


    def LOAD(self):
        con = sqlite3.connect('savethefile')
        cur = con.cursor()
        sv = cur.execute("""SELECT saves FROM savethefile WHERE id IN (?)""", str(ind)).fetchall()[0][0].split()
        print(sv[0: 2])
        global pos
        pos = tuple(map(int, sv[0: 2]))
        self.render(pos)



        '''self.data.setText(sv[1])
        self.label_2.setText(sv[2])
        self.psswrd = sv[3]
        print(self.psswrd)
        self.progress.setValue(int(sv[4]))
        yu2.progress.setValue(int(sv[4]))
        lk.pc = 'def_log.txt'
        if lk.lock == 0:
            ex.hide()
            wn.show()
            wn.label.setText('Что?')
        wn.textEdit.setText()'''


    def game_over(self):
        pygame.draw.rect(screen, (0, 0, 0), ((0, 0), (width, height)))
        font = pygame.font.Font(None, 100)
        r = random.randint(1, 20)
        print('pl')
        print(r)


        text = font.render("Это конец. Выходи.", True, (100, 255, 100))
        text_x = width // 2 - text.get_width() // 2
        text_y = height // 2 - text.get_height() // 2
        screen.blit(text, (text_x, text_y))
        pygame.display.flip()

        while pygame.event.wait().type != pygame.QUIT:
            pass

        self.terminate()

        screen.blit(text, (60, 40))

    def SAVE(self):

        con = sqlite3.connect('savethefile')
        cur = con.cursor()
        svl = []

        svl.append(' '.join(list(map(str, pos))))
        svl.append(str(board))
        svl = '\n'.join(svl)

        ind = 0
        x = 680
        font = pygame.font.Font(None, 70)

        text_coord = 680
        pygame.draw.rect(screen, (255, 255, 255), ((0, x - 2), (width, height - x)), 5)
        pygame.draw.rect(screen, (0, 0, 0), ((0 + 2, x), (width - 5, height - x - 5)))

        text = ("Выберите файл для сохранения", '(Нажмите кпопку 1, 2 или 3 для выбора)',
                '(или 0 или Enter для отмены)')

        for line in text:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()

            text_coord += 10
            intro_rect.top = text_coord

            intro_rect.x = 10
            text_coord += intro_rect.height

            screen.blit(string_rendered, intro_rect)

        while True:
            print(player.timer)
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.terminate()

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_1:
                        f = cur.execute('DELETE from savethefile WHERE id == 1')
                        result = cur.execute('INSERT INTO savethefile(id, saves) VALUES(1, ?)', (svl,))
                        con.commit()
                        con.close()

                        return  # начинаем игру

                    elif event.key == pygame.K_2:
                        f = cur.execute('DELETE from savethefile WHERE id == 2')
                        result = cur.execute('INSERT INTO savethefile(id, saves) VALUES(2, ?)', (svl,))
                        con.commit()
                        con.close()

                        return  # начинаем игру

                    elif event.key == pygame.K_3:
                        f = cur.execute('DELETE from savethefile WHERE id == 3')
                        result = cur.execute('INSERT INTO savethefile(id, saves) VALUES(3, ?)', (svl,))
                        con.commit()
                        con.close()

                        return  # начинаем игру

                    elif event.key == pygame.K_0 or event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:

                        return  # начинаем игру

            pygame.display.flip()
            clock.tick(FPS)



    def next_log(self):
        self.step = 0
        self.dg += 1

    def timerEvent(self):
        con = sqlite3.connect('log_base')
        cur = con.cursor()
        f = cur.execute('''SELECT mod FROM mod where id = 1''').fetchall()
        font = pygame.font.Font(None, 100)
        try:
            f = f[0][0].split('\n')[self.dg]
        except Exception:
            print(3)
            return
        if self.step >= 50:
            return
        self.step = self.step + 1
        print(f[0][0])
        text = font.render(f[:self.step], True, (100, 255, 100))
        print(f)

    def doActionu(self):
        self.timer.start(70, self)


    def i_can_speak(self, screen):
        if board.add_cake == 0:
            font = pygame.font.Font(None, 100)
            r = random.randint(1, 20)
            print('pl')
            print(r)

            if r <= 5:
                text = font.render("Это диалог", True, (100, 255, 100))

            elif r <= 10:
                text = font.render("Это диалг", True, (100, 255, 100))

            elif r <= 13:
                text = font.render("Этот диалог", True, (100, 255, 100))

            elif r <= 16:
                text = font.render("Это диалог...", True, (100, 255, 100))

            elif r <= 19:
                text = font.render("Это диалог :)", True, (100, 255, 100))

            else:
                text = font.render("Это конец. Выходи.", True, (100, 255, 100))
                text_x = width // 2 - text.get_width() // 2
                text_y = height // 2 - text.get_height() // 2
                screen.blit(text, (text_x, text_y))
                pygame.display.flip()

                while pygame.event.wait().type != pygame.QUIT:
                    pass
                self.terminate()
            x = 680
            pygame.draw.rect(screen, (255, 255, 255), ((0, x - 2), (width, height - x)), 5)
            pygame.draw.rect(screen, (0, 0, 0), ((0 + 2, x), (width - 5, height - x - 5)))
            screen.blit(text, (60, x + 40))
            pygame.display.flip()

            while pygame.event.wait().type != pygame.KEYDOWN:
                pass
        else:
            k = ''
            item = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                    'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
            chars = ['с', 'р', 'а', 'к', 'е', 'п', 'м', 'о', 'д']
            for i in range(len(item)):
                if item[i] == board.add_cake:
                    k = str(i)
                    break
            else:
                for i in range(len(chars)):
                    if chars[i] == board.add_cake:
                        k = str(i + 1)

                if self.lil_lock == 1 or self.lil_lock == 3 or self.lil_lock == 4:
                    f = 'фритайм'
                    font = pygame.font.Font(None, 50)
                    f = f[0][0]
                    print(f)
                    text = font.render(f, True, (100, 255, 100))
                    x = 680
                    pygame.draw.rect(screen, (255, 255, 255), ((0, x - 2), (width, height - x)), 5)
                    pygame.draw.rect(screen, (0, 0, 0), ((0 + 2, x), (width - 5, height - x - 5)))
                    screen.blit(text, (60, x + 40))
                    pygame.display.flip()
                    with open('freetime', 'w') as mapFile:
                        mapFile.write(k)
                    self.lil_lock += 1
                    if self.lil_lock == 5:
                        self.big_lock += 1
                    chr.generate_friends('map')
                    chr.generate_friends('maptexturka')


                    while pygame.event.wait().type != pygame.KEYDOWN:
                        pass
                    return
                else:
                    con = sqlite3.connect('log_base')
                    cur = con.cursor()
                    f = cur.execute(f'''SELECT mod FROM mod where id = {k}''').fetchall()
                    font = pygame.font.Font(None, 50)
                    f = f[0][0]
                    '''try:
                        f = f[0][0].split('\n')[self.dg]
                    except Exception:
                        print(3)
                        return
                    if self.step >= 50:
                        return
                    self.step = self.step + 1
                    print(f[0][0])
                    text = font.render(f[:self.step], True, (100, 255, 100))'''
                    print(f)
                    text = font.render(f, True, (100, 255, 100))
                    x = 680
                    pygame.draw.rect(screen, (255, 255, 255), ((0, x - 2), (width, height - x)), 5)
                    pygame.draw.rect(screen, (0, 0, 0), ((0 + 2, x), (width - 5, height - x - 5)))
                    screen.blit(text, (60, x + 40))
                    pygame.display.flip()

                    while pygame.event.wait().type != pygame.KEYDOWN:
                        pass

                    return
            print('k', k, 'self.lil_lock', self.lil_lock)
            if k == '18' and (self.lil_lock == 0 or self.lil_lock == 1):
                game = SnakeGame()
                game.run()
                self.lil_lock = 1
                chr.generate_friends('map')
                chr.generate_friends('maptexturka')

            elif k == '18' and (self.lil_lock == 2 or self.lil_lock == 3):
                game = CakeGame()
                game.run()
                if self.lil_lock <= 3:
                    self.lil_lock = 3
                chr.generate_friends('map')
                chr.generate_friends('maptexturka')
            else:
                con = sqlite3.connect('log_base')
                cur = con.cursor()
                f = cur.execute(f'''SELECT lettuce FROM lettuce where id = {k}''').fetchall()
                font = pygame.font.Font(None, 50)
                f = f[0][0]
                '''try:
                    f = f[0][0].split('\n')[self.dg]
                except Exception:
                    print(3)
                    return
                if self.step >= 50:
                    return
                self.step = self.step + 1
                print(f[0][0])
                text = font.render(f[:self.step], True, (100, 255, 100))'''
                print(f)
                text = font.render(f, True, (100, 255, 100))
                x = 680
                pygame.draw.rect(screen, (255, 255, 255), ((0, x - 2), (width, height - x)), 5)
                pygame.draw.rect(screen, (0, 0, 0), ((0 + 2, x), (width - 5, height - x - 5)))
                screen.blit(text, (60, x + 40))
                pygame.display.flip()

                while pygame.event.wait().type != pygame.KEYDOWN:
                    pass




if __name__ == '__main__':
    # инициализация Pygame:

    pygame.init()
    # размеры окна:
    fl = [0, 0, 0, 0]
    go = [0, 0, 0, 0]

    chr = Chara()

    clock = pygame.time.Clock()
    flag = False

    size = width, height = 1600, 1000
    FPS = 10

    screen = pygame.display.set_mode(size)

    running = True
    runt = 35

    board = Board(30, 30)

    player, pos = Arrow((70, 70)), (526, 491)
    chr.generate_friends('map')
    chr.generate_friends('maptexturka')
    board.start_screen()

    level_x, level_y = board.generate_level(board.load_level('map'))



    while running:
        if board.status == Status.RUN:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    flag = True
                    p_s = event.pos
                    board.get_cell(p_s)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z or event.key == pygame.K_RETURN:
                        player.do(screen, pos)

                    if event.key == pygame.K_q:
                        player.s = 1
                        player.do(screen, pos)

                    if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                        FPS = FPS + 100

                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        fl[0] = 1
                        go = [0, 0, 0, 0]
                        go[0] = 1

                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        fl[1] = 1
                        go = [0, 0, 0, 0]
                        go[1] = 1

                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        fl[2] = 1
                        go = [0, 0, 0, 0]
                        go[2] = 1

                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        fl[3] = 1
                        go = [0, 0, 0, 0]
                        go[3] = 1

                    if event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3:

                        if event.key == pygame.K_1:
                            ind = 1
                            player.LOAD()

                        elif event.key == pygame.K_2:
                            ind = 2
                            player.LOAD()

                        else:
                            ind = 3
                            player.LOAD()

                    if event.key == pygame.K_4:
                        game = CakeGame()
                        game.run()

                    if event.key == pygame.K_0:
                        board.status = Status.LIST

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                        FPS = FPS - 100

                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        fl[0] = 0

                    if event.key == pygame.K_UP or event.key == pygame.K_w:

                        fl[1] = 0

                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        fl[2] = 0

                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        fl[3] = 0
            ps = board.board_condition[board.y][board.x]
            print('ps', ps)
            if player.get_go() == 's' and fl[0]:

                if not board.get_col(pos) or board.cake == 4 or (board.cake == 5 and ps):
                    if board.cake == 4:
                        player.game_over()
                    pos = pos[0], pos[1] + runt

            if player.get_go() == 'w' and fl[1]:

                if not board.get_col(pos) or board.cake == 4 or (board.cake == 5 and ps):

                    if board.cake == 4:
                        player.game_over()
                    pos = pos[0], pos[1] - runt

            if player.get_go() == 'a' and fl[2]:

                if not board.get_col(pos) or board.cake == 4 or (board.cake == 5 and ps):

                    if board.cake == 4:
                        player.game_over()

                    pos = pos[0] - runt, pos[1]

            if player.get_go() == 'd' and fl[3]:

                if not board.get_col(pos) or board.cake == 4 or (board.cake == 5 and ps):

                    pos = pos[0] + runt, pos[1]

                    if board.cake == 4:
                        player.game_over()



            screen.fill((0, 0, 0))

            #board.draw(board.load_level('maptexturka'))

            player.timer += 1

            board.render(screen, pos)

            player.render(pos)

            board.draw_level(board.load_level(player.cur_texture), pos)

            clock.tick(FPS)
            print(player.cur_texture)
            print(player.cur_pol)

            pygame.display.flip()
        elif board.status == Status.QUIT:
            terminate()
        elif board.status == Status.LIST:
            List()
        else:
            board.start_screen()


    # завершение работы:
    pygame.quit()