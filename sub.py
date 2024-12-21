import sys
import pygame
import copy


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 10

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color('white'), (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size), 1)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def on_click(self, cell):
        print(cell)

    def get_cell(self, mouse_pos):
        x = (mouse_pos[0] - self.left) // self.cell_size
        y = (mouse_pos[1] - self.top) // self.cell_size
        if x < 0 or x >= self.width:
            return None
        if y < 0 or y >= self.height:
            return None
        return x, y


def main():
    pygame.init()
    pygame.display.set_caption('Игра «Жизнь»')
    size = w, h = (1000, 1000)
    screen = pygame.display.set_mode(size)
    turn = False
    speed = 0
    tick = 0
    clock = pygame.time.Clock()
    board = Life(90, 90)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                board.get_click(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 or event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                turn = not turn
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                speed += 1
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                speed -= 1
        screen.fill(pygame.Color(0, 0, 0))
        board.render(screen)
        if turn:
            board.next_move()
        if speed < 0:
            speed = 1
        clock.tick(speed)
        pygame.display.flip()
    pygame.quit()


class Life(Board):
    def __init__(self, width, height):
        super().__init__(width, height)

    def on_click(self, cell):
        self.board[cell[1]][cell[0]] = (self.board[cell[1]][cell[0]] + 1) % 2

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x]:
                    pygame.draw.rect(screen, pygame.Color('green'), (
                        x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size),
                                     0)
                pygame.draw.rect(screen, pygame.Color('white'), (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size), 1)

    def next_move(self):
        tmp = copy.deepcopy(self.board)
        for y in range(self.height):
            for x in range(self.width):
                cnt = 0
                for j in range(-1, 2):
                    for i in range(-1, 2):
                        if x + i < 0 or x + i >= self.width or y + j < 0 or y + j >= self.height:
                            continue
                        else:
                            cnt += self.board[y + j][x + i]
                cnt -= self.board[y][x]
                if cnt == 3:
                    tmp[y][x] = 1
                if cnt < 2 or cnt > 3:
                    tmp[y][x] = 0
        self.board = copy.deepcopy(tmp)


if __name__ == '__main__':
    sys.exit(main())
