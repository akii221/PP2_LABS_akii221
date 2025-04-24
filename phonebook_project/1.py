import psycopg2
import csv

# Подключение к БД
conn = psycopg2.connect(
    dbname="phonebook",  # ← сюда вставь свою базу
    user="postgres",        # ← имя пользователя PostgreSQL
    password="1937",  # ← сюда вставь свой пароль
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

# Главное меню
def main():
    while True:
        print("\n📱 Меню:")
        print("1 - Ввод вручную")
        print("2 - Загрузка из CSV")
        print("3 - Обновить запись")
        print("4 - Поиск")
        print("5 - Удалить")
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
        elif option == "0":
            break
        else:
            print("❌ Неверный ввод")

    cur.close()
    conn.close()

# Запуск
if __name__ == "__main__":
    main()
