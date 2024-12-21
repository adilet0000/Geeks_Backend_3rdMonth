from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import database

class AddDish(StatesGroup):
    waiting_for_name = State()
    waiting_for_category = State()
    waiting_for_price = State()
    waiting_for_description = State()
    confirm = State()

admin_router = Router()

@admin_router.message(Command("add_dish"))
async def start_adding_dish(message: types.Message, state: FSMContext):
    await message.answer("Введите название блюда:")
    await state.set_state(AddDish.waiting_for_name)

@admin_router.message(AddDish.waiting_for_name)
async def process_dish_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите категорию блюда (например: \"Супы\":")
    await state.set_state(AddDish.waiting_for_category)

@admin_router.message(AddDish.waiting_for_category)
async def process_dish_category(message: types.Message, state: FSMContext):
    await state.update_data(category=message.text)
    await message.answer("Введите цену блюда:")
    await state.set_state(AddDish.waiting_for_price)

@admin_router.message(AddDish.waiting_for_price)
async def process_dish_price(message: types.Message, state: FSMContext):
    try:
        price = float(message.text)
    except ValueError:
        await message.answer("Цена должна быть числом. Попробуйте снова.")
        return
    await state.update_data(price=price)
    await message.answer("Введите описание блюда:")
    await state.set_state(AddDish.waiting_for_description)

@admin_router.message(AddDish.waiting_for_description)
async def process_dish_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()
    await message.answer(
        f"Подтвердите добавление блюда:\n\n"
        f"Название: {data['name']}\nКатегория: {data['category']}\n"
        f"Цена: {data['price']} руб.\nОписание: {data['description']}",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton(text="Подтвердить")],
                [types.KeyboardButton(text="Отмена")],
            ],
            resize_keyboard=True,
        ),
    )
    await state.set_state(AddDish.confirm)

@admin_router.message(AddDish.confirm, F.text.lower() == "подтвердить")
async def confirm_dish(message: types.Message, state: FSMContext):
    data = await state.get_data()
    database.save_dish(data)
    await message.answer("Блюдо успешно добавлено!", reply_markup=types.ReplyKeyboardRemove())
    await state.clear()

@admin_router.message(AddDish.confirm, F.text.lower() == "отмена")
async def cancel_adding_dish(message: types.Message, state: FSMContext):
    await message.answer("Добавление блюда отменено.", reply_markup=types.ReplyKeyboardRemove())
    await state.clear()
