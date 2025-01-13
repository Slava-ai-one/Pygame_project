import sys
import pygame
import os


from main_charecter import hero
from scecond_charecter import  sceleton

window_size = width, height = (1000, 1000)
FPS = 120
tile_size = (77, 99)
main_charecter = hero([450, 99])
scelet = sceleton([250, 99])

class Map:
    def __init__(self, filename, free_tiles, finish_tale, chest_tale):
        self.map = []
        self.curr_map = []
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
                scelet.move((0, 1))
                main_charecter.move((0, 1))
                return True
            else:
                if len(self.map) == self.current_v[1] - 1:
                    return False
                self.current_v[0] += 1
                self.current_v[1] += 1
                scelet.move((0, -1))
                main_charecter.move((0, -1))
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
                scelet.move((1, 0))
                main_charecter.move((1, 0))
                return True
            else:
                if len(self.map[0]) == self.current_h[1]:
                    return False
                self.current_h[0] += 1
                self.current_h[1] += 1
                scelet.move((-1, 0))
                main_charecter.move((-1, 0))
                return True
        except Exception:
            return False

    def get_tale_invent(self, x, y):
        print(self.map[self.current_v[0] + y][self.current_h[0] + x])
        return self.map[self.current_v[0] + y][self.current_h[0] + x]



def main():
    pygame.init()
    pygame.display.set_caption('Инициализация игры')
    size = w, h = window_size
    screen = pygame.display.set_mode(size)
    labyrinth = Map('Описания.txt', [0, 2], 2, 3)
    x = 500
    y = 99
    x_2 = 200
    y_2 = 200
    all_sprites = pygame.sprite.Group()
    char_1 = pygame.sprite.Group()
    char_2 = pygame.sprite.Group()
    cursor_image = hero.load_image('рыцарь3.png', -1)
    cursor_image_2 = hero.load_image('рыцарь5.png', -1)
    cursor_2 = pygame.sprite.Sprite(char_1)
    cursor_2.image = cursor_image_2
    cursor_2.rect = cursor_2.image.get_rect()
    cursor_2.rect.x = x
    cursor_2.rect.y = y
    #not_cursor_image = load_image_scecond('рыцарь.png')
    #not_cursor = pygame.sprite.Sprite(all_sprites)
    #not_cursor.image = not_cursor_image
    #not_cursor.rect = not_cursor.image.get_rect()
    #not_cursor.rect.x = x_2
    #not_cursor.rect.y = y_2
    cursor = pygame.sprite.Sprite(char_1)
    cursor.image = cursor_image
    cursor.rect = cursor.image.get_rect()
    cursor.rect.x = x
    cursor.rect.y = y
    labyrinth.render(screen)
    main_charecter.render(screen, 0)
    scelet.render(screen, 0)
    running = True
    cnt_2 = 0
    cnt = 0
    side = 1
    flag_up = flag_down = flag_right = flag_left = False
    to_right = 0
    cnt_3 = 0
    MustMoveHero = 0
    MustMoveEnemy = 0
    while running:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
             #   cnt += 1
                flag_right = True
            if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                flag_right = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
             #   cnt += 1
                flag_left = True
            if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                flag_left = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
             #   cnt += 1
                flag_up = True
            if event.type == pygame.KEYUP and event.key == pygame.K_UP:
                flag_up = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            #    cnt += 1
                flag_down = True
            if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                flag_down = False
            #if cnt % 10 == 0 and cnt != 0 and event.type == pygame.KEYDOWN:
            #    side = side * -1
            if event.type == pygame.KEYDOWN:
                x_2 = x_2 + (10 * side)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_KP_ENTER:
                labyrinth.get_tale_invent(main_charecter.get_x(), main_charecter.get_y())
        #not_cursor.rect.x = x_2
        #not_cursor.rect.y = y_2
        cursor.rect.x = x
        cursor.rect.y = y
        cursor_2.rect.x = x
        cursor_2.rect.y = y
        labyrinth.render(screen)
        print('***')
        if MustMoveHero == 5:
            if flag_right:
                cnt_2 += 1
                if not labyrinth.get_tale_invent(main_charecter.get_x() + 1, main_charecter.get_y()) == 1:
                    if main_charecter.get_x() >= 6:
                        labyrinth.update_map_right_left(0)
                        #if labyrinth.update_map_right_left(0):
                        #    main_charecter.move((-1, 0))
                    if int(main_charecter.get_x()) * tile_size[0] + 77 <= w:
                        main_charecter.move((1, 0))

            if flag_left:
                cnt_2 += 1
                if not labyrinth.get_tale_invent(main_charecter.get_x() - 1, main_charecter.get_y()) == 1:
                    if main_charecter.get_x() <= 6:
                        labyrinth.update_map_right_left(1)
                        #if labyrinth.update_map_right_left(1):
                        #    main_charecter.move((1, 0))
                    if int(main_charecter.get_x()) * tile_size[0] - 77 >= 0:
                        main_charecter.move((-1, 0))

            if flag_up:
                cnt_2 += 1
                if not labyrinth.get_tale_invent(main_charecter.get_x(), main_charecter.get_y() - 1) == 1:
                    if main_charecter.get_y() <= 5:
                        labyrinth.update_map_top_bottom(1)
                        #if labyrinth.update_map_top_bottom(1):
                        #    main_charecter.move((0, 1))
                    if int(main_charecter.get_y()) * tile_size[1] - 99 >= 0:
                        main_charecter.move((0, -1))

            if flag_down:
                cnt_2 += 1
                if not labyrinth.get_tale_invent(main_charecter.get_x(), main_charecter.get_y() + 1) == 1:
                    if main_charecter.get_y() >= 5:
                        labyrinth.update_map_top_bottom(0)
                        #if labyrinth.update_map_top_bottom(0):
                        #    main_charecter.move((0, -1))
                    if int(main_charecter.get_y()) * tile_size[1] + 99 + 99 <= h:
                        main_charecter.move((0, 1))
            MustMoveHero = 0
        else:
            MustMoveHero = MustMoveHero + 1
        if scelet.get_x() > 10:
            to_right = False
        elif scelet.get_x() < 2:
            to_right = True
        if MustMoveEnemy == 40:
            if to_right:
                scelet.move((1, 0))
            else:
                scelet.move((-1, 0))
            MustMoveEnemy = 0
        else:
            MustMoveEnemy += 1


        #screen.fill(pygame.Color(0, 255, 255))
        main_charecter.render(screen, cnt_2)
        scelet.render(screen, cnt_2)
        all_sprites.draw(screen)
        pygame.time.Clock().tick(FPS)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    sys.exit(main())
