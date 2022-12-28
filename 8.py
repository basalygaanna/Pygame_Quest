import pygame, random


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

                else:
                    pygame.draw.rect(screen, (255, 255, 255), coord, 1)

    def get_cell(self, coord):
        x, y = coord[0] - self.left, coord[1] - self.top

        if self.width * self.cell_size > x >= 0 and self.height * self.cell_size > y >= 0:

            x, y = x // self.cell_size, y // self.cell_size

            self.board[y][x] = (self.board[y][x] + 1) % 4

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
            self.i_can_speak(screen)

        elif board.get_col(coord) and board.cake == 3:
            print('coolest')
            self.SAVE()

        else:
            print('notcool')

    def SAVE(self):
        print('Bagel')


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
            pygame.quit()
        x = 680
        pygame.draw.rect(screen, (255, 255, 255), ((0, x - 2), (1200, 2 * x + 5)), 5)
        pygame.draw.rect(screen, (0, 0, 0), ((0 + 2, x), (2 * x, 2 * x)))
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
            if not board.get_col(pos):
                pos = pos[0], pos[1] + runt

        if player.get_go() == 'w' and fl[1]:
            if not board.get_col(pos):
                pos = pos[0], pos[1] - runt

        if player.get_go() == 'a' and fl[2]:
            if not board.get_col(pos):
                pos = pos[0] - runt, pos[1]

        if player.get_go() == 'd' and fl[3]:
            if not board.get_col(pos):
                pos = pos[0] + runt, pos[1]

        screen.fill((0, 0, 0))

        board.render(screen)

        player.render(pos)

        clock.tick(FPS)

        pygame.display.flip()

    # завершение работы:
    pygame.quit()