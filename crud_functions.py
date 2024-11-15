import sqlite3


def initiate_db():
    connection = sqlite3.connect("Products.db")
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL)
    ''')

    cursor.execute('SELECT COUNT(*) FROM Products')
    if cursor.fetchone()[0] == 0:
        products = [
            ("Красная Пилюля", "Помогает при простуде", 100),
            ("Синяя Пилюля", "От сглазов и магов", 200),
            ("Зеленая Пилюля", "+500 в Карму", 300),
            ("Желтая Пилюля", "Храбрость и Отвага", 400)
        ]
        cursor.executemany('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)', products)
    connection.commit()
    connection.close()


def get_all_products():
    connection = sqlite3.connect("Products.db")
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()

    connection.close()
    return products
