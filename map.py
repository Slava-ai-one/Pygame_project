import sys
import time

import pygame
import os
import pymorphy3
import sqlite3

from PyQt6.QtWidgets import QInputDialog, QPushButton, QLineEdit, QWidget, QApplication, QMessageBox

from labirint import Map
from main_charecter import hero, load_image
from scecond_charecter import sceleton
from time_or_coins import Time_or_coins


def load_level(level):
    return Map(f'{level}.txt', [0, 2], 2, 3)


window_size = width, height = (1000, 1000)
levels = ['First_level', 'Second_level', 'Thirthd_level']
curr_level = 0
FPS = 120
tile_size = (77, 99)
labyrinth = load_level(levels[curr_level])
main_charecter = hero([539, 495])
scelet_enter = sceleton([847, 1089])
scelet_exit = sceleton([1155, 5247])
Time_left = 180

pygame.init()
# pygame.display.set_caption('Инициализация игры')
size = w, h = window_size


# screen = pygame.display.set_mode(size)

def update(naprav):
    if naprav == 0:
        if labyrinth.update_map_right_left(0):
            #scelet.move((-1, 0))
            scelet_enter.x -= 1
            scelet_exit.x -= 1
            main_charecter.x -= 1
            #main_charecter.move((-1, 0))

    elif naprav == 1:
        if labyrinth.update_map_right_left(1):
            #scelet.move((1, 0))
            scelet_enter.x += 1
            scelet_exit.x += 1
            main_charecter.x += 1
            #main_charecter.move((1, 0))
    elif naprav == 2:
        if labyrinth.update_map_top_bottom(1):
            #scelet.move((0, 1))
            scelet_enter.y += 1
            scelet_exit.y += 1
            main_charecter.y += 1
            #main_charecter.move((0, 1))
    elif naprav == 3:
        if labyrinth.update_map_top_bottom(0):
            #scelet.move((0, -1))
            scelet_enter.y -= 1
            scelet_exit.y -= 1
            main_charecter.y -= 1
            #main_charecter.move((0, -1))


def terminate():
    pygame.quit()
    sys.exit()


def find_quick_path(map, start, end):
    err_count = 0
    start_path = start
    end_path = end
    sosedy = [(1, 0), (-1, 0), (0, -1), (0, 1)]
    next_path = []
    tales = {}
    curr_path = (start, start, 0)
    while curr_path[0] != end_path:
        if err_count > 1000:
            return None
        for i in range(4):
            if map.get_tale_invent(curr_path[0][0] + sosedy[i][0], curr_path[0][1] + sosedy[i][1]) == 0:
                sosed = (curr_path[0][0] + sosedy[i][0], curr_path[0][1] + sosedy[i][1])
                if sosed in tales or (sosed, curr_path[0], (curr_path[2] + 1)) in next_path:
                    continue
                next_path.append((sosed, curr_path[0], (curr_path[2] + 1)))
                err_count += 1
        tales[curr_path[0]] = (curr_path[0], curr_path[1], curr_path[2])
        curr_path = next_path[0]
        next_path.pop(0)
    back_to_start_way = []
    while curr_path[0] != start_path:
        back_to_start_way.append(curr_path[0])
        curr_path = tales[curr_path[1]]
    # print(back_to_start_way)
    if back_to_start_way:
        return back_to_start_way[-1]
    else:
        return None


def start_screen():
    screen = pygame.display.set_mode(size)
    intro_text = ["Правила игры",
                  "Задача игрока: пройти три зала и выбраться   ",
                  "из подземелья, собирая монеты. При встрече  ",
                  "с противником нужно выбрать: жизнь или кошелек"]


    fon = pygame.transform.scale(load_image('begin_page.png'), (w, h))
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


