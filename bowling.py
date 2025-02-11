
import sys
import pygame
import time
from random import randint
import sqlite3


pygame.init()
game_over = False
x1 = 5
x2 = 25
x3 = 50
x28 = 0
back = (199, 21, 133)
mw = pygame.display.set_mode((500, 500))
mw.fill(back)
clock = pygame.time.Clock()
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class Area():
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = back

    def create(self):
        pygame.draw.rect(mw, back, self.rect)

def terminate():
    pygame.quit()
    sys.exit()


class Picture(Area):
    def __init__(self, filename, x, y, width, height):
        Area.__init__(self, x, y, width, height)
        self.image = pygame.image.load(filename)

    def draw(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))


class Label(Area):
    def set_text(self, text, fsize=12, text_color=(0, 0, 0)):
        self.image = pygame.font.SysFont('verdana', fsize).render(text, True, text_color)

    def draww(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))


ball = Picture('ball.png', 225, 300, 50, 50)
platform = Picture('platform.png', 200, 350, 100, 30)
ball.draw()
platform.draw()

platforms = []
enemy = []

for i in range(5):
    p = Picture('pixils.png', x28, 400, 100, 30)
    p.draw()
    platforms.append(p)
    x28 += 100

for i in range(9):
    m = Picture('enemy.png', x1, 5, 50, 50)
    m.draw()
    enemy.append(m)
    x1 += 55

for i in range(8):
    m = Picture('enemy.png', x2, 75, 50, 50)
    m.draw()
    enemy.append(m)
    x2 += 55

for i in range(7):
    m = Picture('enemy.png', x3, 150, 50, 50)
    m.draw()
    enemy.append(m)
    x3 += 55

def bowling(username):
    pygame.display.set_caption('Bowling')
    if username != '':
        pygame.mixer.music.load('4-track-4.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)
    con = sqlite3.connect('users_db.sqlite')
    cnt = 0
    zzz = 500
    move_left = 0
    move_right = 0
    game_over = False
    dx = 3
    dy = 3
    k = 0
    while game_over != True:
        platform.create()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    move_right = True
                if event.key == pygame.K_a:
                    move_left = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    move_right = False
                if event.key == pygame.K_a:
                    move_left = False
        if move_right == True and platform.rect.x != 400:
            platform.rect.x += 5

        if move_left == True and platform.rect.x != 0:
            platform.rect.x -= 5

        screen.fill(pygame.Color(199, 21, 133))

        ball.create()
        ball.rect.x += dx
        ball.rect.y += dy

        if ball.rect.y < 0:
            dy *= -1

        if ball.rect.x > 450 or ball.rect.x < 0:
            dx *= -1
        if ball.rect.colliderect(platform.rect):
            dy *= -1

        for m in enemy:
            m.draw()
            if m.rect.colliderect(ball.rect):
                enemy.remove(m)
                m.create()
                dy *= -1
                counter = Label(0, 450, 50, 50)
                counter.set_text(f'Кеглей выбито: {k}', 40, back)
                counter.draww()
                k += 1
                counter = Label(0, 450, 50, 50)
                counter.set_text(f'Кеглей выбито: {k}', 40, (255, 255, 0))
                counter.draww()

        for p in platforms:
            p.draw()
            if p.rect.colliderect(ball.rect):
                platforms.remove(p)
                p.create()
                dy *= -1

        if ball.rect.y > zzz:
            text = Label(25, 200, 50, 50)
            text.set_text(f"Вы проиграли. Ваш счёт: {k}", 30, GREEN)
            text.draww()
            cur = con.cursor()
            cur.execute(f"""update users_points set points_of_bowling = {k} where username is '{username}'""")
            con.commit()
            if cnt == 20:
                game_over = True
                pygame.quit()
                return 'lose'
            else:
                cnt += 1

        if len(enemy) == 0:
            text = Label(25, 200, 50, 50)
            text.set_text(f"Вы победили. Ваш счёт: {k}", 30, GREEN)
            text.draww()
            zzz = 10000000000000000000000000000000000000000000000000000000000000000000000000000000
            cur = con.cursor()
            cur.execute(f"""update users_points set points_of_bowling = {k} where username is '{username}'""")
            con.commit()
            if cnt == 20:
                game_over = True
                pygame.quit()
                return 'win'
            else:
                cnt += 1
        counter = Label(0, 450, 50, 50)
        counter.set_text(f'Кеглей выбито: {k}', 40, (255, 255, 0))
        counter.draww()

        platform.draw()
        ball.draw()
        pygame.display.update()
        clock.tick(100)
