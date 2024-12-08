import random
from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command

random_recipe_router = Router()

recipes = [
   {"name": "Маргарита", "file": "src/images/margarita_pizza.jpg", "description": "Простая и вкусная пицца."},
   {"name": "Четыре сыра", "file": "src/images/four_cheese.jpg", "description": "Идеально для любителей сыра."},
   {"name": "Пепперони", "file": "src/images/pepperoni_pizza.png", "description": "Острая и сочная пицца."}
]

@random_recipe_router.message(Command("random"))
async def random_recipe_handler(message: Message) -> None:
   recipe = random.choice(recipes)
   photo = FSInputFile(recipe["file"])
   caption = f"Рецепт: {recipe['name']}\nОписание: {recipe['description']}"
   await message.answer_photo(photo, caption=caption)