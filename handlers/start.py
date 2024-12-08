from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from typing import Set

start_router = Router()

unique_users: Set[int] = set()

@start_router.message(Command("start"))
async def start_handler(message: Message) -> None:
   unique_users.add(message.from_user.id)
   user_count = len(unique_users)
   await message.answer(f"Привет, {message.from_user.first_name}!\nНаш бот обслуживает уже {user_count} пользователей.")
