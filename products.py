from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from crud_functions import *
import asyncio

""" Наполнение БД
initiate_db(1,'Клубника', 'под шампанское', 'str.jpg', 100)
initiate_db(2,'Яблоки', 'богаты железом', 'apl.jpg', 200)
initiate_db(3,'Лимоны', 'богаты витамином С', 'lim.jpg', 300)
initiate_db(4,'Виноград', 'очень сладкий', 'vin.jpg', 400)
"""

a = get_all_products()  # чтение содержимого БД

api = '8022767311:AAGPwqgFoP0gUistLliI7WsW6ApCQ6nU56c'  # переменная API-адреса

bot = Bot(token=api)  # переменная бота

dp = Dispatcher(bot, storage=MemoryStorage())  # переменная диспетчера

kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Рассчитать'), KeyboardButton(text='Информация')], [KeyboardButton(text='Купить')]],
    resize_keyboard=True)  # клавиатура с масштабируемыми кнопками

in_kb = InlineKeyboardMarkup()  # инлайн клавиатура расчёта калорий
in_kb_buy = InlineKeyboardMarkup()  # инлайн клавиатура продаж

in_bt_1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')  # инлайн кнопка
in_bt_2 = InlineKeyboardButton(text='Формулы рассчёта', callback_data='formulas')  # инлайн кнопка

in_bt_buy_1 = InlineKeyboardButton(text=a[0][1], callback_data='product_buying')  # инлайн кнопка продаж
in_bt_buy_2 = InlineKeyboardButton(text=a[1][1], callback_data='product_buying')  # инлайн кнопка продаж
in_bt_buy_3 = InlineKeyboardButton(text=a[2][1], callback_data='product_buying')  # инлайн кнопка продаж
in_bt_buy_4 = InlineKeyboardButton(text=a[3][1], callback_data='product_buying')  # инлайн кнопка продаж

in_kb.add(in_bt_1)  # добавление кнопки в инлайн клавиатуру
in_kb.add(in_bt_2)  # добавление кнопки в инлайн клавиатуру

in_kb_buy.add(in_bt_buy_1)  # добавление кнопки в инлайн клавиатуру продаж
in_kb_buy.add(in_bt_buy_2)  # добавление кнопки в инлайн клавиатуру продаж
in_kb_buy.add(in_bt_buy_3)  # добавление кнопки в инлайн клавиатуру продаж
in_kb_buy.add(in_bt_buy_4)  # добавление кнопки в инлайн клавиатуру продаж


class UserStates(StatesGroup):
    age = State()  # возраст
    growth = State()  # рост
    weight = State()  # вес


@dp.message_handler(commands=['Start'])  # хэндлер обработки запускающей команды
async def starter(message):
    await message.answer('Выберите действие', reply_markup=kb)  # вывод клавиатуры


@dp.message_handler(text=['Рассчитать'])  # хэндлер обработки запроса на расчёт калорий
async def main_menu(message):
    await message.answer('Выберите опцию', reply_markup=in_kb)  # запрос действия


@dp.message_handler(text=['Купить'])  # хэндлер обработки запроса на покупку
async def get_buying_list(message):
    for i in range(4):  # вывод предложений
        with open(a[i][3], 'rb') as img:
            await message.answer_photo(img, f'Название: {a[i][1]} | Описание: {a[i][2]} | Цена: {a[i][4]}')
    await message.answer('Выберите продукт для покупки', reply_markup=in_kb_buy)  # вывод ин-клавиатуры покупки


@dp.callback_query_handler(text='product_buying')  # хэндлер обработки выбора продукта
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт')
    await call.answer()


@dp.callback_query_handler(text='formulas')  # хэндлер обработки выбора формулы
async def get_formulas(call):
    await call.message.answer('10 * вес(кг) + 6,25 * рост(см) - 5 * возраст(г) + 5')
    await call.answer()


@dp.callback_query_handler(text=['calories'])  # хэндлер обработки запроса на расчёт калорий
async def set_age(call):
    await call.message.answer('Введите свой возраст в полных годах')  # встречный запрос возраста
    await UserStates.age.set()  # ожидание ввода возраста и сохранение его значения в соответствующий атрибут
    await call.answer()


@dp.message_handler(text=['Информация'])  # хэндлер обработки запроса на расчёт калорий
async def set_age(message):
    await message.answer('Ну что Вам рассказать про Сахалин... ')  # вывод инфо


@dp.message_handler(state=UserStates.age)  # хэндлер обработки, реагирующий на изменение атрибута возраста
async def set_growth(message, state):
    await state.update_data(age=message.text)  # сохранение возраста в локальной БД машины состояний
    await message.answer('Введите свой рост в сантиметрах')  # запрос роста
    await UserStates.growth.set()  # ожидание ввода роста и сохранение его в атрибут


@dp.message_handler(state=UserStates.growth)  # хэндлер обработки, реагирующий на изменение атрибута роста
async def set_weight(message, state):
    await state.update_data(growth=message.text)  # сохранение роста в локальной БД машины состояний
    await message.answer('Введите свой вес в килограммах')  # запрос веса
    await UserStates.weight.set()  # ожидание ввода веса и сохранение его в атрибут


@dp.message_handler()  # реагирование на любое сообщение
async def any(message):
    await message.answer('Введите команду /Start, чтобы начать общение.')


@dp.message_handler(state=UserStates.weight)  # хэндлер обработки, реагирующий на изменение атрибута роста
async def send_calories(message, state):
    await state.update_data(weight=message.text)  # сохранение веса в локальной БД машины состояний
    data = await state.get_data()  # считывание всех атрибутов состояния
    Age = int(data.get('age'))
    Growth = int(data.get('growth'))
    Weight = int(data.get('weight'))
    norma = (10 * Weight) + (6.25 * Growth) - (5 * Age) + 5  # расчёт нормы калорий
    await message.answer(f'Ваша норма калорий {str(norma)}')  # вывод результата расчёта
    await state.finish()


connection.commit()  # сохранение изменений в БД

connection.close()  # закрытие соединения с БД

if __name__ == '__main__':  # запуск программы бота
    executor.start_polling(dp, skip_updates=True)  # исполнитель
