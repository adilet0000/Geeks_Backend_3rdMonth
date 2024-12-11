from aiogram import Router, types
from aiogram.filters import Command
from keyboards.review import get_review_keyboard

start_router = Router()

@start_router.message(Command("start"))
async def start_handler(message: types.Message) -> None:
   await message.answer(
      "Добро пожаловать! Вы можете оставить отзыв, нажав на кнопку ниже.",
      reply_markup=get_review_keyboard()
   )