def end_win(username):
    intro_text = ["Если хотите увидеть таблицу лидеров, нажмите Space.",
                  "Если хотите закрыть, нажмите Escape"]
    con = sqlite3.connect('users_db.sqlite')
    cur = con.cursor()
    coins, time = map(int, (
        cur.execute(f"""select points, time from users_points where username in ('{username}')""").fetchone()))
    print(coins, time,
          cur.execute(f"""select points, time from users_points where username in ('{username}')""").fetchone(),
          sep='\n')
    morph = pymorphy3.MorphAnalyzer()
    worda = 'монета'
    parsed_word_coins = morph.parse(worda)[0]
    parsed_word_minut = morph.parse('минуту')[0]
    parsed_word_second = morph.parse('секунду')[0]
    result_text = [
        f"Вы собрали {coins} {parsed_word_coins.make_agree_with_number(int(coins)).word}, сделав это за {time // 60:0>2} {parsed_word_minut.make_agree_with_number(time // 60).word} и {time % 60:0>2} {parsed_word_second.make_agree_with_number(time % 60).word}"]
    finalka = pygame.sprite.Group()
    final = load_image('final_page.png')
    final_page = pygame.sprite.Sprite(finalka)
    final_page.image = final
    final_page.rect = final_page.image.get_rect()
    final_page.rect.x = 0
    final_page.rect.y = 0
    star_image = load_image('star.png', -1)
    for i in range(coins // 6):
        star = pygame.sprite.Sprite(finalka)
        star.image = pygame.transform.scale(star_image, (75, 75))
        star.rect = star.image.get_rect()
        star.rect.x = 400 + (85 * i)
        star.rect.y = 500

    screen = pygame.display.set_mode(size)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # terminate()
                return 'close'
            # elif event.type == pygame.KEYDOWN or \
            #        event.type == pygame.MOUSEBUTTONDOWN:
            #    return  # начинаем игру
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # terminate()
                return 'table'
        finalka.draw(screen)
        font_result = pygame.font.Font(None, 32)
        text_result_coord = 625
        for line in result_text:
            string_rendered = font_result.render(line, 1, pygame.Color(253, 248, 111))
            result_rect = string_rendered.get_rect()
            text_result_coord += 10
            result_rect.top = text_result_coord
            result_rect.x = 250
            text_result_coord += result_rect.height
            screen.blit(string_rendered, result_rect)
        font = pygame.font.Font(None, 30)
        text_coord = 775
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color(253, 248, 111))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 250
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        pygame.display.flip()


def end_lose(username):
    intro_text = ["Если хотите увидеть таблицу лидеров, нажмите Space.",
                  "Если хотите закрыть, нажмите Escape"]
    con = sqlite3.connect('users_db.sqlite')
    cur = con.cursor()
    coins, time = map(int, (
        cur.execute(f"""select points, time from users_points where username in ('{username}')""").fetchone()))
    print(coins, time,
          cur.execute(f"""select points, time from users_points where username in ('{username}')""").fetchone(),
          sep='\n')
    finalka = pygame.sprite.Group()
    final = load_image('final_page_lose.png')
    final_page = pygame.sprite.Sprite(finalka)
    final_page.image = final
    final_page.rect = final_page.image.get_rect()
    final_page.rect.x = 0
    final_page.rect.y = 0
    screen = pygame.display.set_mode(size)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # terminate()
                return 'close'
            # elif event.type == pygame.KEYDOWN or \
            #        event.type == pygame.MOUSEBUTTONDOWN:
            #    return  # начинаем игру
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # terminate()
                return 'table'
        finalka.draw(screen)
        font = pygame.font.Font(None, 30)
        text_coord = 775
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color(253, 248, 111))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 250
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        pygame.display.flip()

#def reset_timer():
#    global Time_left
#    Time_left = 180

lost_time = time.time()


