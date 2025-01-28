import pygame
import os


tile_size = (77, 99)


class hero:

    def __init__(self, pos):
        self.pos = pos
        self.x = pos[0] // tile_size[0]
        self.y = pos[1] // tile_size[1]

    def move(self, deltas):
        #if floor == 1:
        #    return None
        #elif floor == 0:
        self.x += deltas[0]
        self.y += deltas[1]
        #elif floor == 3:
        #    print('A chest!')
            #chest_open()
        #elif floor == 2:
        #    print('Next level!')
            #next_level()

    def render(self, screen, cnt_2):
        char_1 = pygame.sprite.Group()
        char_2 = pygame.sprite.Group()
        char_3 = pygame.sprite.Group()
        cursor_image = hero.load_image('рыцарь3.png', -1)
        cursor_image_2 = hero.load_image('рыцарь5.png', -1)
        cursor_image_3 = hero.load_image('рыцарь6.png', -1)
        cursor_3 = pygame.sprite.Sprite(char_3)
        cursor_3.image = cursor_image_3
        cursor_3.rect = cursor_3.image.get_rect()
        cursor_3.rect.x = self.x * tile_size[0]
        cursor_3.rect.y = self.y * tile_size[1]
        cursor_2 = pygame.sprite.Sprite(char_2)
        cursor_2.image = cursor_image_2
        cursor_2.rect = cursor_2.image.get_rect()
        cursor_2.rect.x = self.x * tile_size[0]
        cursor_2.rect.y = self.y * tile_size[1]
        cursor = pygame.sprite.Sprite(char_1)
        cursor.image = cursor_image
        cursor.rect = cursor.image.get_rect()
        cursor.rect.x = self.x * tile_size[0]
        cursor.rect.y = self.y * tile_size[1]
        animation = [char_1, char_2, char_3]
        animation[cnt_2 % 3].draw(screen)
        #if cnt_2 % 2 == 0:
        #    char_1.draw(screen)
        #else:
        #    char_2.draw(screen)

    def get_y(self):
        #print(self.y)
        return self.y

    def get_x(self):
        #print(self.x)
        return self.x



    def load_image(name, color_key=None):
        fullname = os.path.join('pictures', name)
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

    def load_image_third(name, color_key=None):
        fullname = os.path.join('pictures', name)
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