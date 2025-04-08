import pygame
import random

# Инициализация Pygame
pygame.init()
REMOVE_FOOD_EVENT = pygame.USEREVENT + 1
# Константы экрана
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20  # Размер одной клетки

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("zmeyka")

# Шрифт для текста
font = pygame.font.SysFont("Arial", 20)

# Функция для генерации случайной позиции еды, избегая змеи
def generate_food(snake):
    while True:
        x = random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE
        y = random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
        if (x, y) not in snake:
            return x, y

def generate_food1(snake):
    while True:
        x = random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE
        y = random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
        if (x, y) not in snake:
            return x, y
# Начальные параметры
snake = [(100, 100)]  # Начальное положение змеи
snake_dir = (CELL_SIZE, 0)  # Движение змеи (вправо)
food = generate_food(snake) 
food1 = generate_food1(snake)
 # Генерация еды
score = 0
level = 1
speed = 10  # Начальная скорость
running = True
clock = pygame.time.Clock()

# Игровой цикл
while running:
    screen.fill(WHITE)
    
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_dir != (0, CELL_SIZE):
                snake_dir = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN and snake_dir != (0, -CELL_SIZE):
                snake_dir = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT and snake_dir != (CELL_SIZE, 0):
                snake_dir = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT and snake_dir != (-CELL_SIZE, 0):
                snake_dir = (CELL_SIZE, 0)
    
    # Движение змеи
    new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
    
    # Проверка столкновения со стенами
    if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
        running = False
    
    # Проверка столкновения с собой
    if new_head in snake:
        running = False
    
    # Добавление нового сегмента
    snake.insert(0, new_head)
    
    # Проверка на поедание еды
    if new_head == food:
        score += 1
        food = generate_food(snake)
        
        
        # Увеличение уровня и скорости каждые 3 очка
        if score % 3 == 0:
            level += 1
            speed += 2
    else:
        snake.pop()  # Удаление последнего сегмента
    
    # Отрисовка змеи
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))
    
    # Отрисовка еды
    pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))
    
    # Отображение счёта и уровня
    score_text = font.render(f"Счёт: {score}  Уровень: {level}", True, BLACK)
    screen.blit(score_text, (10, 10))
    
    # Обновление экрана
    pygame.display.update()
    clock.tick(speed)  # Ограничение FPS в зависимости от уровня

pygame.quit()