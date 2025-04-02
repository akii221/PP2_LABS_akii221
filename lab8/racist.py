import pygame, sys  # Импортируем pygame для работы с графикой и sys для выхода из программы
from pygame.locals import *  # Импортируем все константы из pygame
import random, time  # Импортируем random для генерации случайных чисел и time для задержек

# Инициализируем pygame
pygame.init()

# Устанавливаем частоту кадров (FPS)
FPS = 60
FramePerSec = pygame.time.Clock()

# Определяем цвета в формате RGB
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Переменные игры
SCREEN_WIDTH = 400  # Ширина экрана
SCREEN_HEIGHT = 600  # Высота экрана
SPEED = 5  # Скорость движения врага
SCORE = 0  # Очки
COINS_COLLECTED = 0  # Количество собранных монет

# Настройка шрифтов
font = pygame.font.SysFont("Verdana", 60)  # Крупный шрифт (для "Game Over")
font_small = pygame.font.SysFont("Verdana", 20)  # Маленький шрифт (для очков и монет)
game_over = font.render("Game Over", True, BLACK)  # Текст "Game Over"

# Загружаем фоновое изображение
background = pygame.image.load("AnimatedStreet.png")

# Создаем окно игры
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)  # Заполняем экран белым цветом
pygame.display.set_caption("Game")  # Устанавливаем заголовок окна

# Класс врага (Enemy)
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png")  # Загружаем картинку врага
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)  # Случайное положение сверху экрана

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)  # Двигаем врага вниз
        if self.rect.top > SCREEN_HEIGHT:  # Если враг вышел за пределы экрана
            SCORE += 1  # Увеличиваем счет
            self.rect.top = 0  # Перемещаем врага наверх
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)  # Новая случайная позиция

# Класс игрока (Player)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")  # Загружаем картинку игрока
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)  # Начальная позиция игрока

    def move(self):
        pressed_keys = pygame.key.get_pressed()  # Проверяем, какие клавиши нажаты
        if self.rect.left > 0 and pressed_keys[K_LEFT]:  # Двигаем влево, если не вышли за границы
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:  # Двигаем вправо
            self.rect.move_ip(5, 0)

# Класс монеты (Coin)
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Coin.png").convert_alpha()  # Загружаем картинку монеты
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(500, 550)
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(500, 550))  # Появляется внизу экрана

# Создаем объекты классов
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Создаем группы спрайтов
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

# Добавляем событие для увеличения скорости
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5  # Каждую секунду увеличиваем скорость врагов
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0, 0))  # Отрисовываем фон
    
    # Отображаем счетчики
    scores = font_small.render(f"Score: {SCORE}", True, BLACK)
    coins_display = font_small.render(f"Coins: {COINS_COLLECTED}", True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))  # Отображаем очки в левом верхнем углу
    DISPLAYSURF.blit(coins_display, (SCREEN_WIDTH - 100, 10))  # Отображаем монеты в правом верхнем углу

    P1.move()  # Двигаем игрока
    E1.move()  # Двигаем врага

    # Отрисовываем все объекты
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
    
    # Проверяем столкновение игрока и врага
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('falling-of-heavy-object-291096.mp3').play()  # Проигрываем звук
        time.sleep(0.5)
        DISPLAYSURF.fill(RED)  # Красный экран при проигрыше
        DISPLAYSURF.blit(game_over, (30, 250))  # Отображаем "Game Over"
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()  # Удаляем все объекты
        time.sleep(2)
        pygame.quit()
        sys.exit()
    
    # Проверяем столкновение игрока и монеты
    if pygame.sprite.spritecollideany(P1, coins):
        COINS_COLLECTED += 1  # Увеличиваем счетчик монет
        for coin in coins:
            coin.kill()  # Удаляем текущую монету
        C1 = Coin()  # Создаем новую монету
        coins.add(C1)
        all_sprites.add(C1)

    pygame.display.update()
    FramePerSec.tick(FPS)  # Ограничиваем FPS