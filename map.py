import sys
import pygame
import os

from labirint import Map
from main_charecter import hero
from scecond_charecter import  sceleton

def load_level(level):
    return Map(f'{level}.txt', [0, 2], 2, 3)

window_size = width, height = (1000, 1000)
levels = ['First_level', 'Second_level']
curr_level = 0
FPS = 120
tile_size = (77, 99)
labyrinth = load_level(levels[curr_level])
main_charecter = hero([450, 99])
scelet = sceleton([250, 99])

pygame.init()
pygame.display.set_caption('Инициализация игры')
size = w, h = window_size
screen = pygame.display.set_mode(size)

def update(naprav):
    if naprav == 0:
        if labyrinth.update_map_right_left(0):
            scelet.move((-1, 0))
            main_charecter.move((-1, 0))
    elif naprav == 1:
        if labyrinth.update_map_right_left(1):
            scelet.move((1, 0))
            main_charecter.move((1, 0))
    elif naprav == 2:
        if labyrinth.update_map_top_bottom(1):
            scelet.move((0, 1))
            main_charecter.move((0, 1))
    elif naprav == 3:
        if labyrinth.update_map_top_bottom(0):
            scelet.move((0, -1))
            main_charecter.move((0, -1))

def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Правила игры",
                  "Задача игрока: выбраться из подземелья, собирая монеты",
                  "при встрече с противником нужно выбрать: жизнь или кошелек"]

    fon = pygame.transform.scale(hero.load_image('begin_page.png'), (w, h))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 24)
    text_coord = 845
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(253, 248, 111))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 280
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()

