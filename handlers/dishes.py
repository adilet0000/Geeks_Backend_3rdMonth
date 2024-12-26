from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from config import database
import os

dishes_router = Router()

@dishes_router.message(Command("dishes"))
async def show_dishes(message: types.Message):
    dishes = database.get_dishes()
    if not dishes:
        await message.answer("Список блюд пуст.")
        return

    for name, category, price, description, image_path in dishes:
        text = (
            f"<b>{name}</b>\n"
            f"Категория: {category}\n"
            f"Цена: {price:.2f} сом.\n"
            f"Описание: {description}"
        )
        if os.path.exists(image_path):
            photo = FSInputFile(image_path)
            await message.answer_photo(photo=photo, caption=text, parse_mode="HTML")
        else:
            await message.answer(text, parse_mode="HTML")
