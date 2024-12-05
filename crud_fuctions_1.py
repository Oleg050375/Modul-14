import sqlite3

connection = sqlite3.connect('Products.db')  # создание соединения с БД продуктов
connection_us = sqlite3.connect('Users.db')  # создание соединения с БД пользователей

cursor = connection.cursor()  # создание курсора для БД продуктов
cursor_us = connection_us.cursor()  # создание курсора для БД пользователей

cursor.execute('''CREATE TABLE IF NOT EXISTS Products(
     id INTEGER PRIMARY KEY,
     title TEXT NOT NULL,
     description TEXT NOT NULL,
     picture TEXT NOT NULL,
     price INTEGER NOT NULL)''')  # создание БД продуктов

cursor_us.execute('''CREATE TABLE IF NOT EXISTS Users(
     id INTEGER PRIMARY KEY,
     username TEXT NOT NULL,
     email TEXT NOT NULL,
     age INTEGER NOT NULL,
     balance INTEGER NOT NULL)''')  # создание БД пользователей


def initiate_db(user_id, title, description, picture, price):  # функция наполнения БД продуктов
    cursor.execute('INSERT INTO Products(id,title,description,picture,price) VALUES(?,?,?,?,?)',
                   (f'{user_id}', f'{title}', f'{description}', f'{picture}', f'{price}'))  # занесение в БД
    connection.commit()  # сохранение изменений в БД продуктов


def add_user(username, email, age):  # функция наполнения БД пользователей
    cursor_us.execute('INSERT INTO Users(username,email,age,balance) VALUES(?,?,?,?)',
                      (f'{username}', f'{email}', age, 1000))  # занесение в БД
    connection_us.commit()  # сохранение изменений в БД пользователей


def get_all_products():  # функция получения всех записей БД продуктов
    cursor.execute('SELECT * FROM Products')
    pr_list = cursor.fetchall()
    connection.commit()  # сохранение изменений в БД продуктов
    return pr_list


def is_included(username):  # функция определения наличия пользователя в БД
    cursor_us.execute('SELECT COUNT(*) FROM Users WHERE username = ?', (f'{username}',))
    chec = cursor_us.fetchone()[0]
    connection_us.commit()  # сохранение изменений в БД пользователей
    print(chec)
    if chec == 0:
        return False
    else:
        return True
   