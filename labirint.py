import sys

import pygame
import os

from Prime_1 import load_image


def load_image(name, color_key=None):
    fullname = os.path.join('penis', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as mes:
        print(f'Не могу загрузить файл: {name}')
        print(mes)
        return
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


score = 0
tile_size = (77, 99)

class Map:
    def __init__(self, filename, free_tiles, finish_tale, chest_tale):
        self.map = []
        self.curr_map = []
        self.check_chests = []
        with open(f'{filename}') as input_file:
            for line in input_file:
                self.map.append(list(map(int, line.split())))
        #print(self.map)
        self.map = list(reversed(self.map))
        self.current_h = [0, 13]
        self.current_v = [0, 11]
        #print(self.map)
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.tile_size = tile_size
        self.free_tiles = free_tiles
        self.finish_tiles = finish_tale
        self.chest_tale = chest_tale
        self.score = score

    def render(self, screen):
        colors = [load_image('floor.png'), (2, 11, 92), (0, 0, 0), (0, 125, 125)]
        h = 0
        for y in range(self.current_v[0], self.current_v[1]):
            w = 0
            for x in range(self.current_h[0], self.current_h[1]):
                #print((x, y, h, w), self.get_tale_id((x, y - 1)))
                rect = pygame.Rect(w * self.tile_size[0], h * self.tile_size[1] - self.tile_size[1], self.tile_size[0], self.tile_size[1])
                colors[self.get_tale_id((x, y - 1))].draw(screen)
                w += 1
            h += 1
            #print(f'**** {self.current_v}'
                  #f'**** {self.current_h}')

    def get_tale_id(self, position):
        return self.map[position[1]][position[0]]

    def update_map_top_bottom(self, naprav):
        try:
            if naprav == 1:
                if 0 == self.current_v[0]:
                    return False
                self.current_v[0] -= 1
                self.current_v[1] -= 1
                return True
            else:
                if len(self.map) == self.current_v[1] - 1:
                    return False
                self.current_v[0] += 1
                self.current_v[1] += 1
                return True
        except Exception:
            return False


    def update_map_right_left(self, naprav):
        try:
            if naprav == 1:
                if 0 == self.current_h[0]:
                    return False
                self.current_h[0] -= 1
                self.current_h[1] -= 1
                return True
            else:
                if len(self.map[0]) == self.current_h[1]:
                    return False
                self.current_h[0] += 1
                self.current_h[1] += 1
                return True
        except Exception:
            return False

    def get_tale_invent(self, x, y):
        if self.map[self.current_v[0] + y][self.current_h[0] + x] == 1:
            pass
        if self.map[self.current_v[0] + y][self.current_h[0] + x] == 3:
            if (self.current_v[0] + y, self.current_h[0] + x) in self.check_chests:
                print("A already open chest!!!")
                pass
            else:
                print("A new chest!!")
                self.score += 1
                self.check_chests.append((self.current_v[0] + y, self.current_h[0] + x))
        print(self.map[self.current_v[0] + y][self.current_h[0] + x])
        return self.map[self.current_v[0] + y][self.current_h[0] + x]