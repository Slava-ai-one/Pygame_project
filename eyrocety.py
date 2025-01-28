import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Определяем цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Устанавливаем размеры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D RPG Game")

# Задаем FPS
clock = pygame.time.Clock()

# Определяем классы для игрока, врага и сундука
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Ограничиваем движение игрока в пределах экрана
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > SCREEN_WIDTH - 50:
            self.rect.x = SCREEN_WIDTH - 50
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > SCREEN_HEIGHT - 50:
            self.rect.y = SCREEN_HEIGHT - 50

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - 50)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - 50)

    def update(self, player):
        if player.rect.x < self.rect.x:
            self.rect.x -= 5
        if player.rect.x > self.rect.x:
            self.rect.x += 5
        if player.rect.y < self.rect.y:
            self.rect.y -= 5
        if player.rect.y > self.rect.y:
            self.rect.y += 5

class Chest(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - 30)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - 30)

# Создание спрайтов
player = Player()
enemy = Enemy()
chest = Chest()

all_sprites = pygame.sprite.Group()
sprites = pygame.sprite.Group()
sprites.add(player)
all_sprites.add(enemy)
sprites.add(chest)

# Главный игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Обновляем спрайты
    sprites.update()
    enemy.update(player)

    # Проверка коллизий
    if pygame.sprite.collide_rect(player, chest):
        print("Вы собрали сундук!")
        chest.rect.x = random.randint(0, SCREEN_WIDTH - 30)
        chest.rect.y = random.randint(0, SCREEN_HEIGHT - 30)

    # Отрисовка
    screen.fill(WHITE)
    all_sprites.draw(screen)
    sprites.draw(screen)
    pygame.display.flip()

    # Установка FPS
    clock.tick(60)