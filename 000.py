import pygame, sys

class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 0
        self.top = 0
        self.cell_size = 50

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
                if self.board[y][x]:
                    pygame.draw.rect(screen, (0, 255, 0), coord)
                else:
                    pygame.draw.rect(screen, (255, 255, 255), coord, 1)
    def get_cell(self, coord):
        x, y = coord[0] - self.left, coord[1] - self.top
        if self.width * self.cell_size > x >= 0 and self.height * self.cell_size > y >= 0:
            print(x // self.cell_size, y // self.cell_size)
            x, y = x // self.cell_size, y // self.cell_size
            self.board[y][x] = int(not self.board[y][x])
        else:
            print(None)

    def get_col(self, coord):
        x, y = coord[0] - self.left, coord[1] - self.top
        x2, y2 = coord[0] + player.cs * 2 - self.left, coord[1] + player.cs - self.top
        x2, y2 = x2 // self.cell_size, y2 // self.cell_size
        x, y = x // self.cell_size, y // self.cell_size
        if self.board[y][x] or self.board[y2][x2]:
            return True
        else:
            return False


def draw(screen):
    screen.fill((0, 0, 0))


class Arrow:
    def __init__(self, pos):
        self.cs = 20
        coord = (pos[0], pos[1], self.cs * 2, self.cs)
        pygame.draw.rect(screen, (255, 0, 0), coord)


    def render(self, pos):
        coord = (pos[0], pos[1], self.cs * 2, self.cs)
        pygame.draw.rect(screen, (255, 0, 0), coord)


if __name__ == '__main__':
    # инициализация Pygame:
    pygame.init()
    # размеры окна:
    fl = [0, 0, 0, 0]
    flag = False
    size = width, height = 1000, 1000
    screen = pygame.display.set_mode(size)
    running = True
    board = Board(20, 20)
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
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    fl[0] = 1
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    fl[1] = 1
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    fl[2] = 1
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    fl[3] = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    fl[0] = 0
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    fl[1] = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    fl[2] = 0
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    fl[3] = 0
        if fl:
            if fl[0]:
                if not board.get_col(pos):
                    pos = pos[0], pos[1] + 1
                else:
                    pos = pos[0], pos[1] - 2
            if fl[1]:
                if not board.get_col(pos):
                    pos = pos[0], pos[1] - 1
                else:
                    pos = pos[0], pos[1] + 2
            if fl[2]:
                print(board.get_col(pos))
                if not board.get_col(pos):
                    pos = pos[0] - 1, pos[1]
                else:
                    pos = pos[0] + 2, pos[1]
            if fl[3]:
                if not board.get_col(pos):
                    pos = pos[0] + 1, pos[1]
                else:
                    pos = pos[0] - 2, pos[1]


        screen.fill((0, 0, 0))
        board.render(screen)
        player.render(pos)
        pygame.display.flip()
    # завершение работы:
    pygame.quit()
