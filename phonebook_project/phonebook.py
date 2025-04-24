import psycopg2

try:
    conn = psycopg2.connect(
        dbname="phonebook",     # имя базы данных, которую ты создал в pgAdmin
        user="postgres",           # имя пользователя (по умолчанию postgres)
        password="1937",    # замени на свой пароль
        host="localhost",          # для локальной базы
        port="5432"                # стандартный порт
    )
    cur = conn.cursor()
    print("✅ Успешное подключение к базе данных!")
except Exception as e:
    print("❌ Ошибка подключения:", e)
