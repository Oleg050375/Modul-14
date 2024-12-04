import sqlite3

connection = sqlite3.connect('Products.db')  # создание соединения с БД

cursor = connection.cursor()  # создание курсора

cursor.execute('''CREATE TABLE IF NOT EXISTS Products(
     id INTEGER PRIMARY KEY,
     title TEXT NOT NULL,
     description TEXT NOT NULL,
     picture TEXT NOT NULL,
     price INTEGER NOT NULL)''')  # создание БД


def initiate_db(user_id, title, description, picture, price):  # функция наполнения БД
    cursor.execute('INSERT INTO Products(id,title,description,picture,price) VALUES(?,?,?,?,?)',
                   (f'{user_id}', f'{title}', f'{description}', f'{picture}', f'{price}'))  # занесение в БД
    connection.commit()  # сохранение изменений в БД

def get_all_products():  # функция получения всех записей БД
    cursor.execute('SELECT * FROM Products')
    pr_list = cursor.fetchall()
    connection.commit()  # сохранение изменений в БД
    return pr_list
