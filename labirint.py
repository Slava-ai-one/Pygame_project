import sys

import pygame

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
        colors = [(17, 20, 120), (2, 11, 92), (0, 0, 0), (0, 125, 125)]
        h = 0
        for y in range(self.current_v[0], self.current_v[1]):
            w = 0
            for x in range(self.current_h[0], self.current_h[1]):
                #print((x, y, h, w), self.get_tale_id((x, y - 1)))
                rect = pygame.Rect(w * self.tile_size[0], h * self.tile_size[1] - self.tile_size[1], self.tile_size[0], self.tile_size[1])
                screen.fill(colors[self.get_tale_id((x, y - 1))], rect)
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