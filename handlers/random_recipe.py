import random
from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from config import RECIPES

random_recipe_router = Router()

@random_recipe_router.message(Command("random"))
async def random_recipe_handler(message: Message) -> None:
   recipe = random.choice(RECIPES)
   photo = FSInputFile(recipe["file"])
   caption = f"Рецепт: {recipe['name']}\nОписание: {recipe['description']}"
   await message.answer_photo(photo, caption=caption)