start_screen()
def main():
    global labyrinth, curr_level
    Time_left = 180
    pygame.init()
    pygame.display.set_caption('Инициализация игры')
    size = w, h = window_size
    screen = pygame.display.set_mode(size)
    x = 500
    y = 99
    x_2 = 200
    y_2 = 200
    all_sprites = pygame.sprite.Group()
    monetka_image = pygame.image.load('monetcka.png')
    monetka_image = pygame.transform.scale(monetka_image, (50, 50))
    monetka = pygame.sprite.Sprite(all_sprites)
    monetka.image = monetka_image
    monetka.rect = monetka.image.get_rect()
    monetka.rect.x = 30
    monetka.rect.y = 0
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
    font = pygame.font.Font(None, 50)
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
    to_right = False
    to_left = False
    to_top = False
    to_bottom = False
    cnt_3 = 0
    enemyActive = True
    MustMoveHero = 0
    MustMoveEnemy = 0
    while running:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                terminate()
            #if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
             #   cnt += 1
             #   flag_right = True
            #if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
            #    flag_right = False

            #if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
             #   cnt += 1
            #    flag_left = True
            #if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
            #    flag_left = False
            #if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
             #   cnt += 1
            #    flag_up = True
            #if event.type == pygame.KEYUP and event.key == pygame.K_UP:
            #    flag_up = False
            #if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            #    cnt += 1
            #    flag_down = True
            #if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            #    flag_down = False
            #if cnt % 10 == 0 and cnt != 0 and event.type == pygame.KEYDOWN:
            #    side = side * -1
            if event.type == pygame.KEYDOWN:
                x_2 = x_2 + (10 * side)
            #if event.type == pygame.KEYDOWN and event.key == pygame.K_KP_ENTER:
            #    labyrinth.get_tale_invent(main_charecter.get_x(), main_charecter.get_y())
        #not_cursor.rect.x = x_2
        #not_cursor.rect.y = y_2
        cursor.rect.x = x
        cursor.rect.y = y
        cursor_2.rect.x = x
        cursor_2.rect.y = y
        main_curr_x = main_charecter.get_x()
        main_curr_y = main_charecter.get_y()
        print('***')
        next_tale = 0
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -1
            flag_left = True
        if keys[pygame.K_RIGHT]:
            dx = 1
            flag_right = True
        if keys[pygame.K_UP]:
            dy = -1
            flag_up = True
        if keys[pygame.K_DOWN]:
            dy = 1
            flag_down = True
        if MustMoveHero == 10:
            if flag_right and flag_up:
                if not labyrinth.get_tale_invent(main_curr_x + 1, main_curr_y - 1, ) == 0:
                    flag_up = False
                    flag_right = False
                    continue
            if flag_right and flag_down:
                if not labyrinth.get_tale_invent(main_curr_x + 1, main_curr_y + 1) == 0:
                    flag_down = False
                    flag_right = False
                    continue
            if flag_left and flag_up:
                if not labyrinth.get_tale_invent(main_curr_x - 1, main_curr_y - 1) == 0:
                    flag_up = False
                    flag_left = False
                    continue
            if flag_left and flag_down:
                if not labyrinth.get_tale_invent(main_curr_x - 1, main_curr_y + 1) == 0:
                    flag_down = False
                    flag_left = False
                    continue
            if flag_right:
                cnt_2 += 1
                next_tale = labyrinth.get_tale_invent(main_curr_x + 1, main_curr_y)
                if next_tale == 0:
                    if main_curr_x >= 6:
                        update(0)
                    if int(main_charecter.get_x()) * tile_size[0] + 77 <= w:
                        main_charecter.move((1, 0))
                        #if labyrinth.update_map_right_left(0):
                        #    main_charecter.move((-1, 0))
                flag_right = False

            if flag_left:
                cnt_2 += 1
                next_tale = labyrinth.get_tale_invent(main_curr_x - 1, main_curr_y)
                if next_tale == 0:
                    if main_charecter.get_x() <= 6:
                        update(1)
                    if int(main_charecter.get_x()) * tile_size[0] - 77 >= 0:
                        main_charecter.move((-1, 0))
                        #if labyrinth.update_map_right_left(1):
                        #    main_charecter.move((1, 0))
                flag_left = False

            if flag_up:
                cnt_2 += 1
                next_tale = labyrinth.get_tale_invent(main_curr_x, main_curr_y - 1)
                if next_tale == 0:
                    if main_charecter.get_y() <= 5:
                        update(2)
                    if int(main_charecter.get_y()) * tile_size[1] - 99 >= 0:
                        main_charecter.move((0, -1))
                flag_up = False

            if flag_down:
                cnt_2 += 1
                next_tale = labyrinth.get_tale_invent(main_curr_x, main_curr_y + 1)
                if next_tale == 0:
                    if main_charecter.get_y() >= 5:
                        update(3)
                    if int(main_charecter.get_y()) * tile_size[1] + 99 + 99 <= h:
                        main_charecter.move((0, 1))
                        #if labyrinth.update_map_top_bottom(0):
                        #    main_charecter.move((0, -1))
                flag_down = False

            if next_tale == 2:
                curr_level = (curr_level + 1) % 2
                score = labyrinth.score
                labyrinth = load_level(levels[curr_level])
                labyrinth.score = score
                print(curr_level)
            MustMoveHero = 0
        else:
            MustMoveHero = MustMoveHero + 1
        if scelet.get_x()  > int(main_charecter.get_x()):
            to_left = True
        if scelet.get_x() < int(main_charecter.get_x()):
            to_right = True
        if scelet.get_y() > int(main_charecter.get_y()):
            to_top = True
        if scelet.get_y() < int(main_charecter.get_y()):
            to_bottom = True
        if scelet.get_x() >= 13 or scelet.get_x() < 0:
            enemyActive = False
        if scelet.get_x() < 13 and scelet.get_x() >= 0:
            enemyActive = True
        if MustMoveEnemy == 40:
            if to_right and enemyActive:
                scelet.move((1, 0))
                to_right = False
                to_left = False
                to_top = False
                to_bottom = False
            if to_left and enemyActive:
                scelet.move((-1, 0))
                to_right = False
                to_left = False
                to_top = False
                to_bottom = False
            if to_top and enemyActive:
                scelet.move((0, -1))
                to_right = False
                to_left = False
                to_top = False
                to_bottom = False
            if to_bottom and enemyActive:
                scelet.move((0, 1))
                to_right = False
                to_left = False
                to_top = False
                to_bottom = False

            MustMoveEnemy = 0
        else:
            MustMoveEnemy += 1

        cnt += 1
        if cnt % 120 == 0:
            Time_left -= 1


        screen.fill(pygame.Color(0, 0, 0))
        score = labyrinth.score
        labyrinth.render(screen)
        main_charecter.render(screen, cnt_2)
        scelet.render(screen, cnt_2)
        all_sprites.draw(screen)
        text = font.render(f"{Time_left // 60}:{Time_left % 60}", True, (100, 255, 100))
        screen.blit(text, (550, 0))
        text = font.render(f"{score}", True, (100, 255, 100))
        screen.blit(text, (0, 0))
        pygame.time.Clock().tick(FPS)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    sys.exit(main())
