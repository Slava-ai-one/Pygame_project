import sys
import pygame
import copy
import random


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

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
    width, height, count_of_mines = map(int, input().split())
    pygame.init()
    pygame.display.set_caption('Игра «Жизнь»')
    board = Minesweeper(width, height, count_of_mines)
    size = w, h = (10 + 10 + (width * board.cell_size), 10 + 10 + (height * board.cell_size))
    screen = pygame.display.set_mode(size)
    turn = False
    speed = 0
    tick = 0
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                board.get_click(event.pos)
        screen.fill(pygame.Color(0, 0, 0))
        board.render(screen)
        clock.tick(speed)
        pygame.display.flip()
    pygame.quit()


class Minesweeper(Board):
    def __init__(self, width, height, count_of_mines):
        super().__init__(width, height)
        self.count_of_mines = count_of_mines
        self.mines_drop()

    def mines_drop(self):
        list_of_mines = [-1] * ((self.width * self.height) - self.count_of_mines)
        list_scecond = [10] * self.count_of_mines
        list_of_mines.extend(list_scecond)
        random.shuffle(list_of_mines)
        for y in range(self.height):
            for x in range(self.width):
                self.board[y][x] = list_of_mines[x + (self.width * y)]

    def render(self, screen):
        font = pygame.font.Font(None, 30)
        colors = [pygame.Color('white'), pygame.Color('red')]
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] != 10 and self.board[y][x] != -1:
                    screen.blit(font.render(f'{self.board[y][x]}', True, (0, 255, 0)),
                                (x * self.cell_size + self.left, y * self.cell_size + self.top))
                if self.board[y][x] == -1:
                    pygame.draw.rect(screen, colors[0], (
                        x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size),
                                     1)
                if self.board[y][x] == 10:
                    pygame.draw.rect(screen, colors[1], (
                        x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size),
                                     0)
                pygame.draw.rect(screen, colors[0], (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size),
                                 1)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.open_cell(cell)

    def open_cell(self, cell):
        mins = 0
        down = True
        up = True
        left = True
        right = True
        if cell:
            if self.board[cell[1]][cell[0]] != 10:
                if cell[1] + 1 > self.height - 1:
                    down = False
                if cell[1] - 1 < 0:
                    up = False
                if cell[0] + 1 > self.width - 1:
                    right = False
                if cell[0] - 1 < 0:
                    left = False
                if down and self.board[cell[1] + 1][cell[0]] == 10:
                    mins += 1
                if up and self.board[cell[1] - 1][cell[0]] == 10:
                    mins += 1
                if right and self.board[cell[1]][cell[0] + 1] == 10:
                    mins += 1
                if left and self.board[cell[1]][cell[0] - 1] == 10:
                    mins += 1
                if right and down and self.board[cell[1] + 1][cell[0] + 1] == 10:
                    mins += 1
                if down and left and self.board[cell[1] + 1][cell[0] - 1] == 10:
                    mins += 1
                if up and right and self.board[cell[1] - 1][cell[0] + 1] == 10:
                    mins += 1
                if up and left and self.board[cell[1] - 1][cell[0] - 1] == 10:
                    mins += 1
                self.board[cell[1]][cell[0]] = mins


if __name__ == '__main__':
    sys.exit(main())
