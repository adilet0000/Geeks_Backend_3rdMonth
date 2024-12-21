from aiogram import Router, types
from aiogram.filters import Command
from config import database

dishes_router = Router()

@dishes_router.message(Command("dishes"))
async def show_dishes(message: types.Message):
    dishes = database.get_dishes()
    if not dishes:
        await message.answer("Список блюд пуст.")
        return

    response = "Список блюд:\n\n"
    for name, category, price, description in dishes:
        response += (
            f"Название: {name}\nКатегория: {category}\n"
            f"Цена: {price} руб.\nОписание: {description}\n\n"
        )
    await message.answer(response)
