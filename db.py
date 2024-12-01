import sqlite3

connection = sqlite3.connect('not_telegram.db')  # создание соединения с БД

cursor = connection.cursor()  # создание курсора

cursor.execute('''CREATE TABLE IF NOT EXISTS Users(
 id INTEGER PRIMARY KEY,
 username TEXT NOT NULL,
 email TEXT NOT NULL,
 age INTEGER,
 balance INTEGER NOT NULL)''')  # создание БД

cursor.execute('CREATE INDEX IF NOT EXISTS idx_email ON Users(email)')  # создание индекса

for i in range(1, 10):  # наполнение БД
    cursor.execute('INSERT INTO Users(username, email, age, balance) VALUES(?,?,?,?)',
                   (f'User{i}', f'example{i}@gmail.com', 10 * i, 1000))

for i in [1, 3, 5, 7, 9]:  # изменение значений полей в БД
    cursor.execute('UPDATE Users SET balance = ? WHERE username=?',
                   (500, f'User{i}'))

for i in [1, 4, 7, 10]:  # удаление записей из БД по заданному параметру
    cursor.execute('DELETE FROM Users WHERE username = ?',
                   (f'User{i}',))

cursor.execute('SELECT username, email, age, balance FROM Users WHERE age != ?',
               (60,))  # выборка из БД по заданным параметрам
for i in cursor.fetchall():  # вывод результатов выборки из БД
    print(f'Имя:{i[0]} | Почта:{i[1]} | Возраст:{i[2]} | Баланс:{i[3]}')

connection.commit()  # сохранение изменений в БД

connection.close()  # закрытие соединения с БД
