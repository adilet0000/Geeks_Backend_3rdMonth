import os
from dotenv import load_dotenv
from database import Database
from aiogram import Dispatcher

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

IMAGES_DIR = "src/images"

RECIPES = [
   {"name": "Маргарита", "file": f"{IMAGES_DIR}/margarita_pizza.jpg", "description": "Простая и вкусная пицца."},
   {"name": "Четыре сыра", "file": f"{IMAGES_DIR}/four_cheese.jpg", "description": "Идеально для любителей сыра."},
   {"name": "Пепперони", "file": f"{IMAGES_DIR}/pepperoni_pizza.png", "description": "Острая и сочная пицца."}
]

dispatcher = Dispatcher()
database = Database('db.sqlite3')