def main(username):
    global labyrinth, curr_level, size, Time_left
    pygame.display.set_caption('Инициализация игры')
    size = w, h = window_size
    screen = pygame.display.set_mode(size)
    all_sprites = pygame.sprite.Group()
    choise = Time_or_coins()
    x = 500
    y = 99
    x_2 = 200
    y_2 = 200
    monetka_image = pygame.image.load('monetcka.png')
    monetka_image = pygame.transform.scale(monetka_image, (50, 50))
    monetka = pygame.sprite.Sprite(all_sprites)
    monetka.image = monetka_image
    monetka.rect = monetka.image.get_rect()
    monetka.rect.x = 70
    monetka.rect.y = 0
    char_1 = pygame.sprite.Group()
    char_2 = pygame.sprite.Group()
    cursor_image = load_image('рыцарь3.png', -1)
    cursor_image_2 = load_image('рыцарь5.png', -1)
    cursor_2 = pygame.sprite.Sprite(char_1)
    cursor_2.image = cursor_image_2
    cursor_2.rect = cursor_2.image.get_rect()
    cursor_2.rect.x = x
    cursor_2.rect.y = y
    # not_cursor_image = load_image_scecond('рыцарь.png')
    # not_cursor = pygame.sprite.Sprite(all_sprites)
    # not_cursor.image = not_cursor_image
    # not_cursor.rect = not_cursor.image.get_rect()
    # not_cursor.rect.x = x_2
    # not_cursor.rect.y = y_2
    font = pygame.font.Font(None, 50)
    cursor = pygame.sprite.Sprite(char_1)
    cursor.image = cursor_image
    cursor.rect = cursor.image.get_rect()
    cursor.rect.x = x
    cursor.rect.y = y
    labyrinth.render(screen)
    main_charecter.render(screen)
    scelet_exit.render(screen)
    scelet_enter.render(screen)
    running = True
    cnt_2 = 0
    cnt = 0
    side = 1
    flag_up = flag_down = flag_right = flag_left = False
    final_ready = False
    to_right = False
    to_left = False
    to_top = False
    to_bottom = False
    choise_flag = False
    cnt_3 = 0
    cur_time = 0
    enemyActive_enter = True
    enemyActive_exit = False
    MustMoveHero = 0
    MustMoveEnemy = 0
    while running:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                score = labyrinth.score
                labyrinth = load_level(levels[curr_level])
                labyrinth.give_username(username)
                labyrinth.win(Time_left, score)
                return 'win'
            #   cnt += 1
            #   flag_right = True
            # if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
            #    flag_right = False

            # if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            #   cnt += 1
            #    flag_left = True
            # if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
            #    flag_left = False
            # if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            #   cnt += 1
            #    flag_up = True
            # if event.type == pygame.KEYUP and event.key == pygame.K_UP:
            #    flag_up = False
            # if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            #    cnt += 1
            #    flag_down = True
            # if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            #    flag_down = False
            # if cnt % 10 == 0 and cnt != 0 and event.type == pygame.KEYDOWN:
            #    side = side * -1
            if event.type == pygame.KEYDOWN:
                x_2 = x_2 + (10 * side)
            # if event.type == pygame.KEYDOWN and event.key == pygame.K_KP_ENTER:
            #    labyrinth.get_tale_invent(main_charecter.get_x(), main_charecter.get_y())
        # not_cursor.rect.x = x_2
        # not_cursor.rect.y = y_2
        current_time = int(time.time() - lost_time)
        if current_time != cur_time:
            Time_left -= 1
            cur_time = current_time
        cursor.rect.x = x
        cursor.rect.y = y
        cursor_2.rect.x = x
        cursor_2.rect.y = y
        main_curr_x = main_charecter.get_x()
        main_curr_y = main_charecter.get_y()
        # print('***')
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
                if not labyrinth.get_tale_invent(main_curr_x + 1, main_curr_y - 1, 1) == 0:
                    flag_up = False
                    flag_right = False
                    pass
            if flag_right and flag_down:
                if not labyrinth.get_tale_invent(main_curr_x + 1, main_curr_y + 1, 1) == 0:
                    flag_down = False
                    flag_right = False
                    pass
            if flag_left and flag_up:
                if not labyrinth.get_tale_invent(main_curr_x - 1, main_curr_y - 1, 1) == 0:
                    flag_up = False
                    flag_left = False
                    pass
            if flag_left and flag_down:
                if not labyrinth.get_tale_invent(main_curr_x - 1, main_curr_y + 1, 1) == 0:
                    flag_down = False
                    flag_left = False
                    pass
            if flag_right and not choise_flag:
                cnt_2 += 1
                next_tale = labyrinth.get_tale_invent(main_curr_x + 1, main_curr_y, 1)
                if next_tale == 0:
                    if main_curr_x >= 6:
                        update(0)
                    if int(main_charecter.get_x()) * tile_size[0] + 77 <= w:
                        main_charecter.move((1, 0))
                flag_right = False

            if flag_left and not choise_flag:
                cnt_2 += 1
                next_tale = labyrinth.get_tale_invent(main_curr_x - 1, main_curr_y, 1)
                if next_tale == 0:
                    if main_charecter.get_x() <= 6:
                        update(1)
                    if int(main_charecter.get_x()) * tile_size[0] - 77 >= 0:
                        main_charecter.move((-1, 0))
                flag_left = False

            if flag_up and not choise_flag:
                cnt_2 += 1
                next_tale = labyrinth.get_tale_invent(main_curr_x, main_curr_y - 1, 1)
                if next_tale == 0:
                    if main_charecter.get_y() <= 5:
                        update(2)
                    if int(main_charecter.get_y()) * tile_size[1] - 99 >= 0:
                        main_charecter.move((0, -1))
                flag_up = False

            if flag_down and not choise_flag:
                cnt_2 += 1
                next_tale = labyrinth.get_tale_invent(main_curr_x, main_curr_y + 1, 1)
                if next_tale == 0:
                    if main_charecter.get_y() >= 5:
                        update(3)
                    if int(main_charecter.get_y()) * tile_size[1] + 99 + 99 <= h:
                        main_charecter.move((0, 1))
                flag_down = False
            print(next_tale)

            if next_tale == 2:
                curr_level = (curr_level + 1) % 3
                score = labyrinth.score
                labyrinth = load_level(levels[curr_level])
                labyrinth.give_username(username)
                labyrinth.score = score
                print(curr_level)
                if curr_level == 1:
                    scelet_enter.x = 18
                    scelet_enter.y = 14
                    scelet_exit.x = 32
                    scelet_exit.y = 48
                    main_charecter.x = 5
                    main_charecter.y = 1
                if curr_level == 2:
                    main_charecter.x = 5
                    main_charecter.y = 1
            if next_tale == 5:
                score = labyrinth.score
                labyrinth = load_level(levels[curr_level])
                labyrinth.give_username(username)
                labyrinth.win(Time_left, score)
                return 'win'
            if Time_left <= 0:
                labyrinth.win(Time_left, score, False)
                return 'lose'

            # if final_ready:
            #    final.rect.x += 0.0083
            #    print("jhfjg")

            MustMoveHero = 0
        else:
            MustMoveHero = MustMoveHero + 1
        if scelet_enter.get_x() > int(main_charecter.get_x()):
            to_left = True
        if scelet_enter.get_x() < int(main_charecter.get_x()):
            to_right = True
        if scelet_enter.get_y() > int(main_charecter.get_y()):
            to_top = True
        if scelet_enter.get_y() < int(main_charecter.get_y()):
            to_bottom = True
        if scelet_enter.get_x() >= 13 or scelet_enter.get_x() < 0:
            enemyActive_enter = False
        if scelet_enter.get_y() >= 11 or scelet_enter.get_y() < 0:
            enemyActive_enter = False
        if scelet_enter.get_x() < 13 and scelet_enter.get_x() >= 0 and scelet_enter.get_y() < 11 and scelet_enter.get_y() >= 0:
            enemyActive_enter = True
        if MustMoveEnemy == 20:
            MustMoveEnemy = 0
            if enemyActive_enter:
                next_path = find_quick_path(labyrinth, (scelet_enter.get_x(), scelet_enter.get_y()),
                                            (main_charecter.get_x(), main_charecter.get_y()))
                if next_path:
                    print(next_path)
                    scelet_enter.move((next_path[0] - scelet_enter.get_x(), next_path[1] - scelet_enter.get_y()))
                    if scelet_enter.get_x() == main_charecter.get_x() and scelet_enter.get_y() == main_charecter.get_y():
                        choise.show()
                        choise_flag = True
                        print('#########')
                if choise.get_cur_choise() != None and choise_flag:
                    print(choise.get_cur_choise())
                    # while not choise.get_cur_choise():
                    #    print(choise.get_cur_choise())
                    if choise.get_cur_choise() == 'time':
                        Time_left -= 10
                        choise_flag = False
                        MustMoveEnemy = -100
                        choise.reset_choise()
                    if choise.get_cur_choise() == 'coins':
                        labyrinth.score_minus_two()
                        choise_flag = False
                        MustMoveEnemy = -100
                        choise.reset_choise()

            #    scelet.move((1, 0))
            #    to_right = False
            #    to_left = False
            #    to_top = False
            #    to_bottom = False
            # if to_left and enemyActive:
            #    scelet.move((-1, 0))
            #    to_right = False
            #    to_left = False
            #    to_top = False
            #    to_bottom = False
            # if to_top and enemyActive:
            #    scelet.move((0, -1))
            #    to_right = False
            #    to_left = False
            #    to_top = False
            #    to_bottom = False
            # if to_bottom and enemyActive:
            #    scelet.move((0, 1))
            #    to_right = False
            #    to_left = False
            #    to_top = False
            #    to_bottom = False

        else:
            MustMoveEnemy += 1
        if scelet_exit.get_x() > int(main_charecter.get_x()):
            to_left = True
        if scelet_exit.get_x() < int(main_charecter.get_x()):
            to_right = True
        if scelet_exit.get_y() > int(main_charecter.get_y()):
            to_top = True
        if scelet_exit.get_y() < int(main_charecter.get_y()):
            to_bottom = True
        if scelet_exit.get_x() >= 13 or scelet_exit.get_x() < 0:
            enemyActive_exit = False
        if scelet_exit.get_y() >= 11 or scelet_exit.get_y() < 0:
            enemyActive_exit = False
        if scelet_exit.get_x() < 13 and scelet_exit.get_x() >= 0 and scelet_exit.get_y() < 11 and scelet_exit.get_y() >= 0:
            enemyActive_exit = True
        if MustMoveEnemy == 20:
            MustMoveEnemy = 0
            if enemyActive_exit:
                next_path = find_quick_path(labyrinth, (scelet_exit.get_x(), scelet_exit.get_y()),
                                            (main_charecter.get_x(), main_charecter.get_y()))
                if next_path:
                    print(next_path)
                    scelet_exit.move((next_path[0] - scelet_exit.get_x(), next_path[1] - scelet_exit.get_y()))
                    if scelet_exit.get_x() == main_charecter.get_x() and scelet_exit.get_y() == main_charecter.get_y():
                        choise.show()
                        choise_flag = True
                        print('#########')
                if choise.get_cur_choise() != None and choise_flag:
                    print(choise.get_cur_choise())
                    # while not choise.get_cur_choise():
                    #    print(choise.get_cur_choise())
                    if choise.get_cur_choise() == 'time':
                        Time_left -= 10
                        choise_flag = False
                        MustMoveEnemy = -100
                        choise.reset_choise()
                    if choise.get_cur_choise() == 'coins':
                        labyrinth.score_minus_two()
                        choise_flag = False
                        MustMoveEnemy = -100
                        choise.reset_choise()

            #    scelet.move((1, 0))
            #    to_right = False
            #    to_left = False
            #    to_top = False
            #    to_bottom = False
            # if to_left and enemyActive:
            #    scelet.move((-1, 0))
            #    to_right = False
            #    to_left = False
            #    to_top = False
            #    to_bottom = False
            # if to_top and enemyActive:
            #    scelet.move((0, -1))
            #    to_right = False
            #    to_left = False
            #    to_top = False
            #    to_bottom = False
            # if to_bottom and enemyActive:
            #    scelet.move((0, 1))
            #    to_right = False
            #    to_left = False
            #    to_top = False
            #    to_bottom = False

        else:
            MustMoveEnemy += 1

        screen.fill(pygame.Color(0, 0, 0))
        score = labyrinth.score
        labyrinth.render(screen)
        main_charecter.render(screen)
        scelet_enter.render(screen)
        scelet_exit.render(screen)
        all_sprites.draw(screen)
        text = font.render(f"{Time_left // 60:0>2}:{Time_left % 60:0>2}", True, (100, 255, 100))
        screen.blit(text, (550, 0))
        text = font.render(f"{score}", True, (100, 255, 100))
        screen.blit(text, (0, 0))
        pygame.time.Clock().tick(FPS)
        pygame.display.flip()
    pygame.quit()
