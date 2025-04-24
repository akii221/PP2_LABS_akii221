import pygame
import random
import psycopg2
from psycopg2 import sql

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

# Функция подключения к базе данных
def connect_db():
    return psycopg2.connect(
        host="localhost",
        database="snake_game1",  # Убедитесь, что база данных создана
        user="postgres",       # Ваш пользователь
        password="1937"  # Ваш пароль
    )

# Функция для создания таблиц в базе данных
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL
        );
        CREATE TABLE IF NOT EXISTS user_score (
            id SERIAL PRIMARY KEY,
            user_id INT REFERENCES user(id),
            score INT,
            level INT,
            speed INT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

# Функция для получения пользователя по имени
def get_user(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

# Функция для создания нового пользователя
def create_user(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user (username) VALUES (%s) RETURNING id", (username,))
    user_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return user_id

# Функция для получения последнего счёта пользователя
def get_user_score(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_score WHERE user_id = %s ORDER BY date DESC LIMIT 1", (user_id,))
    score = cursor.fetchone()
    cursor.close()
    conn.close()
    return score

# Функция для сохранения счёта в базу данных
def save_score(user_id, score, level, speed):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO user_score (user_id, score, level, speed) 
        VALUES (%s, %s, %s, %s)
    """, (user_id, score, level, speed))
    conn.commit()
    cursor.close()
    conn.close()

# Начальные параметры игры
snake = [(100, 100)]  # Начальное положение змеи
snake_dir = (CELL_SIZE, 0)  # Движение змеи (вправо)
score = 0
level = 1
speed = 10  # Начальная скорость
running = True
clock = pygame.time.Clock()

# Ввод имени пользователя
username = input("Введите имя пользователя: ")

# Проверка на существование пользователя
user = get_user(username)
if user:
    user_id = user[0]
    score_data = get_user_score(user_id)
    if score_data:
        score, level, speed = score_data[1], score_data[2], score_data[3]
        print(f"Добро пожаловать, {username}! Ваш последний уровень: {level}, счёт: {score}")
    else:
        score, level, speed = 0, 1, 10
        print(f"Добро пожаловать, {username}! Вы начинаете с уровня {level}.")
else:
    user_id = create_user(username)
    score, level, speed = 0, 1, 10
    print(f"Привет, {username}! Это ваша первая игра.")

# Генерация еды
food = generate_food(snake)

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
            elif event.key == pygame.K_p:  # Пауза
                save_score(user_id, score, level, speed)
                print(f"Игра приостановлена. Ваш счёт: {score}, уровень: {level}")
                running = False  # Остановить игру для сохранения

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
