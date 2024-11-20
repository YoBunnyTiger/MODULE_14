import sqlite3


def initiate_db():
    connection = sqlite3.connect("DataBase.db")
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

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL)
    ''')

    connection.commit()
    connection.close()


def add_user(username, email, age):
    conn = sqlite3.connect('DataBase.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Users (username, email, age, balance) '
                   'VALUES (?, ?, ?, 1000)', (username, email, age))
    conn.commit()
    conn.close()


def is_included(username):
    conn = sqlite3.connect('DataBase.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user is not None


def get_all_products():
    connection = sqlite3.connect("DataBase.db")
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()

    connection.close()
    return products
