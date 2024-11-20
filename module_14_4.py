from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from crud_functions import *

api = "7374724689:AAE7FraX7jq8h1vuOPvZTo01AZGeN5EBNPQ"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_calc = KeyboardButton(text='Рассчитать')
button_info = KeyboardButton(text='Информация')
button_buy = KeyboardButton(text='Купить')
button_register = KeyboardButton(text='Регистрация')
kb.add(button_register)
kb.add(button_calc, button_info)
kb.add(button_buy)
inline_keyboard = InlineKeyboardMarkup(row_width=1)
gender_keyboard = InlineKeyboardMarkup(row_width=1)
button_calories = InlineKeyboardButton("Рассчитать норму калорий", callback_data='calories')
button_formulas = InlineKeyboardButton("Формулы расчёта", callback_data='formulas')
button_male = InlineKeyboardButton("Мужской", callback_data='male')
button_female = InlineKeyboardButton("Женский", callback_data='female')
inline_keyboard.add(button_calories, button_formulas)
gender_keyboard.add(button_male, button_female)

product_keyboard = InlineKeyboardMarkup(row_width=1)
button_product1 = InlineKeyboardButton("1. Красная Пилюля", callback_data='product_buying1')
button_product2 = InlineKeyboardButton("2. Синяя Пилюля", callback_data='product_buying2')
button_product3 = InlineKeyboardButton("3. Зеленая Пилюля", callback_data='product_buying3')
button_product4 = InlineKeyboardButton("4. Желтая Пилюля", callback_data='product_buying4')
product_keyboard.add(button_product1, button_product2, button_product3, button_product4)


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью.', reply_markup=kb)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()


@dp.message_handler(text='Регистрация')
async def sing_up(message: types.Message):
    initiate_db()
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message: types.Message, state: FSMContext):
    username = message.text
    if is_included(username):
        await message.answer("Пользователь существует, введите другое имя.")
    else:
        await state.update_data(username=username)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message: types.Message, state: FSMContext):
    email = message.text
    await state.update_data(email=email)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message: types.Message, state: FSMContext):
    age = message.text
    data = await state.get_data()
    username = data.get('username')
    email = data.get('email')

    add_user(username, email, age)
    await message.answer("Регистрация прошла успешно!")
    await state.finish()


@dp.message_handler(text='Рассчитать')
async def main_menu(message: types.Message):
    await message.answer('Выберите опцию:', reply_markup=inline_keyboard)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    formula_message = (
        "Формула Миффлина-Сан Жеора:\n"
        "Для мужчин:\n"
        "BMR = 10 * Вес(кг) + 6.25 * Рост(см) - 5 * Возраст(г) + 5\n"
        "Для женщин:\n"
        "BMR = 10 * Вес(кг) + 6.25 * Рост(см) - 5 * Возраст(г) - 161")
    await call.message.answer(formula_message)


@dp.callback_query_handler(text='calories')
async def set_gender(call: types.CallbackQuery):
    await call.message.answer('Выберите ваш пол:', reply_markup=gender_keyboard)
    await UserState.gender.set()


@dp.callback_query_handler(text='male', state=UserState.gender)
async def male_selected(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(gender='male')
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.callback_query_handler(text='female', state=UserState.gender)
async def female_selected(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(gender='female')
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state: FSMContext):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])
    gender = data['gender']

    if gender == 'male':
        bmr = 10 * weight + 6.25 * growth - 5 * age + 5
        # Формула Миффлина - Сан Жеора для расчета калорий (применим для мужчин)
    else:
        bmr = 10 * weight + 6.25 * growth - 5 * age - 161
        # Формула Миффлина - Сан Жеора для расчета калорий (применим для женщин)

    await message.answer(f'Ваша норма калорий: {bmr:.2f} ккал в день.')
    await state.finish()


@dp.message_handler(text='Купить')
async def get_buying_list(message: types.Message):
    initiate_db()
    products = get_all_products()
    for product_id, product_name, description, price in products:
        await message.answer(f'Название: {product_name} | Описание: {description} | Цена: {price}₽')
        img_path = f'files/{product_id}.png'
        try:
            with open(img_path, "rb") as img_prod:
                await message.answer_photo(img_prod)
        except FileNotFoundError:
            await message.answer("Изображение не найдено.")

    await message.answer("Выберите продукт для покупки:", reply_markup=product_keyboard)


@dp.callback_query_handler(lambda call: call.data.startswith('product_buying'))
async def send_confirm_message(call: types.CallbackQuery):
    product_index = call.data[-1]  # Получаем номер продукта из callback_data
    await call.message.answer(f"Вы успешно приобрели продукт {product_index}!")


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
