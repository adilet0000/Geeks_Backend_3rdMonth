from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

myinfo_router = Router()

@myinfo_router.message(Command("myinfo"))
async def myinfo_handler(message: Message) -> None:
   user = message.from_user
   await message.answer(
      f"Ваш ID: {user.id}\n"
      f"Ваше имя: {user.first_name}\n"
      f"Ваш никнейм: @{user.username if user.username else 'пусто'}"
   )
