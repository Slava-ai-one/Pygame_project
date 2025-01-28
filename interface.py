import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Настройка экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D RPG Game")

# Класс игрока
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.color = GREEN
        self.speed = 5

    def move(self, dx, dy):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

# Класс сундука
class Chest:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.color = BLACK
        self.is_open = False

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def open_chest(self):
        if not self.is_open:
            self.is_open = True
            # Можно добавить логику для получения предмета

# Класс врага
class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.color = RED
        self.speed = 2

    def move(self):
        # Простой алгоритм движения врага
        if random.randint(0, 1) == 0:
            self.rect.x += self.speed * random.choice([-1, 1])
        else:
            self.rect.y += self.speed * random.choice([-1, 1])

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

# Главный игровой цикл
def game_loop():
    clock = pygame.time.Clock()
    player = Player(WIDTH // 2, HEIGHT // 2)
    chests = [Chest(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)) for _ in range(5)]
    enemy = Enemy(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -1
        if keys[pygame.K_RIGHT]:
            dx = 1
        if keys[pygame.K_UP]:
            dy = -1
        if keys[pygame.K_DOWN]:
            dy = 1

        player.move(dx, dy)

        # Проверка на столкновение с сундуком
        for chest in chests:
            if player.rect.colliderect(chest.rect) and not chest.is_open:
                chest.open_chest()

        enemy.move()

        # Рисуем всё на экран
        screen.fill(WHITE)
        player.draw()
        for chest in chests:
            chest.draw()
        enemy.draw()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    game_loop()