import pygame, random, sqlite3, sys
from enum import Enum
r = 1
class Status(Enum):
    otrun = 1
    START = 2
    RUN = 3
    FINISH = 4
    RESTART = 5
    QUIT = 6


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
        return random.choice(['cake1', 'cake2', 'cake3'])

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

        while r == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    player.terminate()
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
    size = 800, 800
    pygame.display.set_mode(size)
    game = CakeGame()
    game.run()


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

    # настройка внешнего вида

    def set_view(self, left, top, cell_size):
        self.left = left

        self.top = top

        self.cell_size = cell_size

    def render(self, screen):

        # pygame.draw.circle(screen, (255, 255, 0), 70, 80)
        for y in range(self.height):

            for x in range(self.width):

                coord = (self.left + x * self.cell_size, self.top + y * self.cell_size, self.cell_size, self.cell_size)

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

                else:
                    pygame.draw.rect(screen, (255, 255, 255), coord, 1)


    def get_cell(self, coord):
        x, y = coord[0] - self.left, coord[1] - self.top

        if self.width * self.cell_size > x >= 0 and self.height * self.cell_size > y >= 0:

            x, y = x // self.cell_size, y // self.cell_size

            self.board[y][x] = (self.board[y][x] + 1) % 6

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

            else:
                self.cake = 1
            print(self.cake)
            print(board.cake)

            self.add_cake = self.board_condition[y][x]
            self.x = x
            self.y = y

            return True

        else:
            print(False)
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
        x, y = None, None
        for y in range(len(level)):
            for x in range(len(level[y])):
                try:
                    if level[y][x] == '.':
                        self.board[y][x] = 0
                    elif level[y][x] == '1':
                        self.board[y][x] = 2
                    elif level[y][x] == '@':
                        self.board[y][x] = 1
                    elif level[y][x] == 's':
                        self.board[y][x] = 3
                    elif level[y][x] == 'd':
                        self.board[y][x] = 5
                except Exception:
                    print('lo')
        # вернем игрока, а также размер поля в клетках
        return x, y


def draw(screen):
    screen.fill((0, 0, 0))


class Arrow:
    def __init__(self, pos):
        self.s = 0
        self.cs = 15
        self.timer = 0
        coord = (pos[0], pos[1], self.cs * 2, self.cs)
        pygame.draw.rect(screen, (255, 0, 0), coord)
        self.dg = 0

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
            self.open_the_door(coord)

        else:
            print('notcool')

    def open_the_door(self, coord):

        print(board.add_cake)
        board.add_cake = not board.add_cake
        print(coord)
        print(board.board_condition)
        board.board_condition[board.y][board.x] = not board.board_condition[board.y][board.x]
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


if __name__ == '__main__':
    # инициализация Pygame:

    pygame.init()
    # размеры окна:
    fl = [0, 0, 0, 0]
    go = [0, 0, 0, 0]

    clock = pygame.time.Clock()
    flag = False

    size = width, height = 1200, 1000
    FPS = 10

    screen = pygame.display.set_mode(size)

    running = True
    runt = 35

    board = Board(30, 30)

    player, pos = Arrow((70, 70)), (73, 75)

    level_x, level_y = board.generate_level(board.load_level('map'))

    while running:
        print(player.timer)
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
                    FPS = 20

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
                    main()

                if event.key == pygame.K_8:
                    board.generate_level(board.load_level('map-1'))

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    FPS = 10

                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    fl[0] = 0

                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    fl[1] = 0

                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    fl[2] = 0

                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    fl[3] = 0
        ps = board.board_condition[board.y][board.x]
        print(pos)
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

        player.timer += 1

        board.render(screen)

        player.render(pos)

        clock.tick(FPS)

        pygame.display.flip()

    # завершение работы:
    pygame.quit()