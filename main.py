import random
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

names = []

unique_users = set()

# START
@dp.message(Command("start"))
async def start_handler(message: Message):
   unique_users.add(message.from_user.id)
   user_count = len(unique_users)
   if message.from_user.username not in names:
      names.append(message.from_user.username)
   await message.answer(f"Привет, {message.from_user.first_name}!\nНаш бот обслуживает уже {user_count} пользователей.")

# MYINFO
@dp.message(Command("myinfo"))
async def myinfo_handler(message: Message):
   user = message.from_user
   await message.answer(f"Ваш ID: {user.id}\nВаше имя: {user.first_name}\nВаш никнейм: @{user.username if user.username else 'пусто'}")

# RANDOM
@dp.message(Command("random"))
async def random_handler(message: Message):
   random_name = random.choice(names)
   await message.answer(f"Случайное имя: {random_name}")

async def main():
   print("Бот запущен!")
   await bot.delete_webhook(drop_pending_updates=True)
   await dp.start_polling(bot)

if __name__ == "__main__":
   asyncio.run(main())