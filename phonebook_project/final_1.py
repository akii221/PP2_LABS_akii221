import psycopg2
import csv

# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(
    dbname="phonebook",  
    user="postgres",      
    password="1937",      
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Функция для загрузки данных из CSV в таблицу
def upload_from_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Пропустить заголовок
        for row in reader:
            cur.execute("INSERT INTO phonebook (username, phone) VALUES (%s, %s)", (row[0], row[1]))
    conn.commit()

# Функция для добавления данных с консоли
def insert_from_console():
    username = input("Введите имя пользователя: ")
    phone = input("Введите номер телефона: ")
    cur.execute("INSERT INTO phonebook (username, phone) VALUES (%s, %s)", (username, phone))
    conn.commit()

# Функция для обновления данных
def update_data():
    username = input("Введите имя пользователя для обновления: ")
    new_phone = input("Введите новый номер телефона: ")
    cur.execute("UPDATE phonebook SET phone = %s WHERE username = %s", (new_phone, username))
    conn.commit()

# Функция для поиска данных с фильтром по имени или телефону
def query_data():
    filter_value = input("Введите часть имени, фамилии или телефонного номера для поиска: ")
    cur.execute("SELECT * FROM phonebook WHERE username LIKE %s OR phone LIKE %s", ('%' + filter_value + '%', '%' + filter_value + '%'))
    rows = cur.fetchall()
    for row in rows:
        print(row)

# Функция для удаления данных по имени пользователя или телефону
def delete_data():
    delete_by = input("Удалить по (username/phone): ").strip().lower()
    value = input("Введите значение для удаления: ")

    if delete_by == "username":
        cur.execute("DELETE FROM phonebook WHERE username = %s", (value,))
    elif delete_by == "phone":
        cur.execute("DELETE FROM phonebook WHERE phone = %s", (value,))

    conn.commit()

# Функция для поиска записей по паттерну
def search_by_pattern():
    pattern = input("Введите паттерн для поиска: ")
    cur.execute("SELECT * FROM phonebook WHERE username LIKE %s OR phone LIKE %s", ('%' + pattern + '%', '%' + pattern + '%'))
    rows = cur.fetchall()
    for row in rows:
        print(row)

# Функция для добавления пользователя или обновления телефона, если пользователь уже существует
def insert_or_update_user():
    username = input("Введите имя пользователя: ")
    phone = input("Введите номер телефона: ")

    cur.execute("SELECT 1 FROM phonebook WHERE username = %s", (username,))
    if cur.fetchone():
        cur.execute("UPDATE phonebook SET phone = %s WHERE username = %s", (phone, username))
    else:
        cur.execute("INSERT INTO phonebook (username, phone) VALUES (%s, %s)", (username, phone))
    
    conn.commit()

# Функция для добавления нескольких пользователей с проверкой корректности номера телефона
def insert_many_users():
    users = []
    num_users = int(input("Сколько пользователей добавить? "))
    for _ in range(num_users):
        username = input("Введите имя пользователя: ")
        phone = input("Введите номер телефона: ")

        if phone and phone.isdigit():
            users.append((username, phone))
        else:
            print(f"Неверный номер телефона: {phone}")
    
    for user in users:
        cur.execute("INSERT INTO phonebook (username, phone) VALUES (%s, %s)", user)
    
    conn.commit()

# Функция для поиска с пагинацией
def query_with_pagination():
    limit = int(input("Введите лимит: "))
    offset = int(input("Введите смещение (offset): "))
    cur.execute("SELECT * FROM phonebook LIMIT %s OFFSET %s", (limit, offset))
    rows = cur.fetchall()
    for row in rows:
        print(row)

# Функция для удаления данных по имени пользователя или телефону
def delete_user():
    value = input("Введите username или телефон для удаления: ")
    cur.execute("DELETE FROM phonebook WHERE username = %s OR phone = %s", (value, value))
    conn.commit()

# Главное меню
def main_menu():
    while True:
        print("\nГлавное меню:")
        print("1. Загрузить данные из CSV")
        print("2. Добавить пользователя через консоль")
        print("3. Обновить данные пользователя")
        print("4. Поиск данных")
        print("5. Удалить данные")
        print("6. Поиск по паттерну")
        print("7. Добавить или обновить пользователя")
        print("8. Добавить несколько пользователей")
        print("9. Пагинация")
        print("10. Удалить пользователя по имени или телефону")
        print("0. Выход")

        choice = input("Выберите опцию: ")

        if choice == "1":
            filename = input("Введите имя файла CSV: ")
            upload_from_csv(filename)
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            update_data()
        elif choice == "4":
            query_data()
        elif choice == "5":
            delete_data()
        elif choice == "6":
            search_by_pattern()
        elif choice == "7":
            insert_or_update_user()
        elif choice == "8":
            insert_many_users()
        elif choice == "9":
            query_with_pagination()
        elif choice == "10":
            delete_user()
        elif choice == "0":
            break
        else:
            print("Неверный выбор!")

# Закрыть соединение с базой данных
def close_connection():
    cur.close()
    conn.close()

if __name__ == "__main__":
    try:
        main_menu()
    finally:
        close_connection()
