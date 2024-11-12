import sqlite3

connection = sqlite3.connect("not_telegram.db")
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL)''')

for i in range(1, 11):
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)",
                   (f'User{i}', f'example{i}@gmail.com', f'{i}0', 1000))

cursor.execute("SELECT id FROM Users")
user_ids = cursor.fetchall()

"""Обновите balance у каждой 2ой записи начиная с 1ой на 500:"""
for index, (user_id,) in enumerate(user_ids):
    if index % 2 == 0:
        cursor.execute("UPDATE Users SET balance = 500 WHERE id = ?", (user_id,))

"""Удалите каждую 3ую запись в таблице начиная с 1ой:"""
for index, (user_id,) in enumerate(user_ids):
    if index % 3 == 0:
        cursor.execute("DELETE FROM Users WHERE id = ?", (user_id,))


cursor.execute("SELECT username, email, age, balance FROM Users WHERE age != ?", (60,))
users = cursor.fetchall()
for user in users:
    print(f'Имя: {user[0]} | Почта: {user[1]} | Возраст: {user[2]} | Баланс: {user[3]}')

connection.commit()
connection.close()
