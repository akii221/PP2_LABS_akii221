import pygame
import random
import psycopg2

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
pygame.display.set_caption("Zmeyka")

# Шрифт для текста
font = pygame.font.SysFont("Arial", 20)

# Функция для подключения к базе данных PostgreSQL
def connect_db():
    conn = psycopg2.connect(
        dbname="snake_eye", 
        user="postgres", 
        password="1937", 
        host="localhost", 
        port="5432"
    )
    return conn

# Функция для получения или создания пользователя
def get_user(username):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO "user" ("username") VALUES (%s) RETURNING id', (username,))

    user = cur.fetchone()
    if not user:
        cur.execute('INSERT INTO "user" ("username") VALUES (%s) RETURNING id', (username,))

        user_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return user_id, 0, 1  # Новый пользователь, уровень 1
    else:
        user_id = user[0]
        cur.execute("SELECT score, level FROM user_score WHERE user_id = %s ORDER BY timestamp DESC LIMIT 1", (user_id,))
        score, level = cur.fetchone() if cur.fetchone() else (0, 1)  # Получаем последний счёт и уровень
        cur.close()
        conn.close()
        return user_id, score, level

# Функция для сохранения состояния игры
def save_game_state(user_id, score, level, game_state):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO user_score (user_id, score, level, game_state) VALUES (%s, %s, %s, %s)", 
                (user_id, score, level, game_state))
    conn.commit()
    cur.close()
    conn.close()

# Функция для генерации случайной позиции еды, избегая змеи
def generate_food(snake):
    while True:
        x = random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE
        y = random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
        if (x, y) not in snake:
            return x, y

# Начальные параметры
username = input("Enter your username: ")
user_id, score, level = get_user(username)  # Получаем пользователя из базы
speed = 10  # Начальная скорость
running = True
clock = pygame.time.Clock()

snake = [(100, 100)]  # Начальное положение змеи
snake_dir = (CELL_SIZE, 0)  # Движение змеи (вправо)
food = generate_food(snake)  # Генерация еды
game_state = ""  # Пустое состояние игры (можно будет сохранять картину игры)

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
            elif event.key == pygame.K_p:  # Пауза и сохранение
                save_game_state(user_id, score, level, game_state)
                print(f"Game paused. Your score is {score}, level is {level}. State saved.")

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
