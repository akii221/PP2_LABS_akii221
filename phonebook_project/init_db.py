import psycopg2

conn = psycopg2.connect(
    dbname="phonebook",
    user="postgres",
    password="aki1937",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(50),
        phone VARCHAR(20)
    );
""")

conn.commit()
cur.close()
conn.close()

print("✅ Таблица 'phonebook' успешно создана!")