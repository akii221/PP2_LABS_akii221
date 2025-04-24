import psycopg2
import csv

# Подключение к БД
conn = psycopg2.connect(
    dbname="phonebook",  # ← сюда вставь свою базу
    user="postgres",     # ← имя пользователя PostgreSQL
    password="1937",     # ← сюда вставь свой пароль
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# Создание таблицы
cur.execute("""
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        username VARCHAR(100) NOT NULL,
        phone VARCHAR(20) NOT NULL
    );
""")
conn.commit()

# Вставка из CSV
def insert_from_csv():
    path = input("Введите путь к CSV-файлу: ")
    with open(path, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 2:
                cur.execute("INSERT INTO phonebook (username, phone) VALUES (%s, %s);", (row[0], row[1]))
    conn.commit()
    print("✔ Данные из CSV добавлены.")

# Ввод вручную
def insert_from_console():
    username = input("Введите имя: ")
    phone = input("Введите номер: ")
    cur.execute("INSERT INTO phonebook (username, phone) VALUES (%s, %s);", (username, phone))
    conn.commit()
    print("✔ Данные добавлены.")

# Обновление данных
def update_entry():
    search = input("Введите имя или телефон для обновления: ")
    field = input("Что обновить? (1 - имя, 2 - телефон): ")
    if field == "1":
        new_name = input("Введите новое имя: ")
        cur.execute("UPDATE phonebook SET username = %s WHERE username = %s OR phone = %s;", (new_name, search, search))
    elif field == "2":
        new_phone = input("Введите новый телефон: ")
        cur.execute("UPDATE phonebook SET phone = %s WHERE username = %s OR phone = %s;", (new_phone, search, search))
    conn.commit()
    print("✔ Обновление выполнено.")

# Поиск
def query_data():
    choice = input("Фильтр (1 - по имени, 2 - по номеру, 3 - всё): ")
    if choice == "1":
        name = input("Введите имя: ")
        cur.execute("SELECT * FROM phonebook WHERE username ILIKE %s;", ('%' + name + '%',))
    elif choice == "2":
        phone = input("Введите номер: ")
        cur.execute("SELECT * FROM phonebook WHERE phone LIKE %s;", ('%' + phone + '%',))
    else:
        cur.execute("SELECT * FROM phonebook;")

    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("Нет данных.")

# Удаление
def delete_entry():
    choice = input("Удалить по (1 - имени, 2 - телефону): ")
    if choice == "1":
        name = input("Введите имя: ")
        cur.execute("DELETE FROM phonebook WHERE username = %s;", (name,))
    elif choice == "2":
        phone = input("Введите телефон: ")
        cur.execute("DELETE FROM phonebook WHERE phone = %s;", (phone,))
    conn.commit()
    print("✔ Удаление выполнено.")

# Функция поиска по паттерну
def search_records_by_pattern(pattern):
    cur.execute("""
        SELECT * FROM phonebook 
        WHERE username ILIKE %s OR phone LIKE %s;
    """, ('%' + pattern + '%', '%' + pattern + '%'))
    
    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("Нет записей по паттерну.")

# Процедура для вставки или обновления пользователя
def insert_or_update_user(username, phone):
    cur.callproc('insert_or_update_user', [username, phone])
    conn.commit()
    print("✔ Данные добавлены или обновлены.")

# Процедура для множественной вставки пользователей
def insert_many_users(usernames, phones):
    cur.callproc('insert_many_users', [usernames, phones])
    conn.commit()
    print("✔ Множественная вставка выполнена.")

# Запрос с пагинацией
def query_phonebook_with_pagination(limit, offset):
    cur.execute("SELECT * FROM query_phonebook_with_pagination(%s, %s);", (limit, offset))
    rows = cur.fetchall()
    for row in rows:
        print(row)

# Удаление пользователя по имени или телефону
def delete_user_or_phone(input_value):
    cur.callproc('delete_user_or_phone', [input_value])
    conn.commit()
    print("✔ Запись удалена.")

# Главное меню
def main():
    while True:
        print("\n📱 Меню:")
        print("1 - Ввод вручную")
        print("2 - Загрузка из CSV")
        print("3 - Обновить запись")
        print("4 - Поиск")
        print("5 - Удалить")
        print("6 - Поиск по паттерну")
        print("7 - Вставить/Обновить пользователя")
        print("8 - Множественная вставка пользователей")
        print("9 - Запрос с пагинацией")
        print("0 - Выход")

        option = input("Выбор: ")
        if option == "1":
            insert_from_console()
        elif option == "2":
            insert_from_csv()
        elif option == "3":
            update_entry()
        elif option == "4":
            query_data()
        elif option == "5":
            delete_entry()
        elif option == "6":
            pattern = input("Введите паттерн для поиска: ")
            search_records_by_pattern(pattern)
        elif option == "7":
            username = input("Введите имя: ")
            phone = input("Введите телефон: ")
            insert_or_update_user(username, phone)
        elif option == "8":
            usernames = input("Введите имена пользователей (через запятую): ").split(',')
            phones = input("Введите телефоны пользователей (через запятую): ").split(',')
            insert_many_users(usernames, phones)
        elif option == "9":
            limit = int(input("Введите лимит: "))
            offset = int(input("Введите оффсет: "))
            query_phonebook_with_pagination(limit, offset)
        elif option == "0":
            break
        else:
            print("❌ Неверный ввод")

    cur.close()
    conn.close()

# Запуск
if __name__ == "__main__":
    main()
