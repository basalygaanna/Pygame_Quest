import pygame, random, sqlite3, sys


class Board:
    # создание поля
    def __init__(self, width, height):

        self.width = width

        self.height = height

        self.board = [[0] * width for _ in range(height)]

        # значения по умолчанию

        self.left = 0

        self.top = 0

        self.cell_size = 40

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

                else:
                    pygame.draw.rect(screen, (255, 255, 255), coord, 1)

    def get_cell(self, coord):
        x, y = coord[0] - self.left, coord[1] - self.top

        if self.width * self.cell_size > x >= 0 and self.height * self.cell_size > y >= 0:

            x, y = x // self.cell_size, y // self.cell_size

            self.board[y][x] = (self.board[y][x] + 1) % 5

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

            else:
                self.cake = 1
            print(self.cake)

            return True

        else:
            print(False)
            return False


def draw(screen):
    screen.fill((0, 0, 0))


class Arrow:
    def __init__(self, pos):
        self.s = 0
        self.cs = 20
        coord = (pos[0], pos[1], self.cs * 2, self.cs)
        pygame.draw.rect(screen, (255, 0, 0), coord)

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

        else:
            print('notcool')

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
    runt = 40

    board = Board(30, 25)

    player, pos = Arrow((100, 100)), (100, 100)

    while running:

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

        if player.get_go() == 's' and fl[0]:
            if not board.get_col(pos) or board.cake == 4:
                if board.cake == 4:
                    player.game_over()
                pos = pos[0], pos[1] + runt

        if player.get_go() == 'w' and fl[1]:
            if not board.get_col(pos) or board.cake == 4:
                if board.cake == 4:
                    player.game_over()
                pos = pos[0], pos[1] - runt

        if player.get_go() == 'a' and fl[2]:
            if not board.get_col(pos) or board.cake == 4:
                if board.cake == 4:
                    player.game_over()
                pos = pos[0] - runt, pos[1]

        if player.get_go() == 'd' and fl[3]:
            if not board.get_col(pos) or board.cake == 4:
                if board.cake == 4:
                    player.game_over()
                pos = pos[0] + runt, pos[1]

        screen.fill((0, 0, 0))

        board.render(screen)

        player.render(pos)

        clock.tick(FPS)

        pygame.display.flip()

    # завершение работы:
    pygame.quit()